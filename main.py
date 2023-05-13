import requests
# from sqlalchemy import create_engine
import pyodbc
import pandas as pd
# import os
import urllib.parse
import numpy as np


def check_for_table(conn, table_name, names):
    cursor = conn.cursor()
    names = [name.replace(" ", "_") for name in names]
    names = " varchar(255),\n".join(names) + " varchar(255)"
    # check if the table exists
    if cursor.tables(table=table_name, tableType='TABLE').fetchone():
        # query = f"DROP TABLE {table_name}"
        # cursor.execute(query)
        return
    # create the table if it does not exist
    query = f"CREATE TABLE {table_name} ({names})".format(
            names = names
        )

    print(query)
    cursor.execute(query)
    print(f"Table {table_name} created successfully.")

    # close the cursor and connection
    cursor.close()
    return

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    server = 'DESKTOP-0E91BGO'
    database = 'HDiSBI_projekt'
    username = 'sa'
    password = 'AnhLinh24072001'
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    # Nawiązanie połączenia do bazy danych
    conn = pyodbc.connect(connection_string)

    apikey = '9e511e7a-be05-47fe-a578-34190f4bfe2c'

    df = pd.read_csv('listaprzystankow.csv', index_col=0)
    df = df.drop(columns = ['Przystanek'])
    df.columns = ['nazwa']
    df['numer'] = df['nazwa'].apply(lambda x: x.strip(" ").split(" ")[-1])
    df['nazwa'] = df['nazwa'].apply(lambda x: x[:-5])
    # print(np.unique(df['numer']))
    df = df[:50]


    # API ENDPOINT 1
    zespoly = []
    for nazwaprzystanku in np.unique(df['nazwa']):

        url1 = 'https://api.um.warszawa.pl/api/action/dbtimetable_get?id=b27f4c17-5c50-4a5b-89dd-236b282bc499&name=' + nazwaprzystanku + '&apikey=' + apikey

        response = requests.get(url1)
        if response.status_code == 200:
            # Odpowiedź jest udana, można przetwarzać dane
            data = response.json()  # Jeśli odpowiedź jest w formacie JSON

        dictionaries = []
        for i in range(len(data['result'])):
            dictionary = {}
            for j in range(len(data['result'][i]['values'])):
                # print(data['result'][i]['values'][j]['key'], data['result'][i]['values'][j]['value'])
                c = data['result'][i]['values'][j]['key']
                v = data['result'][i]['values'][j]['value']
                dictionary[c] = v
            dictionaries.append(dictionary)
        df1 = pd.DataFrame(dictionaries)
        if len(dictionaries) == 0:
            continue
        zespoly += list(df1['zespol'])

        check_for_table(conn, 'test1', df1.columns)
        cursor = conn.cursor()
        # Insert Dataframe into SQL Server:
        for index, row in df1.iterrows():
            cursor.execute("INSERT INTO test1 (Zespol,Nazwa) values(?,?)",
                           (row.zespol, row.nazwa))
        conn.commit()
        cursor.close()


    # API ENDPOINT 2
    for busstopId in zespoly:
        for busstopNr in np.unique(df['numer']):
    # busstopId = str(7009)  # 7009
    # busstopNr = "01"  # 01

            url2 = 'https://api.um.warszawa.pl/api/action/dbtimetable_get?id=88cd555f-6f31-43ca-9de4-66c479ad5942&busstopId=' + busstopId + '&busstopNr=' + busstopNr + '&apikey=' + apikey

            response = requests.get(url2)
            if response.status_code == 200:
                # Odpowiedź jest udana, można przetwarzać dane
                data = response.json()  # Jeśli odpowiedź jest w formacie JSON

            dictionaries2 = []
            for i in range(len(data['result'])):
                dictionary2 = {"stop id": busstopId,
                              "stop nr": busstopNr}
                for j in range(len(data['result'][i]['values'])):
                    # print(data['result'][i]['values'][j]['key'], data['result'][i]['values'][j]['value'])
                    c = data['result'][i]['values'][j]['key']
                    v = data['result'][i]['values'][j]['value']
                    dictionary2[c] = v
                dictionaries2.append(dictionary2)
            if len(dictionaries2) == 0:
                continue
            df2 = pd.DataFrame(dictionaries2)
            check_for_table(conn, 'test2', df2.columns)

            cursor = conn.cursor()
            # Insert Dataframe into SQL Server:
            for index, row in df2.iterrows():
                cursor.execute("INSERT INTO test2 (stop_id, stop_nr, linia) values(?,?,?)",
                               (row['stop id'], row['stop nr'], row.linia))
            conn.commit()
            cursor.close()

            # API ENDPOINT 3
            for index, row in df2.iterrows():
                busstopid = row['stop id']
                busstopnr = row['stop nr']
                linia = row['linia']

                url3 = 'https://api.um.warszawa.pl/api/action/dbtimetable_get?id=e923fa0e-d96c-43f9-ae6e-60518c9f3238&busstopId=' + str(
                    busstopid) + '&busstopNr=' + busstopnr + '&line=' + str(linia) + '&apikey=' + apikey

                response = requests.get(url3)
                if response.status_code == 200:
                    # Odpowiedź jest udana, można przetwarzać dane
                    data = response.json()  # Jeśli odpowiedź jest w formacie JSON

                dictionaries3 = []
                for i in range(len(data['result'])):
                    dictionary3 = {'stop id': busstopid,
                                  "stop nr": busstopnr,
                                  'linia': linia}
                    for j in range(len(data['result'][i]['values'])):
                        # print(data['result'][i]['values'][j]['key'], data['result'][i]['values'][j]['value'])
                        c = data['result'][i]['values'][j]['key']
                        v = data['result'][i]['values'][j]['value']
                        dictionary3[c] = v
                    dictionaries3.append(dictionary3)
                if len(dictionaries3) == 0:
                    continue
                df3 = pd.DataFrame(dictionaries3)

                check_for_table(conn, 'test3', df3.columns)

                cursor = conn.cursor()
                # Insert Dataframe into SQL Server:
                for index, row in df3.iterrows():

                    cursor.execute("INSERT INTO test3 (stop_id,	stop_nr, linia, symbol_2, symbol_1, brygada, kierunek, trasa, czas) values(?,?,?,?,?,?,?,?,?)",
                                   (row['stop id'], row['stop nr'], row.linia, row.symbol_2, row.symbol_1, row.brygada, row.kierunek, row.trasa, row.czas))
                conn.commit()
                cursor.close()
    conn.close()





