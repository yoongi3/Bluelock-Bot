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
BASE_URL = "https://po2scans.com"
HOME_URL = "https://po2scans.com/series/blue-lock"

# Global variables
driver = None
LATEST_CHAPTER = None

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
    driver = ensure_driver()
    driver.get(HOME_URL)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    latest_chapter_card = soup.find(class_="chap-link")
    latest_chapter_text = latest_chapter_card.text.strip()
    sections = [section for section in latest_chapter_text.split("\n") if section.strip()]

    chapter_title = sections[0]
    chapter_date = sections[2]

    global LATEST_CHAPTER
    LATEST_CHAPTER = chapter_title.split()[1]

    return (chapter_title,chapter_date)

async def get_chapter_link(chapter_number):
    driver = ensure_driver()   
    driver.get(HOME_URL)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    chap_section = soup.find("div", class_="chap-section")
    if chap_section:
        chap_divs = chap_section.find_all("div", class_="chap")
        for chap_div in chap_divs:
            if chapter_number in chap_div.text:
                link = chap_div.find("div", class_="link").find("a")
                return link.get("href")
            
    return None
    

# Bot events and commands
@bot.event
async def on_ready():
    channel = bot.get_channel(channel_ID)
    print ("Bot ready")
    
    latest_chapter_title, latest_chapter_date = await get_latest_chapter()
    if latest_chapter_title:
        await channel.send(f"Latest chapter: {latest_chapter_title} \nReleased: {latest_chapter_date}")
    else:
        await channel.send("Latest chapter not found")

@bot.command(name="read")
async def load_manga(ctx, chapter = None):
    if chapter is None:
        if LATEST_CHAPTER:
            chapter_link = await get_chapter_link(LATEST_CHAPTER)
            await ctx.send(f"Latest chapter: {BASE_URL}/{chapter_link}")
        else:
            await ctx.send("Latest chapter not available.")
    else:
        chapter_link = await get_chapter_link(chapter)
        if chapter_link:
            await ctx.send(f"Chapter {chapter}: {BASE_URL}/{chapter_link}")
        else:
            await ctx.send(f"Chapter {chapter} not found.")

# Run bot
bot.run(bot_token)
