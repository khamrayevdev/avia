import json
import asyncio
from flask import Flask, request, jsonify
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession
import logging

TOKEN = "8004671583:AAF6vHfb19OZUmaIdMdzo3lSeaMfPuJ77Sc"
ADMIN_ID = "6098825037"  # Admin Telegram ID
app = Flask(__name__)

# Aiogram 3.x versiyasi uchun yangi konfiguratsiya
logging.basicConfig(level=logging.INFO)
session = AiohttpSession()
bot = Bot(token=TOKEN, session=session)
dp = Dispatcher()
router = Router()

db_file = "users.json"
try:
    with open(db_file, "r") as file:
        users = json.load(file)
except FileNotFoundError:
    users = {}

def save_users():
    with open(db_file, "w") as file:
        json.dump(users, file)

@app.route("/check_limit", methods=["POST"])
def check_limit():
    data = request.get_json()
    user_id = str(data.get("user_id"))
    
    if user_id in users and users[user_id]['limit'] >= 5:
        return jsonify({"status": "error", "message": "Kunlik limit tugagan"})
    else:
        if user_id not in users:
            users[user_id] = {"limit": 0}
        users[user_id]['limit'] += 1
        save_users()
        return jsonify({"status": "success", "signal": round(1.4 + (5.2 - 1.4) * asyncio.get_event_loop().time() % 1, 2)})

@router.message(Command("start"))
async def start(message: Message):
    user_id = str(message.from_user.id)
    
    if user_id in users and users[user_id]['limit'] >= 5:
        await message.answer("\U0001F6AB Sizning kunlik limitigiz tugagan! Yangi signal olish mumkin emas.")
    else:
        users.setdefault(user_id, {"limit": 0})
        save_users()
        
        mini_app_url = "https://zingy-frangollo-0b400b.netlify.app/web_sie"
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="\U0001F680 Mini-ilovani ochish", web_app=WebAppInfo(url=mini_app_url))]]
        )
        await message.answer("\U0001F680 Mini-ilovani ishga tushirish uchun pastdagi tugmani bosing.", reply_markup=keyboard)

@router.message(Command("broadcast"))
async def broadcast(message: Message):
    if str(message.from_user.id) != ADMIN_ID:
        await message.answer("Siz bu buyruqni bajarishga ruxsatga ega emassiz!")
        return
    
    broadcast_text = message.text.split(maxsplit=1)
    if len(broadcast_text) < 2:
        await message.answer("Xabar matnini kiriting: /broadcast Xabar matni")
        return
    
    broadcast_message = broadcast_text[1]
    failed_users = []
    
    for user_id in users.keys():
        try:
            await bot.send_message(user_id, broadcast_message)
        except:
            failed_users.append(user_id)
    
    await message.answer(f"Xabar {len(users) - len(failed_users)} foydalanuvchiga yuborildi!")

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

# Mini-ilova JavaScript integratsiyasi
tg_mini_app_script = """
<script>
    window.Telegram.WebApp.expand(); // Mini-ilovani butun ekran qilish

    async function getSignal() {
        const userId = window.Telegram.WebApp.initDataUnsafe.user?.id;
        if (!userId) {
            document.getElementById('signal').innerText = "Telegram identifikatsiyasi topilmadi!";
            return;
        }

        const response = await fetch('https://yourserver.com/check_limit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId })
        });
        const data = await response.json();

        if (data.status === 'success') {
            document.getElementById('signal').innerText = `\uD83D\uDCF1 Sizning signal: ${data.signal}`;
        } else {
            document.getElementById('signal').innerText = "\u26D4 Kunlik limit tugagan! Yangi signal olish mumkin emas.";
        }
    }
</script>
"""
