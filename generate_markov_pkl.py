# # # # #
# generate_markov_pkl.py
# v1.1.0 05/11/2019
# # # # #

from markov import Markov
import pickle

RAW_CHAT_LOG_LOCATION     = 'lines.txt'
MARKOV_DATA_SAVE_LOCATION = 'markov_data.pkl'

print('opening raw chat logs...')
try:
    log_file = open(RAW_CHAT_LOG_LOCATION, 'r', encoding='utf-8', errors='replace')
except IOError as e:
    print('could not open file. ({})'.format(str(e)))
    exit()

messages = log_file.readlines()
log_file.close()

markov = Markov()
num_msgs = len(messages)
count = 0
print('found {} messages in log. digesting... '.format(num_msgs))
for message in messages:
    message = message.strip().lower()
    markov.DigestInput(message)
    count += 1
    print('\r... {} / {}'.format(count, num_msgs), end='')

print('\nsaving pickle...')
try:
    with open(MARKOV_DATA_SAVE_LOCATION, 'wb') as pickle_file:
        pickle.dump(markov.GetData(), pickle_file)
        pickle_file.close()
except IOError as e:
    print('could not save file. ({})'.format(str(e)))