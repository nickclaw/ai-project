import re

punctuation_pattern = r"\,|\.|\?|\!|\;|\:"
case_map = {
    'i': 'you',
    'me': 'you',
    'you': 'me',
    'my': 'your',
    'your': 'my',
    'yours': 'mine',
    'mine': 'yours',
    'am': 'are',
    "are": "am",
    "get": "got",
    "did": "do"
}


'''Returns a string without any punctuation.'''
def remove_punctuation(string):
    return re.sub(punctuation_pattern, '', string).lower()


'''Returns a list of words with no punctuation'''
def to_wordlist(string):
    string = re.split(punctuation_pattern, string)[0]
    return re.split("\s", remove_punctuation(string))


def invert(wordlist):
    wordlist = wordlist[:]
    for i in range(len(wordlist)):
        word = wordlist[i]
        if word in case_map: wordlist[i] = case_map[word]

    return wordlist