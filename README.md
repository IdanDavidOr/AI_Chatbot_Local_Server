# AI Chatbot Local Server

A FastAPI-based local server that provides a chat interface powered by OpenRouter AI. This server enables real-time communication through WebSockets and serves a clean web interface for interacting with the AI.

## Features

- Real-time chat interface using WebSockets
- Integration with OpenRouter AI API
- Clean and responsive web UI
- Easy local deployment
- AWS Lambda compatible (using Mangum)

## Prerequisites

- Python 3.8+
- pip or conda for package management

## Installation

1. Clone the repository:
   ```bash
   git clone [your-repo-url]
   cd ai-chatbot-local-server
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=your_api_key_here
   ```

## Usage

1. Start the server:
   ```bash
   python main.py
   ```
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000
   ```

## Project Structure

```
ai-chatbot-local-server/
├── app/
│   └── templates/      # HTML templates
├── static/            # Static files (CSS, JS)
├── main.py           # Main application file
├── requirements.txt  # Project dependencies
└── .env             # Environment variables (not tracked in git)
```

## Configuration

The server can be configured using environment variables in the `.env` file:

- `OPENROUTER_API_KEY`: Your OpenRouter API key
- Additional configuration can be added in the `.env` file as needed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Security Note

Never commit your `.env` file or expose your API keys. The `.gitignore` file is configured to prevent this, but always verify before committing. 