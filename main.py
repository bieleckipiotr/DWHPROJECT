import requests
# from sqlalchemy import create_engine
import pyodbc
import pandas as pd
# import os
import urllib.parse


def zapytanie(url):
    # Przykładowe zapytanie do API Warszawy
    response = requests.get(url)

    # Sprawdzenie poprawności odpowiedzi
    if response.status_code == 200:
        # Odpowiedź jest udana, można przetwarzać dane
        data = response.json()  # Jeśli odpowiedź jest w formacie JSON
        return data

    else:
        # Odpowiedź nie jest udana, obsłuż błąd
        print('Wystąpił błąd podczas komunikacji z API')
        return None

def migracja(url):
    # Konfiguracja połączenia do bazy danych SQL Server
    server = 'DESKTOP-0E91BGO'
    database = 'HDiSBI_projekt'
    username = 'sa'
    password = 'AnhLinh24072001'
    # connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    # Nawiązanie połączenia do bazy danych
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Pobranie danych z API
    # response = requests.get('adres_api')
    # data = response.json()
    data = zapytanie(url)

    if data is not None:
        # Wstawienie danych do tabeli w bazie danych
        for element in data['result']:
            v = element['values']
            keys = []
            values = []

            for d in v:
                keys.append(d['key'])
                values.append(f"'{d['value']}'")

            placeholder_columns = ", ".join(keys)
            placeholder_values = ", ".join(values)

            # Przygotowanie zapytania SQL wstawiającego dane do tabeli
            query = f"INSERT INTO test ({placeholder_columns}) VALUES ({placeholder_values})".format(
                placeholder_columns = placeholder_columns,
                placeholder_values = placeholder_values
            )
            print(query)
            cursor.execute(query)
            conn.commit()

    # Zamknięcie połączenia
    cursor.close()
    conn.close()


def csv_to_sql(path):
    df = pd.read_csv(path, index_col=0)
    df = df.drop(columns = ['Przystanek'])
    df.columns = ['nazwa']
    # print(df['nazwa'][2].strip(" ").split(" "))
    df['numer'] = df['nazwa'].apply(lambda x: x.strip(" ").split(" ")[-1])
    df['nazwa'] = df['nazwa'].apply(lambda x: x[:-5])




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    csv_to_sql('listaprzystankow.csv')
    apikey = '9e511e7a-be05-47fe-a578-34190f4bfe2c'

    print('Typ wywolania:\n\t1 - pobranie zespołu przystanków\n\t2 - pobranie linii dostępnych na przystanku\n\t3 - pobranie rozkładu jazdy dla linii')
    wywolanie = int(input())

    if wywolanie == 1:
        print('--Pobranie zespołu przystanków--')

        print('Nazwa przystanku:')
        nazwaprzystanku = str(input())     # Marsza%C5%82kowska
        nazwaprzystanku = urllib.parse.quote(nazwaprzystanku)

        url = 'https://api.um.warszawa.pl/api/action/dbtimetable_get?id=b27f4c17-5c50-4a5b-89dd-236b282bc499&name=' + nazwaprzystanku + '&apikey=' + apikey

    elif wywolanie == 2:
        print('--Pobranie linii dostępnych na przystanku--')

        print('ID przystanku:')
        busstopId = str(input())     # 7009

        print('Numer przystanku:')
        busstopNr = str(input())     # 01
        url = 'https://api.um.warszawa.pl/api/action/dbtimetable_get?id=88cd555f-6f31-43ca-9de4-66c479ad5942&busstopId=' + busstopId + '&busstopNr=' + busstopNr + '&apikey=' + apikey
    else:
        print('--Pobranie rozkładu jazdy dla linii--')

        print('ID przystanku:')
        busstopId = str(input())     # 7009

        print('Numer przystanku:')
        busstopNr = str(input())     # 01

        print('Linia autobusowa:')
        line = str(input())     # 523

        url = 'https://api.um.warszawa.pl/api/action/dbtimetable_get?id=e923fa0e-d96c-43f9-ae6e-60518c9f3238&busstopId=' + busstopId + '&busstopNr=' + busstopNr + '&line=' + line + '&apikey=' + apikey

    data = zapytanie(url)
    print(*data['result'], sep='\n')
    # # print(*data['result']['values'], sep='\n')
    # migracja(url)




