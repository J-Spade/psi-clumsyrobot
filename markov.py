# # # # #
# markov.py
# v0.0.1 12/21/2018
# # # # #

import random
import copy
import math
import pickle

# internally-used delimiter marking the start or end of a chain
_ENDPOINT = '__#END#__'

# template for data structure containing Markov chain data
# under the hood, this is "just" a dictionary
_DATA_TEMPLATE =    {
                        _ENDPOINT:               # keyword
                        (                           
                            [                    # preceding in chain
                                (_ENDPOINT, 1)   # (value, count)
                            ],
                            [                    # following in chain
                                (_ENDPOINT, 1)   # (value, count)
                            ]
                        )
                    }

class Markov:
# A class representing a collection of Markov chain data.
#
# All data is assumed to be strings; other data types must be serialized as strings
# in order to be used in Markov operations.

    class _MarkovData:
    # Internal class used by Markov to maintain the Markov chain data.

        def __init__(self, init_data):
            # Markov class passes in DATA_TEMPLATE if no data is provided by the user.
            self._data = copy.deepcopy(init_data)

            # initialize key counts
            self._keycounts = {}
            for key in self._data.keys():
                keycount = 0
                # (any time a key is digested, it adds one more preceding value)
                for value in self.GetPrecedingValues(key):
                    keycount += value[1]
                self._keycounts[key] = keycount

        def _ValueListIndex(self, value, list):
        # Return the index of the value in the list.
        # Returns -1 if the value is not in the list.
            for index in range (0, len(list)):
                if list[index] == value:
                    return index
            return -1

        def KeyCount(self, key):
        # Return the number of times the provided key was digested.
            if key in self._keycounts:
                return self._keycounts[key]
            else:
                return 0

        def GetPrecedingValues(self, key):
        # Gets the list of preceding values and counts for a given key in the structure.
        # Returns an empty list if the key does not exist.
            if key in self._data:
                return self._data.get(key)[0]
            else:
                return []

        def GetFollowingValues(self, key):
        # Gets the list of following values and counts for a given key in the structure.
        # Returns an empty list if the key does not exist.
            if key in self._data:
                return self._data.get(key)[1]
            else:
                return []

        def AddKeyPair(self, firstkey, secondkey):
        # Adds two sequential keys from a chain into the data structure, and increments value counts.
        # Assumes firstkey is a valid key in the structure, but adds secondkey if necessary.
            if firstkey not in self._data:
                return False

            # add secondkey as a following value for firstkey
            after_first = self.GetFollowingValues(firstkey)

            index = self._ValueListIndex(firstkey, after_first)
            if index == -1:
                after_first.append( (secondkey, 1) )
            else:
                oldcount = after_first[index][1]
                after_first[index] = (secondkey, oldcount + 1)

            # add firstkey as a preceding value for secondkey
            before_second = self.GetPrecedingValues(secondkey)

            if len(before_second) == 0:
                self._data[secondkey] = ([(firstkey, 1)],[])
            else:
                index = self._ValueListIndex(firstkey, before_second)
                if index == -1:
                    before_second.append( (firstkey, 1) )
                else:
                    oldcount = before_second[index][1]
                    before_second[index] = (firstkey, oldcount + 1)

            # increment keycounts
            if firstkey in self._keycounts:
                oldcount = self._keycounts[firstkey]
                self._keycounts[firstkey] = oldcount + 1
            else:
                self._keycounts[firstkey] = 1

            if secondkey in self._keycounts:
                oldcount = self._keycounts[secondkey]
                self._keycounts[secondkey] = oldcount + 1
            else:
                self._keycounts[secondkey] = 1

            return True

        def GetDataCopy(self):
        # return a copy of the data structure
            return copy.deepcopy(self._data)

    def __init__(self, init_data = _DATA_TEMPLATE):
        # Create internal data structure.
        self._markovdata = Markov._MarkovData(init_data)

    def _RandomFromWeightedValues(self, values):
    # Randomly chooses a value from a list containing values and their associated counts.
        total = 0
        stops = []
        for key in values:
            total = total + key[1]
            stops.append(total)
        
        rand = random.randint(0, total)
        for index in range(0, len(values)):
            if rand <= stops[index]:
                return values[index][0]

        return values[0][0]

    def _TF_IDF(self, key, keys):
    # Analysis metric intended to determine the relative importance of a key to a chain.
        count = 0
        for k in keys:
            if k == key:
                count += 1

        tf = float(count)/len(keys)
        idf = math.log(float(self._markovdata.KeyCount(_ENDPOINT)) / self._markovdata.KeyCount(key))

        return tf * idf

    def DigestInput(self, input, delimiter=' '):
    # Pulls a chain of keys apart and processes it into the internal Markov data structure.
    # It is assumed that the chain is a string.
        keys = input.split(delimiter)

        # put _ENDPOINT on either end
        keys.insert(0, _ENDPOINT)
        keys.append(_ENDPOINT)

        # Add all the keys to the structure
        for index in range (0, len(keys) - 1):
            self._markovdata.AddKeyPair(keys[index], keys[index + 1])

    def GenerateChain(self, input, delimiter=' '):
    # Creates a new chain using an input chain as a starting reference.
    # For best results, the user should always call DigestChain() on the input first.
    # It is assumed that the input is a string
        keys = input.split(delimiter)

        # try to determine which key is the "most relevant"
        seed = _ENDPOINT
        relevance = 0
        for key in keys:
            if self._markovdata.KeyCount(key) > 0:
                tf_idf = self._TF_IDF(key, keys)
                if tf_idf > relevance:
                    relevance = tf_idf
                    seed = key

        # start building the chain from the seed key
        chain = seed

        # work forwards until the end of the chain
        next = self._RandomFromWeightedValues(self._markovdata.GetFollowingValues(seed))
        while next != _ENDPOINT:
            chain = chain + delimiter + next
            next = self._RandomFromWeightedValues(self._markovdata.GetFollowingValues(next))

        # work backards until the start of the chain
        next = self._RandomFromWeightedValues(self._markovdata.GetPrecedingValues(seed))
        while next != _ENDPOINT:
            chain = next + delimiter + chain
            next = self._RandomFromWeightedValues(self._markovdata.GetPrecedingValues(next))

        return chain

    def GetData(self):
    # Get a copy of the markov chain data structure.
        return self._markovdata.GetDataCopy()