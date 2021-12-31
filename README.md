# TableBot
A Discord bot that helps optimize tabletop gameplay through the use of chat commands

### Currently Implemented
- Dice Roller
 - Users roll dice, the bot responds with an image of the results along with a calculated total
 - Command regex `['^/r\d+d\d+$', '^/r\d+d\d+\+\d+$']`

### To Be Implemented
- Dungeons
 - Quickly generate dungeons within disord to use on your tabletop adventures
- Combat Tracker
 - Keep track of combat related stats like health, initiative, and status effects.
- Character Keeper
 - Store your character data, such as inventory, feats, and spells.

### Python environments used
- discord.py
- Pillow

### Create bot with this code
- Create folder and file within the /bot folder named /creds/creds.py
 - This is how your bot will communicate with Discord API

- Add the following content to the newly created file
```
TOKEN = 'TOKEN_ID_FROM_DISCORD_API_HERE'
```
