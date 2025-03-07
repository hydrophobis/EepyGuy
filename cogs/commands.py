import discord
from discord.ext import commands
import subprocess
import os
from config import SERVER_VERSION, MOD_LIST
import sys
import requests
import time

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Define all your slash commands inside the class
        @commands.slash_command(description="start")
        async def start(self, ctx):
            try:
                await ctx.defer()
                subprocess.run(['taskkill', '/F', '/IM', 'cmd.exe'])
                subprocess.run(['cmd.exe', '/C', 'start', 'C:/Vanilla 1.21.1/run.bat'])
                os.execv(sys.executable, ['python', '"C:/Vanilla 1.21.1/run_bot.py'] + sys.argv)
            except Exception as e:
                await ctx.respond(f"There was an error with the start command: {e}", ephemeral=True)

        @commands.slash_command(description="Get IP address")
        async def ip(self, ctx):
            await ctx.respond("Java: technology-utilities.gl.joinmc.link" + "\nBedrock: page-evolution.gl.at.ply.gg:3043")

        @commands.slash_command(description="Return server version")
        async def version(self, ctx):
            await ctx.respond(SERVER_VERSION + "/n" + MOD_LIST, ephemeral=True)

        @commands.slash_command(description="Refresh command")
        async def refresh(self, ctx):
            try:
                repo_url = "https://github.com/hydrophobis/EepyGuy"
                clone_dir = "C:/Users/MINI PC/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
                
                subprocess.run(['git', 'clone', repo_url, clone_dir], check=True)
        
                await ctx.send(f"Successfully cloned the repository from {repo_url}!")
        
                await ctx.send("Restarting bot...")
        
                time.sleep(2)
        
                # Terminate the current bot instance and start a new one
                os.execv(sys.executable, ['python', 'C:/Vanilla 1.21.1/run_bot.py'] + sys.argv)
        
            except subprocess.CalledProcessError as e:
                await ctx.respond(f"Error refreshing: {e}", ephemeral=True)
        
            except Exception as e:
                await ctx.respond(f"Failed to refresh and restart the bot: {e}", ephemeral=True)

        # Add the get_public_ip function as a slash command inside the cog
        @commands.slash_command(description="Get public IP address of the machine")
        async def get_ip(self, ctx, ip_version="IPv6"):
            """
            Retrieves the public IP address of the machine, either IPv4 or IPv6.
        
            Args:
                ip_version (str): The version of IP address to retrieve ('IPv4' or 'IPv6'). Default is 'IPv6'.
            
            Returns:
                str: The public IP address or an error message.
            """
            try:
                # Run the ipconfig command and capture the output
                result = subprocess.run(['ipconfig'], capture_output=True, text=True)

                # Check if the ipconfig command was successful
                if result.returncode != 0:
                    return await ctx.send(f"Error: Failed to execute ipconfig command. Return code: {result.returncode}")

                # Search for the relevant IP address based on the requested version
                ip_line = None
                search_str = "IPv6 Address" if ip_version == "IPv6" else "IPv4 Address"
                
                # Find the line containing the requested IP address
                for line in result.stdout.splitlines():
                    if search_str in line:
                        ip_line = line
                        break
                
                # Check if the IP line was found
                if ip_line:
                    ip_address = ip_line.split(":")[1].strip()  # Extract the IP address part
                    return await ctx.send(f"The {ip_version} address is: {ip_address}")
                else:
                    return await ctx.send(f"{ip_version} address not found")
                
            except Exception as e:
                return await ctx.send(f"Error retrieving {ip_version} address: {e}")

def setup(bot):
    bot.add_cog(Commands(bot))
