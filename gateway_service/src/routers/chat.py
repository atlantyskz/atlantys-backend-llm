import datetime
import logging
from uuid import uuid4
from fastapi import WebSocket, APIRouter, Depends, WebSocketDisconnect
from fastapi.websockets import WebSocketState
from src.core.enums import LLM_ENDPOINT
from src.models.chat import ChatDialogueHistory
from src.services.ai_chat import AiChatService, get_service as get_ai_chat_service

chat_router = APIRouter(prefix='/api')

@chat_router.websocket("/ws/chat/{type}")
async def websocket_endpoint(
    websocket: WebSocket,
    type: str ,
    ai_chat_service: AiChatService = Depends(get_ai_chat_service)
):
    llm_endpoint = None
    if type == 'tg':
        llm_endpoint = LLM_ENDPOINT.TELEGRAM_CLIENT.value
    if type == 'web':
        llm_endpoint = LLM_ENDPOINT.WEB_CLIENT.value

    await websocket.accept()
    
    session_id = str(uuid4())
    
    chat_history = ChatDialogueHistory(
        session_id=session_id,
        messages=[],
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now()
    )

    await websocket.send_json({"session_id": session_id})
    print(f"Session ID: {session_id} connected.")
    if websocket.application_state == WebSocketState.CONNECTED:
        await websocket.send_text("Connection established")
    bot_intro_message = "Здравствуйте! Я представляю компанию Atlantys. Мы помогаем бизнесам решать задачи и делать работу проще с помощью ИИ решений. Как я могу к вам обращаться?"
    await chat_history.add_message(sender="assistant", message=bot_intro_message) 
    try:
        while True:
            print("Waiting for data")
            data = await websocket.receive_json()
            
            if "message" not in data:
                await websocket.send_json({"error": "Message field is required."})
                continue

            user_message = data["message"]
            await chat_history.add_message(sender="user", message=user_message)
            
            history_content = "\n".join([f"{msg.role}: {msg.content}" for msg in chat_history.messages if msg.content])

            # Create a single 'assistant' message that includes the full history as content
            messages = [{
                'role': 'assistant',
                'content': history_content  # Add the full history here as the assistant's content
            }]
            
        
            messages.append({
                'role':'user',
                'content':user_message
            })
            
            bot_response = await ai_chat_service.handle_ai_chat_response({"messages":messages},
            llm_endpoint
            )
            logging.info(bot_response)
            bot_message = bot_response.get("llm_response").get('message')

            await chat_history.add_message(sender="assistant", message=bot_message) 
            
            await websocket.send_json(bot_response.get('llm_response'))
            print("Chat history updated successfully.")

    except WebSocketDisconnect:
        print("Client disconnected.")
    except Exception as e:
        print(f"Exception occurred: {e}")
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_text(f"Error: {str(e)}")
    finally:
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_text("Connection closed")
            await websocket.close()


@chat_router.get("/chat-history/{session_id}/summary")
async def get_chat_history(session_id: str, ai_chat_service: AiChatService = Depends(get_ai_chat_service)):
    summary = await ai_chat_service.summarize_chat_history(session_id)
    return summary