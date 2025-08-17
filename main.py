from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from openai import OpenAI
import os
import json
import asyncio
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="OpenWebUI - FastAPI",
    description="A FastAPI-based OpenWebUI application with OpenAI integration",
    version="1.0.0"
)

# OpenAI configuration
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if not os.getenv("OPENAI_API_KEY"):
    logger.warning("OPENAI_API_KEY not found in environment variables")

# Models
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: str = "gpt-4o-mini"  # Updated default to GPT-4o-mini
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    stream: bool = False

class ChatResponse(BaseModel):
    response: str
    model: str
    usage: Optional[Dict[str, Any]] = None

# HTML template as Python string
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenWebUI - FastAPI</title>
    <link rel="stylesheet" href="/static/css/style.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1><i class="fas fa-robot"></i> OpenWebUI</h1>
            <div class="header-controls">
                <select id="modelSelect" class="model-select">
                    <option value="gpt-4o-mini" selected>GPT-4o Mini</option>
                    <option value="gpt-4o">GPT-4o</option>
                    <option value="gpt-4-turbo">GPT-4 Turbo</option>
                    <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                </select>
                <button id="clearHistory" class="btn btn-secondary">
                    <i class="fas fa-trash"></i> Clear History
                </button>
            </div>
        </header>

        <main class="main">
            <div class="chat-container">
                <div id="chatMessages" class="chat-messages"></div>
                
                <div class="chat-input-container">
                    <div class="input-wrapper">
                        <textarea 
                            id="messageInput" 
                            class="message-input" 
                            placeholder="Type your message here..."
                            rows="3"
                        ></textarea>
                        <button id="sendButton" class="btn btn-primary send-btn">
                            <i class="fas fa-paper-plane"></i>
                        </button>
                    </div>
                    <div class="input-controls">
                        <label class="temperature-control">
                            Temperature: <span id="tempValue">0.7</span>
                            <input type="range" id="temperature" min="0" max="2" step="0.1" value="0.7">
                        </label>
                        <label class="max-tokens-control">
                            Max Tokens: <span id="maxTokensValue">1000</span>
                            <input type="range" id="maxTokens" min="100" max="4000" step="100" value="1000">
                        </label>
                    </div>
                </div>
            </div>
        </main>

        <footer class="footer">
            <p>Powered by FastAPI & OpenAI</p>
        </footer>
    </div>

    <script src="/static/js/app.js"></script>
</body>
</html>
"""

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory storage for chat history (in production, use a database)
chat_history: List[Dict[str, Any]] = []

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Main chat interface"""
    return HTMLResponse(content=HTML_TEMPLATE)

@app.get("/api/models")
async def get_models():
    """Get available OpenAI models"""
    try:
        models = openai_client.models.list()
        return {"models": [model.id for model in models.data]}
    except Exception as e:
        logger.error(f"Error fetching models: {e}")
        return {"models": ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"]}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint using OpenAI API"""
    try:
        # Prepare messages for OpenAI
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # Call OpenAI API
        response = openai_client.chat.completions.create(
            model=request.model,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=request.stream
        )
        
        # Extract response
        if request.stream:
            return StreamingResponse(
                stream_response(response),
                media_type="text/plain"
            )
        else:
            content = response.choices[0].message.content
            usage = response.usage.dict() if response.usage else None
            
            # Store in chat history
            chat_history.append({
                "timestamp": datetime.now().isoformat(),
                "messages": request.messages,
                "response": content,
                "model": request.model
            })
            
            return ChatResponse(
                response=content,
                model=request.model,
                usage=usage
            )
            
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def stream_response(response):
    """Stream OpenAI response"""
    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    """Streaming chat endpoint"""
    try:
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        response = openai_client.chat.completions.create(
            model=request.model,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=True
        )
        
        return StreamingResponse(
            stream_response(response),
            media_type="text/plain"
        )
        
    except Exception as e:
        logger.error(f"Error in streaming chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chat/history")
async def get_chat_history():
    """Get chat history"""
    return {"history": chat_history}

@app.delete("/api/chat/history")
async def clear_chat_history():
    """Clear chat history"""
    global chat_history
    chat_history.clear()
    return {"message": "Chat history cleared"}

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket endpoint for real-time chat"""
    await websocket.accept()
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Process with OpenAI
            messages = [{"role": msg["role"], "content": msg["content"]} 
                       for msg in message_data["messages"]]
            
            response = openai_client.chat.completions.create(
                model=message_data.get("model", "gpt-4o-mini"),  # Updated default to GPT-4o-mini
                messages=messages,
                temperature=message_data.get("temperature", 0.7),
                stream=True
            )
            
            # Stream response back to client
            for chunk in response:
                if chunk.choices[0].delta.content:
                    await websocket.send_text(chunk.choices[0].delta.content)
                    
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
