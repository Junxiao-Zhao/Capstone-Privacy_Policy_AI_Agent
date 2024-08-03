import logging
import logging.config

import uvicorn
import llama_index.core
from dotenv import load_dotenv

load_dotenv()

logging.config.fileConfig('./config/logging.cfg')
llama_index.core.set_global_handler(
    "simple",
    logger=logging.getLogger(__name__),
)

if __name__ == '__main__':
    from src.generation_api import app

    uvicorn.run(app, host='127.0.0.1', port=9999)
