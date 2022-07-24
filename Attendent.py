from selenium import webdriver
from selenium.webdriver.common.by import By
from Word import *
from time import *


DATA_STATES_VALID = ['present', 'correct', 'absent']
SUGGESTIONS = """Try one of those:\\n" +
    "1.  CRANE\\n" +
    "2.  SLATE\\n" +
    "3.  CRATE\\n" +
    "4.  SLANT\\n" +
    "5.  TRACE\\n" +
    "6.  LANCE\\n" +
    "7.  CARTE\\n" +
    "8.  LEAST\\n" +
    "9.  TRICE\\n" +
    "10. ROAST"""
PRINT_NODE_STYLE ="""
    node.style.color = "#FFFFFF";
    node.style.background = "#050505";
    node.style.position = "absolute";
    node.style.left = 0;
    node.style.overflowY = "auto";
    node.style.margin = "10px";
    node.style.fontFamily = "monospace";
    node.style.width = "30%";
    node.style.height = "50%";
    """

class Attendent:
    def __init__(self):
        """
        Initialize.
        """
        self.round = 1
        self.result = 0
        self.word = Word()

    def create_driver(self):
        '''
        Creates Driver.
        '''
        driver = webdriver.Firefox(service_log_path='nul')
        driver.get("https://www.nytimes.com/games/wordle/index.html")
        self.driver = driver

    def _create_print_node(self):
        """
        Prepares node on site to printing text.
        """
        script = """var node = document.createElement("div");
                node.setAttribute("id", "print_node");
                document.getElementById("wordle-app-game").appendChild(node);
                """
        self.driver.execute_script(script + PRINT_NODE_STYLE)

    def print_line(self, txt):
        """
        Pushes text to already created node on site.
        """
        script = f'document.getElementById("print_node").innerText += "{txt}";'
        self.driver.execute_script(script)

    def print_clear(self):
        """
        Clears text in node on site.
        """
        script = "document.getElementById('print_node').innerText = '';"
        self.driver.execute_script(script)

    def prepare_board(self):
        '''
        Clears Pop-ups and notifications.
        Prints suggested openers.
        '''

        __popups_xpaths = [
            ["Banner", "//*[@id='pz-gdpr-btn-closex']"],
            ["Instructions", "/html/body/div/div[3]/div/div"]
        ]

        while len(__popups_xpaths) != 0:
            for xpath in __popups_xpaths:
                try:
                    element = self.driver.find_element(By.XPATH, xpath[1])
                    element.click()
                    __popups_xpaths.remove(xpath)
                except Exception as error:
                    print("'{}' can't be clearned, due to {}"
                          .format(xpath[0], error))
                    sleep(0.5)

        print("Board: Up & Ready!\n")
        self._create_print_node()
        self.print_line(SUGGESTIONS)

    def next_round(self):
        """
        Increments round counter.
        """
        self.round += 1

    def _get_tiles(self):
        """
        Locates, scraps and saves all tiles from website as array.
        """
        tiles = []
        for i in range(1, 6):
            tiles.append(
                self.driver.find_elements(
                    By.XPATH,
                    "/html/body/div/div[1]/div/div[{}]/div[{}]/div"
                    .format(self.round, i)
                    )
                )
        return tiles

    def get_tile(self, number):
        """
        Returns specific tile in current round.
        """
        return self._get_tiles()[number-1][0]

    def watch(self):
        """
        Loop that checks if user approved word.
        """
        while self.get_tile(5).get_attribute('data-state')\
                not in DATA_STATES_VALID:
            sleep(0.5)

    def summary(self):
        """
        Pushes chars from tiles to processing.
        Checks if game is over.
        """
        for i in range(1, 6):
            tile = self.get_tile(i)
            self.word.check(tile.text.lower(),
                            str(i-1),
                            tile.get_attribute('data-state'))

        if self.word.completed:
            self.result = 1
        elif self.round == 6:
            self.result = -1

    def propositions(self):
        """
        Calculates possible words and prints them in node on site.
        """
        print("Round ", self.round)
        print(repr(self.word))

        self.word.calculate_propositions()
        self.print_clear()

        if len(self.word.possible()) > 0:
            self.print_line(" ".join(self.word.possible()))
        else:
            self.print_line(SUGGESTIONS)
