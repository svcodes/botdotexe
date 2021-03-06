# obtain proper libraries for hypixel stats and discord.py
import discord
from discord.ext import commands
import aiohttp
import asyncpraw
import random
import ksoftapi
import time

#initialize stuff
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = ".", intents = intents)

reddit = asyncpraw.Reddit(client_id="h",
                     client_secret="h",
                     user_agent="script: Python (by /u/h)")
client.load_extension("jishaku")

client.session = aiohttp.ClientSession()
kclient = ksoftapi.Client("h")
"""
command not work too laz to fix
@client.command()
async def gay(ctx):
    async with client.session.get(f"https://some-random-api.ml/canvas/gay?avatar={str(ctx.author.avatar_url_as(format="png"))}") as r:
       #res = await r.json()
       await ctx.send(r)
"""







@commands.has_permissions(manage_messages=True)
@client.command(help = "sets slowmode. Usage: .slowmode <seconds>")
async def slowmode(ctx, secs: int):
    await ctx.channel.edit(slowmode_delay=secs)
    await ctx.send(f"Slowmode set to {secs} seconds") 


    
@commands.has_permissions(manage_messages=True)
@client.command(name="6hrs")
async def sixhrs(ctx):
    await ctx.channel.edit(slowmode_delay=21600)
    await ctx.send(f"Slowmode set to 6 hours :)") 


@client.command()
async def lyrics(ctx, *,query):
    try:
        results = await kclient.music.lyrics(query=query,clean_up=True)
    except ksoftapi.NoResults:
        await ctx.send('No lyrics found for ' + query)
    else:
        first = results[0]
        embed = discord.Embed(title = f"Lyrics for {first.name} by {first.artist}", description=first.lyrics)
        embed.set_footer(text="Lyrics provided by KSoft.Si")
        await ctx.send(embed=embed)

@client.command()
async def weather(ctx, loc):
    await ctx.send(f"https://wttr.in/{loc}.png?u")
"""
@client.event
async def on_message(message):
   if message.guild.id == 733508936216477706 and "bye" in message.content.lower():
      await message.add_reaction("\U0001f44b")
   if message.author.id == 743162094710423572 and not message.channel.id == 770073072153133076:
      await message.add_reaction("\U0001f60b")
   if message.author.id == 348149669899272196 and "." in message.content.lower() and not message.channel.id == 770073072153133076:
      await message.add_reaction("\U0001f633")
   if message.guild.id == 693891574609739777 and message.channel.id == 740011566501724171 and message.author.id == 155149108183695360:
      await message.add_reaction("\U00002b06")
      await message.add_reaction("\U00002b07")
   
   await client.process_commands(message)
"""
@client.command()
async def suggest(ctx,*,suggestion):
  
  if ctx.guild.id == 693891574609739777:
      await ctx.message.delete()
      embed = discord.Embed(title = "Suggestion", description=suggestion)
      embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url = str(ctx.author.avatar_url))
      chan = client.get_channel(740011566501724171)
      msg = await chan.send(embed=embed)
      await msg.add_reaction("\U00002b06")
      await msg.add_reaction("\U00002b07")
  elif ctx.guild.id == 733508936216477706:
      await ctx.message.delete()
      embed = discord.Embed(title = "Suggestion", description=suggestion)
      embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url = str(ctx.author.avatar_url))
      chan = client.get_channel(735619559318487123)
      msg = await chan.send(embed=embed)
      await msg.add_reaction("\U00002b06")
      await msg.add_reaction("\U00002b07")
  else:
      await ctx.send("no")
    
@client.command()
async def chatbot(ctx,*, msg: str):
    async with client.session.get(f"https://some-random-api.ml/chatbot?message={msg}") as r:
       res = await r.json()
       await ctx.send(res['response'])

                      
@client.command()
async def hystats(ctx,mcuser):
        async with client.session.get(f'https://api.slothpixel.me/api/players/{mcuser}') as r:
            res = await r.json()  # returns dict
            await ctx.send(res['total_coins'])

@client.command()
async def aww(ctx):
    aww = await kclient.images.random_aww()
    await ctx.send(aww.image_url)
          
          
@client.group()
async def gd(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Please add a subcommand! (profile, level)")
@gd.command()
async def profile(ctx,username):
        async with client.session.get(url = f'https://gdbrowser.com/api/profile/{username}') as r:
            res = await r.json()
              
            if res == "-1":
                await ctx.send("error! you either entered the name wrong/gdbrowser api is down. try again later")
            else:
                embed = discord.Embed(title = f"GD Stats for {res['username']}")
                embed.set_thumbnail(url = f'https://gdbrowser.com/icon/{username}')
                embed.add_field(name = 'Stars', value = res['stars'], inline=False)
                embed.add_field(name = 'Coins', value = res['coins'],inline=False)
                embed.add_field(name = 'Demons', value = res['demons'],inline=False)
                embed.set_footer(text="All info is obtained from https://gdbrowser.com")
                await ctx.send(embed=embed)
@gd.command()
async def level(ctx, id: int):
    async with client.session.get(f'https://gdbrowser.com/api/level/{id}') as r:
        res = await r.json()
        embed = discord.Embed(title = f"GD Level: {res['name']}")
        embed.add_field(name="Author", value = res['author'],inline=False)
        embed.add_field(name="Difficulty", value = res['difficulty'],inline=False)
        embed.add_field(name="Downloads", value = res['downloads'],inline=False)
        embed.add_field(name="Stars", value = res['stars'],inline=False)
        embed.add_field(name="Song Name", value = res['songName'],inline=False)
        await ctx.send(embed=embed)

@client.command()
async def mcserver(ctx,ipaddr):
    async with client.session.get(f'https://api.mcsrvstat.us/2/{ipaddr}') as r:
        res = await r.json()
        embed = discord.Embed(title = f"Server Stats for {ipaddr}")
        motdpath = res['motd']['clean']
        if len(motdpath) == 2:
            embed.description = (f"""**MOTD:** 
            {res['motd']['clean'][0]}
            {res['motd']['clean'][1]}
            **Players:** {res['players']['online']}/{res['players']['max']}
            **Version:** {res['version']}""")
        else: 
            embed.description = (f"""**MOTD:** 
            {res['motd']['clean'][0]}
            **Players:** {res['players']['online']}/{res['players']['max']}

            **Version:** {res['version']}""")

      
        await ctx.send(embed=embed)
        
@client.command()
async def coinflip(ctx):
    options = ["Heads","Tails"]
    await ctx.send(f"It's {random.choice(options)}!")
    
@client.command()
async def dadjoke(ctx):
    
    async with client.session.get(url='https://icanhazdadjoke.com/slack') as r:
        res = await r.json()
        await ctx.send(res['attachments'][0]['text'])

@client.command()
async def pograte(ctx, user: discord.Member = None):
    if user == None:
      await ctx.send(f"{ctx.author.display_name} is {random.randint(1,100)}% pog.")
    else:
      await ctx.send(f"{user.display_name} is {random.randint(1,100)}% pog.")
@client.command()
async def testmeme(ctx):
    meme = await kclient.images.random_meme()
    await ctx.send(meme.image_url)


#sends a message to the console when the bot is connected
@client.event
async def on_ready():
    print(f"{client.user} is ready!")

    
#basic ping command
@client.command(brief = "Tells you the ping in ms", description = "Tells you the time to connect from idiot.exes pc to the discord server (in ms)")
async def ping(ctx):
    await ctx.send(f"pong! {round(client.latency * 1000, 4)} ms")


#funny meme command
@client.command(brief = "haha brrr go brrrr", description = "brrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
async def brr(ctx):
    await ctx.send("https://i.clouds.tf/hys8/7nvo.png")

@client.command()
async def poll(ctx, *, question):
  await ctx.message.delete()
  pollembed = discord.Embed(title= question, colour = discord.Colour(0x7289da))
  pollembed.set_author(name=f"{ctx.author.name} asks: ")
  pogmessage = await ctx.send(embed=pollembed)
  await pogmessage.add_reaction("\U0001f44d")
  await pogmessage.add_reaction("\U0001f44e")
  await pogmessage.add_reaction("\U0001f90f")
                              


#links the skyleamoe page for a given user
@client.command()
async def sbprof(ctx,mcname,profile = None):
    if profile == None:
        await ctx.send(f"https://sky.shiiyu.moe/stats/{mcname}")
    else:
        await ctx.send(f'https://sky.shiiyu.moe/stats/{mcname}/{profile}')

@client.command()
async def gn(ctx, user : discord.Member = None):
  if user == None:
    await ctx.send(f"{ctx.author.name} says goodnight")
  else:
    await ctx.send(f"{ctx.author.name} says goodnight to {user.name}")
    
@client.command()
async def gm(ctx, user : discord.Member = None):
  if user == None:
    await ctx.send(f"{ctx.author.name} says good morning")
  else:
    await ctx.send(f"{ctx.author.name} says good morning to {user.name}")


@client.command()
async def ga(ctx, user : discord.Member = None):
  if user == None:
    await ctx.send(f"{ctx.author.name} says good afternoon")
  else:
    await ctx.send(f"{ctx.author.name} says good afternoon to {user.name}")




#uses my token to run the code and start sending it over to discord
client.run("h")
