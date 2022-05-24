
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, DetrendOperations, FilterTypes
import os
import time
import json
import threading
import pandas as pd
from datetime import datetime
import numpy as np
from pymongo import MongoClient


class Menu:
    def __init__(self, board, mongo):
        self.__board = board
        self.__mongo = mongo
        self.__validActions = ['brazo derecho',
                            'brazo izquierdo',
                            'relajado',
                            'musica',
                            'hablar',
                            'leer',
                            'andar']
        

    def printStatus(self):
        print(self.__board)
        print()
    
    def printMenu(self):
        self.printStatus()
        print("Que opcion quieres?\n")
        print("1 - Cambiar lote")
        print("2 - Cambiar Usuario")
        print("3 - Cambiar Accion")
        print("4 - Activar/Parar Recoleccion de datos")
        print("5 - Parar sin guardar/Reiniciar datos")
        print("6 - Salir  \n")
        while True:
            try:
                return int(input("Opcion: "))
            except ValueError as ve:
                print("Invalid input.")
                continue

    def manageSettings(self, option, value):
        if option == 1:
            self.__board.lote = int(value)
        if option == 2:
            self.__board.user = value
        if option == 3:
            if value in self.__validActions:
                self.__board.action = value
            else:
                print("\nAction not allowed. Valid actions are:")
                print(*self.__validActions, sep = ", ")
        


    def manageOption(self, option):
        if option in [1, 2, 3]:
            if self.__board.collectingData:
                print("\nCannot change settings while fetching data\n")
                return
            if (option == 3):
                print(f"Allowed actions: {', '.join(self.__validActions)}")
            value = input("New value: ")
            self.manageSettings(option, value)
        if option == 4:
            if self.__board.collectingData:
                self.__mongo.save_list_dataset(self.__board.dataFiltered)
            else:
                self.__board.lote += 1
            self.__board.collectingData = not self.__board.collectingData
            self.__board.dataFiltered = []
        if option == 5:
            self.__board.collectingData = False
            self.__board.dataFiltered = []
        if option == 6:
            if len(self.__board.dataFiltered):
                val = input(f"Hay {len(self.__board.dataFiltered)} registros sin guardar.\nQuieres guardar antes de salir? [Y/n]:")
                if val in ['yes', 'y', 'YES', 'Y']:
                    self.__mongo.save_list_dataset(self.__board.dataFiltered)
            self.__mongo.close()
            self.__board.stop()

# opcion = 0
#brain = BrainFlow()
#while opcion != 6:
#    opcion = brain.printMenu()
#    brain.manageOption(opcion)