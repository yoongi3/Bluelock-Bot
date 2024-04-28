from discord.ext import commands
import discord
import os
from dotenv import load_dotenv
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

    latest_chapter = "latest chapter" # Placeholder
    return (latest_chapter)

# Bot events and commands
@bot.event
async def on_ready():
    print ("Bot ready")
    global driver
    driver = init_driver()
    channel = bot.get_channel(channel_ID)
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
