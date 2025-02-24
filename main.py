import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import json


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="*", intents=intents)
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

#Customise and display an embedded message in the channel
@bot.tree.command(name = "create_embed", description = "Embed a Message")
async def create_embed(interaction: discord.Interaction, title:str, hexc:str, message_content:str, author:str=None):
    jsO = refreshJsonStore()
    
    # if there is no author, set it to the user who sent the command
    if author is None:
        author = interaction.user
    #Remove any '#' from the colour hex
    hexc= hexc.strip('#')
    hex_int = int(hexc, base=16)

    # Create the embed template, setting parameters to the command inputs
    embed = discord.Embed(title=title, description=message_content, color=hex_int)
    embed.set_author(name=author)
    # set up the dictionary to export to json file
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
    # check if the embed already exists inside the list of current embeds
    jsO, dosend = inpListIfNotMatch(embDict, jsO)
    # if it doesnt match (i.e. if Do Send is true)
    if dosend:
        # send the embed, and attach it to a variable
        sent = await interaction.channel.send(embed=embed)
        # update the appropriate value in the active embeds storage
        jsO[len(jsO)-1]["metadata"]["message_id"] = sent.id
        # send ephemeral status message
        await interaction.response.send_message("Embed Created successfully", ephemeral=True)
    # If an embed by the same name already exists
    else:
        # Send error
        await interaction.response.send_message("Same title and channel embed already exists", ephemeral=True)
    # send active embeds  to json file
    with open(os.path.dirname(os.path.realpath(__file__))+"/embeds.json", 'w') as o:
        json.dump(jsO, o)
    print(jsO)



@bot.tree.command(name="delembed", description="delete an embed")
async def delembed(interaction:discord.Interaction, message_id:str):
    # turn into int (bypass weird API limit, doesn't handle integers of ID-length client-side)
    message_id = int(message_id)
    #Refresh the list of embeds
    jsO = refreshJsonStore()
    # iterate through the list of embeds.....
    for i in list(jsO):
        #... To find embed specified by the parameter
        if i["metadata"]["message_id"] == message_id:
            # Find the channel (to ensure command doesn't have to be used in the origin channel)
            chan = bot.get_channel(i["metadata"]["channel_id"])
            # fetch the specified message
            msg = await chan.fetch_message(message_id)
            # delete the embed
            await msg.delete()
            # remove from active list of embeds
            jsO.remove(i)
            # Update json storage file
            with open(os.path.dirname(os.path.realpath(__file__))+"/embeds.json", 'w') as o:
                json.dump(jsO, o)
            # send confirmation epheremal message
            await interaction.response.send_message("Message Deleted", ephemeral=True)
            # send timed confirmation message in the parent channel of the embed
            await chan.send(f"Embed in this channel with the id {message_id} was successfully removed", delete_after=5)


@bot.tree.command(name="clearallembeds", description="Clear all embeds")
async def clearallembeds(interaction:discord.Interaction):
    # refresh to up-to-date list of embeds
    jsO = refreshJsonStore()
    # for every embed...
    for i in jsO:
        # ... get the channel of the embed ....
        chan = bot.get_channel(i["metadata"]["channel_id"])
        # ... get the message object of the embed ...
        msg = await chan.fetch_message(i["metadata"]["message_id"])
        # ... delete the message
        await msg.delete()
        # send feedback
        await chan.send(f"embed in channel {chan.id} with the id {msg.id} has been removed", delete_after=5)
    # clear program-side storage and json file
    clearJsonStore()
    await interaction.response.send_message(f"All Embeds cleared. Current length of embed list is {len(jsO)}")

# Input: dict and list to compare
# Returns: finalised list, True/False whether to send
def inpListIfNotMatch(d1:dict, ls:list):
    # For object in the list
    for i in ls:
        # if the titles and channels match...
        if (i["embedinfo"]["title"].lower() == d1["embedinfo"]["title"].lower()) and (i["metadata"]["channel_id"] == d1["metadata"]["channel_id"]):
            print("matched")
            # Return the list, and send "False"
            return (ls, False)
    # Else if no repeat was found, add object to end of list, ordered chrono. 
    ls.append(d1)
    # Return updated list, with true param to indicate embed can be sent
    return (ls, True)

@bot.command()
@commands.is_owner()
async def sync(ctx):
    print("syncing")
    synced = await bot.tree.sync()
    print(f"synced {len(synced)}")

@bot.command()
async def ping(ctx):
    await ctx.send("Ping")

# Refresh the embed storage
async def refreshEmbedsStore(ctx):
    jsO=refreshJsonStore()
    ctx.send(f"Refreshed {len(jsO)}")

# clear the embed storage
async def clearEmbedStore(ctx):
    jsO = clearJsonStore()
    ctx.send(f"Refreshed {len(jsO)}")


# Run the bot using .env file (not shown in github due to safety)
bot.run(os.getenv("BOT_TOKEN"))
