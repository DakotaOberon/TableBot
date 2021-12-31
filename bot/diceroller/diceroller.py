import os
import random
import re
import math

import discord
from PIL import Image, ImageDraw, ImageFont

from module.module import Module


class Dice:
    '''Dice Object'''

    def __init__(self, size=64, x=0, y=0):
        self.size = size
        self.x = x
        self.y = y

class DiceRoller(Module):
    '''TableBots DiceRoller module'''

    # Set Defaults
    command_regex = ['^/r\d+d\d+$', '^/r\d+d\d+\+\d+$']

    image_resolution = 128
    dice_set = "default"
    max_resolution = 640

    max_cols = 10
    max_rows = 10

    dice_size = {
        "d2": Dice(64),
        "d4": Dice(40, y=8),
        "d6": Dice(64),
        "d8": Dice(32),
        "d10": Dice(32, y=8),
        "d12": Dice(32),
        "d20": Dice(16),
    }

    padding = (4, 4)

    def content(self, message):
        '''Retrieve content from Discord Message'''

        return message.content.replace(" ", "")

    def generate_message(self, number=1, dice=6, add=0):
        '''Generate message for reply'''

        total = 0
        rolls = []
        for x in range(0, number):
            # Roll dice and track rolls to display later
            roll = random.randrange(0, dice) + 1
            rolls.append(roll)
            total += roll

        content = f'Total: {total + add}'
        content = content + f' *({total} + {add})*' if (add) else content
        message = { "content": content }

        if (number > 100):
            return message
        else:
            dice_image = self.create_dice_image(f'd{dice}', rolls)
            tmp_filename = f'.\diceroller\images\\tmp\{number}_{dice}_{total}_{add}.png'
            dice_image.save(tmp_filename)
            message['file'] = discord.File(tmp_filename)

        return message

    async def run(self, message, content):
        content = content[2:]

        number = int(re.match("\d+", content).group(0))

        dice = int(re.search("d\d+", content).group(0)[1:])
        add =  int(re.search("\d+$", content).group(0)) if bool(re.search("\+", content)) else 0

        await message.reply(**self.generate_message(number, dice, add))

    def create_dice_image(self, dice, rolls):
        '''Create image file for dice rolls'''

        # Grab dice image
        dice_file = f'.\diceroller\images\dice\default\{dice}.png'
        if (not os.path.exists(dice_file)):
            dice_file = f'.\diceroller\images\dice\default\d6.png'

        # Grab dice specs
        dice_size = self.dice_size['d6']
        if (dice in self.dice_size):
            dice_size =  self.dice_size[dice]

        dice_image = Image.open(dice_file)

        number_of_rolls = len(rolls)

        # Get rows and columns
        columns = self.max_cols
        rows = 1
        if (number_of_rolls < self.max_cols):
            columns = number_of_rolls
        elif (number_of_rolls > self.max_cols):
            rows = math.ceil(number_of_rolls / self.max_cols)

        # Set dice resolution
        resolution = self.image_resolution
        div = 1
        if (number_of_rolls > 1):
            resolution = math.ceil(resolution / 2)
            div = 2

        # Get total padding
        total_padding = ((columns + 1) * self.padding[0], (rows + 1) * self.padding[1])

        # Create blank canvas
        size = (int(columns * resolution) + total_padding[0], int(rows * resolution) + total_padding[1])
        return_image = Image.new('RGBA', size)

        # Get dice width and height
        W, H = (resolution, resolution)

        # Create dice image at set width and height
        dice_image.thumbnail((W, H))
        font = ImageFont.truetype('.\diceroller\\fonts\DigitalDream.ttf', math.floor(dice_size.size / div))

        # Draw dice to canvas
        row = 0
        for i, r in enumerate(rolls):
            # Current position
            col = (i % columns)
            x = ((col) * resolution) + ((col + 1) * self.padding[0])
            y = (row * resolution) + ((row + 1) * self.padding[1])

            # Paste dice to canvas
            if (r == int(dice[1:])):
                highlight = self.highlight(dice_image, (0, 255, 0))
                return_image.paste(highlight, (x, y))
            elif (r == 1):
                highlight = self.highlight(dice_image, (255, 0, 0))
                return_image.paste(highlight, (x, y))
            else: 
                return_image.paste(dice_image, (x, y))
            
            # Write value onto dice
            draw = ImageDraw.Draw(return_image)
            w, h = draw.textsize(str(r), font=font)
            draw.text((x + ((W - w) / 2) + dice_size.x, y + ((H - h) / 2) + dice_size.y), str(r), font=font, fill=(0, 0, 0))

            if (col == 9):
                row += 1

        return return_image

    def highlight(self, img, color=(0, 255, 0)):
        '''Highlight the borders of an image'''
        return_img = img.copy()
        data = img.load()

        # Loop over each pixel in the image
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                # Get current values of pixel
                dr, dg, db, da = data[x, y]

                # Check if pixel is a border
                if ((dr < 200 and dg < 200 and db < 200)):
                    r, g, b = color
                    fill = (r, g, b, da)

                    return_img.putpixel((x, y), fill)

        return return_img
