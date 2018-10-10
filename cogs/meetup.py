meetup_channels = (400567035249033217, 362691852274630657)
meetup_mention = '<@&487120797190848534>'

x_emojis = ['❎', '❌', '✖️']
check_emojis = ['☑️', '✔️', '✅']

cancel_messages = ['cancel', 'stop']

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

event_list = []

def check_meetup_channel(ctx):
	return ctx.message.channel.id in meetup_channels

@bot.event
async def on_reaction_add(reaction, user):
	for event in event_list:
		if event[0].id == reaction.message.id:
			if str(reaction.emoji) in x_emojis and user == event[1]:
				event_list.remove(event)
				await reaction.message.channel.send("❎ Event Deleted!", delete_after=5.0)
				await event[0].delete()
			elif str(reaction.emoji) in check_emojis and user == event[1]:
				event_list.remove(event)
				await reaction.message.channel.send("✅ Event Unpinned!", delete_after=5.0)
				await event[0].unpin()

@bot.event
async def on_message_delete(message):
	if message.author.id == rx_uw_bot_id:
		for event in event_list:
			if event[0].id == message.id:
				event_list.remove(event)

@bot.command()
@commands.cooldown(rate=1,per=120,type=commands.BucketType.user)
@commands.check(check_meetup_channel)
@commands.has_any_role('meetup', 'Mods', 'Admins')
async def meetup(ctx):
	event = {}
	bot_messages = []

	def check(msg):
		return msg.author == ctx.author and msg.channel.id in meetup_channels

	def is_url(url):
		prog = re.compile(url_pattern)
		return prog.search(url)

	def append_embed(qid, question):
		bot_messages.append(await ctx.send(question, delete_after=60.0))
		msg = await bot.wait_for('message', timeout=60.0, check=check)
		event[qid] = msg 
		if msg in cancel_messages: raise asyncio.TimeoutError

	try:
		for k,v in meetup_dict:
			append_embed(k,v)
		
	except asyncio.TimeoutError:
		await ctx.send(":thumbsdown:, Your request timed out", delete_after=15.0)

		for key, msg in event.items():
			await msg.delete()

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
			meetup_mention = '<@&489719429224071168>'
		elif ctx.message.channel.id == 362691852274630657:
			meetup_mention = '<@&487120797190848534>'

		embed_msg = await ctx.send('A new {} has appeared!'.format(meetup_mention), embed=embed)
		await embed_msg.pin()
		await embed_msg.add_reaction('👍')
		await embed_msg.add_reaction('👀')
		await embed_msg.add_reaction('👎')

		event_list.append((embed_msg, ctx.author))

		await ctx.send("👍 Meetup successfully created! Add any X emoji to the message to delete the event. Add any check emoji to unpin the event.", delete_after=10.0)

		for key, msg in event.items():
			await msg.delete()

		for msg in bot_messages:
			await msg.delete()

		await ctx.message.delete()