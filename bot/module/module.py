import re

class Module():
    command_regex = ['/']

    def content(self, message):
        '''Retrieve content from Discord Message'''

        return message.content.replace(" ", "")

    async def watch_roll(self, message):
        '''Watch for roll command'''
        content = self.content(message)

        for x in self.command_regex:
            if (bool(re.match(x, content))):
                await self.run(message, content)
                return

    async def run(self, message, content):
        return
