blocked = False
reason = "Spidermun ciagle jest budowany, cierpliwosci :)"

import discord
from discord.ext import tasks
from discord import app_commands
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
import pytz
import json
import asyncio
import random

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

load_dotenv("secrets.env")
discord_api_token = os.getenv("discord_api_token")

global trusted_user_ids
global permanent_categories
global categories_to_add_list

with open('./storage/data.json', 'r') as file:
    data = json.load(file)
    trusted_user_ids = data["trusted_user_ids"]
    permanent_categories = data["permanent_categories"]
    categories_to_add_list = data["categories_to_add_list"]
    


class TrustedError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


async def only_for_staff(interaction): # if you want a command to be only avaible to staff members, add this line: await only_for_staff(interaction) at the start of any command
    if(interaction.user.id in trusted_user_ids.values()):
        staff_name = [key for key, value in trusted_user_ids.items() if value == interaction.user.id][0]
        await interaction.channel.send(f"Witaj, {staff_name} :saluting_face:")
    else:
        await interaction.channel.send(f"Ta komenda dostepna jest tylko dla administracji.")
        raise TrustedError(f"Uzytkownik {interaction.user.display_name} nie jest czlonkiem administracji.")


async def get_categories(interaction):
    categories_dictionary = interaction.guild.categories
    categories_list = []

    for category in categories_dictionary:
        categories_list.append(category.name)

    return categories_list


async def get_channels_in_directory(interaction, text_or_audio: str = "", category: str="0"):
    if(text_or_audio == "text"):
        category = discord.utils.get(interaction.guild.categories, name=f"{category}-text")
    elif(text_or_audio == "audio"):
        category = discord.utils.get(interaction.guild.categories, name=f"{category}-audio")
    else:
        category = discord.utils.get(interaction.guild.categories, name=category)

    channels = []

    if category is not None:
        for channel in category.channels:
            channels.append(channel.name)

    return channels


async def log(message: str):
    # create a timezone for Warsaw
    warsaw_timezone = pytz.timezone('Europe/Warsaw')

    # get the current time in Warsaw
    warsaw_time = datetime.now(warsaw_timezone)

    log_record = warsaw_time.strftime(f"%d/%m/%Y - %H:%M:%S > {message}")
    print(log_record)

    with open("./storage/logs.dat", 'a') as f:
        f.write(f"{log_record} \n")


async def delete_category(category):
    channels = category.channels

    for channel in channels:
        await channel.delete()
    
    await category.delete()


@client.event
async def on_ready():
    # await tree.sync(guild=discord.Object(id=1144632862314860675)) # comment this line and uncomment the next one in production
    await tree.sync()
    await client.change_presence(activity=discord.Game(name="Uncle Ben Saving Simulator 2023"))
    print(f"Spidermun running as: {client.user}")


@client.event
async def on_member_update(before, after):
    roles = []

    for role in before.roles:
        roles.append(role.name)

    if(len(roles) == 1): # if the user didn't have any roles before (had only one (the @everyone role (is new to the server))) try to give him access to certain categories
        school_years = ["1", "2", "3", "-1"]
        class_name = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]

        right_class = ""

        for role in after.roles:
            if(role.name in school_years or role.name in class_name):
                right_class += role.name

        for classes in class_name:
            if(right_class.startswith(classes)):
                right_class = right_class[::-1]
                break

        rules_channel = after.guild.get_channel(1144633291538976779)
        khenzii = await after.guild.fetch_member(714462696061403176)

        try:
            category = discord.utils.get(after.guild.categories, name=f"{right_class}-text")
            await category.set_permissions(after, read_messages=True)

            category = discord.utils.get(after.guild.categories, name=f"{right_class}-audio")
            await category.set_permissions(after, read_messages=True)

            await after.guild.system_channel.send(f"Witaj, {after.mention}! Zostaly ci przyznane permisje pozwalajace wyswietlac kategorie: {right_class}-TEXT i {right_class}-AUDIO. Jesli chcesz, mozesz zapoznac sie z regulaminem na {rules_channel.mention}. Jesli uwazasz ze przyznalem ci zle permisje, skontaktuj sie z {khenzii.mention}. Milej zabawy :)")
        except Exception as e:
            # print for debug uses (if the user won't get the permissions even tho he should, you will be able to check the logs later)
            print(f"most of the time, you should ignore this print (the user prolly just choose the 'Guest' option so we didn't grant him any permissions, however if he should have gotten some permissions, you can check what went wrong here) exception: {e}, category name (tried to add permissions to that thing (with '-TEXT' and '-AUDIO' at the end)): {right_class}, user: '{after.display_name}'")
            await after.guild.system_channel.send(f"Witaj, {after.mention}! Jesli chcesz, mozesz zapoznac sie z regulaminem na {rules_channel.mention}. Milej zabawy :)")

@client.event
async def on_member_remove(member):
    khenzii = await member.guild.fetch_member(714462696061403176)

    goodbyes = [f"Dzis, ", f"{member.mention} postanowil nas opuscic - Dowidzenia :/", f"Zegnaj, {member.mention} :<"]
    random_number = random.randint(0, len(goodbyes)-1)

    if(random_number == 0):
        gmt_plus_2 = timezone(timedelta(hours=2))
        current_datetime = datetime.now(gmt_plus_2)
        current_datetime_formated = current_datetime.strftime(f"%d/%m/%Y")
        
        random_message = goodbyes[0]
        random_message += f"{current_datetime_formated}, opuscil nas {member.mention}. Zegnaj!"
    else:
        random_message = goodbyes[random_number]
    

    await member.guild.system_channel.send(f"{random_message}\n\n{khenzii.mention}")


@tree.command(name="ping", description="pong!")
async def ping(interaction):
    await interaction.response.send_message(":thumbsup:")

    if(blocked == True and interaction.user.id != 714462696061403176):
        await interaction.channel.send(f"Bot obecnie jest zablokowany. Przyczyna: {reason}")
        return

    await log(f"{interaction.user.display_name} ran the ping command")

    await interaction.channel.send("pong :)")


@tree.command(name="help", description="displays some info and stuff")
@app_commands.describe(language="en/pl (default: pl)")
async def help_command(interaction, language: str="pl"):
    await interaction.response.send_message(":thumbsup:")

    if(blocked == True and interaction.user.id != 714462696061403176):
        await interaction.channel.send(f"Bot obecnie jest zablokowany. Przyczyna: {reason}")
        return

    await log(f"{interaction.user.display_name} ran the help command")

    if(language == "pl"):
        await interaction.channel.send("Liste komend i ich opisy znajdziesz w publicznym repo Spidermuna: https://github.com/Khenziii/Spidermun")
    elif(language == "en"):
        await interaction.channel.send("All of the commands are explained in Spidermun's public github repo: https://github.com/Khenziii/Spidermun")
    else:
        await interaction.channel.send("Liste komend i ich opisy znajdziesz w publicznym repo Spidermuna: https://github.com/Khenziii/Spidermun")


@tree.command(name="push_newyear", description="zmienia nazwy kanalow w ten sposob, aby pasowaly do nowych klas")
async def push_newyear(interaction):
    await interaction.response.send_message(":thumbsup:")

    if(blocked == True and interaction.user.id != 714462696061403176):
        await interaction.channel.send(f"Bot obecnie jest zablokowany. Przyczyna: {reason}")
        return

    await log(f"{interaction.user.display_name} ran the push_newyear command")
    await only_for_staff(interaction)

    await interaction.channel.send("Ta komenda nie zostala jeszcze zaimplementowana. Aby przyspieszyc jej produkcje, skontaktuj sie z Khenzii'm :) https://khenzii.dev/")


@tree.command(name="push", description="pushuje kategorie i channelsy w kategoriach, wiecej info -> /help")
async def push(interaction):
    await interaction.response.send_message(":thumbsup:")

    if(blocked == True and interaction.user.id != 714462696061403176):
        await interaction.channel.send(f"Bot obecnie jest zablokowany. Przyczyna: {reason}")
        return

    await log(f"{interaction.user.display_name} ran the push command")
    await only_for_staff(interaction)


    chars = ['\\', '|', '/', '-']
    message = await interaction.channel.send(":)")

    @tasks.loop(seconds=1)
    async def waiting_animation():
        for char in chars:
            await asyncio.sleep(1)  # wait for 1 second
            await message.edit(content=char)

    waiting_animation.start()
    

    categories_list = await get_categories(interaction)
    channels_to_add_list_text = await get_channels_in_directory(interaction, text_or_audio="text")
    channels_to_add_list_audio = await get_channels_in_directory(interaction, text_or_audio="audio")

    for category in categories_to_add_list:
        # create categories (if they don't exist yet)
        if(not (f"{category}-text" in categories_list)):
            await interaction.guild.create_category(f"{category}-text")

        if(not (f"{category}-audio" in categories_list)):
            await interaction.guild.create_category(f"{category}-audio")

        # create channels in those categories (if they don't exist yet)
        category_object = discord.utils.get(interaction.guild.categories, name=f"{category}-text")

        if(category_object is not None):
            for channel in channels_to_add_list_text:
                if discord.utils.get(category_object.channels, name=channel) is None:
                    await interaction.guild.create_text_channel(channel, category=category_object)
                
        category_object = discord.utils.get(interaction.guild.categories, name=f"{category}-audio")

        if(category_object is not None):
            for channel in channels_to_add_list_audio:
                if discord.utils.get(category_object.channels, name=channel) is None:
                    await interaction.guild.create_voice_channel(channel, category=category_object)


    waiting_animation.stop()
    await asyncio.sleep(5)
    await message.edit(content="done!")
        

@tree.command(name="stash", description="stashuje kategorie i channelsy w kategoriach, wiecej info -> /help")
async def stash(interaction):
    await interaction.response.send_message(":thumbsup:")

    if(blocked == True and interaction.user.id != 714462696061403176):
        await interaction.channel.send(f"Bot obecnie jest zablokowany. Przyczyna: {reason}")
        return

    await log(f"{interaction.user.display_name} ran the stash command \n")

    await only_for_staff(interaction)


    chars = ['\\', '|', '/', '-']
    message = await interaction.channel.send(":)")

    @tasks.loop(seconds=1)
    async def waiting_animation():
        for char in chars:
            await asyncio.sleep(1)  # wait for 1 second
            await message.edit(content=char)

    waiting_animation.start()


    categories_list = await get_categories(interaction)
    channels_list_text = await get_channels_in_directory(interaction, text_or_audio="text")
    channels_list_audio = await get_channels_in_directory(interaction, text_or_audio="audio")

    for category in categories_list:
        # delete categories if they are not in permanent_categories and in categories_to_add_list
        category_object = discord.utils.get(interaction.guild.categories, name=f"{category}")

        if(category not in permanent_categories and (category[:-5] not in categories_to_add_list and category[:-6] not in categories_to_add_list)):
            await delete_category(category_object)
            continue # If we have the category, there is no channels anyway, no point in going further.

        # if we haven't deleted the category, check if they are channels inside of it that need to be deleted
        if(category in permanent_categories):
            continue # there for sure are no channels that should be deleted inside of the permanent categories


        current_channels_list = await get_channels_in_directory(interaction, category=category)

        if(category.endswith("text") == True):
            if(category_object is not None):
                for channel_in_category in current_channels_list:
                    if(channel_in_category not in channels_list_text):
                        channel = discord.utils.get(category_object.channels, name=channel_in_category)
                        await channel.delete()
                    
        elif(category.endswith("audio") == True):
            if(category_object is not None):
                for channel_in_category in current_channels_list:
                    if(channel_in_category not in channels_list_audio):
                        channel = discord.utils.get(category_object.channels, name=channel_in_category)
                        await channel.delete()


    waiting_animation.stop()
    await asyncio.sleep(5)
    await message.edit(content="done!")
            

@tree.command(name="show_trusted_ids", description="Pokazuje zaufane id. Wiecej info -> /help")
async def show_trusted_ids(interaction):
    await interaction.response.send_message(":thumbsup:")

    if(blocked == True and interaction.user.id != 714462696061403176):
        await interaction.channel.send(f"Bot obecnie jest zablokowany. Przyczyna: {reason}")
        return

    await log(f"{interaction.user.display_name} ran the show_trusted_id command")

    global trusted_user_ids
    await interaction.channel.send(trusted_user_ids)


@tree.command(name="set_trusted_ids", description="Zmienia zaufane id. Wiecej info -> /help")
@app_commands.describe(ids="Slownik nowych id.")
async def set_trusted_ids(interaction, ids: str):
    await interaction.response.send_message(":thumbsup:")

    if(blocked == True and interaction.user.id != 714462696061403176):
        await interaction.channel.send(f"Bot obecnie jest zablokowany. Przyczyna: {reason}")
        return

    await log(f"{interaction.user.display_name} ran the set_trusted_id command")
    await only_for_staff(interaction)

    
    if(str(714462696061403176) in ids):
        try:
            old_ids = data["trusted_user_ids"]

            ids_dict = json.loads(ids.replace("'", '"'))
            data["trusted_user_ids"] = ids_dict
        
            with open("./storage/data.json", "w") as file:
                json.dump(data, file)

            global trusted_user_ids
            trusted_user_ids = ids_dict
        except:
            await interaction.channel.send("Skrzaniles syntax XD. Sprobuj ponownie.")
            return
    else:
        await interaction.channel.send("Pamietaj aby w swoim slowniku zawrzec id Khenzii'ego. Aby zobaczyc obecny slownik uzyj komendy /show_trusted_ids.")
        return
    
    await interaction.channel.send("Zmienilem!")
    await interaction.channel.send(f"{old_ids} --> {data['trusted_user_ids']}")


@tree.command(name="show_permanent_categories", description="Pokazuje permanentne kategorie. Wiecej info -> /help")
async def show_permanent_categories(interaction):
    await interaction.response.send_message(":thumbsup:")

    if(blocked == True and interaction.user.id != 714462696061403176):
        await interaction.channel.send(f"Bot obecnie jest zablokowany. Przyczyna: {reason}")
        return

    await log(f"{interaction.user.display_name} ran the show_permanent_categories command")

    global permanent_categories
    await interaction.channel.send(permanent_categories)


@tree.command(name="set_permanent_categories", description="Zmienia permanentne kategorie. Wiecej info -> /help")
@app_commands.describe(kategorie="Lista nowych kategorii")
async def set_permanent_categories(interaction, kategorie: str):
    await interaction.response.send_message(":thumbsup:")

    if(blocked == True and interaction.user.id != 714462696061403176):
        await interaction.channel.send(f"Bot obecnie jest zablokowany. Przyczyna: {reason}")
        return

    await log(f"{interaction.user.display_name} ran the set_permanent_categories command")
    await only_for_staff(interaction)
    
    try:
        old_categories = data["permanent_categories"]
        lista_kategorie = json.loads(kategorie.replace("'", '"'))
        data["permanent_categories"] = lista_kategorie
        
        with open("./storage/data.json", "w") as file:
            json.dump(data, file)

        global permanent_categories
        permanent_categories = lista_kategorie
    except:
        await interaction.channel.send("Skrzaniles syntax XD. Sprobuj ponownie.")
        return
    
    await interaction.channel.send("Zmienilem!")
    await interaction.channel.send(f"{old_categories} --> {data['permanent_categories']}")


@tree.command(name="show_klasy", description="Pokazuje klasy. Wiecej info -> /help")
async def show_klasy(interaction):
    await interaction.response.send_message(":thumbsup:")

    if(blocked == True and interaction.user.id != 714462696061403176):
        await interaction.channel.send(f"Bot obecnie jest zablokowany. Przyczyna: {reason}")
        return

    await log(f"{interaction.user.display_name} ran the show_klasy command")

    global categories_to_add_list
    await interaction.channel.send(categories_to_add_list)


@tree.command(name="set_klasy", description="Zmienia klasy. Wiecej info -> /help")
@app_commands.describe(klasy="Lista nowych klas")
async def set_permanent_categories(interaction, klasy: str):
    await interaction.response.send_message(":thumbsup:")

    if(blocked == True and interaction.user.id != 714462696061403176):
        await interaction.channel.send(f"Bot obecnie jest zablokowany. Przyczyna: {reason}")
        return

    await log(f"{interaction.user.display_name} ran the set_klasy command")
    await only_for_staff(interaction)
    
    old_klasy = data["categories_to_add_list"]
    lista_klasy = json.loads(klasy.replace("'", '"'))
    data["categories_to_add_list"] = lista_klasy
    
    with open("./storage/data.json", "w") as file:
        json.dump(data, file)

    global categories_to_add_list
    categories_to_add_list = lista_klasy
    
    await interaction.channel.send("Zmienilem!")
    await interaction.channel.send(f"{old_klasy} --> {data['categories_to_add_list']}")


client.run(discord_api_token)