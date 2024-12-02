import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv.main import load_dotenv
import json

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="*", intents=intents)
type colorForm = list[int]
load_dotenv()

#@bot.tree.command(name = "hello", description="Hi")
#async def hello(interaction: discord.Interaction):
#    await interaction.response.send_message("Test Output Hi")

@bot.tree.command(name = "embed", description = "Embed a Message")
async def embed(interaction: discord.Interaction, title:str, hexc:str, message_content:str, author:str=None):
    jsO = None
    with open('embeds.json', 'r') as i:
        jsO = json.load(i)
    print(jsO)

    if author is None:
        author = interaction.user
    hexc= hexc.strip('#')
    hex_int = int(hexc, base=16)

    embed = discord.Embed(title=title, description=message_content, color=hex_int)
    embed.set_author(name=author)
    embDict = {
        "title":title,
        "hex_int":hex_int,
        "author":str(author),
        "content":message_content}
    if embDict not in jsO:

jsO.append(embDict)

    with open('embeds.json', 'w') as o:
        json.dump(jsO, o)
    await interaction.response.send_message(embed=embed)
    await interaction.followup.send("Embed Created successfully", ephemeral=True)





@bot.command()
@commands.is_owner()
async def sync(ctx):
    print("syncing")
    synced = await bot.tree.sync()
    print(f"synced {len(synced)}")

@bot.command()
async def ping(ctx):
    await ctx.send("Ping")






bot.run(os.getenv("BOT_TOKEN"))
