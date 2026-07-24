import discord
from discord.ext import tasks, commands
import datetime
from datetime import timedelta
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Dữ liệu sinh nhật
birthdays = {
    "demacianking1": {"name": "Cường", "birthday": {"day": 5, "month": 1}},
    "thanh0374": {"name": "Thành", "birthday": {"day": 19, "month": 10}},
    "dangialanrangu": {"name": "Dũng Còi", "birthday": {"day": 17, "month": 11}},
    "manted1229": {"name": "Ngọc Điếc", "birthday": {"day": 4, "month": 1}},
    "vyanhduc": {"name": "Đức", "birthday": {"day": 25, "month": 12}},
    "pta.zyud": {"name": "Tuấn Anh", "birthday": {"day": 6, "month": 6}},
}

@bot.event
async def on_ready():
    print(f"{bot.user} đã online!")
    check_birthday.start()

@bot.command(name="setbirthday", aliases=["sinhnhat", "sn"])
async def set_birthday(ctx, day: int, month: int):
    # ... (giữ nguyên như trước)
    pass

@tasks.loop(hours=24)
async def check_birthday():
    today = datetime.date.today()
    channel_id = int(os.getenv("CHANNEL_ID", 0))  # Lấy từ Environment Variable

    channel = bot.get_channel(channel_id)
    if not channel:
        return

    for user_id, data in birthdays.items():
        b = data["birthday"]
        if b["day"] == today.day and b["month"] == today.month:
            member = channel.guild.get_member(int(user_id)) or channel.guild.get_member_named(data["name"])
            if member:
                await channel.send(
                    f"🎉 **CHÚC MỪNG SINH NHẬT** 🎂\n"
                    f"{member.mention} ({data['name']}) chúc mừng sinh nhật **{today.day}/{today.month}**! "
                    f"Chúc bạn một tuổi mới vui vẻ, hạnh phúc và thành công! 🥳✨"
                )

def run_bot():
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ DISCORD_TOKEN chưa được set!")
        return
    bot.run(token)