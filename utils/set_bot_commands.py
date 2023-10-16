from aiogram import types



async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Foydalanishni boshlash"),
        types.BotCommand("buy", "Buyurtma berish"),
        types.BotCommand("help", "Xizmat haqida"),
        types.BotCommand("terms", "Foydalanish shartlari"),
        types.BotCommand("support", "Biz bilan aloqa"),
    ])
