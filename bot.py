import discord
import requests
from discord.ext import commands
import subprocess
import os
import sys
import time

SERVER_VERSION = "Vanilla Java Edition 1.21.1"
COMMAND_LIST = {'ip', 'version', 'hcommand', 'eepyhelp', 'refresh(do not run)'}

# Load environment variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Check if tokens are loaded
if not GITHUB_TOKEN or not DISCORD_TOKEN:
    raise ValueError("Environment variables for GitHub token or Discord token are missing.")

# Define the intents
intents = discord.Intents.default()
intents.message_content = True

# Create a bot instance with a command prefix and intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Event: On bot ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

def get_public_ip():
    try:
        # Run ipconfig and use findstr to search for 'IPv6 Address'
        result = subprocess.run(['ipconfig'], capture_output=True, text=True)
        
        # Check if the ipconfig command was successful
        if result.returncode != 0:
            return "Error: Failed to execute ipconfig command."

        # Find the line containing 'IPv6 Address'
        ipv6_line = None
        for line in result.stdout.splitlines():
            if "IPv6 Address" in line:
                ipv6_line = line
                break
        # If we found the line with IPv6 address, extract the address
        if ipv6_line:
            ip_address = ipv6_line.replace("IPv6 Address. . . . . . . . . . . : ", "")
            return ip_address
        else:
            return "IPv6 Address not found."
            
    except Exception as e:
        return f"Error retrieving IP address: {e}"


# Command: !ip
@bot.command(name='ip')
async def public_ip(ctx):
    # Get the IPv6 address and send it in the message
    await ctx.send(get_public_ip())

# Command: !version
@bot.command(name='version')
async def version(ctx):
    await ctx.send(SERVER_VERSION)
    
@bot.command(name='hcommand')
async def hcommand(ctx): # Shows Windows and Linux install commands
    await ctx.send(f"Windows: runas /user:Administrator \"echo '{get_public_ip()} hydrophobis.mc' >> C:\Windows\System32\drivers\etc\hosts\"\nLinux: sudo echo '{get_public_ip()} hydrophobis.mc' >> /etc/hosts")

@bot.command(name='eepyhelp')
async def help(ctx):
    await ctx.send(COMMAND_LIST)
    
# Command: !refresh (new command)
@bot.command(name='refresh')
async def refresh(ctx):
    try:
        # Define the GitHub URL and the output file name
        url = 'https://github.com/hydrophobis/EepyGuy/bot.py/?raw=true' 

        # Make a GET request to download the file
        response = requests.get(url)

        if response.status_code == 200:
            # Save the downloaded content to a file
            with open('bot.py', 'wb') as f:
                f.write(response.content)
            
            await ctx.send("Successfully refreshed and downloaded the latest version!")

            # Restart the bot
            await ctx.send("Restarting the bot...")

            # Give it a moment before restarting
            time.sleep(2)

            # Terminate the current bot instance and start a new one
            os.execv(sys.executable, ['python'] + sys.argv)
        else:
            await ctx.send(f"Error refreshing: {response.status_code} - {response.text}")

    except Exception as e:
        await ctx.send(f"Failed to refresh and restart the bot: {e}")

# Run the bot
bot.run(DISCORD_TOKEN)
