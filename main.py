import sys
import os

# # show the current working directory and system path
# print("#"*100)
# print(f"{os.getcwd()=}")
# for path in sys.path:
#     print(f" - {path}")
# print("#"*100)

from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates  # Import Jinja2Templates
from pathlib import Path
import logging
import json
import requests
from mangum import Mangum

from dotenv import load_dotenv
# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Create a handler for AWS Lambda
handler = Mangum(app)

# # Get the root directory
local_server_path = Path(__file__).parent
# # Get the static directory
static_path = local_server_path / 'static'

# # Mount the static directory 
app.mount("/static", StaticFiles(directory=static_path.resolve()), name="static")


# Set your OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # Replace with your actual API key

async def openrouter_api_call(data: str):
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                # "HTTP-Referer": f"{YOUR_SITE_URL}", # Optional
                # "X-Title": f"{YOUR_APP_NAME}", # Optional
            },
            data=json.dumps({
                # "model": "meta-llama/llama-3.1-405b-instruct:free",  # Optional
                "model": "meta-llama/llama-3.2-3b-instruct:free",
                "messages": [
                    {
                        "role": "user",
                        "content": data
                    }
                ]
            })
        )
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

templates = Jinja2Templates(directory=(Path(__file__).parent / "app" / "templates").resolve())  # Set the templates directory

@app.get("/")
async def get(request: Request) -> HTMLResponse:
    """
    Render the chat page.

    Parameters
    ----------
    request : Request
        The request object.

    Returns
    -------
    HTMLResponse
        The rendered HTML page.
    """
    return templates.TemplateResponse("chat_page.html", {"request": request})  # Render the HTML file


async def autoresponder(data: str, delay: int = 1) -> str:
    """
    Respond to the incoming data.
    mocking a response from the AI

    Parameters
    ----------
    data : str
        The incoming data from the WebSocket.
    delay : int
        The delay in seconds before sending the response.
    """
    api_response = await openrouter_api_call(data) 
    
    if "error" in api_response:
        response = api_response['error']['message']
        logger.info(f"Error: {response}")
    else:
        response = api_response['choices'][0]['message']['content']
        logger.info(f"AI: {response}")

    return response, api_response

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """
    Handle WebSocket connections for real-time communication.

    Parameters
    ----------
    websocket : WebSocket
        The WebSocket connection object.

    Returns
    -------
    None
        This function does not return a value. It sends messages back to the client.
    
    Raises
    ------
    WebSocketDisconnect
        If the WebSocket connection is closed by the client.
    Exception
        For any other exceptions that may occur during message handling.
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Call the OpenRouter API
            response, api_response = await autoresponder(data)
            # Extract the response content
            await websocket.send_text(f"AI: {response}")
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed.")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


# Change the main block to use the handler
if __name__ == "__main__":
    import uvicorn
    # Change the app reference to an import string
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)