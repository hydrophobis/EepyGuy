import discord
import subprocess
from discord.ext import commands

SERVER_VERSION = "Vanilla Java Edition 1.21.1"
COMMAND_LIST = {'ip', 'version', 'hcommand'}

# Define the intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent if you need to read messages

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

@bit.command(name='help')
async def help(ctx):
    await ctx.send(COMMAND_LIST)

# Run the bot
bot.run('MTI0NTUzNDEzNTE4Mzg2Nzk2NQ.Gpy--8.QJfKqH2YKa3Ingfr6RA64RcJNUU0Jgswkxj308')
