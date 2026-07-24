import discord
from discord.ext import tasks, commands
import datetime
import os
import time
import random
import google.generativeai as genai

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ====================== CONFIG ======================
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

BIRTHDAY_IMAGES = [
    "https://i.imgur.com/0zJ8v0K.jpeg",
    "https://i.imgur.com/5z3pL8D.jpeg",
    "https://i.imgur.com/X7pK2mN.jpeg",
    "https://i.imgur.com/8vL9pQm.jpeg",
    "https://i.imgur.com/JfR2vXt.jpeg",
]

# ====================== DỮ LIỆU SINH NHẬT ======================
birthdays = {
    "demacianking1": {"name": "Cường", "birthday": {"day": 5, "month": 1}, "year": 2000},
    "thanh0374": {"name": "Thành", "birthday": {"day": 19, "month": 10}, "year": 2000},
    "dangialanrangu": {"name": "Dũng Còi", "birthday": {"day": 17, "month": 11}, "year": 2000},
    "manted1229": {"name": "Ngọc Điếc", "birthday": {"day": 4, "month": 1}, "year": 2000},
    "vyanhduc": {"name": "Đức", "birthday": {"day": 25, "month": 12}, "year": 1999},
    "pta.zyud": {"name": "Tuấn Anh", "birthday": {"day": 6, "month": 6}, "year": 2000},
}
# ============================================================

def get_current_date():
    now1 = datetime.datetime.now().date()
    now2 = datetime.date.fromtimestamp(time.time())
    return now1, now2

def is_date_reliable():
    date1, date2 = get_current_date()
    if date1 == date2:
        return True, date1
    return False, None

def generate_birthday_message(name):
    try:
        model = genai.GenerativeModel('gemini-3.5-flash')
        prompt = f"""
        Viết một lời chúc sinh nhật cực kỳ ngọt ngào, ấm áp, đáng yêu dành cho {name}.
        Sử dụng emoji hợp lý, vui tươi. 
        Độ dài khoảng 2-3 câu, giọng điệu gần gũi, chân thành.
        Không dùng từ quá sến hoặc quá dài dòng.
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except:
        return f"Chúc mừng sinh nhật {name}! Chúc bạn một tuổi mới tràn đầy niềm vui, hạnh phúc và những điều tốt đẹp nhất! 🎉🥳"

@bot.event
async def on_ready():
    print(f"{bot.user} đã online!")
    check_birthday.start()

@tasks.loop(minutes=30)
async def check_birthday():
    reliable, today = is_date_reliable()
    if not reliable:
        print("❌ Date check failed!")
        return

    channel_id = int(os.getenv("CHANNEL_ID", 0))
    channel = bot.get_channel(channel_id)
    if not channel:
        return

    for user_id, data in birthdays.items():
        b = data["birthday"]
        if b["day"] == today.day and b["month"] == today.month:
            member = channel.guild.get_member(int(user_id)) or channel.guild.get_member_named(data.get("name"))
            if member:
                name = data["name"]
                message = generate_birthday_message(name)
                image_url = random.choice(BIRTHDAY_IMAGES)
                
                embed = discord.Embed(
                    title="🎂 CHÚC MỪNG SINH NHẬT! 🎉",
                    description=message,
                    color=0xFF69B4
                )
                embed.set_image(url=image_url)
                embed.set_footer(text=f"Hôm nay là ngày {today.day}/{today.month} 💕")
                
                await channel.send(content=member.mention, embed=embed)

@bot.command(name="testbirthday")
async def test_birthday(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author
    name = member.display_name
    message = generate_birthday_message(name)
    image_url = random.choice(BIRTHDAY_IMAGES)
    
    embed = discord.Embed(title="🎂 Test Sinh Nhật", description=message, color=0xFF69B4)
    embed.set_image(url=image_url)
    await ctx.send(content=member.mention, embed=embed)

def run_bot():
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ DISCORD_TOKEN chưa set!")
        return
    bot.run(token)
