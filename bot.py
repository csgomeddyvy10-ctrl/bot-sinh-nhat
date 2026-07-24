import discord
from discord.ext import tasks, commands
import datetime
import os
import time
import google.generativeai as genai
import random

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ====================== CONFIG ======================
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Danh sách một số link ảnh sinh nhật đẹp (có thể thêm nhiều hơn)
BIRTHDAY_IMAGES = [
    "https://i.imgur.com/0zJ8v0K.jpeg",
    "https://i.imgur.com/5z3pL8D.jpeg",
    "https://i.imgur.com/X7pK2mN.jpeg",
    "https://i.imgur.com/8vL9pQm.jpeg",
    "https://i.imgur.com/JfR2vXt.jpeg",
]

# ====================== DOUBLE DATE CHECK ======================
def get_current_date():
    now1 = datetime.datetime.now().date()
    now2 = datetime.date.fromtimestamp(time.time())
    return now1, now2

def is_date_reliable():
    date1, date2 = get_current_date()
    if date1 == date2:
        return True, date1
    return False, None

# ====================== GEMINI CHÚC MỪNG ======================
def generate_birthday_message(name):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Viết một lời chúc sinh nhật cực kỳ ngọt ngào, ấm áp, đáng yêu dành cho {name}.
        Sử dụng emoji hợp lý, vui tươi. 
        Độ dài khoảng 2-3 câu, giọng điệu gần gũi, chân thành.
        Không dùng từ quá sến hoặc quá dài dòng.
        """

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Gemini error:", e)
        # Fallback message
        return f"Chúc mừng sinh nhật {name}! Chúc bạn một tuổi mới tràn đầy niềm vui, hạnh phúc và những điều tốt đẹp nhất! 🎉🥳"

# ====================== MAIN ======================
birthdays = { ... }  # giữ nguyên dữ liệu

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
                
                # Tạo lời chúc bằng Gemini
                message = generate_birthday_message(name)
                
                # Chọn ảnh ngẫu nhiên
                image_url = random.choice(BIRTHDAY_IMAGES)
                
                # Gửi embed đẹp
                embed = discord.Embed(
                    title="🎂 CHÚC MỪNG SINH NHẬT! 🎉",
                    description=message,
                    color=0xFF69B4
                )
                embed.set_image(url=image_url)
                embed.set_footer(text=f"Hôm nay là ngày {today.day}/{today.month} 💕")
                
                await channel.send(content=member.mention, embed=embed)

# Lệnh test
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
