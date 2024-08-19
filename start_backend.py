import os
import logging
import logging.config

import uvicorn
import tiktoken
import nest_asyncio
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings, set_global_handler
from llama_index.core.callbacks import CallbackManager, TokenCountingHandler

nest_asyncio.apply()
load_dotenv()

if os.getenv("LOGGING_MODE") == "simple":
    logging.config.fileConfig('./config/logging.cfg')
    set_global_handler(
        "simple",
        logger=logging.getLogger('agent'),
    )
else:
    set_global_handler(os.getenv("LOGGING_MODE"))

llm = OpenAI(model=os.getenv("OPENAI_MODEL_ID"))
Settings.llm = llm

tokenizer_fn = tiktoken.encoding_for_model(os.getenv("OPENAI_MODEL_ID")).encode
token_counter = TokenCountingHandler(tokenizer=tokenizer_fn, verbose=True)
Settings.callback_manager = CallbackManager([token_counter])

if __name__ == '__main__':
    from src.generation_api import app

    uvicorn.run(app, host='127.0.0.1', port=9999)
