import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from logging import Logger
from sofia.sofia_file import SQLChatbot, create_bot
from pydantic import BaseModel

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

print('Running server script.')

class UserMessage(BaseModel):
    content: str

sql_bot : SQLChatbot = None

@app.post('/chat/{bot_name}/{conv_id}')
async def handleChat(message: UserMessage, bot_name, conv_id):
    # if bot_name == BOT_DOCUMENT and file is not None:
    #     print('Got file!')
    global sql_bot
    if not sql_bot:
        sql_bot = create_bot()
    chat_response = sql_bot.call_llm(message.content)
    return JSONResponse(content={"response": chat_response}, status_code=200)




    