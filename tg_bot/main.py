import json
import logging
import asyncio
import os
import websockets
from typing import Dict
from datetime import datetime, timedelta
from aiogram.filters import CommandStart,Command
from aiogram import Bot, Dispatcher, types
from aiogram.enums.chat_action import ChatAction
from dotenv import load_dotenv


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
load_dotenv()

BOT_TOKEN=os.getenv("BOT_TOKEN")
WS_URL=os.getenv("WS_URL") 

ws_connections: Dict[int, websockets.WebSocketClientProtocol] = {}
user_sessions: Dict[int, str] = {}
last_activity: Dict[int, datetime] = {}
user_messages: Dict[int, str] = {}  
INACTIVITY_TIMEOUT = timedelta(hours=6)
CLEANUP_INTERVAL = 30 * 60  
MESSAGE_TIMEOUT = 5  

dp = Dispatcher()
bot = Bot(BOT_TOKEN)

async def connect_to_ws(user_id: int):
    try:
        ws_client = await websockets.connect(WS_URL)
        logging.info(f"Connected to WebSocket server for user {user_id}")
        
        session_msg = await ws_client.recv()
        session_data = json.loads(session_msg)
        user_sessions[user_id] = session_data.get('session_id')
        logging.info(f"Session info for user {user_id}: {session_msg}")
        
        connect_msg = await ws_client.recv()
        logging.info(f"Connection message for user {user_id}: {connect_msg}")
        
        ws_connections[user_id] = ws_client
        last_activity[user_id] = datetime.now()
        return True
    except Exception as e:
        logging.error(f"Failed to connect to WebSocket server for user {user_id}: {e}")
        return False

async def close_inactive_connection(user_id: int):
    try:
        await bot.send_message(user_id, "Так как вы не проявляли активность в течение 30 минут, мы решили приостановить вашу сессию.")

        if user_id in ws_connections and not ws_connections[user_id].closed:
            await ws_connections[user_id].close()
            logging.info(f"Closed inactive WebSocket connection for user {user_id}")
        
        ws_connections.pop(user_id, None)
        user_sessions.pop(user_id, None)
        last_activity.pop(user_id, None)
        
    except Exception as e:
        logging.error(f"Error closing connection for user {user_id}: {e}")

async def cleanup_inactive_connections():
    while True:
        try:
            current_time = datetime.now()
            inactive_users = []
            
            for user_id, last_active in last_activity.items():
                if current_time - last_active > INACTIVITY_TIMEOUT:
                    inactive_users.append(user_id)
            
            for user_id in inactive_users:
                await close_inactive_connection(user_id)
                logging.info('All Inactive connections was closed')
                
        except Exception as e:
            logging.error(f"Error in cleanup task: {e}")
            
        await asyncio.sleep(CLEANUP_INTERVAL)

@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in ws_connections:
        connected = await connect_to_ws(user_id)
        if not connected:
            await message.reply("Не удалось установить соединение с сервером. Попробуйте позже.")
            return
        await message.reply("Здравствуйте! Я представляю компанию Atlantys. Мы помогаем бизнесам решать задачи и делать работу проще с помощью ИИ решений. Как я могу к вам обращаться?")

@dp.message(Command(commands=['reset']))
async def reset_handler(message:types.Message):
    user_id = message.from_user.id
    if user_id in ws_connections:
        await close_inactive_connection(user_id)
        await message.reply("Ваше соединение с сервером сброшено. Вы можете начать заново.")
    else:
        await message.reply("Активного соединения с сервером не обнаружено.")


async def send_combined_message(user_id: int):
    combined_message = user_messages.pop(user_id, "")
    if not combined_message:
        return

    ws_client = ws_connections[user_id]
    message_data = {
        "message": combined_message,
    }
    
    try:
        await bot.send_chat_action(user_id, ChatAction.TYPING)
        await ws_client.send(json.dumps(message_data))
        
        response = await asyncio.wait_for(ws_client.recv(), timeout=30)
        logging.info(f"Received response for user {user_id}: {response}")
        
        if not response:
            await bot.send_message(user_id, "Получен пустой ответ от сервера. Попробуйте еще раз.")
            return
            
        try:
            logging.info(response)
            response_data = json.loads(response)
        except json.JSONDecodeError as json_error:
            logging.error(f"Invalid JSON received from server: {response}")
            logging.error(f"JSON parse error: {json_error}")
            await bot.send_message(user_id, "Получен некорректный ответ от сервера. Попробуйте еще раз.")
            return
            
        if not isinstance(response_data, dict):
            logging.error(f"Unexpected response format: {response_data}")
            await bot.send_message(user_id, "Неверный формат ответа от сервера. Попробуйте еще раз.")
            return
            
        reply = response_data.get("message", str(response_data))
        if not reply:
            await bot.send_message(user_id, "Пустой ответ от сервера. Попробуйте еще раз.")
            return
            
        await bot.send_message(user_id, reply)
        
    except asyncio.TimeoutError:
        await bot.send_message(user_id, "Сервер не ответил вовремя. Попробуйте еще раз.")
    except websockets.ConnectionClosed:
        await close_inactive_connection(user_id)
        await bot.send_message(user_id, "Соединение с сервером прервано. Попробуйте еще раз.")
    except Exception as e:
        logging.error(f"Error in send_combined_message for user {user_id}: {e}")
        await bot.send_message(user_id, "Произошла ошибка при обработке сообщения. Попробуйте еще раз.")


@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    last_activity[user_id] = datetime.now()
    
    if user_id not in ws_connections or ws_connections[user_id].closed:
        connected = await connect_to_ws(user_id)
        if not connected:
            await message.reply("Сервер недоступен. Попробуйте позже.")
            return

    if user_id not in user_messages:
        user_messages[user_id] = message.text
    else:
        user_messages[user_id] += f" {message.text}" 

    await asyncio.sleep(MESSAGE_TIMEOUT)
    
    if user_id in user_messages and (datetime.now() - last_activity[user_id]).total_seconds() >= MESSAGE_TIMEOUT:
        await send_combined_message(user_id)

async def on_shutdown(dp):
    for user_id in list(ws_connections.keys()):
        await close_inactive_connection(user_id)

async def main():
    logging.info("Starting bot...")
    cleanup_task = asyncio.create_task(cleanup_inactive_connections())
    
    try:
        await dp.start_polling(bot, on_shutdown=on_shutdown, skip_updates=True)
    finally:
        cleanup_task.cancel()
        try:
            await cleanup_task
        except asyncio.CancelledError:
            pass

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.error(f"Fatal error: {e}")
