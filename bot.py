import discord
from discord.ext import commands
import os
import asyncio

# Configure
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Ensure token exists
if not GITHUB_TOKEN or not DISCORD_TOKEN:
    raise ValueError("Environmental variable for 'DISCORD_TOKEN' or 'GITHUB_TOKEN' is missing.")

# Define intents
intents = discord.Intents.all()
intents.message_content = True

# Create bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

# Print statement to confirm bot is online 
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# Load cogs from cogs directory
async def load_extensions():
    print("Loading cogs..")
    cogs_path = 'C:\\Users\\MINI PC\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\EepyGuy\\cogs'
    for filename in os.listdir(cogs_path):
        if filename.endswith('.py'):
            try:
                # Await the load_extension coroutine here
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"cogs.{filename[:-3]} loaded")
            except Exception as e:
                print(f"Error loading cogs.{filename[:-3]}: {e}")

# Run bot
async def main():
    async with bot:
        await load_extensions()  # Await the load_extensions coroutine
        await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
