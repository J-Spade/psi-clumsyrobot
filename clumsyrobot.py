# # # # #
# clumsyrobot.py
# v1.1.1 05/11/2019
# # # # #

from markov import Markov
from random import random
import pickle
try:
    import discord
except ImportError:
    print('ERROR: discord.py must be installed! (pip install -U discord.py)')
    exit()

# # # # #
# Config values
# # # # #

# read the config file
CONFIG_FILE_NAME = 'clumsyrobot.cfg'
print('*** Loading config data from {}...'.format(CONFIG_FILE_NAME))
try:
    config_file = open(CONFIG_FILE_NAME, 'r')
except IOError:
    print('*** Could not load config file!')
    exit()

# parse the config data
try:
    config = {}
    for line in config_file.readlines():
        var, val = line.split('=')
        config[var.strip()] = val.strip()
    config_file.close()
except ValueError:
    print('*** Malformed config file!')
    exit()

# DISCORD_API_TOKEN: bot token used to authenticate with Discord API
try:
    DISCORD_API_TOKEN = str(config['DISCORD_API_TOKEN'])
except KeyError:
    print('*** No DISCORD_API_TOKEN value specified in config file! Cannot connect to Discord!')
    exit()
except TypeError:
    print('*** DISCORD_API_TOKEN value in config file is malformed! Cannot connect to Discord!')
    exit()

# MESSAGES_PER_AUTOSAVE: messages received before backing up markov data
try:
    MESSAGES_PER_AUTOSAVE = int(config['MESSAGES_PER_AUTOSAVE'])
except KeyError:
    print('No MESSAGES_PER_AUTOSAVE value specified in config file. Using default.')
    MESSAGES_PER_AUTOSAVE = 25
except TypeError:
    print('*** MESSAGES_PER_AUTOSAVE value in config file is malformed!')
    exit()

# RESPONSE_FREQUENCY: probability that clumsy will respond to any given message
try:
    RESPONSE_FREQUENCY = float(config['RESPONSE_FREQUENCY'])
except KeyError:
    print('No RESPONSE_FREQUENCY value specified in config file. Using default.')
    RESPONSE_FREQUENCY = 0.05
except TypeError:
    print('*** RESPONSE_FREQUENCY value in config file is malformed!')
    exit()

# MARKOV_DATA_SAVE_LOCATION: path to the file where the serialized markov data is saved
try:
    MARKOV_DATA_SAVE_LOCATION = str(config['MARKOV_DATA_SAVE_LOCATION'])
except KeyError:
    print('No MARKOV_DATA_SAVE_LOCATION value specified in config file. Using default.')
    MARKOV_DATA_SAVE_LOCATION = 'markov_data.pkl'
except TypeError:
    print('*** MARKOV_DATA_SAVE_LOCATION value in config file is malformed!')
    exit()

# # # # #
# Discord client implementation
# # # # #

class ClumsyRobot(discord.Client):

    def __init__(self):
        # load the markov chain data
        print('*** Loading markov data from {}...'.format(MARKOV_DATA_SAVE_LOCATION))
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
            print('*** Saving markov data to {}...'.format(MARKOV_DATA_SAVE_LOCATION))
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