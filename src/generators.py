import pandas as pd
from llama_index.core import SummaryIndex, PromptTemplate, Settings
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.query_pipeline import QueryPipeline
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.readers.web import SimpleWebPageReader

from .formats import Syllabus, Judges
from .prompts import (
    ASK_SYLLABUS_TEMPLATE,
    FORMAT_SYLLABUS_TEMPLATE,
    JUDGE_SECTION_TEMPLATE,
    FORMAT_JUDGE_TEMPLATE,
)
from .law_model import HuggingFaceLLMModified


def prepare_regulation_query_engine(
        links_df: pd.DataFrame) -> SubQuestionQueryEngine:
    """Prepare a query engine for regulations

    :param links_df: a DataFrame with columns 'regulations' and 'links'
    :return: a query engine for regulations
    """

    # read regulations
    regulation_text = SimpleWebPageReader(html_to_text=True).load_data(
        links_df['links'].to_list())

    # pack into query engine tools
    regulation_query_tools = [
        QueryEngineTool(
            query_engine=SummaryIndex.from_documents([
                regulation_text[i]
            ]).as_query_engine(response_mode="tree_summarize"),
            metadata=ToolMetadata(
                name=links_df.loc[i, 'regulations'],
                description=(
                    "refer the text when you want to make something be "
                    f"{links_df.loc[i, 'regulations']} compliant"),
            ),
        ) for i in range(len(regulation_text))
    ]

    # create sub-query engine
    regulation_query_engine = SubQuestionQueryEngine.from_defaults(
        query_engine_tools=regulation_query_tools, verbose=True)

    return regulation_query_engine


def prepare_regulation_syllabus_pipeline(
    regulation_query_engine: SubQuestionQueryEngine,
    ask_syllabus_template: str = ASK_SYLLABUS_TEMPLATE,
    format_syllabus_template: str = FORMAT_SYLLABUS_TEMPLATE,
    verbose: bool = False,
) -> QueryPipeline:
    """Prepare a pipeline for generating a privacy policy syllabus
    compliant with regulations

    :param regulation_query_engine: a query engine for regulations
    :param ask_syllabus_template: a template for asking a syllabus
    :param format_syllabus_template: a template for formatting a syllabus
    :param verbose: whether to show verbose output
    :return: a pipeline for generating a syllabus for regulations
    """

    ask_syllabus_template = PromptTemplate(ask_syllabus_template)
    syllabus_parser = PydanticOutputParser(Syllabus)
    format_syllabus_template = PromptTemplate(
        syllabus_parser.format(format_syllabus_template))

    # create a pipeline
    syllabus_pipeline = QueryPipeline(chain=[
        ask_syllabus_template,
        regulation_query_engine,
        format_syllabus_template,
        Settings.llm,
        syllabus_parser,
    ],
                                      verbose=verbose)

    return syllabus_pipeline


def prepare_section_judge_pipeline(
        law_llm: HuggingFaceLLMModified,
        judge_section_template: str = JUDGE_SECTION_TEMPLATE,
        format_judge_template: str = FORMAT_JUDGE_TEMPLATE,
        verbose: bool = False) -> QueryPipeline:
    """Prepare a pipeline for judging a section of a privacy policy

    :param law_llm: a law LLM to judge a section
    :param judge_section_template: a template for judging a section
    :param format_judge_template: a template for formatting a judge
    :param verbose: whether to show verbose output
    :return: a pipeline for judging a section of a privacy policy
    """

    judge_section_template = PromptTemplate(judge_section_template)
    judge_parser = PydanticOutputParser(Judges)
    format_judge_template = PromptTemplate(
        judge_parser.format(format_judge_template))

    # create a pipeline
    judge_pipeline = QueryPipeline(chain=[
        judge_section_template,
        law_llm,
        format_judge_template,
        Settings.llm,
        judge_parser,
    ],
                                   verbose=verbose)

    return judge_pipeline
