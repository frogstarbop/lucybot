import discord
from discord import app_commands
from discord.ext import app_commands


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="*", intents=intents)

@bot.tree.command(name = "hello", description="Hi")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Test Output Hi")

