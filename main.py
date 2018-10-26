import discord
import logging
import asyncio

from discord.ext import commands

import sys, traceback
import random
import tk

''' Returns prefixes for bot '''
def get_prefix(bot, message):
	prefixes = ['>']

	# If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
	return commands.when_mentioned_or(*prefixes)(bot, message)

extensions = ['cogs.meetup', 'cogs.random']

bot = commands.Bot(command_prefix=get_prefix, description='The RX UW Bot.... of Doom V2.0')

logging.basicConfig(level="INFO")
bot.logger = logging.getLogger(type(bot).__qualname__)

''' Loads the extensions '''
if __name__ == '__main__':
	for ext in extensions:
		try:
			bot.load_extension(ext)
			print(f'Loaded: {ext}!')
		except Exception as e:
			print(f'Failed to load extension {ext}.', file=sys.stderr)
			traceback.print_exc()

''' Runs when bot loads up '''
@bot.event
async def on_ready():
	print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

	# Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
	await bot.change_presence(activity=discord.Game(name='Life is cool! (prefix: ~)'))
	print('Successfully logged in and booted...!')

hello_list = [
		"Honestly, if you see this message, you are amazing. This message has a 0.1% chance of showing."
		"You, {}, are a motherfucking God\n\nDo screenshot this. \n~ Rx",

		"Wow, you lucky duck. {}, you just hit the 1% lottery!",

		"Good day, my good sir, {}",

		"Hello?",

		"Hello world!"
	]

hello_weights = [
		0.001,
		0.01,
		0.1,
		0.25,
		0.639
	]

''' Stupid hello command ^_^ '''
@bot.command()
@commands.cooldown(rate=20,per=10,type=commands.BucketType.user)
async def hello(ctx):
	await ctx.send(random.choices(hello_list, hello_weights)[0].format(ctx.author))

bot.run(tk.token(), bot=True, reconnect=True)