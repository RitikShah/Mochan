import discord
import logging
import asyncio
import os.path
from discord.ext import commands

class SentenceCog:
	LOGGER = logging.getLogger('Sentence')
	
	def __init__(self, bot):
		self.bot = bot

	def read_file(self, name):
		with open(name + '.txt', 'r') as file:
			return file.split('\n')

	@commands.group(invoke_without_command=True)
	async def sentence(self, ctx):
		print('hello world')

	@sentence.command(name="generate")
	async def sentence_generate(self, ctx):
		await ctx.send("")

	@sentence.command(name="new")
	async def sentence_new(self, ctx, file_name):
		LOGGER.info('Sentence new ran')
		lines = ''

		if os.path.exists(file_name + '.txt'):
			LOGGER.info('Found file')

			with open(file_name + '.txt', 'r') as file:
				lines = file.read()

			

def setup(bot):
	bot.add_cog(SentenceCog(bot))