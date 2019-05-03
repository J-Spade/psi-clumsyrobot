# # # # #
# clumsyrobot.py
# v1.0.0 05/02/2019
# # # # #

from markov import Markov
from random import random
from os import environ
import pickle
try:
    import discord
except ImportError:
    print('ERROR: discord.py must be installed! (pip install -U discord.py)')
    exit()

# # # # #
# Constants
# # # # #

DISCORD_API_TOKEN         = environ.get('CLUMSYROBOT_DISCORD_TOKEN')
MESSAGES_PER_AUTOSAVE     = 25
RESPONSE_FREQUENCY        = 0.05
MARKOV_DATA_SAVE_LOCATION = 'markov_data.pkl'

# # # # #
# Discord client implementation
# # # # #

class ClumsyRobot(discord.Client):

    def __init__(self):
        # load the markov chain data
        print('*** Loading {}...'.format(MARKOV_DATA_SAVE_LOCATION))
        try:
            with open(MARKOV_DATA_SAVE_LOCATION, 'rb') as markov_file:
                self._markov = Markov(pickle.load(markov_file))
                markov_file.close()
        except IOError:
            print('*** Unable to load file!')
            self._markov = Markov()
        
        self._messages_since_last_autosave = 0
        super().__init__()

    # Connected as a discord client
    async def on_ready(self):
        print('*** Connected as {}.'.format(self.user))

    # Message received
    async def on_message(self, message):
        # don't respond to or learn from our own messages
        if message.author == self.user:
            return

        # learn and occasionally engage in discussion
        content = message.content.lower()
        self._markov.DigestInput(content)

        if random() < RESPONSE_FREQUENCY:
            response = self._markov.GenerateChain(content)
            await message.channel.send(response)

        # save the markov data sometimes
        self._messages_since_last_autosave += 1
        if self._messages_since_last_autosave == MESSAGES_PER_AUTOSAVE:
            print('*** Saving {}...'.format(MARKOV_DATA_SAVE_LOCATION))
            try:
                with open(MARKOV_DATA_SAVE_LOCATION, 'wb') as markov_file:
                    pickle.dump(self._markov.GetData(), markov_file)
                    markov_file.close()
                self._messages_since_last_autosave = 0
            except IOError:
                print('*** Unable to save file!')

# # # # #
# Startup/Initialization
# # # # #

print('*** Starting clumsyrobot...')
clumsy = ClumsyRobot()
clumsy.run(DISCORD_API_TOKEN)