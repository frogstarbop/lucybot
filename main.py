import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import json
import random

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="*", intents=intents)
type colorForm = list[int]
load_dotenv()
jsO = None
def refreshJsonStore():
    with open(os.path.dirname(os.path.realpath(__file__))+"/embeds.json",'r') as i:
        jsO = json.load(i)
    return jsO
jsO = refreshJsonStore()
def clearJsonStore():
    with open(os.path.dirname(os.path.realpath(__file__))+"/embeds.json",'w') as o:
        json.dump([], o)
    jsO = refreshJsonStore()
    return jsO

#@bot.tree.command(name = "hello", description="Hi")
#async def hello(interaction: discord.Interaction):
#    await interaction.response.send_message("Test Output Hi")

@bot.tree.command(name = "create_embed", description = "Embed a Message")
async def create_embed(interaction: discord.Interaction, title:str, hexc:str, message_content:str, author:str=None):
    jsO = refreshJsonStore()
    print(jsO)

    if author is None:
        author = interaction.user
    hexc= hexc.strip('#')
    hex_int = int(hexc, base=16)

    embed = discord.Embed(title=title, description=message_content, color=hex_int)
    embed.set_author(name=author)
    embDict = {
            "metadata":{

                "channel_id":interaction.channel.id,
                "message_id": ""
            },
            "embedinfo":{
                "title":title,
                "hex_int":hex_int,
                "author":str(author),
                "content":message_content
                }
            }
    jsO, dosend = inpListIfNotMatch(embDict, jsO)
    if dosend:
        sent = await interaction.channel.send(embed=embed)
        jsO[len(jsO)-1]["metadata"]["message_id"] = sent.id
        await interaction.response.send_message("Embed Created successfully", ephemeral=True)
    else:
        await interaction.response.send_message("Same title and channel embed already exists", ephemeral=True)






    with open(os.path.dirname(os.path.realpath(__file__))+"/embeds.json", 'w') as o:
        json.dump(jsO, o)



@bot.tree.command(name="delembed", description="delete an embed")
async def delembed(interaction:discord.Interaction, message_id:int):

    jsO = refreshJsonStore()
    for i in list(jsO):
        if i["metadata"]["message_id"] == message_id:
            msg = await discord.channel.fetch_message(message_id)
            await msg.delete()
            jsO.remove(i)
            await interaction.response.send_message("Message Deleted", ephemeral=True)

@bot.tree.command(name="clearallembeds", description="Clear all embeds")
async def clearallembeds(interaction:discord.Interaction):
    clearJsonStore()
    await interaction.response.send_message(f"All Embeds cleared. Current length of embed list is {len(jsO)}")

def inpListIfNotMatch(d1:dict, ls:list):
    for i in ls:
        if (i["embedinfo"]["title"].lower() == d1["embedinfo"]["title"].lower()) and (i["metadata"]["channel_id"] == d1["metadata"]["channel_id"]):
            print("matched")
            return (ls, False)
    ls.append(d1)
    return (ls, True)
def getUniqueID(ls:list):
    j = 0
    for i in ls:
        j = random.randint(1000,9999)
        if i["metadata"]["id"] == j:
            return False
    return j


@bot.command()
@commands.is_owner()
async def sync(ctx):
    print("syncing")
    synced = await bot.tree.sync()
    print(f"synced {len(synced)}")

@bot.command()
async def ping(ctx):
    await ctx.send("Ping")

async def refreshEmbedsStore(ctx):
    jsO=refreshJsonStore()
    ctx.send(f"Refreshed {len(jsO)}")

async def clearEmbedStore(ctx):
    jsO = clearJsonStore()
    ctx.send(f"Refreshed {len(jsO)}")



bot.run(os.getenv("BOT_TOKEN"))
