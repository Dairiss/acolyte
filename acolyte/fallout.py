from pathlib import Path
import os
import random

import discord
import markovify


class Fallout:
    """Иногда отвечает на сообщения игроков,
    используя цепи Маркова, построенные на файлах
    диалогов из Fallout 2.
    """

    def __init__(self, bot):
        self.bot = bot
        current_file = os.path.dirname(os.path.abspath(__file__))
        with open(Path(current_file).parent / 'data' / 'fallout.txt') as fallout_phrases:
            self.model = markovify.NewlineText(fallout_phrases.read(), state_size=3)

    async def on_message(self, message):
        cant_hold_it = random.randint(0, 50) // 50
        if cant_hold_it or self.bot.user.mentioned_in(message):
            phrase = self.model.make_sentence()
            phrase = phrase[0].lower() + phrase[1:]
            await self.bot.send_message(
                message.channel,
                f'{message.author.mention}, {phrase}'
            )

def setup(bot):
    bot.add_cog(Fallout(bot))
