import MySQLdb
import discord
from discord.ext import commands
import asyncio
from pokemonlist import pokemon, pokejson, base_stats, cp_multipliers
from config import bot_channel, token, host, user, password, database, website, log_channel, raids_channel, spawn_channel, quest_channel
import datetime
import calendar
import math
import sys
import traceback
from geopy.geocoders import Nominatim

bot = commands.Bot(command_prefix = '.')#set prefix to .

database = MySQLdb.connect(host,user,password,database)
database.ping(True)
cursor = database.cursor()

def find_pokemon_id(name):
    if name == 'Nidoran-F':
        return 29
    elif name == 'Nidoran-M':
        return 32
    elif name == 'Mr-Mime':
        return 122
    elif name == 'Ho-oh':
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
    
def calculate_cp(pokemon, level, iv_attack, iv_defense, iv_stamina):
    stats = base_stats[str(pokemon)]
    cpm = cp_multipliers[str(level)]

    return math.floor(
        (cpm * cpm *
         (stats['attack'] + iv_attack)
         * math.sqrt((stats['defense'] + iv_defense))
         * math.sqrt((stats['stamina'] + iv_stamina))) / 10)

def get_time(minute):
    future = datetime.datetime.utcnow() + datetime.timedelta(minutes=minute)
    return calendar.timegm(future.timetuple())

#raid function
@bot.command(pass_context=True)
async def raid(ctx, arg, arg2, arg3, arg4):  # arg = gym name, arg2 = pokemon name, arg3 = level, arg4 = time remaining
    if ctx and ctx.message.channel.id == str(bot_channel) and str(arg2).lower() in pokemon:
        pokemon_id = find_pokemon_id(str(arg2).capitalize())
        time = get_time(int(arg4))
        try:
            cursor.execute("SELECT url FROM forts WHERE name LIKE '" + str(arg) + "%';")
            image = str(cursor.fetchall())
            image = image.split(',')
            image = image[0].split("'")
            cursor.execute("SELECT name FROM forts WHERE name LIKE '" + str(arg) + "%';")
            gym_title = str(cursor.fetchall())
            if '"' in gym_title:
                gym_title = gym_title.split('"')
            elif "'" in gym_title:
                gym_title = gym_title.split("'")
            cursor.execute("SELECT lat FROM forts WHERE name LIKE '" + str(arg) + "%';")
            lat = str(cursor.fetchall())
            lat = lat.split(',')
            lat = lat[0].split('(')
            cursor.execute("SELECT lon FROM forts WHERE name LIKE '" + str(arg) + "%';")
            lon = str(cursor.fetchall())
            lon = lon.split(',')
            lon = lon[0].split('(')
            cursor.execute("SELECT id FROM forts WHERE name LIKE '" + str(arg) + "%';")
            gym_id = str(cursor.fetchall())
            gym_id = gym_id.split(',')
            gym_id = gym_id[0].split('((')
            raid_embed = discord.Embed(
                title=(str(gym_title[1])),
                url=("https://www.google.com/maps/?q=" + str(lat[2]) + "," + str(lon[2])),
                description=str(arg2).capitalize() + " raid is available on the live map!\n"
                                                     "**Level:** " + str(arg3) + "\n"
                                                     "**L20 100%:** " + str(calculate_cp(pokemon_id, 20, 15, 15, 15)) + "\n"
                                                     "**L25 100%:** " + str(calculate_cp(pokemon_id, 25, 15, 15, 15)) + "\n"
                                                     "**Minutes Remaining:** " + str(arg4) + "\n"
                                                     "**Live Map:** "+ str(website),
                color=3447003
            )
            raid_embed.set_thumbnail(url=image[1])
            raid_embed.set_image(url="http://www.pokestadium.com/sprites/xy/" + str(arg2).lower() + ".gif")
            cursor.execute("INSERT INTO raids("
                           "id, external_id, fort_id , level, "
                           "pokemon_id, move_1, move_2, time_spawn, "
                           "time_battle, time_end, cp)"
                           "VALUES "
                           "(null, null, %s, "
                           "%s, %s, null, null, "
                           "null, null, %s, null);"
                           , (str(gym_id[1]), str(arg3), str(pokemon_id), str(time)))
            database.commit()
            await bot.say('Successfully added your raid to the live map.')
            await bot.send_message(discord.Object(id=raids_channel), embed=raid_embed)
            await bot.send_message(discord.Object(id=log_channel),
                                   str(ctx.message.author.name) + ' said there was a ' + str(arg2) +
                                   ' raid going on at ' + str(arg)) and print(
                str(ctx.message.author.name) + ' said there was a ' + str(arg2) +
                ' raid going on at ' + str(arg))
        except:
            database.rollback()
            tb = traceback.print_exc(file=sys.stdout)
            print(tb)
            await bot.say('Unsuccessful in database query, your raid was not added to the live map.')
            
@bot.command(pass_context=True)
async def spawn(ctx, arg, arg2, arg3, arg4=None):
    if ctx and ctx.message.channel.id == str(bot_channel) and str(arg).lower() in pokemon:
        pokemon_id = find_pokemon_id(str(arg).capitalize())
        time = get_time(15)
        desc = str(arg4)
        try:
            cursor.execute("INSERT INTO sightings("
                           "id, pokemon_id, spawn_id, expire_timestamp, encounter_id, lat, lon, "
                           "atk_iv, def_iv, sta_iv, move_1, move_2, gender, "
                           "form, cp, level, updated, weather_boosted_condition, weather_cell_id, weight) "
                           "VALUES (null, %s, null, %s, null, %s , %s"
                           ", null, null, null, null, null, null,"
                           " null, null, null, null, null, null, null);"
                           , (str(pokemon_id), str(time), str(arg2), str(arg3)))
            database.commit()
            await bot.say('Successfully added your spawn to the live map.\n'
                          '*Pokemon timers are automatically given 15 minutes since the timer is unknown.*')
            spawn_embed=discord.Embed(
                title='Click for directions!',
                url=("https://www.google.com/maps/?q=" + str(arg2) + "," + str(arg3)),
                description=('A wild ' + str(arg).capitalize() + ' is available!\n\n'
                                                                 '**Time Remaining:** ~15 minutes.\n'
                                                                 '**Description:** ' + str(desc) + '\n'
                                                                 '**Spotted by:** ' + str(ctx.message.author.name) + '!'),
                color=3447003
            )
            spawn_embed.set_image(url="http://www.pokestadium.com/sprites/xy/" + str(arg).lower() + ".gif")
            await bot.send_message(discord.Object(id=spawn_channel), embed=spawn_embed)
            await bot.send_message(discord.Object(id=log_channel), str(ctx.message.author.name) + ' said there was a wild ' + str(arg) +
                                   ' at these coordinates: ' + str(arg2) + ', ' + str(arg3))  and print(str(ctx.message.author.name) + ' said there was a wild ' + str(arg) +
                                   ' at these coordinates: ' + str(arg2) + ', ' + str(arg3))
        except:
            tb = traceback.print_exc(file=sys.stdout)
            print(tb)
            await bot.say('Unsuccessful in database query, your reported spawn was not added to the live map.')

@bot.command(pass_context=True)
async def quest(ctx, arg, arg2, arg3):
    if ctx:
        try:
            cursor.execute("SELECT lat FROM pokestops WHERE name LIKE '%" + str(arg) + "%'")
            lat = str(cursor.fetchall())
            lat = lat.split(',')
            lat = lat[0].split('((')
            lat = lat[1]
            cursor.execute("SELECT lon FROM pokestops WHERE name LIKE '%" + str(arg) + "%'")
            lon = str(cursor.fetchall())
            lon = lon.split(',')
            lon = lon[0].split('((')
            lon = lon[1]
            url = ('https://www.google.com/maps/?q=' + str(lat) + ',' + str(lon))
            cursor.execute("SELECT name FROM pokestops WHERE name LIKE '%" + str(arg) + "%'")
            stop_name = str(cursor.fetchall())
            stop_name = stop_name.split("(('")
            stop_name = str(stop_name[1]).split("',)")
            stop_name = str(stop_name[0])
            embed = discord.Embed(
                title = 'Quest Reported! Click for directions!',
                url = str(url),
                description = ('**Pokestop: **' + str(stop_name) + '\n\n'
                			   '**Quest: **' + str(arg2).capitalize() + '\n\n'
                               '**Reward: **' + str(arg3).capitalize() + '')
            )
            embed.set_footer(text='Reported by: ' + str(ctx.message.author.name))
            embed.set_thumbnail(url=('https://78.media.tumblr.com/7afe8f0cc9db095e6b3e3d00b2ff8dd7/tumblr_od0n3p2RtX1s2kttoo1_400.gif'))
            await bot.send_message(discord.Object(id=quest_channel), embed=embed)
            await bot.say('Successfully shared your report in #cspm_quests, thank you for sharing!')
        except:
            database.rollback()
            tb = traceback.print_exc(file=sys.stdout)
            print(tb)
            await bot.say('Unsuccessful in database query, your reported quest was not added to the quest channel.')

@bot.command()
async def coords(*, message:str):
    geo = Nominatim()
    coord = geo.geocode(str(message))
    try:
        await bot.say('The coordinates you requested for the address are shown below, you can now copy and paste it for the spawn command.')
        await bot.say(str(coord.latitude) + ' ' + str(coord.longitude))
    except:
        tb = traceback.print_exc(file=sys.stdout)
        print(tb)
        await bot.say('An error has occurred processing your request.')

@bot.command(pass_context=True)
async def map(ctx):
    if ctx:
        await bot.say('Hey! Visit ' + str(website) + ' to see our crowd-sourced raids and spawns!')

@bot.command(pass_context=True)
async def helpme(ctx):
    if ctx:
        help_embed=discord.Embed(
            title='CSPM Help',
            description='**Mapping Raids:**\n'
                        'To add a raid to the live map, use the following command:\n'
                        '`.raid <gym_name> <pokemon_name> <raid_level> <minutes_remaining>`\n'
                        'Example: `.raid "Fave Bird Mural" Lugia 5 45`\n\n'
                        '**Mapping Spawns:**\n'
                        'To add a spawn to the live map, use the following command:\n'
                        '`.spawn <pokemon_name> <latitude> <longitude> <optional_description>`\n'
                        'Example: `.spawn larvitar 34.101085 -118.287312`\n\n'
                        '**Sharing Quests**\n'
                        'To add a quest to the quests channel, use the following command:\n'
                        '`.quest <stop_name> <quest_type> <quest_reward>`\n\n'
                        '**Converting Address to Coordinates:**\n'
                        '`.coords <address>`\n\n'
                        '*To see raids that are crowdsourced, please make sure you tick the raids option in layers (top right)*',
            color=3447003
        )
        await bot.say(embed=help_embed)
        
bot.run(token)
