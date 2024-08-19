import os
import json
import logging
import asyncio
import tempfile
import functools
from typing import Dict, List, Any, Callable

import pandas as pd
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from llama_index.core import (
    StorageContext,
    SimpleDirectoryReader,
    SummaryIndex,
    Document,
)
from llama_index.core.memory import VectorMemory
from llama_index.core.indices import load_index_from_storage
from llama_index.llms.text_generation_inference import TextGenerationInference
from llama_parse import LlamaParse

from .prompts import (
    GENERATE_PROMPT,
    REGENERATE_PROMPT,
    COMPOSE_SYLLABUS_TEMPLATE,
    QUERY_SYLLABUS_SECTION_TEMPLATE,
    QUERY_SECTION_KEY_POINTS_TEMPLATE,
)
from .law_model import prepare_law_llm
from .pipelines import (
    prepare_regulation_syllabus_pipeline,
    prepare_generate_pipeline,
    prepare_section_judge_pipeline,
    prepare_region_selection_pipeline,
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
links_df = pd.read_csv('./data/regulations/Region Data Regulation.csv',
                       encoding='utf-8')
syllabus_pipeline = prepare_regulation_syllabus_pipeline(verbose=verbose)
generate_pipline = prepare_generate_pipeline(GENERATE_PROMPT, verbose=verbose)
regenerate_pipeline = prepare_generate_pipeline(REGENERATE_PROMPT,
                                                verbose=verbose)
judge_pipeline = prepare_section_judge_pipeline(law_llm, verbose=verbose)
region_selection_pipeline = prepare_region_selection_pipeline(verbose=verbose)

# load regulation memory and pdf parser
stored_history = StorageContext.from_defaults(
    persist_dir='./data/regulations/vector_memory')
regulation_memory = VectorMemory(
    vector_index=load_index_from_storage(stored_history),
    retriever_kwargs={"similarity_top_k": 1},
)
parser = LlamaParse(result_type="text")


def retry_on_exception(retries: int = 5, delay: float = 1.0):
    """Retry on exception decorator

    :param retries: the number of retries
    :param delay: the delay between retries
    :return: a retry decorator
    """

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

            logging.getLogger(__name__).exception(last_exception)
            raise HTTPException(status_code=500, detail=str(last_exception))

        return wrapper

    return decorator


@app.post("/regulations")
@retry_on_exception(retries=3, delay=2.0)
async def select_regulations(areas: str = Form(...)):
    """Select regulations based on the areas of services

    :param areas: the areas of services
    :return: a list of selected regulations, regions, and links
    """

    regions = await region_selection_pipeline.arun(user_input=areas)

    sub_links_df = links_df.loc[links_df['regions'].isin(regions)]
    sub_links_df = sub_links_df.drop(columns='file_paths', errors='ignore')

    return sub_links_df.to_dict(orient='records')


@app.post("/syllabus")
@retry_on_exception(retries=3, delay=2.0)
async def get_syllabus(
        regulations: str = Form(""),
        upload_files: List[UploadFile] = File([]),
) -> Dict[str, List[str]]:
    """Get a privacy policy syllabus

    :param regulations: the regulations to comply with
    :param upload_files: the user uploaded files
    :return: a privacy policy syllabus
    """

    if not regulations and not upload_files:
        return {}

    regulations = map(str.strip, regulations.split(','))
    stored_regulations = set(links_df['regulations'].to_list())
    query_str = ''

    for regulation in regulations:

        if regulation in stored_regulations:
            syllabus_content = regulation_memory.get(regulation)[1:]
            query_str += COMPOSE_SYLLABUS_TEMPLATE.format(
                regulation=regulation,
                sections=syllabus_content[0].content,
                key_points=syllabus_content[1].content,
            )

    if upload_files:
        with tempfile.TemporaryDirectory() as temp_dir:
            for file in upload_files:
                file_path = os.path.join(temp_dir, file.filename)
                with open(file_path, "wb") as temp_file:
                    temp_file.write(await file.read())

            documents = SimpleDirectoryReader(
                input_dir=temp_dir,
                file_extractor={
                    ".pdf": parser
                },
            ).load_data()

        tasks = [
            get_raw_syllabus_from_document(document) for document in documents
        ]
        results = await asyncio.gather(*tasks)
        query_str += ''.join(results)

    syllabus = await syllabus_pipeline.arun(query_str=query_str)
    return syllabus


async def get_raw_syllabus_from_document(document: Document) -> str:
    """Get a privacy policy syllabus from a document

    :param document: the llamaindex document
    :return: a privacy policy's sections and key points
    """

    query_engine = SummaryIndex.from_documents([document])\
        .as_query_engine(response_mode="tree_summarize")
    file_name = document.metadata['file_name'].split('.')[0]

    sections = await query_engine.aquery(
        QUERY_SYLLABUS_SECTION_TEMPLATE.format(regulation=file_name))

    key_points = await query_engine.aquery(
        QUERY_SECTION_KEY_POINTS_TEMPLATE.format(
            sections=sections.response,
            regulation=file_name,
        ))

    query_str = COMPOSE_SYLLABUS_TEMPLATE.format(
        regulation=file_name,
        sections=sections.response,
        key_points=key_points.response,
    )

    return query_str


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
        return {
            "success": True,
            "content": section_content.content,
            "suggestions": "",
        }

    if threshold <= 0:
        return {
            "success": False,
            "content": section_content.content,
            "suggestions": judge['suggestions'],
        }

    regenerate_result = await regenerate(
        section_name=section_name,
        section_text=section_content.content,
        syllabus=syllabus,
        regulations=regulations,
        suggestions=judge['suggestions'],
        threshold=threshold,
    )

    return regenerate_result


@app.post("/regenerate")
async def api_regenerate(
        section_name: str = Form(...),
        section_text: str = Form(...),
        syllabus: str = Form(...),
        regulations: str = Form(...),
        suggestions: str = Form(...),
        threshold: int = Form(3),
) -> Dict[str, Any]:
    """
    Regenerate a section of a privacy policy using the
    existing `regenerate` function.

    :param section_name: the name of the section
    :param section_text: the text of the section
    :param syllabus: the syllabus for generating sections
    :param regulations: the regulations to comply with
    :param suggestions: the suggestions for improvement
    :param threshold: the maximum number of attempts to regenerate
    :return: success or not and the regenerated section
    """
    syllabus_dict = json.loads(syllabus)

    # Call the existing regenerate function directly
    result = await regenerate(section_name=section_name,
                              section_text=section_text,
                              syllabus=syllabus_dict,
                              regulations=regulations,
                              suggestions=suggestions,
                              threshold=threshold)

    return result


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
            return {
                "success": True,
                "content": regenerate_result.content,
                "suggestions": "",
            }

        else:
            suggestions = judge['suggestions']
            section_text = regenerate_result.content

    return {
        "success": False,
        "content": section_text,
        "suggestions": suggestions,
    }
