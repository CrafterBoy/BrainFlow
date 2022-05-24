from brainflow import board_shim, data_filter
import os
import time
import json
import threading
import pandas as pd
from datetime import datetime
import numpy as np


class Board:
    def __init__(self, com='COM3', board_id=2, sleep_time=.01):
        self.user = ''
        self.lote = 1
        self.action = ''
        self.collectingData = False
        self.sleep_time = sleep_time
        self.__serial_port = com
        self.__board_id = board_id
        self.__sampling_rate = board_shim.BoardShim.get_sampling_rate(self.__board_id)
        self.params = board_shim.BrainFlowInputParams()
        self.params.serial_port = self.__serial_port

        self.iterate = True
        self.dataFiltered = []

        self.__board = board_shim.BoardShim(self.__board_id, self.params)
        self.__board.prepare_session()
        self.__board.start_stream()

        # time.sleep(1.0)
        # self.start()
        
    def run(self) -> None:
        while self.iterate:
            data = self.__board.get_current_board_data(1)
            if len(data[0]) != 0 and self.collectingData:
                # print(f"{len(data)}: and {data}")
                timeStampData = data[30]
                dateTime_Str = datetime.fromtimestamp(timeStampData[0]).strftime("%Y-%m-%d %H:%M:%S")
                for sensor in range(0, 15):
                    data_filter.DataFilter.perform_bandpass(data[sensor], self.__sampling_rate, 0.5, 45.0, 2, data_filter.FilterTypes.BUTTERWORTH.value, 0)
                filtered_data = np.append([self.lote, self.user, time.time(), dateTime_Str, self.action],np.reshape(data, 32)[0:16])
                # print(np.reshape(data, 32))
                self.dataFiltered.append(filtered_data)
            time.sleep(self.sleep_time)

    def start(self) -> None:
        # launch thread
        hilo1 = threading.Thread(target=self.run, args=(), daemon=True)
        hilo1.start()

    def stop(self) -> None:
        self.iterate = False
        time.sleep(1.0)
        self.__board.stop_stream()
        self.__board.release_session()

    def __str__(self) -> str:
        return f"\nLote: {self.lote}, Usuario: {self.user}, Action: {self.action}\nRecogiendo datos({len(self.dataFiltered)} rows): {self.collectingData}"


