import discord
import logging
import asyncio
from random import getrandbits
from discord.ext import commands

class RandoCog:
	LOGGER = logging.getLogger('Rando')
	
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def weird(self, ctx, *, arg):
		await ctx.send(''.join(list(map(lambda c: c.upper() if bool(getrandbits(1)) else c, arg.lower()))))

def setup(bot):
	bot.add_cog(RandoCog(bot))