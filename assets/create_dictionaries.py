import json
import os.path
from string import ascii_lowercase


CORE_FILE = 'english_all_words.txt'
FILES = [
    'english_words_5_length.json',
    'english_words_5_length_divided.json',
    'prepeared_list.json'
]


def _list_files():
    """
    Checks if files are in folder.
    Return number of missing files.
    """
    errors = 0
    for file in FILES:
        if os.path.isfile(file):
            print(f'File exists: {file}')
        else:
            print(f'File is missing {file}')
            errors += 1
    return errors


def selection_by_length():
    '''
    Chooses only 5 char long words from English dictionary.
    Creates 'english_words_5_length.json' file.
    '''
    try:
        with open(CORE_FILE, "r") as in_file, \
             open("english_words_5_length.json", "w") as out_file:

            result = {"5_length": []}

            for line in in_file:
                if len(line) == 6:
                    result["5_length"].append(line[:5])
            json.dump(result, out_file)
            print("Created file: 'english_words_5_length.json'")

    except FileNotFoundError:
        print(f"Missing file: '{CORE_FILE}'")


def divide_to_parts():
    '''
    Divides each word to 2 dictionaries.
    First dictionary contain number of characters.
    Second contain chars on specific position in word.
    Creates 'english_words_5_length_divided.json' file.
    '''
    try:
        with open("english_words_5_length.json", "r") as in_file, \
             open('english_words_5_length_divided.json', 'w') as out_file:

            in_file = json.load(in_file)
            result = {}

            for line in in_file["5_length"]:
                amount = {}
                index = {}
                result[line] = {
                    'char_amount': {},
                    'char_index': {}
                    }

                for id_char, char in enumerate(line):
                    if char not in amount:
                        amount[char] = 1
                    else:
                        amount[char] += 1

                    index[id_char] = char

                result[line]['char_amount'] = amount
                result[line]['char_index'] = index

            json.dump(result, out_file)
            print("Created file: 'english_words_5_length_divided.json'")

    except FileNotFoundError:
        print("Missing file: 'english_words_5_length.json'")


def create_dictionary():
    '''
    Creates list of words for every alphabet letter.
    First part contain index where letter occurs.
    Second part contain words where letter is present.
    Creates 'prepeared_list.json' file.
    '''
    try:
        with open("english_words_5_length_divided.json", "r") as in_file, \
             open('prepeared_list.json', 'w') as jsonFile:

            result = {}
            in_file = json.load(in_file)

            for alphabet_letter in ascii_lowercase:
                result[alphabet_letter] = {
                    "index": {
                        "0": [],
                        "1": [],
                        "2": [],
                        "3": [],
                        "4": []
                    },
                    "present": {
                        1: [],
                        2: [],
                        3: [],
                        4: [],
                        5: []
                    }
                }

                for word in in_file:
                    for index, char in in_file[word]["char_index"].items():
                        if alphabet_letter == char:
                            result[alphabet_letter]["index"][index].append(word)

                    for char, amount in in_file[word]['char_amount'].items():
                        if char == alphabet_letter:
                            result[alphabet_letter]["present"][amount].append(word)

            json.dump(result, jsonFile)
            print("Created file: 'prepeared_list.json'")

    except FileNotFoundError:
        print("Missing file: 'english_words_5_length_divided.json'")

if __name__ == "__main__":
    if not os.path.isfile(CORE_FILE):
        print('''
            Missing core file: '{}'
            Save site as txt file in folder
            https://tinyurl.com/4wk97ppe
                '''.format(CORE_FILE))

    else:
        if _list_files() != 0:
            print("Fixing files...")

            selection_by_length()
            divide_to_parts()
            create_dictionary()

            print("Inspectining...")
            _list_files()
