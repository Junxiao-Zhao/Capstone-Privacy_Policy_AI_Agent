import logging
import logging.config

import uvicorn
import tiktoken
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings, set_global_handler
from llama_index.core.callbacks import CallbackManager, TokenCountingHandler

load_dotenv()

logging.config.fileConfig('./config/logging.cfg')
set_global_handler(
    "simple",
    logger=logging.getLogger('agent'),
)

if __name__ == '__main__':
    from src.generation_api import app

    llm = OpenAI(model="gpt-4o")
    Settings.llm = llm

    tokenizer_fn = tiktoken.encoding_for_model("gpt-4o").encode
    token_counter = TokenCountingHandler(tokenizer=tokenizer_fn, verbose=True)
    Settings.callback_manager = CallbackManager([token_counter])

    uvicorn.run(app, host='127.0.0.1', port=9999)
