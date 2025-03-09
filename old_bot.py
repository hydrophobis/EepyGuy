import discord
import requests
from discord.ext import commands
import subprocess
import os
import sys
import time

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
    subprocess.run(['taskkill', '/F', '/IM', 'cmd.exe'])
    subprocess.run(['cmd.exe', '/C', 'start', 'C:/Vanilla 1.21.1/run.bat'])
    os.execv(sys.executable, ["python", "C:\\Users\\MINI PC\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\EepyGuy\\old_bot.py"] + sys.argv)

# Command: !ip
@bot.command(name='ip')
async def public_ip(ctx):
    # Get the IPv6 address and send it in the message
    await ctx.send("Java: technology-utilities.gl.joinmc.link" + "\nBedrock: page-evolution.gl.at.ply.gg:3043")

# Command: !version
@bot.command(name='version')
async def version(ctx):
    await ctx.send(SERVER_VERSION + "\nMods: " + MOD_LIST)
    
@bot.command(name='hcommand')
async def hcommand(ctx): # Shows Windows and Linux install commands
    await ctx.send(f"Windows: runas /user:Administrator \"echo '{get_public_ip()} hydrophobis.mc' >> C:\Windows\System32\drivers\etc\hosts\"\nLinux: sudo echo '{get_public_ip()} hydrophobis.mc' >> /etc/hosts")
    
@bot.command(name='refresh')
async def refresh(self, ctx):
    try:
        repo_url = "https://github.com/hydrophobis/EepyGuy"
        clone_dir = "C:/Users/MINI PC/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
        
        subprocess.run(['git', 'clone', repo_url, clone_dir], check=True)

        await ctx.send(f"Successfully cloned the repository from {repo_url}!")

        await ctx.send("Restarting bot...")

        time.sleep(2)

        # Terminate the current bot instance and start a new one
        os.execv(sys.executable, ['python', '["python", "C:\\Users\\MINI PC\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\EepyGuy\\old_bot.py"]'] + sys.argv)


while(True):# Run the bot
    bot.run(DISCORD_TOKEN)
