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

	def create(self, filename: str, raw: str):
		grammar = {}

		spaces = re.compile('\\s+')
		bars = re.compile('\\|')

		# Ensure every line has ':=='
		for line in [ele.split('::=') for ele in raw.split('\n')]:
			assert(len(line) == 2)
			assert(line[0] not in grammar)

			grammar[line[0]] = [spaces.split(ele) for ele in bars.split(line[1].strip())]

		return grammar

	def generate(self, sym, grammar):
		def _gen(symbol):
			if symbol not in grammar:
				return symbol
			else:
				output = [_gen(symb) for symb in random.choice(grammar[symbol])]
				return ' '.join(output)

		return _gen(sym)

	@commands.group(invoke_without_command=True)
	async def sentence(self, ctx):
		print('hello world')

	@sentence.command(name="generate")
	async def sentence_generate(self, ctx):
		await ctx.send("")

	@sentence.command(name="new")
	async def sentence_new(self, ctx, filename):
		self.LOGGER.info('Sentence new ran')

		def check(msg):
			return (msg.author == ctx.author) and (msg.guild is None)

		try:
			lines = ''

			# If file exists, output contents to user and proceed (if client wishes to)
			if os.path.exists('cogs/grammar/' + filename + '.json'):
				self.LOGGER.info('Found file')

				with open('cogs/grammar/' + filename + '.json', 'r') as file:
					lines = file.read()

				await ctx.send("You have been dm'd with instructions.", delete_after=15.0)

				await ctx.author.send('```' + lines + '```')
				await ctx.author.send('Creating a new grammar file will override the above. Proceed? (Y/N)')
				msg = await self.bot.wait_for('message', timeout=60.0, check=check)

				if msg.content.lower()[0] != 'y':
					self.LOGGER.info('Command execution cancelled')
					raise asyncio.TimeoutError

			# Makes new (or replaces) file w/ grammar
			await ctx.author.send("Send me a message of your grammar file surrounded by \\`\\`\\`'s. Send stop or cancel to cancel the command.")
			msg = await self.bot.wait_for('message', timeout=60.0, check=check)

			if msg.content.lower() in self.cancel_messages:
				self.LOGGER.info('Command execution cancelled')
				raise asyncio.TimeoutError

			print(msg.content)

			with open('cogs/grammar/' + filename + '.json', 'w') as outfile:
				json.dump(create(msg.content.replace('```', '')), outfile)
				self.LOGGER.info('Created file: ' + filename + '.json')

			await ctx.send("Success! :white_check_mark:")

		except asyncio.TimeoutError:
			await ctx.send(":thumbsdown:, Your request timed out")
			
def setup(bot):
	bot.add_cog(SentenceCog(bot))