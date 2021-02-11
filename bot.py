import discord
from discord import channel
from discord.ext import commands
import random
import datetime
import youtube_dl

import os
from discord.utils import get
import requests
from PIL import Image, ImageFont, ImageDraw
import io

#-PREFIX-
pref = '-'
bad_words = [ 'мать ебал', 'mq', 'сын шлюхи', 'шалава' ]

client = commands.Bot( command_prefix = pref )
client.remove_command( 'help' )

@client.event

async def on_ready():
    print ( 'Bot Started | Version 1.0.0' )
    await client.change_presence( status = discord.Status.online, activity = discord.Game( 'vivi-bot.xyz | -help' ) )
#--------------------------Команды--------------------------
@client.event
async def on_command_error( ctx, error ):
    pass

#-ИНФО О СЕРВЕРЕ-#
@client.command()
async def serverinfo(ctx):
  name = str(ctx.guild.name)

  id = str(ctx.guild.id)
  region = str(ctx.guild.region)
  memberCount = str(ctx.guild.member_count)

  icon = str(ctx.guild.icon_url)
   
  embed = discord.Embed(
      title=name + " Информация о сервере",
      color=discord.Color.blue()
    )
  embed.set_thumbnail(url=icon)
  embed.add_field(name="ID сервера", value=id, inline=True)
  embed.add_field(name="Регион", value=region, inline=True)
  embed.add_field(name="Пользователей", value=memberCount, inline=True)

  await ctx.send(embed=embed)

#-МУЗЫКА-#
@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile('song.mp3')
 
    try:
        if song_there:
            os.remove('song.mp3')
            print('[log] Старый файл удален')
    except PermissionError:
        print('[log] Не удалось удалить файл')
 
    await ctx.send('Пожалуйста ожидайте')
 
    voice = get(client.voice_clients, guild = ctx.guild)
 
    ydl_opts = {
        'format' : 'bestaudio/best',
        'postprocessors' : [{
            'key' : 'FFmpegExtractAudio',
            'preferredcodec' : 'mp3',
            'preferredquality' : '192'
        }],
    }
 
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('[log] Загружаю музыку...')
        ydl.download([url])
 
    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            print(f'[log] Переименовываю файл: {file}')
            os.rename(file, 'song.mp3')
 
    voice.play(discord.FFmpegPCMAudio('song.mp3'), after = lambda e: print(f'[log] {name}, музыка закончила свое проигрывание'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07
 
    song_name = name.rsplit('-', 2)
    await ctx.send(f'Сейчас проигрывает музыка: {song_name[0]}')

#-CONNECT VOICE-
@client.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send(f'Бот присоеденился к {channel}')
#-DISCONNECT VOICE-
@client.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.connect()
        await ctx.send(f'Бот отключился от {channel}')
#-ПРЕДУПРЕЖДЕНИЕ-
@client.event
async def on_message( message ):
    await client.process_commands( message )

    msg = message.content.lower()

    if msg in bad_words:
        await message.delete()
        await message.author.send( f'{ message.author.name }, нельзя такое писать!' )
#-CLEAR CHAT-
@client.command()
@commands.has_permissions( administrator =  True )
async def clear( ctx, amount : int ):
    await ctx.channel.purge ( limit = amount )
    await ctx.send(embed = discord.Embed(description = f':white_check_mark: Удалено {amount} сообщений!'))
#-BAN-
@client.command()
@commands.has_permissions ( administrator = True )

async def ban( ctx, member: discord.Member, *, reason = None ):
    emb = discord.Embed( title = 'Ban', colour = discord.Color.red() )
    await ctx.channel.purge( limit = 1 )
    
    await member.ban ( reason = reason )

    emb.set_author( name = member.name, icon_url = member.avatar_url )
    emb.add_field( name = 'Ban', value = 'Забанен пользователь : {}'.format( member.mention ) )
    
    await ctx.send( embed = emb )

#-KICK-
@client.command()
@commands.has_permissions ( administrator = True )

async def kick( ctx, member: discord.Member, *, reason = None ):
    await ctx.channel.purge( limit = 1 )
    await member.kick ( reason = reason )
    await ctx.send( f'Был кикнут: { member.mention }' )
#-MUTE-
@client.command()
@commands.has_permissions( administrator = True )

async def mute( ctx, member: discord.Member ):
	await ctx.channel.purge( limit = 1 )

	mute_role = discord.utils.get( ctx.message.guild.roles, name = 'MUTE' )

	await member.add_roles( mute_role )
	await ctx.send( f'У { member.mention }, бан чата!' )
#-UNMUTE-
@client.command()
@commands.has_permissions( administrator = True )

async def unmute( ctx, member: discord.Member ):
	await ctx.channel.purge( limit = 1 )

	mute_role = discord.utils.get( ctx.message.guild.roles, name = 'MUTE' )

	await member.remove_roles( mute_role )
	await ctx.send( f'У { member.mention }, был снят бан чата!' )


#-HELP-
@client.command()

async def help( ctx ):
    emb = discord.Embed( title = 'Помощь по командам' )
    emb.add_field( name = '{}clear'.format( pref ), value = 'ТЕСТ КМД' )
    emb.add_field( name = '{}ban'.format( pref ), value = 'ТЕСТ КМД' )
    emb.add_field( name = '{}kick'.format( pref ), value = 'ТЕСТ КМД' )

    await ctx.send( embed = emb )


#Версия бота
@client.command() 
async def version ( ctx ) :
    await ctx.send( 'Версия бота 1.0' )

#-CARD USER-
@client.command(aliases = ['card', 'cards']) # .я
async def card_user(ctx):
    await ctx.channel.purge(limit = 1)
 
    img = Image.new('RGBA', (400, 200), '#232529')
    url = str(ctx.author.avatar_url)[:-10]
 
    response = requests.get(url, stream = True)
    response = Image.open(io.BytesIO(response.content))
    response = response.convert('RGBA')
    response = response.resize((100, 100), Image.ANTIALIAS)
 
    img.paste(response, (15, 15, 115, 115))
 
    idraw = ImageDraw.Draw(img)
    name = ctx.author.name # Fsoky
    tag = ctx.author.discriminator # 9610
 
    headline = ImageFont.truetype('arial.ttf', size = 20)
    undertext = ImageFont.truetype('arial.ttf', size = 12)
 
    idraw.text((145, 15), f'{name}#{tag}', font = headline) # Fsoky#9610
    idraw.text((145, 50), f'ID: {ctx.author.id}', font = undertext)
 
    img.save('user_card.png')
 
    await ctx.send(file = discord.File(fp = 'user_card.png'))
#clear
@clear.error
async def clear_error( ctx, error ):
    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.send( f'{ ctx.author.name }, укажиите аргумент!' )

        if isinstance( error, commands.MissingPermissions ):
            await ctx.send( f'{ ctx.author.name }, у вас недостаточно прав!' )
#Подключение
token = os.environ.get('BOT_TOKEN')

bot.run(str(token))
