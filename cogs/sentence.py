import discord
import logging
import asyncio
import os.path
import re
from discord.ext import commands

class SentenceCog:
	LOGGER = logging.getLogger('Sentence')

	cancel_messages = ('cancel', 'stop')

	reg_exp = re.compile('(([`"]{3}).*?\\2)')
	
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
		self.LOGGER.info('Sentence new ran')

		def check(msg):
			return (msg.author == ctx.author) and (msg.guild is None)

		try:
			lines = ''

			# If file exists, output contents to user and proceed (if client wishes to)
			if os.path.exists(file_name + '.txt'):
				self.LOGGER.info('Found file')

				with open(file_name + '.txt', 'r') as file:
					lines = file.read()

				await ctx.send("You have been dm'd with instructions.", delete_after=15.0)

				await ctx.author.send('```' + lines + '```')
				await ctx.author.send('Creating a new grammar file will override the above. Proceed? (Y/N)')
				msg = await ctx.wait_for(timeout=60.0, check=check)

				if msg.content.lower()[0] != 'y':
					self.LOGGER.info('Command execution canceled')
					raise asyncio.TimeoutError

			# Makes new (or replaces) file w/ grammar
			await ctx.author.send("Send me a message of your grammar file surrounded by \\`\\`\\`'s. Send stop or cancel to cancel the command.")
			msg = await ctx.wait_for(timeout=60.0, check=check)

			if msg.content.lower() in self.cancel_messages:
				self.LOGGER.info('Command execution canceled')
				raise asyncio.TimeoutError

			gram = Grammar

		except asyncio.TimeoutError:
			await ctx.send(":thumbsdown:, Your request timed out")
			
#with open(filename + '.json', 'w') as outfile:
		#json.dump(grammar, outfile)
def setup(bot):
	bot.add_cog(SentenceCog(bot))