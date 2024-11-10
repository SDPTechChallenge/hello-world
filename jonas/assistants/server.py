from pydantic import BaseModel
from typing import Optional, List
# from marcus.document_assistant import DocumentAssistant
# from thalita.search_assistant import InternetSearchAssistant
# from sofia.sql_assistant import SQLAssistant
# from utils.helpers import get_root_filepath
from general_assistant import GeneralAssistant
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi import FastAPI, File, UploadFile
import os

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
search_bot = None

document_filepaths = []

UPLOAD_DIRECTORY = "uploaded_files"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


def remove_uploaded_files():
    for file in document_filepaths:
        os.remove(file)
    document_filepaths.clear()

# A function that reads a directory and returns a list of all files in it. By default, we will read the "uploaded_files" directory.


@app.get('/teste')
def show_message():
    return JSONResponse(content={"response": "Hello, world!"}, status_code=200)


@app.post('/documents')
async def handle_document_upload(files: List[UploadFile] = File(...)):
    try:
        file_count = 0
        for file in files:
            if file:
                file_path = get_root_filepath(
                    f"{UPLOAD_DIRECTORY}/{file.filename}")
                with open(file_path, "wb") as buffer:
                    buffer.write(await file.read())
                file_count += 1
        if document_bot:
            document_bot.load_document(file_path)
        return JSONResponse(content={"response": f'{file_count} files saved at uploaded_files'}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# A function that gets the absolute path to the first .pdf file in the "uploaded_files" directory.


@app.post('/chat/{bot_name}')
def handleChat(message: Optional[UserMessage], bot_name=BOT_DOCUMENT):
    global sql_bot
    global document_bot
    global internet_bot
    global document_filepaths

    print(f'Got request for: {bot_name}')
    print(f'Content: {message.content}')

    