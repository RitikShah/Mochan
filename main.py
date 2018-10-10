import discord
import logging
import asyncio

from discord.ext import commands

import sys, traceback
import tk

logging.basicConfig(level="WARNING")

bot = commands.Bot(command_prefix="~", description="Rx has the best bot let that be heard.")
setattr(bot, "logger", logging.getLogger("log"))
url_pattern = '(https?:\\/\\/(?:www\\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\\.[^\\s]{2,}|www\\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\\.[^\\s]{2,}|https?:\\/\\/(?:www\\.|(?!www))[a-zA-Z0-9]\\.[^\\s]{2,}|www\\.[a-zA-Z0-9]\\.[^\\s]{2,})'

''' Returns prefixes for bot '''
def get_prefix(bot, message):
	prefixes = ['~']

	# If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
	return commands.when_mentioned_or(*prefixes)(bot, message)

extensions = ['cogs.meetup']

bot = commands.Bot(command_prefix=get_prefix, description='The RX UW Bot.... of Doom V2.0')

''' Loads the extensions '''
if __name__ == '__main__':
	for ext in extensions:
		try:
			bot.load_extension(ext)
		except Exception as e:
			print(f'Failed to load extension {ext}.', file=sys.stderr)
			traceback.print_exc()

''' Runs when bot loads up '''
@bot.event
async def on_ready():
	print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

	# Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
	await bot.change_presence(game=discord.Game(name='Life is cool! (prefix: ~)'))
	print('Successfully logged in and booted...!')

''' Stupid hello command ^_^ '''
@bot.command()
@commands.cooldown(rate=20,per=10,type=commands.BucketType.user)
async def hello(ctx):
	rint = randint(0,1000)
	if rint > 999:
		message = await ctx.send("Honestly, if you see this message, you are amazing. This message has a 0.1% chance of showing. \nYou, {}, are a motherfucking God\n\nDo screenshot this. \n~ Rx".format(ctx.author))
	elif rint > 990:
		message = await ctx.send("Wow, you lucky duck. {}, you just hit the 1% lottery!".format(ctx.author))
	elif rint > 900:
		message = await ctx.send("Good day, my good sir, {}".format(ctx.author))
	elif rint == 666:
		message = await ctx.send("*glares into your soul*")
	elif rint > 500:
		message = await ctx.send("Hello?")
	else:
		message = await ctx.send("Hello world!")

bot.run(tk.token(), bot=True, reconnect=True)