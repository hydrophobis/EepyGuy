import discord
from discord.ext import commands
from discord.commands import Option
import subprocess
import os
from config import SERVER_VERSION, MOD_LIST
from helpers import get_public_ip
import sys
import requests
import time

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @commands.slash_command(description="start")
        async def start(self, ctx):
            try:
                await ctx.defer()
                subprocess.run(['taskkill', '/F', '/IM', 'cmd.exe'])
                subprocess.run(['cmd.exe', '/C', 'start', 'C:/Vanilla 1.21.1/run.bat'])
                os.execv(sys.executable, ['python', '"C:\\Vanilla 1.21.1\\run_bot.py'] + sys.argv)
            except Exception as e:
                await ctx.respond(f"There was an error with the start command: {e}", ephemeral=True)

        @commands.slash_command(description="Get IP address")
        async def ip(self, ctx):
            await ctx.respond("Java: technology-utilities.gl.joinmc.link" + "\nBedrock: page-evolution.gl.at.ply.gg:3043")

        @commands.slash_command(description="Return server version")
        async def version(self, ctx):
            await ctx.respond(SERVER_VERSION + "\n" + MOD_LIST, ephemeral=True)

        @commands.slash_command(description="Show installation commands")
        async def hcommand(self, ctx):
            await ctx.respond(f"Windows: runas /user:Administrator \"echo '{get_public_ip()} hydrophobis.mc' >> C:\Windows\System32\drivers\etc\hosts\"\nLinux: sudo echo '{get_public_ip()} hydrophobis.mc' >> /etc/hosts", ephemeral=True)

        @commands.slash_command(description="Refresh command")
        async def refresh(self, ctx):
            try:
                url = "GITHUB_URL_HERE"
                response = requests.get(url)

                if response.status_code == 200:
                    with open('bot.py', 'wb') as f:
                        f.write(response.content)

                    await ctx.send("Successfully refreshed and downloaded the latest version!")

                    # Restart the bot
                    await ctx.send("Restarting bot...")

                    time.sleep(2)

                    # Terminate the current bot instance and start a new one
                    os.execv(sys.executable, ['python', '"C:\\Vanilla 1.21.1\\run_bot.py"'] + sys.argv)
                
                else:
                    await ctx.respond(f"Error refreshing: {response.status_code} - {response.text}", ephemeral=True)

            except Exception as e:
                await ctx.respond(f"Failed to refresh and restart the bot: {e}", ephemeral=True)

def setup(bot):
    bot.add_cog(Commands(bot))