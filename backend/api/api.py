import openai
import services as services
import settings
from api.responses import CustomJSONResponse
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes.chats_routes import chats_api_router

openai.api_key = settings.OPENAI_API_KEY

app = FastAPI(
    default_response_class=CustomJSONResponse,
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/api")
async def root():
    return {"message": "Check docs for more info."}

app.include_router(chats_api_router)

### CHATBOT ###
        
@app.post("/api/assistant")
async def assistantChat(request: Request):
    # return await services.assistantChat(request)
    return await services.customAgentChat(request)
