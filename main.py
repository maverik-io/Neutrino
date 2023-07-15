import discord
import datetime
import os
from dotenv import load_dotenv
from discord.ext import commands
from keep_alive import keep_alive,formatted_time
import pickle
import random

badWords = []
Currency = {}
with open('badWords.txt','r') as f:
  badWords = f.read().split(',')
with open('Vars.dat','rb') as f:
  Currency = pickle.load(f)



load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="$")
start_time = None


@bot.event
async def on_ready():
    global start_time
    start_time = datetime.datetime.now()
    #print(f"Logged in as {bot.user}")


@bot.event
async def on_message(message):
    if message.guild.id in [1108293590679031918,935202323003752508]:
        l = []
        if message.author != bot.user:
            if bot.user.mention in message.content:
              await message.channel.send("Please refrain from mentioning me. (I'll kill you!)")
            if message.content == "hello":
              await message.channel.send("Am I supposed to wave back at your ugly face?")
            if message.content.lower().find('egg') != -1:
              await message.add_reaction('🥚')
        
            for i in badWords:
              if i in message.content.lower() and message.author != bot.user:
                await message.add_reaction('🤬')
                l.append(i)
            if l:
              await message.channel.send(f"```My dear {message.author},\nI\
just want you to know that I am mortified by your use of '{', '.join(l)}'```")
        
        
            if message.channel.id == 1120674868397101067:
                try:
                    Currency[str(message.author)] += 1
                    with open('Vars.dat','wb') as f:
                        pickle.dump(Currency,f)
                except Exception as e:
                    await message.channel.send(f'```{e} is not a valid user```')
    
        
        await bot.process_commands(message)


@bot.command(help="Check if the bot is awake")
async def ping(ctx):
    await ctx.channel.send("I'm awake!")


# points stuff---------------------------------------
@bot.command(help="Gives balance of server members")
async def bal(ctx,user = None):
    if user is None:
        string = '\n'.join([f'{name} : ∆{Currency[name]}' for name in Currency])
    else:
        user = str(bot.get_user(int(user[2:-1])))
        string = f'{user} : {Currency[user]}'
    await ctx.channel.send('```'+string+'```')

@bot.command(help='Sign up to the bank')
async def signup(ctx,user = None):
    if user is None:user = ctx.message.author
    else : user = bot.get_user(int(user[2:-1]))
    
    
    if str(user) in Currency:
      await ctx.channel.send('Already a member')
    else:
      await ctx.channel.send(f'adding...{user}')
      
      Currency[str(user)] = 100
      with open('Vars.dat','wb') as f:
        pickle.dump(Currency,f)

@bot.command(help='Give Money to someone')
async def give(ctx, member:discord.User,amt):
  if Currency[str(ctx.message.author)] > int(amt):
    try:
      Currency[str(member)] += int(amt)
      Currency[str(ctx.message.author)] -= int(amt)
      with open('Vars.dat','wb') as f:
        pickle.dump(Currency,f)
      await ctx.channel.send(f'```{ctx.message.author}  >>-∆{int(amt)}->>  {member}```')
      await bot.get_user(member.id).send(f'```|- You have recieved ∆{amt}/- from {ctx.message.author} -|```')
    except Exception as e:
      await ctx.channel.send(f'```{e} is not a valid user```')
    
  else:
    await ctx.channel.send('```Insufficient funds```')

@bot.command(help='Beg the bot for money')
async def beg(ctx,):
      amt = random.randint(1,6)
      Currency[str(ctx.message.author)] += amt
      with open('Vars.dat','wb') as f:
        pickle.dump(Currency,f)
      await ctx.channel.send(f'```Phoo! Here take a measly ∆{amt}/- ```')
      await bot.get_user(ctx.message.author.id).send(f'```|- You have recieved ∆{amt}/- from me -|```')
# ----------------------------------------------------

@bot.command(help="Deletes messages")
async def delete(ctx,num):
  await ctx.channel.purge(limit=int(num))

@bot.command(help="Returns uptime")
async def uptime(ctx):
    now = datetime.datetime.now()
    uptime = now - start_time
    uptime_str = str(uptime).split(".")[0]
    await ctx.channel.send(f"```Uptime: {uptime_str}```")


@bot.command(help="Prints the list of values back to the channel.")
async def print(ctx, *args):
    response = " ".join(args)
    await ctx.channel.send('```'+response+'```')


@bot.command(help="Performs math calculation")
async def math(ctx, *args):
    expression = "".join(args)
    try:
        result = eval(expression)
        await ctx.channel.send(str('```'+str(result)+'```'))
    except Exception as e:
        await ctx.channel.send(f"```Error: Invalid expression\n{e}```")



@bot.command(help="Displays current time")
async def time(ctx):
    await ctx.channel.send(f"```The Bot woke up at:\n{formatted_time.replace('<br>',' | ')}```")

@bot.command(help="Lists online members in the server")
async def online(ctx):
    members = [f"{member.name}#{member.discriminator}" for member in ctx.guild.members if member.status == discord.Status.online]
    members_str = "\n".join(members)
    await ctx.channel.send(f"```Online members:\n{members_str}```")

@bot.command(help= 'Ban people')
@commands.has_any_role("Admin")
async def ban (ctx, member:discord.User=None, reason =None):
    if member == None or member == ctx.message.author:
        await ctx.channel.send("You cannot ban yourself")
        return
    if reason == None:
        reason = "being a jerk!"
    message = f"You have been banned from {ctx.guild.name} for {reason}"
    await member.send(message)
    await ctx.guild.ban(member, reason=reason)
    await ctx.channel.send(f"{member} is banned!")

@bot.command()
async def id(ctx):
    await ctx.channel.send(ctx.guild.id)

keep_alive()
bot.run(DISCORD_TOKEN)
