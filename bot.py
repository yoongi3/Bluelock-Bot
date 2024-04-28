from discord.ext import commands
import discord
import os
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Load environment variables
load_dotenv()
bot_token = os.getenv("BOT_TOKEN")
channel_ID = int(os.getenv("CHANNEL_ID"))

bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print ("hello, ready to go")
    await get_latest_chapter()

@bot.command(name="read")
async def load_manga(ctx, chapter = None):
    driver = init_driver()
    
    if driver is None:
        await ctx.send("Driver is not initialized.")
        return
    
    await ctx.send("manga pages")

async def get_latest_chapter():
    return ("latest chapter")

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Enable headless mode
    driver = webdriver.Chrome(options=chrome_options)
    return driver