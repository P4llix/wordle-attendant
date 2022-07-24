import json


class Word:
    def __init__(self):
        """
        Initialize variables.
        """
        self.__correct = ['_', '_', '_', '_', '_']
        self.__present = {}
        self.__absent = []
        self.__possible = []
        self.__list = self._load_list()
        self.completed = 0

    def __repr__(self):
        """
        Defines custom repr.
        """
        print("Correct: {}".format(''.join(self.__correct)))

        print("Present: ")
        for char in (self.__present):
            print("\t", char, ','.join(sorted(self.__present[char])))

        print("Absent: {}".format(' '.join(sorted(self.__absent))))

        return ""

    def list_size(self):
        """
        Returns size of loaded list.
        """
        return len(self.__list)

    def possible(self):
        """
        Returns possible words as array.
        """
        return self.__possible          

    def check(self, char, index, state):
        """
        Checks char and assign it to appropriate array.
        Also check if word is completed.
        """

        if state == 'correct':
            self.__correct[int(index)] = char

            if char in self.__present:
                if index in self.__present[char]:
                    if len(self.__present[char]) is 1:
                        self.__present.pop(char)
                    else:
                        self.__present[char].remove(index)

        elif state == 'present':
            if char not in self.__correct:
                if char not in self.__present:

                    self.__present[char] = [index]
                elif index not in self.__present[char]:
                    self.__present[char].append(index)

        elif state == 'absent':
            if all([char not in self.__absent,
                    char not in self.__correct,
                    char not in self.__present]):
                self.__absent.append(char)

        if self.__correct.count('_') is 0:
            self.completed = 1

    def _load_list(self):
        """
        Load prepeared list as object.
        """
        try:
            with open("assets/prepeared_list.json", "r") as in_file:
                return json.load(in_file)

        except FileNotFoundError:
            print("Missing file: 'prepeared_list.json'")
            return {}      

    def _exclude_char(self, char):
        """
        Excludes words containing specific char from possible words.
        """
        for i in self.__list[char]['present']:
            for word in self.__list[char]['present'][i]:
                if word in self.__possible:
                    self.__possible.remove(word)

    def _join_char(self, char, index):
        """
        Makes intersection of already possible words and array of new ones.
        """
        if len(self.__possible) == 0:
            self.__possible = self.__list[char]['index'][index]
            return

        temp = []
        for word in self.__possible:
            if word in self.__list[char]['index'][index]:
                temp.append(word)
        self.__possible = temp

    def _include_char(self, char, index):
        """
        Checks if array of possible words contain included chars.
        In case of none hitted chars takes words where char is present.
        """
        if len(self.__possible) == 0:
            for i in range(0, 5):
                if i != index:
                    for word in self.__list[char]['index'][str(i)]:
                        if word not in self.__possible:
                            self.__possible.append(word)

        else:
            temp = []
            for word in self.__possible:
                if char in word:
                    if char != list(word)[index]:
                        temp.append(word)
            self.__possible = temp

    def calculate_propositions(self):
        """
        Creates list of possible words by joinning,
        including and excluding already founded chars.
        """

        for index, char in enumerate(self.__correct):
            if char != '_':
                self._join_char(char, str(index))

        for char in self.__present:
            for index in self.__present[char]:
                self._include_char(char, int(index))

        for char in self.__absent:
            if char not in self.__correct:
                self._exclude_char(char)
