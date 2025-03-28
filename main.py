from datetime import datetime
from os import getenv, listdir
from time import time

import discord
import yaml
from discord import option
from discord.ext import commands
from dotenv import load_dotenv
from rich.console import Console

start_time = time()
console = Console()

load_dotenv()

settings = None
with open("settings.yaml") as stream:
    try:
        settings = list(yaml.safe_load_all(stream))
    except yaml.YAMLError as error:
        console.log(error)
        exit(1)  # fuck that im not going any further

bot = discord.Bot(
    intents=discord.Intents.all(),
    debug_guilds=settings[0]["debug_guilds"],
    owner_ids=settings[0]["owner_ids"],
    status=discord.Status.dnd,
    activity=discord.Game(name="Initializing...")
)
bot.core_settings = settings[0]
bot.chatbot_settings = settings[1]
bot.chatbot_thinking = False
bot.chatbot_message_history = []

with open(
        f"data/characters/{bot.chatbot_settings["default_character"]}/{bot.chatbot_settings["default_character"]}.yaml") as stream:
    try:
        bot.chatbot_character = yaml.safe_load(stream)
    except yaml.YAMLError as error:
        console.log(error)
        exit(1)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('oobabooga'), status=discord.Status.online)
    console.log(f"{bot.user} started @ {datetime.now().strftime('%I:%M %p, %m/%d/%Y')} | "
                f"Time to start: {round(time() - start_time, 4)} seconds")


def owner_only(ctx):
    if ctx.author.id in bot.owner_ids:
        return True
    else:
        return False


admin = bot.create_group("admin", "Admin only commands", checks=[owner_only])


@admin.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.respond("o7", ephemeral=True)
    await bot.close()


edit = admin.create_subgroup("edit", "Profile related commands")


@edit.command()
@commands.is_owner()
@option("name", description="New name for the bot to use")
async def username(ctx,
                   name: str):
    old_name = bot.user.name
    try:
        await bot.user.edit(username=name)
    except discord.HTTPException as error:
        await ctx.respond(f"**Error:** Username could not be changed. `({error.code})`\n"
                          f"**HTTP Status:** {error.status}\n"
                          f"**Error Details:** `{error.text}`",
                          ephemeral=True)
    await ctx.respond(f"Successfully changed my username from `{old_name}` to **{bot.user.name}**.", ephemeral=True)


@edit.command()
@commands.is_owner()
@option("picture", description="New avatar for the bot to use")
async def avatar(ctx,
                 picture: discord.Attachment):
    try:
        await bot.user.edit(avatar=await picture.read())
    except discord.HTTPException as error:
        await ctx.respond(f"**Error:** Avatar could not be changed. `({error.code})`\n"
                          f"**HTTP Status:** {error.status}\n"
                          f"**Error Details:** `{error.text}`",
                          ephemeral=True)
    except discord.InvalidArgument:
        await ctx.respond(f"**Error**: The picture supplied isn't in the right format.",
                          ephemeral=True)
    await ctx.respond(f"Successfully changed my avatar!", ephemeral=True)


@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond("This command is currently on cooldown!")
    else:
        try:
            await ctx.respond(
                embed=discord.Embed(
                    title=error.__class__.__name__,
                    description=str(error),
                    color=discord.Color.red(),
                ), ephemeral=True
            )
            raise error
        finally:
            raise error


@bot.slash_command(name="hello", description="Say hello to the bot")
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond("Hey!")


for filename in listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

if __name__ == '__main__':
    bot.run(getenv("TOKEN"))
