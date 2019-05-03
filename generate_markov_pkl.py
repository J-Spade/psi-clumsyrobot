# # # # #
# generate_markov_pkl.py
# v1.0.0 05/02/2019
# # # # #

from markov import Markov
import pickle

RAW_CHAT_LOG_LOCATION     = 'chat_logs.txt'
MARKOV_DATA_SAVE_LOCATION = 'markov_data.pkl'

print('opening raw chat logs...')
try:
    log_file = open(RAW_CHAT_LOG_LOCATION, 'r')
except IOError as e:
    print('could not open file. ({})'.format(str(e)))
    exit()

messages = log_file.readlines()
log_file.close()

markov = Markov()
print('found {} messages in log. digesting...'.format(len(messages)))
for message in messages:
    markov.DigestInput(message)

print('saving pickle...')
try:
    with open(MARKOV_DATA_SAVE_LOCATION, 'wb') as pickle_file:
        pickle.dump(markov.GetData(), pickle_file)
        pickle_file.close()
except IOError as e:
    print('could not save file. ({})'.format(str(e)))