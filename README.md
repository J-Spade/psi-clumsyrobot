# psi-clumsyrobot
Radio PSI's favorite nonsense factory is back!

## Getting set up:
* clumsyrobot runs in Python 3 (and is incompatible with Python 2)
* clumsyrobot requires (discord.py)[https://github.com/Rapptz/discord.py], a Discord API wrapper for Python 3.
    * You can use `pip install -U discord.py` to install it locally.
* You will need to specify the Discord API bot token as an environment variable, `CLUMSYROBOT_DISCORD_TOKEN`.
    * (please don't hard-code it in the python script-- the internet doesn't need to see that)
    * See (the developer portal on discord)[https://discordapp.com/developers/applications/] for more information on bots/tokens
* I've included a simple script to convert raw chat lines from an existing chat log into a serialized markov data file (using pickle)
    * Change the path strings in the script to the right filenames and run it!
        * `python generate_markov_pkl.py`
    * NOTE: if the chat logs include usernames/timestamps, you might want to modify the script to parse those out first.

Once everything is properly set up, all you need to do is run the clumsyrobot script: `python clumsyrobot.py`

## Configuration:
The following values are all configurable as constants in `clumsyrobot.py`:
* `DISCORD_API_TOKEN`
    * The token the bot will use to authenticate with the Discord servers.
    * Seriously, though. Don't put the token on github. At least save it in a separate file and add that to `.gitignore`
* `MESSAGES_PER_AUTOSAVE`
    * The number of new messages clumsy will receive before backing up the markov data to disk.
    * Set this lower if you want to make sure as little is lost on a crash as possible.
    * Set this higher if you'd rather not write to disk all the time.
* `RESPONSE_FREQUENCY`
    * The probability that clumsyrobot will respond to any given message.
    * You probably don't want this set much higher than 0.05 (5%) -- what's endearing on occasion can get annoying with more frequency.
* `MARKOV_DATA_SAVE_LOCATION`
    * The path to the file where the serialized markov data should be saved.
    * For extra credit, occasionally copy this file so there's a backup!