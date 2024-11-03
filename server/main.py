from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from logging import Logger

app = FastAPI()

BOT_DOCUMENT = "bot_document"
BOT_SQL = "bot_sql"
BOT_INTERNET = "bot_internet"

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=['POST', 'GET', 'PUT', 'DELETE'], 
    allow_headers=["*"]
)

@app.post('/chat/{bot_name}/{conv_id}')
async def handleChat(bot_name, conv_id, file: UploadFile = File(None)):
    if bot_name == BOT_DOCUMENT and file is not None:
        print('Got file!')

    