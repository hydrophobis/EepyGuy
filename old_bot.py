import discord
import requests
from discord.ext import commands
import subprocess
import os
import sys
import time
import psutil
import getpass

SERVER_VERSION = "Vanilla Java Edition 1.21.4"
MOD_LIST = {
    "NONE"
}

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

@bot.command(name='start')
async def start(ctx):
    ctx.send("Beginning restart process")
    try:
        # Get the current bot process ID (PID) and the current user's username
        current_pid = os.getpid()
        current_user = getpass.getuser()
        print(f"Current User: {current_user}")
        print(f"Current PID: {current_pid}")
        
        # Iterate over all processes
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                # Check if the process is owned by the current user and isn't the bot process
                if proc.info['username'] == current_user and proc.info['pid'] != current_pid:
                    print(f"Killing process {proc.info['pid']} - {proc.info['name']} owned by {proc.info['username']}")
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass  # Ignore processes that can't be killed or have disappeared
                
        # Run the startup.bat file
        subprocess.run(['cmd.exe', '/C', 'start', 'C:/Users/MINI PC/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/startup.bat'])

        # Kill the bot process itself
        os._exit(0)  # Use os._exit() to terminate the bot process

    except Exception as e:
        await ctx.send(f"Error occurred: {e}")


# Command: !ip
@bot.command(name='ip')
async def public_ip(ctx):
    # Get the IPv6 address and send it in the message
    await ctx.send("Java: technology-utilities.gl.joinmc.link" + "\nBedrock: page-evolution.gl.at.ply.gg:3043")

# Command: !version
@bot.command(name='version')
async def version(ctx):
    await ctx.send(SERVER_VERSION + "\nMods: " + MOD_LIST)


bot.run(DISCORD_TOKEN)
