import os
import pandas as pd
from datetime import datetime
from pymongo import MongoClient


class Mongo:
    def __init__(self, host="192.168.193.133", port=27017, dummy=False) -> None:
        self.__dummy = dummy
        self.__client = MongoClient(
            host=host,
            port=port,
            connect=True
        )

        self.__db = self.__client['OpenBCI']
        self.__brainflow_collection = self.__db['brainflow']

    def save_pandas_dataset(self, dataframe) -> None:
        # df = pd.DataFrame(dataFiltered, columns=getColumns())
        if not self.__dummy:
            self.__brainflow_collection.insert_many(dataframe.to_dict(orient='records'))

    def save_list_dataset(self, dataFiltered) -> None:
        df = pd.DataFrame(dataFiltered, columns=self.getColumns())
        if not self.__dummy:
            self.__brainflow_collection.insert_many(df.to_dict(orient='records'))

    def close(self):
        self.__client.close()


    @classmethod
    def getColumns(self):
        columnas = []
        columnas.append("lote")
        columnas.append("user")
        columnas.append("timestamp")
        columnas.append("datetime")
        columnas.append("action")
        for i in range(1,17):
            columnas.append("sensor"+str(i))
        return columnas

    @classmethod
    def generate_csv(df):
        if not os.path.exists('Backup'):
            os.makedirs('Backup')
        now = datetime.now()
        df.to_csv(f'./Backup/{now.strftime("%Y%m%d_%H%M%S")}.csv', index=True)

