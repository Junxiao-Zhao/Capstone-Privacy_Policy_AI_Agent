from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from transformers import pipeline
import pandas as pd
import nest_asyncio
import json
import sys
from typing import List, Dict, Any, Optional

import tiktoken
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from llama_index.core import SummaryIndex, VectorStoreIndex
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core.tools import BaseTool, FunctionTool
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.agent import ReActAgent
from llama_index.core.response_synthesizers import TreeSummarize
from llama_index.core.query_pipeline import QueryPipeline, FnComponent
from llama_index.core import PromptTemplate
from llama_index.core import get_response_synthesizer
from llama_index.core.response_synthesizers import ResponseMode
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.callbacks import CallbackManager, TokenCountingHandler
from pydantic import BaseModel, Field, conlist, field_validator
from enum import Enum
from IPython.display import Markdown, display
from duckduckgo_search import DDGS
import os
script_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, '..'))

nest_asyncio.apply()
from frontend.constants import *

from frontend.policy_generator import *


from src.pipelines import (
    prepare_regulation_syllabus_pipeline,
    prepare_regulation_query_engine,
    prepare_generate_pipeline,
    prepare_section_judge_pipeline,
    prepare_region_selection_pipeline,
)

from src.generators import (
    prepare_regulation_syllabus_pipeline,
    prepare_regulation_query_engine,
    prepare_generate_pipeline,
    prepare_section_judge_pipeline,
    PrivacyPolicyGenerator,
)
from src.prompts import (
    ASK_SYLLABUS_TEMPLATE,
    FORMAT_SYLLABUS_TEMPLATE,
    REGENERATE_PROMPT,
    GENERATE_PROMPT,
    JUDGE_SECTION_TEMPLATE,
    FORMAT_JUDGE_TEMPLATE,
)
from src.formats import (
    Syllabus,
    SectionNames,
    Judges,
    Judge,
    SectionContent,
)
from src.law_model import prepare_law_llm

#from src.tool import dict_to_markdown

app = FastAPI()

links_df = pd.read_csv('../data/regulations/regulations.csv', encoding='utf-8')
sub_links_df = None
regulation_syllabus = None

#初始化模型防止重复生成
generator_region_selection = None
generator_regulation_query = None
generator_regulation_syllabus = None
generator_generate_pipline = None
generator_regenerate_pipline = None
generator_law_llm = None
generator_section_judge_pipeline = None

class InputData(BaseModel):
    type: str
    content: str = None
    #content: List[str]


def get_generator_region_selection(verbose = DISPLAY_TEMPLATE):
    global generator_region_selection
    if generator_region_selection is None:
        generator_region_selection = prepare_region_selection_pipeline(verbose=verbose)
    return generator_region_selection

def get_generator_regulation_query(verbose = DISPLAY_TEMPLATE):
    global generator_regulation_query
    if generator_regulation_query is None:
        generator_regulation_query = prepare_regulation_query_engine( sub_links_df ,verbose=verbose)
    return generator_regulation_query

def get_generator_regulation_syllabus(verbose = DISPLAY_TEMPLATE):
    global generator_regulation_syllabus
    if generator_regulation_syllabus is None:
        generator_regulation_syllabus = prepare_regulation_syllabus_pipeline(
            get_generator_regulation_query(verbose = verbose).run(), verbose=verbose)
    return generator_regulation_syllabus

def get_generator_generate_pipline(verbose = DISPLAY_TEMPLATE):
    global generator_generate_pipline
    if generator_generate_pipline is None:
        generator_generate_pipline = prepare_generate_pipeline(GENERATE_PROMPT,
                                                     verbose=verbose)
    return generator_generate_pipline

def get_generator_regenerate_pipline(verbose = DISPLAY_TEMPLATE):
    global regenerate_pipeline
    if regenerate_pipeline is None:
        regenerate_pipeline = prepare_generate_pipeline(REGENERATE_PROMPT,
                                                        verbose=verbose)
    return regenerate_pipeline

def get_generator_law_llm():
    global generator_law_llm
    if generator_law_llm is None:
        generator_law_llm = prepare_law_llm()
    return generator_law_llm

def get_generator_section_judge_pipeline(verbose = DISPLAY_TEMPLATE):
    global generator_section_judge_pipeline
    if generator_section_judge_pipeline is None:
        generator_section_judge_pipeline = prepare_section_judge_pipeline(get_generator_law_llm(),
                                                        verbose=verbose)
    return generator_section_judge_pipeline

@app.post("/process_input/")
async def process_input(data: InputData):
    global links_df
    global sub_links_df
    global regulation_syllabus
    input_type = data.type
    content = data.content
    
    
    if input_type == 'region_selection':
        # e.g. content = "San Diego"
        content = data.content
        if content is None or type(content) is not str:
            raise HTTPException(status_code=400, detail="Content error region_selection.")
        generator = get_generator_region_selection()
        result = generator().run(content)
        sub_links_df = links_df.loc[links_df['regions'].isin(result)]
        return {"message": f"Parameter links_df updated to {result}"}
        """
        #不一定会有,保留
        elif input_type == 'Region_query':
            content = data.content
            if content is None:
                raise HTTPException(status_code=400, detail="Content error regulation_query.")
            generator = get_generator_regulation_query()
            result = generator().run()
            #待修改
            return {"response": result[0]['generated_text']}
        """
    elif input_type == 'regulation_syllabus':
        # e.g. content = List[regulation], ["CCPA"]
        content = data.content
        if content is None:
            raise HTTPException(status_code=400, detail="Content error regulation_syllabus.")
        generator = get_generator_regulation_syllabus()
        regulations = ', '.join(content)
        result = generator().run(regulations = regulations)
        regulation_syllabus = result
        # 可能要转为json格式
        return {"response": result[0]['generated_text']}
    
    elif input_type == 'generate_pipline':
        content = data.content
        if content is None:
            raise HTTPException(status_code=400, detail="Content error generate_pipline.")
        generator = get_generator_generate_pipline()
        result = generator().run()
        #待修改
        return {"response": result[0]['generated_text']}
    
    elif input_type == 'regenerate_pipline':
        content = data.content
        if content is None:
            raise HTTPException(status_code=400, detail="Content error regenerate_pipline.")
        generator = get_generator_regenerate_pipline()
        result = generator().run()
        #待修改
        return {"response": result[0]['generated_text']}
    
    elif input_type == 'law_llm':
        content = data.content
        if content is None:
            raise HTTPException(status_code=400, detail="Content error law_llm.")
        generator = get_generator_law_llm()
        result = generator().run()
        #待修改
        return {"response": result[0]['generated_text']}
    
    elif input_type == 'section_judge_pipeline':
        content = data.content
        if content is None:
            raise HTTPException(status_code=400, detail="Content error section_judge_pipeline.")
        generator = get_generator_section_judge_pipeline()
        result = generator().run()
        #待修改
        return {"response": result[0]['generated_text']}
    
    else:
        raise HTTPException(status_code=400, detail=f"Invalid input type{input_type}. Must be one of the defined types.")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8000)