import discord
import asyncio
import re
import json
from random import randint
from discord.ext import commands

class MeetupCog:
	meetup_channels = (400567035249033217, 362691852274630657)
	meetup_mention = '<@&487120797190848534>'

	x_emojis = ('❎', '❌', '✖️', '🇽')
	check_emojis = ('☑️', '✔️', '✅')

	cancel_messages = ('cancel', 'stop')

	meetup_dict = {
		'title': "What is the title of this meetup?",
		'when_where': "When and Where (Ex: Tommorow 3 @ Starbucks)",
		'time': "What is the period of time (Ex: 12:30)?",
		'type': "Is this casual or structured?",
		'activity': "What are we doing?",
		'cost': "What is the cost range?",
		'description': "Write a small description about this meetup.",
		'location': "Paste a link to Google Maps or anything else (Optional, put a non-url to skip)."
	}

	num_to_emoji = [':zero:', ':one:', ':two:', ':three:', ':four:', 
					':five:', ':six:', ':seven:', ':eight:', ':nine:']

	rx_uw_bot_id = 489158438086115328

	url_pattern = '(https?:\\/\\/(?:www\\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\\.[^\\s]{2,}|www\\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\\.[^\\s]{2,}|https?:\\/\\/(?:www\\.|(?!www))[a-zA-Z0-9]\\.[^\\s]{2,}|www\\.[a-zA-Z0-9]\\.[^\\s]{2,})'

	json_file = 'data.json'

	def __init__(self, bot):
		self.bot = bot

	def check_meetup_channel(ctx):
		return ctx.message.channel.id in (400567035249033217, 362691852274630657)

	def check_rx(ctx):
		return ctx.message.author.id == 136278937532628993

	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
		 	await ctx.send(f'That command is on cooldown. Please try after {int(error.retry_after) + 1} second(s).')

	async def on_reaction_add(self, reaction, user):
		print(str(reaction.emoji))
		try:
			for event in self.data[f'{reaction.message.guild.id}']['events']:
				if event['embed_id'] == reaction.message.id and user.id == event['author']:
					if str(reaction.emoji) in self.x_emojis:
						print('x')
						del(event)
						await reaction.message.channel.send("❎ Event Deleted!", delete_after=5.0)
						await reaction.message.delete()
					elif str(reaction.emoji) in self.check_emojis:
						print('check')
						del(event)
						await reaction.message.channel.send("✅ Event Success!", delete_after=5.0)
						await reaction.message.unpin()

			with open(self.json_file, "w+") as file:
				json.dump(self.data, file)

		except KeyError:
			pass

	async def on_message_delete(self, message):
		if self.data[f'{message.guild.id}'] is not None and message.author.id == self.rx_uw_bot_id:
			for event in self.data[f'{message.guild.id}']['events']:
				if event['embed_id'] == message.id: del(event)
	
	async def on_ready(self):
		print(f'Reading {self.json_file}')
		with open(self.json_file) as file:
			self.data = json.load(file)
			print(self.data)
			print('Data successfully loaded!')

	'''
	@commands.command()
	@commands.check(check_rx)
	async def setpin(self, ctx):
		pin_msg = ctx.send("This message needs to be pinned manually!")
		try:
			self.data[f'{ctx.guild.id}']['pin'] = pin_msg

		except KeyError:
			self.data[ctx.guild.id] = {"pin": pin_msg, "event": []}
			print(self.data)

		with open(self.json_file, "w+") as file:
			json.dump(self.data, file)

		await ctx.send("Database successfully updated!", delete_after=15.0)
		await ctx.message.add_reaction("👍")
	'''

	@commands.command()
	@commands.cooldown(rate=1,per=60,type=commands.BucketType.user)
	@commands.check(check_meetup_channel)
	@commands.has_any_role('meetup', 'Mods', 'Admins')
	async def meetup(self, ctx):
		event = {}

		def check(msg):
			return (msg.author == ctx.author) and (msg.guild is None)

		def is_url(url):
			prog = re.compile(self.url_pattern)
			return prog.search(url)

		await ctx.send("You have been dm'd with instructions.", delete_after=15.0)
		await ctx.author.send("I will ask you a few questions about your meetup. \nSay cancel or stop at any point to cancel.\n\n")

		async with ctx.typing():
			try:
				for k,v in self.meetup_dict.items():
					await ctx.author.send(v)
					msg = await self.bot.wait_for('message', timeout=60.0, check=check)
					event[k] = msg.content
					if msg.content.lower() in self.cancel_messages: raise asyncio.TimeoutError
				
			except asyncio.TimeoutError:
				await ctx.send(":thumbsdown:, Your request timed out")

			else:
				if is_url(event['location']) is not None:
					embed = discord.Embed(title=event['title'], url=event['location'], description=event['when_where'], color=0x00baa6)
				else:
					embed = discord.Embed(title=event['title'], description=event['when_where'], color=0x00baa6)
				
				embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
				embed.add_field(name='Type', value=event['type'], inline=True)
				embed.add_field(name='Time', value=event['time'], inline=True)
				embed.add_field(name='Activity', value=event['activity'], inline=True)
				embed.add_field(name='Cost', value=event['cost'], inline=True)
				embed.set_footer(text=event['description'])
				
				if ctx.message.channel.id == 400567035249033217:
					self.meetup_mention = '<@&489719429224071168>'
				elif ctx.message.channel.id == 362691852274630657:
					self.meetup_mention = '<@&487120797190848534>'

				embed_msg = await ctx.send(f'A new {self.meetup_mention} has appeared!', embed=embed)
				await embed_msg.pin()
				await embed_msg.add_reaction('👍')
				await embed_msg.add_reaction('👀')
				await embed_msg.add_reaction('👎')

				event['embed_id'] = embed_msg.id
				event['author'] = ctx.author.id

				await ctx.author.send("Success!")
				await ctx.send("👍 Meetup successfully created! Add any X emoji to the message to delete the event. Add any check emoji to unpin the event.", delete_after=20.0)

				try:
					self.data[f'{ctx.guild.id}']['events'].append(event)

				except KeyError:
					self.data[f'{ctx.guild.id}'] = {'events': [event]}

				with open(self.json_file, "w+") as file:
					json.dump(self.data, file)

				print(self.data)

				await ctx.message.delete()

	@commands.command()
	@commands.check(check_meetup_channel)
	async def list(self, ctx):
		s_msg = ''
		counter = 0
		for event in self.data[f'{ctx.guild.id}']['events']:
			counter += 1
			s_msg += self.num_to_emoji[counter] + ' ' + event['title'] + ': ' + event['time'] + '\n'

		msg = await ctx.send(s_msg)
		for num in len(self.data[f'{ctx.guild.id}']['events']):
			await msg.add_reaction(self.num_to_emoji[num])


	@commands.command()
	@commands.check(check_rx)	
	async def testpin(self, ctx):
		msg = await ctx.send("This message is pinned and self-destruct in 20 seconds", delete_after=20.0)
		await msg.pin()

	@commands.command()
	@commands.check(check_rx)
	async def testreaction(self, ctx):
		msg = await ctx.send("This message will be auto-reacted and self-destruct in 20 seconds", delete_after=20.0)
		await msg.add_reaction('👍')

	@commands.command()
	@commands.check(check_rx)
	async def testdm(self, ctx):
		def check_dm(msg):
			return msg.author == ctx.author and msg.guild is None
		await ctx.author.send("A test DM Message. Please reply...")
		msg = await self.bot.wait_for('message', check=check_dm)
		await ctx.author.send("You said: " + msg.content)

	@commands.command()
	@commands.check(check_rx)
	async def testtype(self, ctx):
		print('command ran')
		await ctx.send("The bot is now typing", delete_after=5.0)
		async with ctx.typing():
			print('typing')
			await asyncio.sleep(5)
			await ctx.send("The bot done typing", delete_after=5.0)

def setup(bot):
    bot.add_cog(MeetupCog(bot))
