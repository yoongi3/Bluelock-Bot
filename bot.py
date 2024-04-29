from discord.ext import commands
import discord
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Load environment variables
load_dotenv()
bot_token = os.getenv("BOT_TOKEN")
channel_ID = int(os.getenv("CHANNEL_ID"))

# Constants
URL = "https://po2scans.com/series/blue-lock"

# Global variables
driver = None
latest_chapter = None

# Initialize bot
bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())

# Initialize driver
def init_driver():
    global driver
    if driver is None:
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Enable headless mode
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    
# Ensure the driver is initialized
def ensure_driver():
    global driver
    if driver is None:
        init_driver()
    return driver
    
async def get_latest_chapter():
    global driver
    if driver is None:
        print("Driver is not initialized.")
        return None
    
    driver.get(URL)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    latest_chapter_card = soup.find(class_="chap-link")
    latest_chapter_text = latest_chapter_card.text.strip()
    sections = [section for section in latest_chapter_text.split("\n") if section.strip()]

    chapter_title = sections[0]
    chapter_date = sections[2]

    global latest_chapter
    latest_chapter = chapter_title.split()[1]

    print(latest_chapter)
    return (f"Latest chapter: {chapter_title} \nReleased: {chapter_date}")

# Bot events and commands
@bot.event
async def on_ready():
    channel = bot.get_channel(channel_ID)
    print ("Bot ready")

    global driver
    driver = init_driver()
    
    latest_chapter = await get_latest_chapter()
    if latest_chapter:
        await channel.send(latest_chapter)

@bot.command(name="read")
async def load_manga(ctx, chapter = None):
    driver = ensure_driver()
    driver.get(URL)

    await ctx.send("manga pages")

# Run bot
bot.run(bot_token)
