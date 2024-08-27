import logging
from typing import Dict, List, Any

import pandas as pd
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.query_pipeline import QueryPipeline

from .prompts import (
    GENERATE_PROMPT,
    REGENERATE_PROMPT,
)
from .law_model import prepare_law_llm
from .pipelines import (
    prepare_regulation_query_engine,
    prepare_regulation_syllabus_pipeline,
    prepare_generate_pipeline,
    prepare_section_judge_pipeline,
)


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
