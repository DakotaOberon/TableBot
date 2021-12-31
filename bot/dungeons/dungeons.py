from module.module import Module


class Tile:
    def __init__(self, texture='blank'):
        self.texture = texture

class Dungeons(Module):
    command_regex = ['^/dungeon\d+x\d+$', '^/dungeon']

    async def run(self, message, content):
        return

    def generate_dungeon(self, width, height):
        dungeon = self.blank_dungeon()

    def blank_dungeon(self, width, height):
        dungeon = []

        for i in range(0, width):
            dungeon.append([])
            for j in range(0, height):
                dungeon[i].append(Tile())
