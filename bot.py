import discord, asyncio
import os
import shutil
import subprocess
from discord.ext import commands
import json
import time
import sys

if not os.path.exists('config.json'):
    data = {
        'token': "",
        'prefix': "",
    }
    with open('config.json', 'w') as f:
        json.dump(data, f)

config = json.loads(open("config.json","r").read())
token = config['token']
prefix = config['prefix']

def checkConfig():
    if not token == "" and not prefix == "":
        return
    else: 
        if token == "":
            config['token'] = input('What is your token?\n')
        if prefix == "":
            config['prefix'] = input('Please choose a prefix for your commands e.g "+"\n')
        open('config.json','w+').write(json.dumps(config,indent=4,sort_keys=True))
        print('The program will now close so everything works correctly.')
        time.sleep(5)
        sys.exit()
        return

Client = discord.Client()
Client = commands.Bot(
    description='cnr selfbot',
    command_prefix=config['prefix'],
    self_bot=True
)
Client.remove_command('help') 

def getav(url, user):
    return discord.Embed(title='Avatar', color=0x2f3136).set_image(url=url).set_footer(text=user)    

@Client.event
async def on_ready():
    
    os.system('cls')
    width = shutil.get_terminal_size().columns

    def ui():
        print()
        print("owo".center(width))
        print()
        print("[-] Developed by cnr [-]".center(width))
        print("[-] User: {0} [-]".format(Client.user).center(width))
        print()
        print("[-] Commands:".format(Client.user).center(width))
        print(f" {prefix}av (displays a user's avatar)".format(Client.user).center(width))
    ui()
 

    @Client.command(aliases=['avatar', 'pfp'])
    async def av(ctx):
        args = ctx.message.content.split()
        await ctx.message.delete()
        embed = None
        if len(ctx.message.mentions) == 0:
            if len(args) == 1:
                embed = getav(ctx.message.author.avatar_url, ctx.author)
            else:
                if not args[1].isdigit():
                    embed = getembed(f"**{args[1]}** is not a valid number lol")
                    return await ctx.send(embed=embed,delete_after=30)
                user = bot.get_user(int(args[1]))
                if user == None:
                    return await ctx.send(embed=getembed(f"User ID **{args[1]}** is invalid."))
                embed = getav(user.avatar_url, user)
        else:
            embed = getav(ctx.message.mentions[0].avatar_url, ctx.message.mentions[0])
        await ctx.send(embed=embed,delete_after=30)

checkConfig()
Client.run(config['token'], bot=False, reconnect=True)