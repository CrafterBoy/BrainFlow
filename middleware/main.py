# importam els objectes
from BrainMenu import Menu
from MongoCli import Mongo
from PyBoard import Board
import time

# brazo derecha
# brazo izquierdo
# relajado
# musica
# hablar
# leer
# andar

# cream els objectes
mongo = Mongo(host="192.168.193.133", port=27017, dummy=False) # llevar dummy per development
board = Board()
menu = Menu(board=board, mongo=mongo)


# iniciam el board
board.start()

# inicim el menu
while True:
    value = menu.printMenu()
    menu.manageOption(value)
    if value == 6:
        break
            

quit()
