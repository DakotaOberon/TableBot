import discord
from diceroller.diceroller import DiceRoller
from creds.creds import TOKEN

client = discord.Client()
Dice = DiceRoller()

@client.event
async def on_ready():
    print('{0.user} has logged in'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        await Dice.watch_roll(message)

client.run(TOKEN)
