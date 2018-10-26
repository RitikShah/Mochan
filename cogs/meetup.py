import discord
import logging
import asyncio
import re
from random import randint
from discord.ext import commands

class MeetupCog:
	LOGGER = logging.getLogger('MeetupCog')

	meetup_channels = (400567035249033217, 362691852274630657)
	meetup_mention = '<@&487120797190848534>'

	x_emojis = ('❎', '❌', '✖️')
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

	rx_uw_bot_id = 489158438086115328

	url_pattern = '(https?:\\/\\/(?:www\\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\\.[^\\s]{2,}|www\\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\\.[^\\s]{2,}|https?:\\/\\/(?:www\\.|(?!www))[a-zA-Z0-9]\\.[^\\s]{2,}|www\\.[a-zA-Z0-9]\\.[^\\s]{2,})'

	def __init__(self, bot):
		self.bot = bot
		self.event_list = []

	def check_meetup_channel(ctx):
		return ctx.message.channel.id in (400567035249033217, 362691852274630657)

	def check_rx(ctx):
		return ctx.message.author.id == 136278937532628993

	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
		 	await ctx.send(f'That command is on cooldown. Please try after {int(error.retry_after) + 1} second(s).')

	async def on_reaction_add(self, reaction, user):
		for event in self.event_list:
			if event[0].id == reaction.message.id:
				if str(reaction.emoji) in self.x_emojis and user == event[1]:
					self.event_list.remove(event)
					await reaction.message.channel.send("❎ Event Deleted!", delete_after=5.0)
					await event[0].delete()
				elif str(reaction.emoji) in self.check_emojis and user == event[1]:
					self.event_list.remove(event)
					await reaction.message.channel.send("✅ Event Unpinned!", delete_after=5.0)
					await event[0].unpin()

	async def on_message_delete(self, message):
		if message.author.id == self.rx_uw_bot_id:
			for event in self.event_list:
				if event[0].id == message.id:
					self.event_list.remove(event)

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
		await ctx.author.send("I will ask you a few questions about your meetup. \nSay cancel or stop at any point to cancel.\n ")

		async with ctx.typing:
			try:
				for k,v in self.meetup_dict.items():
					await ctx.author.send(v)
					msg = await self.bot.wait_for('message', timeout=60.0, check=check)
					event[k] = msg 
					if msg.content.lower() in self.cancel_messages: raise asyncio.TimeoutError
				
			except asyncio.TimeoutError:
				await ctx.send(":thumbsdown:, Your request timed out")

			else:
				if is_url(event['location'].content) is not None:
					embed = discord.Embed(title=event['title'].content, url=event['location'].content, description=event['when_where'].content, color=0x00baa6)
				else:
					embed = discord.Embed(title=event['title'].content, description=event['when_where'].content, color=0x00baa6)
				
				embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
				embed.add_field(name='Type', value=event['type'].content, inline=True)
				embed.add_field(name='Time', value=event['time'].content, inline=True)
				embed.add_field(name='Activity', value=event['activity'].content, inline=True)
				embed.add_field(name='Cost', value=event['cost'].content, inline=True)
				embed.set_footer(text=event['description'].content)
				
				if ctx.message.channel.id == 400567035249033217:
					self.meetup_mention = '<@&489719429224071168>'
				elif ctx.message.channel.id == 362691852274630657:
					self.meetup_mention = '<@&487120797190848534>'

				embed_msg = await ctx.send('A new {} has appeared!'.format(self.meetup_mention), embed=embed)
				await embed_msg.pin()
				await embed_msg.add_reaction('👍')
				await embed_msg.add_reaction('👀')
				await embed_msg.add_reaction('👎')

				self.event_list.append((embed_msg, ctx.author))

				await ctx.author.send("Success!")
				await ctx.send("👍 Meetup successfully created! Add any X emoji to the message to delete the event. Add any check emoji to unpin the event.", delete_after=20.0)

				await ctx.message.delete()

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

def setup(bot):
	bot.add_cog(MeetupCog(bot))
