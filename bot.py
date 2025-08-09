import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

API_TOKEN = "8357198659:AAFXMEdroWZNxj0k2-a1dI_JBlPs6y13Q0o"
CHANNEL = "@ipkoArman"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def is_subscribed(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL, user_id=user_id)
        if member.status in ("creator", "administrator", "member", "restricted"):
            return True
    except Exception as e:
        print("get_chat_member error:", e)
    return False

@dp.message(Command(commands=["start", "help"]))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    if await is_subscribed(user_id):
        await message.answer("خوش آمدی — شما عضو کانال هستید. دسترسی داده شد.")
        return

    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(text="عضویت در کانال", url=f"https://t.me/{CHANNEL.lstrip('@')}"),
    )
    kb.row(
        InlineKeyboardButton(text="✅ من عضو شدم — بررسی کن", callback_data="check_join")
    )
    await message.answer(
        "برای استفاده از ربات باید ابتدا در کانال ما عضو شوی.\n"
        "لطفاً روی دکمه «عضویت در کانال» کلیک کن، سپس روی «من عضو شدم» بزن تا وضعیتت بررسی شود.",
        reply_markup=kb.as_markup()
    )

@dp.callback_query(lambda c: c.data == "check_join")
async def cb_check_join(query: CallbackQuery):
    user_id = query.from_user.id
    await query.answer()
    if await is_subscribed(user_id):
        await query.message.edit_text("✅ بررسی شد — شما عضو کانال هستید. دسترسی داده شد.")
    else:
        await query.message.answer("⚠️ هنوز عضو کانال نیستی. لطفا ابتدا عضو شو و دوباره تایید کن.")

if __name__ == "__main__":
    try:
        print("Bot is running...")
        asyncio.run(dp.start_polling(bot))
    except KeyboardInterrupt:
        print("Stopped")
