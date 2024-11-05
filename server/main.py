from pydantic import BaseModel
from typing import Optional
from marcus.marcus_chat import MarcusChatbot
from sofia.sofia_file import SQLChatbot, create_bot
from logging import Logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi import FastAPI, File, UploadFile
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

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


sql_bot = None
document_bot = None
internet_bot = None


def stream_generator(response, callback_fn, *args, **kwargs):
    complete_response = ""

    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content or ""
            complete_response += content
            yield content

    if callback_fn:
        callback_fn(complete_response, *args, **kwargs)


document_filepaths: [str] = []

UPLOAD_DIRECTORY = "uploaded_files"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


@app.post('/chat/{bot_name}/{conv_id}')
async def handleChat(message: Optional[UserMessage], bot_name=BOT_DOCUMENT, conv_id="", file: UploadFile = File(None)):
    global sql_bot
    global document_bot
    global internet_bot
    global document_filepaths

    # Let's save the document to file and its path to the list
    if document:
        file_path = os.path.abspath(
            os.path.join(UPLOAD_DIRECTORY, file.filename))
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        document_filepaths.append(file_path)
        return JSONResponse(content={"response": f'File saved at {file_path}'}, status_code=200)

    if bot_name == BOT_DOCUMENT:
        if not document_bot:
            document_bot = MarcusChatbot()
        response = document_bot(message.content)
        return StreamingResponse(content=stream_generator(response, lambda message: document_bot.messages.append({"role": "assistant", "content": message})), status_code=200)

    if bot_name == BOT_SQL:
        if not sql_bot:
            sql_bot = create_bot()
        response = sql_bot(message.content)
        return JSONResponse(content={"response": response}, status_code=200)
        # return StreamingResponse(content=stream_generator(response, lambda message: sql_bot.messages.append({"role": "assistant", "content": message})), status_code=200)
