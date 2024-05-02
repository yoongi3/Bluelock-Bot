# Blue Lock Bot
## Introduction
The Blue Lock Bot is a Discord bot designed to provide users with the latest chapters of the Blue Lock manga series. It retrieves chapter information and images from the PO2Scans website and sends them directly to Discord channels.

## Features
**Latest Chapter Updates:** Automatically fetches and sends the latest chapter of the Blue Lock manga series.
**Chapter Read:** Allows users to read specific chapters by providing the chapter number as a command parameter.
**Message Cleanup:** Provides a command to delete a specified number of messages in the channel (requires appropriate permissions).

## Setup
To set up the Blue Lock Bot for your Discord server, follow these steps:

1. **Clone the Repository:** Clone this repository to your local machine using the following command:
```bash
git clone https://github.com/yourusername/bluelock-bot.git
```
2. **Install Dependencies:** Navigate to the project directory and install the required dependencies using the following command:
```bash
pip install -r requirements.txt
```
3. **Set Environment Variables:** Create a '.env' file in the project directory and add your Discord bot token and channel ID:
```makefile
BOT_TOKEN=your_discord_bot_token
CHANNEL_ID=your_discord_channel_id
```
4. **Run the Bot:** Execute the 'bot.py' file to start the Blue Lock Bot:
```bash 
python bot.py
```

## Usage
Once the bot is running and added to your Discord server, you can use the following commands:

- **?read:** Fetches and sends the latest chapter of the Blue Lock manga series.
    - Example: '?read' or '?read 50' (to read chapter 50)
- **?clean:** Deletes a specified number of messages in the channel (requires appropriate permissions).
    - Example: '?clean 10' (to delete 10 messages)