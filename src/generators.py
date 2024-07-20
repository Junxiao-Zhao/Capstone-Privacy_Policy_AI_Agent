import logging
from typing import Optional, Dict, List, Any

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
from llama_index.readers.web import SimpleWebPageReader

from .formats import (
    Syllabus,
    Judges,
    SectionContent,
)
from .prompts import (
    ASK_SYLLABUS_TEMPLATE,
    FORMAT_SYLLABUS_TEMPLATE,
    GENERATE_PROMPT,
    REGENERATE_PROMPT,
    JUDGE_SECTION_TEMPLATE,
    FORMAT_JUDGE_TEMPLATE,
)
from .law_model import HuggingFaceLLMModified, prepare_law_llm


class PrivacyPolicyGenerator:

    def __init__(
        self,
        regulation_query_engine: SubQuestionQueryEngine,
        syllabus_pipeline: QueryPipeline,
        generate_pipeline: QueryPipeline,
        regenerate_pipeline: QueryPipeline,
        judge_pipeline: QueryPipeline,
    ):
        """Constructor

        :param regulation_query_engine: a query engine for regulations
        :param syllabus_pipeline: a pipeline for generating a syllabus
        :param generate_pipeline: a pipeline for generating a section
        :param regenerate_pipeline: a pipeline for regenerating a section
        :param judge_pipeline: a pipeline for judging a section
        """

        self.regulation_query_engine = regulation_query_engine
        self.syllabus_pipeline = syllabus_pipeline
        self.generate_pipeline = generate_pipeline
        self.regenerate_pipeline = regenerate_pipeline
        self.judge_pipeline = judge_pipeline

    @classmethod
    def from_defaults(cls, links_df: pd.DataFrame, verbose: bool = False):
        """Create a privacy policy generator from defaults

        :param links_df: a DataFrame with columns 'regulations' and 'links'
        :param verbose: whether to show verbose output
        :return: a privacy policy generator
        """

        regulation_query_engine = prepare_regulation_query_engine(links_df)
        syllabus_pipeline = prepare_regulation_syllabus_pipeline(
            regulation_query_engine, verbose=verbose)
        generate_pipline = prepare_generate_pipeline(GENERATE_PROMPT,
                                                     verbose=verbose)
        regenerate_pipeline = prepare_generate_pipeline(REGENERATE_PROMPT,
                                                        verbose=verbose)
        law_llm = prepare_law_llm()
        judge_pipeline = prepare_section_judge_pipeline(law_llm,
                                                        verbose=verbose)

        return cls(
            regulation_query_engine=regulation_query_engine,
            syllabus_pipeline=syllabus_pipeline,
            generate_pipeline=generate_pipline,
            regenerate_pipeline=regenerate_pipeline,
            judge_pipeline=judge_pipeline,
        )

    def get_syllabus(self, regulations: List[str]) -> Dict[str, List[str]]:
        """Get a privacy policy syllabus

        :param regulations: the regulations to comply with
        :return: a privacy policy syllabus
        """

        self.regulations = ', '.join(regulations)
        self.syllabus = self.syllabus_pipeline.run(
            regulations=self.regulations)

        return self.syllabus

    def generate(
        self,
        section_name: str,
        information: str,
        threshold: int = 5,
    ) -> Dict[str, Any]:
        """Generate a section of a privacy policy

        :param section_name: the name of the section
        :param information: the information for generating the section
        :param threshold: the maximum number of attempts to regenerate
        :return: success or not and the generated section
        """

        # generate a section
        section_content = self.generate_pipeline.run(
            section_name=section_name,
            information=information,
            key_points='\n'.join(self.syllabus[section_name]),
        )

        # judge the section
        judge = self.judge_pipeline.run(
            section_name=section_name,
            section_text=section_content.content,
            regulations=self.regulations,
        )

        if judge['pass']:
            return {"success": True, "content": section_content.content}

        return self.regenerate(
            section_name=section_name,
            section_text=section_content.content,
            suggestions=judge['suggestions'],
            threshold=threshold,
        )

    def regenerate(
        self,
        section_name: str,
        section_text: str,
        suggestions: str,
        threshold: int = 5,
    ):
        """Regenerate a section of a privacy policy

        :param section_name: the name of the section
        :param section_text: the text of the section
        :param suggestions: the suggestions for improvement
        :param threshold: the maximum number of attempts to regenerate
        :return: success or not and the regenerated section
        """

        key_points = '\n'.join(self.syllabus[section_name])

        for i in range(threshold):

            regenerate = self.regenerate_pipeline.run(
                section_name=section_name,
                section_text=section_text,
                suggestions=suggestions,
                key_points=key_points,
            )

            judge = self.judge_pipeline.run(
                section_name=section_name,
                section_text=regenerate.content,
                regulations=self.regulations,
            )

            if judge['pass']:
                return {"success": True, "content": regenerate.content}

            else:
                suggestions = judge['suggestions']
                section_text = regenerate.content
        else:
            logging.getLogger(__name__).warn(
                "Failed to pass law model after threshold %d.", threshold)

        return {"success": False, "content": regenerate.content}


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


def prepare_generate_pipeline(
    generate_template: str,
    token_counter: Optional[TokenCountingHandler] = None,
    verbose: bool = False,
) -> QueryPipeline:
    """Prepare a pipeline for (re)generating a section of a privacy policy

    :param generate_template: a template for (re)generating a section
    :param token_counter: a token counter for counting tokens
    :param verbose: whether to show verbose output
    :return: a pipeline for (re)generating a section of a privacy policy
    """

    generate_parser = PydanticOutputParser(SectionContent)
    generate_template = PromptTemplate(
        generate_parser.format(generate_template))
    regenerate_pipeline = QueryPipeline(
        chain=[generate_template, Settings.llm, generate_parser],
        callback_manager=CallbackManager([token_counter])
        if token_counter else None,
        verbose=verbose,
    )

    return regenerate_pipeline


def prepare_section_judge_pipeline(
    law_llm: HuggingFaceLLMModified,
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

        for judge in judges.judges:
            if judge.name.value == section_name:
                return {"pass": False, "suggestions": judge.suggestions}

        return {"pass": True, "suggestions": ""}

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
