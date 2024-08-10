from typing import Optional

import pandas as pd
from llama_index.core import SummaryIndex, PromptTemplate, Settings
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.query_pipeline import (
    QueryPipeline,
    FnComponent,
    InputComponent,
)
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.callbacks import CallbackManager, TokenCountingHandler
from llama_index.core.llms.llm import LLM
from llama_index.readers.web import SimpleWebPageReader

from .formats import (
    Syllabus,
    Judges,
    SectionContent,
    SelectedRegions,
)
from .prompts import (
    ASK_SYLLABUS_TEMPLATE,
    FORMAT_SYLLABUS_TEMPLATE,
    MERGE_SYLLABUS_TEMPLATE,
    JUDGE_SECTION_TEMPLATE,
    FORMAT_JUDGE_TEMPLATE,
    REGION_SELECTION_TEMPLATE,
)


def prepare_regulation_query_engine(
        links_df: pd.DataFrame) -> SubQuestionQueryEngine:
    """Prepare a query engine for regulations

    :param links_df: a DataFrame with columns 'regulations' and 'links'
    :return: a query engine for regulations
    """

    links_df.reset_index(drop=True, inplace=True)

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


def prepare_regulation_syllabus_pipeline_with_query_engine(
    regulation_query_engine: SubQuestionQueryEngine,
    ask_syllabus_template: str = ASK_SYLLABUS_TEMPLATE,
    format_syllabus_template: str = FORMAT_SYLLABUS_TEMPLATE,
    token_counter: Optional[TokenCountingHandler] = None,
    verbose: bool = False,
) -> QueryPipeline:
    """Prepare a pipeline for generating a privacy policy syllabus
    compliant with regulations

    :param regulation_query_engine: a query engine for regulations
    :param ask_syllabus_template: a template for asking a syllabus
    :param format_syllabus_template: a template for formatting a syllabus
    :param token_counter: a token counter for counting tokens
    :param verbose: whether to show verbose output
    :return: a pipeline for generating a syllabus for regulations
    """

    ask_syllabus_template = PromptTemplate(ask_syllabus_template)
    syllabus_parser = PydanticOutputParser(Syllabus)
    format_syllabus_template = PromptTemplate(
        syllabus_parser.format(format_syllabus_template))

    # create a pipeline
    syllabus_pipeline = QueryPipeline(
        chain=[
            ask_syllabus_template,
            regulation_query_engine,
            format_syllabus_template,
            Settings.llm,
            syllabus_parser,
            FnComponent(
                fn=lambda input: {
                    section.name.value: section.key_points
                    for section in input.sections
                }),
        ],
        callback_manager=CallbackManager([token_counter])
        if token_counter else None,
        verbose=verbose,
    )

    return syllabus_pipeline


def prepare_regulation_syllabus_pipeline(
    format_syllabus_template: str = MERGE_SYLLABUS_TEMPLATE,
    token_counter: Optional[TokenCountingHandler] = None,
    verbose: bool = False,
) -> QueryPipeline:
    """Prepare a pipeline for generating a privacy policy syllabus
    compliant with regulations

    :param format_syllabus_template: a template for formatting a syllabus
    :param token_counter: a token counter for counting tokens
    :param verbose: whether to show verbose output
    :return: a pipeline for generating a syllabus for regulations
    """

    syllabus_parser = PydanticOutputParser(Syllabus)
    format_syllabus_template = PromptTemplate(
        syllabus_parser.format(format_syllabus_template))

    # create a pipeline
    syllabus_pipeline = QueryPipeline(
        chain=[
            format_syllabus_template,
            Settings.llm,
            syllabus_parser,
            FnComponent(
                fn=lambda input: {
                    section.name.value: section.key_points
                    for section in input.sections
                }),
        ],
        callback_manager=CallbackManager([token_counter])
        if token_counter else None,
        verbose=verbose,
    )

    return syllabus_pipeline


def prepare_generate_pipeline(
    generate_template: str,
    generation_llm: LLM = Settings.llm,
    token_counter: Optional[TokenCountingHandler] = None,
    verbose: bool = False,
) -> QueryPipeline:
    """Prepare a pipeline for (re)generating a section of a privacy policy

    :param generate_template: a template for (re)generating a section
    :param generation_llm: a language model for (re)generating a section
    :param token_counter: a token counter for counting tokens
    :param verbose: whether to show verbose output
    :return: a pipeline for (re)generating a section of a privacy policy
    """

    generate_parser = PydanticOutputParser(SectionContent)
    generate_template = PromptTemplate(
        generate_parser.format(generate_template))
    regenerate_pipeline = QueryPipeline(
        chain=[generate_template, generation_llm, generate_parser],
        callback_manager=CallbackManager([token_counter])
        if token_counter else None,
        verbose=verbose,
    )

    return regenerate_pipeline


def prepare_section_judge_pipeline(
    law_llm: LLM,
    judge_section_template: str = JUDGE_SECTION_TEMPLATE,
    format_judge_template: str = FORMAT_JUDGE_TEMPLATE,
    token_counter: Optional[TokenCountingHandler] = None,
    verbose: bool = False,
) -> QueryPipeline:
    """Prepare a pipeline for judging a section of a privacy policy

    :param law_llm: a law LLM to judge a section
    :param judge_section_template: a template for judging a section
    :param format_judge_template: a template for formatting a judge
    :param token_counter: a token counter for counting tokens
    :param verbose: whether to show verbose output
    :return: a pipeline for judging a section of a privacy policy
    """

    input_component = InputComponent()
    judge_section_template = PromptTemplate(judge_section_template)
    judge_parser = PydanticOutputParser(Judges)
    format_judge_template = PromptTemplate(
        judge_parser.format(format_judge_template))

    def determine_judge(judges: Judges, section_name: str):

        improve_suggestions = ""

        for judge in judges.judges:
            if judge.name.value == section_name and judge.suggestions:
                improve_suggestions += judge.suggestions + "\n"

        if not improve_suggestions:
            return {"pass": True, "suggestions": ""}

        return {"pass": False, "suggestions": improve_suggestions}

    # create a pipeline
    judge_pipeline = QueryPipeline(
        modules={
            "input": input_component,
            "judge_section_template": judge_section_template,
            "law_llm": law_llm,
            "format_judge_template": format_judge_template,
            "llm": Settings.llm,
            "judge_parser": judge_parser,
            "determine_judge": FnComponent(fn=determine_judge),
        },
        callback_manager=CallbackManager([token_counter])
        if token_counter else None,
        verbose=verbose,
    )

    judge_pipeline.add_link("input",
                            "judge_section_template",
                            src_key="section_name",
                            dest_key="section_name")
    judge_pipeline.add_link("input",
                            "judge_section_template",
                            src_key="section_text",
                            dest_key="section_text")
    judge_pipeline.add_link("input",
                            "judge_section_template",
                            src_key="regulations",
                            dest_key="regulations")
    judge_pipeline.add_link("judge_section_template", "law_llm")
    judge_pipeline.add_link("law_llm", "format_judge_template")
    judge_pipeline.add_link("format_judge_template", "llm")
    judge_pipeline.add_link("llm", "judge_parser")
    judge_pipeline.add_link("judge_parser",
                            "determine_judge",
                            dest_key="judges")
    judge_pipeline.add_link("input",
                            "determine_judge",
                            src_key="section_name",
                            dest_key="section_name")

    return judge_pipeline


def prepare_region_selection_pipeline(
    region_selection_template: str = REGION_SELECTION_TEMPLATE,
    token_counter: Optional[TokenCountingHandler] = None,
    verbose: bool = False,
) -> QueryPipeline:
    """Prepare a pipeline for selecting regions based on user input

    :param region_selection_template: a template for selecting regions
    :param token_counter: a token counter for counting tokens
    :param verbose: whether to show verbose output
    :return: a pipeline for selecting regions
    """

    regions_parser = PydanticOutputParser(SelectedRegions)
    region_selection_template = PromptTemplate(
        regions_parser.format(region_selection_template))

    region_selection_pipeline = QueryPipeline(
        chain=[
            region_selection_template,
            Settings.llm,
            regions_parser,
            FnComponent(
                fn=lambda input: set([each.value for each in input.regions])),
        ],
        callback_manager=CallbackManager([token_counter])
        if token_counter else None,
        verbose=verbose,
    )

    return region_selection_pipeline
