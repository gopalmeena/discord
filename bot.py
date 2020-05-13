import discord
import os

from discord.ext import commands
from cogs.utils.logger import logger


initial_extensions = (
    'cogs.google',
    'cogs.recent',
)

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print("Let's rock and roll!")


@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.errors.CommandNotFound):
		await ctx.send(f"Invalid command.Valid commands are:\n\n"\
			f"hey\n!google <search query>\n!recent <search query>")
	if isinstance(error, commands.errors.MissingRequiredArgument):
		await ctx.send("Please enter a valid search query with command.")
	logger.error(error)


@bot.event
async def on_message(message):
    # Prevent replying to itself
    if bot.user.id == message.author.id:
        return
    # if message is equal to "hey", than reply back "hi"
    # else try to process them as commands
    if str(message.content.lower()) == "hey":
        await message.channel.send('hi')
    await bot.process_commands(message)


# load all extensions listed above
for extension in initial_extensions:
    try:
        bot.load_extension(extension)
    except Exception as e:
        logger.error(f'Failed to load extension {extension}.')
        logger.error(e)

bot.run(os.environ.get("BOT_TOKEN"))