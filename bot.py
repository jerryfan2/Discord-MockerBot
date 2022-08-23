import discord
from discord.ext import commands

import json

from random import choice

# load bot token from gitignore file
with open(".gitignore\config.json") as file:
    config = json.load(file)
token = config['token']

# initialize bot
intents = discord.Intents.all()

client = commands.Bot(command_prefix='%%', intents=intents)

@client.event
async def on_ready():
    print("Bot is ready.")


# randomizes capitalization of all characters in a given string
def mock_text(text):
    result = []
    for letter in text:
        letter_case = choice((0, 1))

        if letter_case == 0:
            result.append(letter.lower())
        else:
            result.append(letter.upper())

    return "".join(result)


# command for mocking users by applying mock function
@client.command()
async def mock(ctx, arg=None):
    try:
        # mocks user status
        if arg == "stat":
            for user_num, mention in enumerate(ctx.message.mentions):
                mocked = mock_text(f"{ctx.message.mentions[user_num].name} "
                                   f"is currently {ctx.message.mentions[user_num].status}")
                await ctx.send(mocked)
        # mocks user activities
        elif arg == "act":
            for user_num, mention in enumerate(ctx.message.mentions):
                for act_num, activity in enumerate(ctx.message.mentions[user_num].activities):
                    if ctx.message.mentions[user_num].activities[act_num].type == discord.ActivityType.listening:
                        text = mock_text(f"{ctx.message.mentions[user_num].name} "
                                         f"is listening to {ctx.message.mentions[user_num].activities[act_num].title} "
                                         f"on spotify")
                        await ctx.send(text)
                    elif ctx.message.mentions[user_num].activities[act_num].type == discord.ActivityType.playing:
                        text = mock_text(f"{ctx.message.mentions[user_num].name} "
                                         f"is playing {ctx.message.mentions[user_num].activities[act_num].name}")
                        await ctx.send(text)
                    elif ctx.message.mentions[user_num].activities[act_num].type == discord.ActivityType.streaming:
                        text = mock_text(f"{ctx.message.mentions[user_num].name} "
                                         f"is streaming {ctx.message.mentions[user_num].activities[act_num].name}")
                        await ctx.send(text)
        # mocks message replied to
        elif ctx.message.reference:
            msg_id = ctx.message.reference.message_id
            msg = await ctx.fetch_message(msg_id)
            text = msg.content
            mocked = mock_text(text)
            await ctx.send(mocked)
    except TypeError:
        pass

client.run(token)
