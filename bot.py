from discord.ext import commands
import discord
import os
import requests
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

WELCOME_MESSAGE = """
------------------------------------
**⚽ Ｂｌｕｅ Ｌｏｃｋ Ｂｏｔ ⚽**
------------------------------------

*Commands:* 
**?read / ?read (x)** : latest chapter / chapter (x)
**?clean (x)** : delete (x) chat messages

*Latest Chapter:*
"""

# Global variables
driver = None
LATEST_CHAPTER = None
command_in_progress = False

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
    
# Get latest chapter information
async def get_latest_chapter():
    driver = ensure_driver()
    driver.get(HOME_URL)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    latest_chapter_card = soup.find(class_="chap-link")
    if latest_chapter_card:
        latest_chapter_text = latest_chapter_card.text.strip()
        chapter_title, chapter_date, chapter_num = split_text(latest_chapter_text)

        global LATEST_CHAPTER
        LATEST_CHAPTER = chapter_num

        return chapter_title, chapter_date
    else:
        return None, None

# Split chapter text into title, date, and chapter number
def split_text(text):
    sections = [section for section in text.split("\n") if section.strip()]

    title = sections[0]
    date = sections[2]
    chap_num = title.split()[1]

    return title, date, chap_num

# Get chapter link based on chapter number
async def get_chapter_link(chapter_number):
    driver = ensure_driver()   
    driver.get(HOME_URL)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    chap_section = soup.find("div", class_="chap-section")
    if chap_section:
        chap_divs = chap_section.find_all("div", class_="chap")
        for chap_div in chap_divs:
            _ , _, chap = split_text(chap_div.text)
            if chapter_number == chap:
                link = chap_div.find("div", class_="link").find("a")
                return link.get("href")
    return None
    
async def get_chapter(ctx, link):
    driver = ensure_driver()
    driver.get(link)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    container_div = soup.find("div", class_="swiper-container")
    if container_div:
        slide_divs = container_div.find_all("div", class_="swiper-slide")
        images = []
        for index, slide_div in enumerate(slide_divs, start=1):
            image_tag = slide_div.find("img")
            if image_tag:
                image_url = image_tag.get("src")
                filename = download_image(BASE_URL + image_url, f"page_{index}.png")
                if filename:
                    images.append(filename) 
                else:
                    await ctx.send(f"Failed to download image {index}")
        # Send all images
        for image in images:
            file = discord.File(image)
            await ctx.send(file=file)
            os.remove(image)
    else:
        await ctx.send("No images found for this chapter")
    
# Download image from URL
def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename
    else:
        return None

# Bot events and commands
@bot.event
async def on_ready():
    channel = bot.get_channel(channel_ID)
    print ("Bot ready")
    
    latest_chapter_title, latest_chapter_date = await get_latest_chapter()
    await channel.send(WELCOME_MESSAGE)
    if latest_chapter_title:
        await channel.send(f"**{latest_chapter_title}** \nReleased: *{latest_chapter_date}*")
    else:
        await channel.send("Latest chapter not found")

@bot.command(name="read")
async def load_manga(ctx, chapter = None):
    # load_manga has to complete before being called again
    global command_in_progress
    if command_in_progress:
        await ctx.send("Another command is already in progress.")
        command_in_progress = False
        return
    command_in_progress = True
    
    if chapter is None:
        chapter = LATEST_CHAPTER

    identifier = await get_chapter_link(chapter)

    if identifier is None:
        await ctx.send(f"Can't find chapter {chapter}")
        command_in_progress = False
        return
    
    await ctx.send(f"Loading chapter {chapter}\nPlease wait")
    chapter_link = f"{BASE_URL}/{identifier}"
    await get_chapter(ctx, chapter_link)
    command_in_progress = False
    await ctx.send(f"Chapter {chapter} loaded")

@bot.command()
async def clean(ctx, amount: int):
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount + 1)  # Add 1 to also delete the command message
        await ctx.send(f"{amount} messages cleared by {ctx.author.mention}.", delete_after=5)
    else:
        await ctx.send("You don't have the required permissions to use this command.")


# Run bot
bot.run(bot_token)
