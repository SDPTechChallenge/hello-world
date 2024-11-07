from pydantic import BaseModel
from typing import Optional, List
from marcus.document_assistant import DocumentAssistant
from thalita.search_assistant import InternetSearchAssistant
from sofia.sql_assistant import SQLAssistant
from utils.helpers import get_root_filepath
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

UPLOAD_DIRECTORY = "uploaded_files"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


def remove_uploaded_files():
    for file in document_filepaths:
        os.remove(file)
    document_filepaths.clear()

# A function that reads a directory and returns a list of all files in it. By default, we will read the "uploaded_files" directory.


def get_uploaded_files(dir=UPLOAD_DIRECTORY):
    # Absolute path of the dir:
    dir = get_root_filepath(dir)
    return [file for file in os.listdir(dir) if os.path.isfile(get_root_filepath(f"{dir}/{file}"))]


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
            document_bot = DocumentAssistant(filepath=document_filepaths[0])
        response = document_bot.process_user_message(message.content)
        return JSONResponse(content={"response": response}, status_code=200)

    if bot_name == BOT_SQL:
        if not sql_bot:
            sql_bot = SQLAssistant.create()
        response = sql_bot(message.content)
        return JSONResponse(content={"response": response}, status_code=200)
        # return StreamingResponse(content=stream_generator(response, lambda message: sql_bot.messages.append({"role": "assistant", "content": message})), status_code=200)

    if bot_name == BOT_INTERNET:
        if not internet_bot:
            internet_bot = InternetSearchAssistant.create()
        try:
            response = internet_bot.get_completion(message.content)
            if response:
                return JSONResponse(content={"response": response}, status_code=200)
        except Exception as e:
            return JSONResponse(content={"error": str(e)}, status_code=500)


sqlbot = SQLAssistant.create()
print('SQLBot created.')

search_bot = InternetSearchAssistant.create()
print('SearchBot created.')

print(get_uploaded_files())
