from pydantic import BaseModel
from typing import Optional, List
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
        if isinstance(chunk, dict):
            if 'answer' in chunk:
                content = chunk['answer'] or ""
                complete_response += content
                yield content
            else:
                continue
        elif chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content or ""
            complete_response += content
            yield content

    if callback_fn:
        callback_fn(complete_response, *args, **kwargs)


document_filepaths = []
saved_files = []

UPLOAD_DIRECTORY = "uploaded_files"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


def remove_uploaded_files():
    for file in document_filepaths:
        os.remove(file)
    document_filepaths.clear()


@app.post('/documents')
async def handle_document_upload(files: List[UploadFile] = File(...)):
    # First remove all files from the previous request
    # remove_uploaded_files()
    try:
        for file in files:
            if file:
                file_path = os.path.abspath(
                    os.path.join(UPLOAD_DIRECTORY, file.filename))
                with open(file_path, "wb") as buffer:
                    buffer.write(await file.read())
                document_filepaths.append(file_path)
                saved_files.append(file_path)
        return JSONResponse(content={"response": f'Files saved at {saved_files}'}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post('/chat/{bot_name}/{conv_id}')
def handleChat(message: Optional[UserMessage], bot_name=BOT_DOCUMENT, conv_id=""):
    global sql_bot
    global document_bot
    global internet_bot
    global document_filepaths

    print(f'Got request for: {bot_name}')
    print(f'Content: {message.content}')

    if bot_name == BOT_DOCUMENT:
        if not document_bot:
            document_bot = MarcusChatbot(filepath=document_filepaths[0])
        response = document_bot.process_user_message(message.content)
        print(response)
        return StreamingResponse(content=stream_generator(response, lambda message: document_bot.messages.append({"role": "assistant", "content": message})), status_code=200, headers={"Content-Type": "text/event-stream"})

    if bot_name == BOT_SQL:
        if not sql_bot:
            sql_bot = create_bot()
        response = sql_bot(message.content)
        return JSONResponse(content={"response": response}, status_code=200, headers={"Content-Type": "application/json"})
        # return StreamingResponse(content=stream_generator(response, lambda message: sql_bot.messages.append({"role": "assistant", "content": message})), status_code=200)
