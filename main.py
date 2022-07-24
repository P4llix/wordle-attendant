from Attendent import *


helper = Attendent()

if helper.word.list_size() == 0:
    exit()

helper.create_driver()
helper.prepare_board()

while True:
    if helper.result == 1:
        print('GG')
        helper.print_clear()
        helper.print_line("GG :D")
        break
    elif helper.result == -1:
        print('Game over')
        helper.print_clear()
        helper.print_line("Game over D:")
        break

    helper.watch()
    helper.summary()
    helper.propositions()
    helper.next_round()
