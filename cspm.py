import MySQLdb
import discord
from discord.ext import commands
import asyncio
from pokemonlist import pokemon, pokejson
from config import bot_channel, token, host, user, password, database, website, log_channel
import datetime
import calendar

bot = commands.Bot(command_prefix = '.')#set prefix to .

database = MySQLdb.connect(host,user,password,database)

cursor = database.cursor()

def find_pokemon_id(name):
    if name == 'Nidoran-F':
        return 29
    elif name == 'Nidoran-M':
        return 32
    elif name == 'Mr-Mime':
        return 122
    elif name == 'Ho-Oh':
        return 250
    elif name == 'Mime-Jr':
        return 439
    else:
        name = name.split('-')[0]
        for k in pokejson.keys():
            v = pokejson[k]
            if v == name:
                return int(k)
        return 0

def get_time(minute):
    future = datetime.datetime.utcnow() + datetime.timedelta(minutes=minute)
    return calendar.timegm(future.timetuple())

#raid function
@bot.command(pass_context=True)
async def raid(ctx, arg, arg2, arg3, arg4):#arg = gym name, arg2 = pokemon name, arg3 = level, arg4 = time remaining
    if ctx and ctx.message.channel.id == str(bot_channel):
        pokemon_id = find_pokemon_id(str(arg2).capitalize())
        time = get_time(int(arg4))
        try:
            cursor.execute("SELECT id FROM forts WHERE NAME LIKE '" + str(arg) + "%';")
            gym_id = str(cursor.fetchall())
            gym_id = gym_id.split(',')
            gym_id = gym_id[0].split('((')
            cursor.execute("INSERT INTO raids("
                           "id, external_id, fort_id , level, "
                           "pokemon_id, move_1, move_2, time_spawn, "
                           "time_battle, time_end, cp)"
                           "VALUES "
                           "(null, null, " + str(gym_id[1]) + ", "
                           + str(arg3) + ", " + str(pokemon_id) + ", null, null, "
                           "null, null, " + str(time) + ", null);")
            database.commit()
            await bot.say('Successfully added your raid to the live map.')
            await bot.send_message(discord.Object(id=log_channel), str(ctx.message.author.name) + ' said there was a ' + str(arg2) +
                                   ' raid going on at ' + str(arg)) and print(str(ctx.message.author.name) + ' said there was a ' + str(arg2) +
                                   ' raid going on at ' + str(arg))
        except:
            database.rollback()
            await bot.say('Unsuccesful in database query, your raid was not added to the live map.')
@bot.command(pass_context=True)
async def spawn(ctx, arg, arg2, arg3):
    if ctx and ctx.message.channel.id == str(bot_channel) and arg in pokemon:
        pokemon_id = find_pokemon_id(str(arg).capitalize())
        time = get_time(15)
        try:
            cursor.execute("INSERT INTO sightings("
                           "id, pokemon_id, spawn_id, expire_timestamp, encounter_id, lat, lon, "
                           "atk_iv, def_iv, sta_iv, move_1, move_2, gender, "
                           "form, cp, level, updated, weather_boosted_condition, weather_cell_id, weight) "
                           "VALUES (null, " + str(pokemon_id) +", null," + str(time) + ", null," + str(arg2) + ", " + str(arg3) +
                           ", null, null, null, null, null, null,"
                           " null, null, null, null, null, null, null);")
            database.commit()
            await bot.say('Successfully added your spawn to the live map.\n'
                          '*Pokemon timers are automatically given 15 minutes since the timer is unknown.*')
            await bot.send_message(discord.Object(id=log_channel), str(ctx.message.author.name) + ' said there was a wild ' + str(arg) +
                                   ' at these coordinates: ' + str(arg2) + ', ' + str(arg3))  and print(str(ctx.message.author.name) + ' said there was a wild ' + str(arg) +
                                   ' at these coordinates: ' + str(arg2) + ', ' + str(arg3))
        except:
            await bot.say('Unsuccessful in database query, your reported spawn was not added to the live map.')
@bot.command(pass_context=True)
async def map(ctx):
    if ctx:
        await bot.say('Hey! Visit' + str(website) + ' to see our crowd-sourced spawns!')

bot.run(token)
