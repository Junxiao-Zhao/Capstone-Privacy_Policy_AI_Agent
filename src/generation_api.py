import os
import json
import logging
import asyncio
import functools
from typing import Dict, List, Any, Callable

import pandas as pd
from fastapi import FastAPI, UploadFile, HTTPException, Form
from llama_index.llms.text_generation_inference import TextGenerationInference

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
from .formats import SectionNames

if os.getenv("TGI_ENDPOINT"):
    law_llm = TextGenerationInference(
        model_url=os.getenv("TGI_ENDPOINT"),
        model_name=os.getenv("LAW_MODEL_ID"),
        token=False,
    )
else:
    law_llm = prepare_law_llm(os.getenv("LAW_MODEL_ID"))

verbose = os.getenv("VERBOSE", "false").lower() == "true"
app = FastAPI(version=os.getenv("VERSION", "beta"))

# prepare pipelines
links_df = pd.read_csv('./data/regulations/regulations.csv', encoding='utf-8')
regulation_query_engine = prepare_regulation_query_engine(links_df)
syllabus_pipeline = prepare_regulation_syllabus_pipeline(
    regulation_query_engine, verbose=verbose)
generate_pipline = prepare_generate_pipeline(GENERATE_PROMPT, verbose=verbose)
regenerate_pipeline = prepare_generate_pipeline(REGENERATE_PROMPT,
                                                verbose=verbose)
judge_pipeline = prepare_section_judge_pipeline(law_llm, verbose=verbose)


def retry_on_exception(retries: int = 5, delay: float = 1.0):

    def decorator(func: Callable):

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for _ in range(retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    await asyncio.sleep(delay)
            raise HTTPException(status_code=500, detail=str(last_exception))

        return wrapper

    return decorator


@app.post("/syllabus")
@retry_on_exception(retries=3, delay=2.0)
async def get_syllabus(regulations: str = Form(...)) -> Dict[str, List[str]]:
    """Get a privacy policy syllabus

    :param regulations: the regulations to comply with
    :return: a privacy policy syllabus
    """

    syllabus = await syllabus_pipeline.arun(regulations=regulations)
    return syllabus


@app.post("/generate")
@retry_on_exception(retries=3, delay=2.0)
async def generate(
        section_name: SectionNames = Form(...),
        information: str = Form(...),
        syllabus: str = Form(...),
        regulations: str = Form(...),
        threshold: int = Form(3),
) -> Dict[str, Any]:
    """Generate a section of a privacy policy

    :param section_name: the name of the section
    :param information: the information for generating the section
    :param syllabus: the syllabus for generating sections
    :param regulations: the regulations to comply with
    :param threshold: the maximum number of attempts to regenerate
    :return: success or not and the generated section
    """

    section_name = section_name.value
    syllabus = json.loads(syllabus)

    # generate a section
    section_content = await generate_pipline.arun(
        section_name=section_name,
        information=information,
        key_points='\n'.join(syllabus[section_name]),
    )

    # judge the section
    judge = await judge_pipeline.arun(
        section_name=section_name,
        section_text=section_content.content,
        regulations=regulations,
    )

    if judge['pass']:
        return {"success": True, "content": section_content.content}

    regenerate_result = await regenerate(
        section_name=section_name,
        section_text=section_content.content,
        syllabus=syllabus,
        regulations=regulations,
        suggestions=judge['suggestions'],
        threshold=threshold,
    )

    return regenerate_result


@retry_on_exception(retries=3, delay=2.0)
async def regenerate(
    section_name: str,
    section_text: str,
    syllabus: Dict[str, List[str]],
    regulations: str,
    suggestions: str,
    threshold: int = 5,
):
    """Regenerate a section of a privacy policy

    :param section_name: the name of the section
    :param section_text: the text of the section
    :param syllabus: the syllabus for generating sections
    :param regulations: the regulations to comply with
    :param suggestions: the suggestions for improvement
    :param threshold: the maximum number of attempts to regenerate
    :return: success or not and the regenerated section
    """

    key_points = '\n'.join(syllabus[section_name])

    for i in range(threshold):

        regenerate_result = await regenerate_pipeline.arun(
            section_name=section_name,
            section_text=section_text,
            suggestions=suggestions,
            key_points=key_points,
        )

        judge = await judge_pipeline.arun(
            section_name=section_name,
            section_text=regenerate_result.content,
            regulations=regulations,
        )

        if judge['pass']:
            return {"success": True, "content": regenerate_result.content}

        else:
            suggestions = judge['suggestions']
            section_text = regenerate_result.content

    return {"success": False, "content": regenerate_result.content}
