import os

from typing import List, Tuple, Optional
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings, VectorStoreIndex
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.readers.web import SimpleWebPageReader
from .data_regulation_prompts import REGION_TEMPLATE
import json
import pandas as pd

#DATA_REGULATION_PATH = '../data/regulations/region_data_regulations.json'
REGION_DATA_REGULATION_PATH = '../data/regulations/Region Data Regulations.csv'

class DataRegulationAgent:

    def __init__(
            self,
            api_key: str,
            model: str = 'gpt-4o',
            region_template: str = REGION_TEMPLATE
                 ):
        self.api_key = api_key
        self.llm = OpenAI(model=model, openai_api_key=api_key)
        Settings.llm = self.llm
        self.REGION_TEMPLATE = region_template
        self.region_data_regulations = pd.read_csv(REGION_DATA_REGULATION_PATH)
        self.region_url_dict = dict(zip(self.region_data_regulations['regions'], 
                                        self.region_data_regulations['links']))

    def determine_region(self, user_input: str, 
                         temperature: float = 0.3, 
                         max_tokens: int = 50) -> str:
        """
        Finding a region corresponding to the user's input.
        """
        prompt = self.REGION_TEMPLATE.format(user_input=user_input)
        response = self.llm.complete(prompt=prompt, max_tokens = max_tokens, temperature=temperature)
        answer = response.text
        return answer

    def clean_region_output(self, text: str) -> str:
        """
        Clean generated response
        """
        text = text.strip().replace("The regions that the user input belongs to is (are):", "").strip()
        text = text.split('\n')[0]
        return text

    def get_data_regulation_url(self, region_name: str) -> str:
        """
        Get data regulation url.
        """
        return self.region_url_dict.get(region_name, "Privacy law URL not found for this region")

    def get_data_regulation_links(self, user_input: str) -> Tuple[List[str], List[str]]:
        """
        Get all data regulation links that are relevant to the user's input location.
        """
        regions = self.determine_region(user_input)
        regions = self.clean_region_output(regions)
        region_list = regions.split(', ')
        links: List[str] = [self.get_data_regulation_url(region) for region in region_list]
        return region_list, links
    
    def get_data_regulation_info(self, location: str) -> Optional[QueryEngineTool]:
        """
        Return a QueryEngineTool
        """
        regions, links = self.get_privacy_law_links(location)

        # if location's data regulation link not store in self.region_data_regulations
        if  'Privacy law URL not found for this region' in links:
            print('Data regulation law URL not found for this location.')
            return None
        
        # Load data from the provided links using SimpleWebPageReader
        reader = SimpleWebPageReader(html_to_text=True).load_data(links)
    
        # Create a list of QueryEngineTool objects for each region and its corresponding data
        data_regulation_query_tool = [
            QueryEngineTool(
                query_engine=VectorStoreIndex.from_documents([reader[i]]).as_query_engine(),
                metadata=ToolMetadata(
                    name=f"fta_regulation_for_{regions[i]}",
                    description=(f"useful for when you want to know {regions[i]}'s data regulation"),
                ),
            ) for i in range(len(links))
        ]
        
        # Create a SubQuestionQueryEngine using the list of QueryEngineTool objects
        data_regulation_query_engine = SubQuestionQueryEngine.from_defaults(
            query_engine_tools=data_regulation_query_tool
        )
        
        # Create the final QueryEngineTool for handling sub-questions related to data regulations
        data_regulation_query_engine_tool = QueryEngineTool(
            query_engine=data_regulation_query_engine,
            metadata=ToolMetadata(
                name="sub_question_query_engine_for_data_regulation",
                description=(
                    "useful for when you want to answer queries that require analyzing"
                    f" multiple data regulations from different regions, including: {', '.join(regions)}"
                ),
            ),
        )
        return data_regulation_query_engine_tool


