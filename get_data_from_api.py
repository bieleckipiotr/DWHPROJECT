import requests
import pyodbc
import pandas as pd

def connect():
    server = '' # WYPEŁNIĆ WŁASNYMI DANYMI
    database = '' # BAZA PRZEJŚCIOWA
    username = ''
    password = ''
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    # Nawiązanie połączenia do bazy danych
    conn = pyodbc.connect(connection_string)
    return(conn)

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
    conn.commit()
    cursor.close()
    return

if __name__ == "__main__":

    # KLUCZ DO WARSZAWSKIEGO API
    apikey = ''


    df = pd.read_csv('./listaprzystanków.csv', index_col=0)
    df = df.drop(columns = ['Przystanek'])
    df.columns = ['nazwa']
    df['numer'] = df['nazwa'].apply(lambda x: x.strip(" ").split(" ")[-1])
    df['nazwa'] = df['nazwa'].apply(lambda x: x[:-5])

    dictionaries = []
    for i, nazwaprzystanku in enumerate(np.unique(df['nazwa'])):
        url1 = 'https://api.um.warszawa.pl/api/action/dbtimetable_get?id=b27f4c17-5c50-4a5b-89dd-236b282bc499&name=' + nazwaprzystanku + '&apikey=' + apikey

        ### dla url 1
        response = requests.get(url1)
        if response.status_code == 200:
        # Odpowiedź jest udana, można przetwarzać dane
            data = response.json()  # Jeśli odpowiedź jest w formacie JSON
        try:
            for i in range(len(data['result'])):
                dictionary = {}
                for j in range(len(data['result'][i]['values'])):
                    # print(data['result'][i]['values'][j]['key'], data['result'][i]['values'][j]['value'])
                    c = data['result'][i]['values'][j]['key']
                    v = data['result'][i]['values'][j]['value']
                    dictionary[c] = v
                dictionaries.append(dictionary)
        except:
            continue
    stopcode = pd.DataFrame(dictionaries)


    conn = connect()
    table_name = "Stopcode"
    check_for_table(conn, table_name, stopcode.columns)
    cursor = conn.cursor()
    # Insert Dataframe into SQL Server:
    for index, row in stopcode.iterrows():
        cursor.execute(f"INSERT INTO {table_name} (Zespol,Nazwa) values(?,?)",
                    (row.zespol, row.nazwa))
    conn.commit()
    cursor.close()

    dictionaries = []
    zespoly = list(stopcode['zespol'].unique())
    for i, zespol in enumerate(zespoly):
        name = list(stopcode[stopcode['zespol'] == zespol].nazwa)[0]

        for busstopNr in list(df[df['nazwa'] == name.upper()].numer):
            
            url2 = 'https://api.um.warszawa.pl/api/action/dbtimetable_get?id=88cd555f-6f31-43ca-9de4-66c479ad5942&busstopId=' + zespol + '&busstopNr=' + busstopNr + '&apikey=' + apikey

            ### dla url 2
            response = requests.get(url2)
            if response.status_code == 200:
                # Odpowiedź jest udana, można przetwarzać dane
                data = response.json()  # Jeśli odpowiedź jest w formacie JSON
                # print(data)
            for i in range(len(data['result'])):
                dictionary = {"zespol" : zespol,
                            "stop nr" : busstopNr}
                for j in range(len(data['result'][i]['values'])):
                    # print(data['result'][i]['values'][j]['key'], data['result'][i]['values'][j]['value'])
                    c = data['result'][i]['values'][j]['key']
                    v = data['result'][i]['values'][j]['value']
                    dictionary[c] = v
                dictionaries.append(dictionary)
    stopinfo = pd.DataFrame(dictionaries)


    conn = connect()
    check_for_table(conn, table_name, stopinfo.columns)
    cursor = conn.cursor()
    # Insert Dataframe into SQL Server:
    for index, row in stopinfo.iterrows():
        cursor.execute("INSERT INTO Stopinfo (zespol, stop_nr, linia) values(?,?,?)",
                        (row['zespol'], row['stop nr'], row.linia))
    conn.commit()
    cursor.close()
    conn.close()


    tmp = stopinfo.merge(stopcode, how='inner', on = 'zespol')
    dictionaries = []
    for i, row in tmp.iterrows():
        zespol = row.zespol
        slupek = row['stop nr']
        linia = row['linia']
        if type(slupek) == tuple:
            slupek = slupek[0]

        url3 = 'https://api.um.warszawa.pl/api/action/dbtimetable_get?id=e923fa0e-d96c-43f9-ae6e-60518c9f3238&busstopId=' + str(zespol) + '&busstopNr=' + slupek + '&line=' + str(linia) + '&apikey=' + apikey

        ### dla url 3
        response = requests.get(url3)
        if response.status_code == 200:
            # Odpowiedź jest udana, można przetwarzać dane
            data = response.json()  # Jeśli odpowiedź jest w formacie JSON
        for k in range(len(data['result'])):
            dictionary = {'zespol' : zespol,
                        "slupek" : slupek,
                        'linia' : linia}
            for j in range(len(data['result'][k]['values'])):
                # print(data['result'][i]['values'][j]['key'], data['result'][i]['values'][j]['value'])
                c = data['result'][k]['values'][j]['key']
                v = data['result'][k]['values'][j]['value']
                dictionary[c] = v
            dictionaries.append(dictionary)
    schedule = pd.DataFrame(dictionaries)

    conn = connect()
    check_for_table(conn, 'Schedules', schedule.columns)
    cursor = conn.cursor()
    # Insert Dataframe into SQL Server:
    for index, row in schedule.iterrows():
    # Check if the record already exists
        cursor.execute("SELECT COUNT(*) FROM Schedules WHERE zespol = ? AND slupek = ? AND linia = ? AND symbol_1 = ? AND symbol_2 = ? AND brygada = ? AND kierunek = ? AND trasa = ? AND czas = ?",
                   (row['zespol'], row['slupek'], row['linia'], row['symbol_1'], row['symbol_2'], row['brygada'], row['kierunek'], row['trasa'], row['czas']))
        result = cursor.fetchone()

        if result[0] == 0:
            # Insert the record if it doesn't exist
            cursor.execute("INSERT INTO Schedules (zespol, slupek, linia, symbol_1, symbol_2, brygada, kierunek, trasa, czas) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (row['zespol'], row['slupek'], row['linia'], row['symbol_1'], row['symbol_2'], row['brygada'], row['kierunek'], row['trasa'], row['czas']))

    conn.commit()
    cursor.close()

    conn.close()

    # trasy pojazdów routes

    url = f"https://api.um.warszawa.pl/api/action/public_transport_routes/?apikey={apikey}"
    dictionaries = []

    response = requests.get(url)
    if response.status_code == 200:
        # Odpowiedź jest udana, można przetwarzać dane
        data = response.json()  # Jeśli odpowiedź jest w formacie JSON
        for linia in data['result'].keys():
            for key in data['result'][linia].keys():
                for key2 in  data['result'][linia][key].keys():
                    dictionary = {'linia' : linia,
                                'kod' : key,
                                'nr przystanku na trasie' : key2}
                    
                    for c, v in data['result'][linia][key][key2].items():
                        dictionary[c] = v
                    dictionaries.append(dictionary)
        # print(data['result'][i]['values'][j]['key'], data['result'][i]['values'][j]['value'])  
    routes = pd.DataFrame(dictionaries)
    routes = routes.rename(columns={'nr przystanku na trasie' : 'enroute_nr'})

    conn = connect()
    check_for_table(conn, 'Routes', routes.columns)
    cursor = conn.cursor()
    # Insert Dataframe into SQL Server:
    for index, row in routes.iterrows():
    # Check if the record already exists
        cursor.execute("SELECT COUNT(*) FROM Routes WHERE linia = ? AND kod = ? AND enroute_nr = ? AND odleglosc = ? AND ulica_id = ? AND nr_zespolu = ? AND typ = ? AND nr_przystanku = ?",
                    (row['linia'], row['kod'], row['enroute_nr'], row['odleglosc'], row['ulica_id'], row['nr_zespolu'], row['typ'], row['nr_przystanku']))
        result = cursor.fetchone()

        if result[0] == 0:
            # Insert the record if it doesn't exist
            cursor.execute("INSERT INTO Routes (linia, kod, enroute_nr, odleglosc, ulica_id, nr_zespolu, typ, nr_przystanku) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (row['linia'], row['kod'], row['enroute_nr'], row['odleglosc'], row['ulica_id'], row['nr_zespolu'], row['typ'], row['nr_przystanku']))

    conn.commit()
    cursor.close()
    conn.close()


    # pozycje przystanków autobusowych
    url = f'https://api.um.warszawa.pl/api/action/dbstore_get?id=ab75c33d-3a26-4342-b36a-6e5fef0a3ac3&apikey={apikey}'

    response = requests.get(url)
    if response.status_code == 200:
        print('ok')
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
    stops = pd.DataFrame(dictionaries)

    conn = connect()
    check_for_table(conn, 'Stops', stops.columns)
    cursor = conn.cursor()
    # Insert Dataframe into SQL Server:
    for index, row in stops.iterrows():
    # Check if the record already exists
        cursor.execute("SELECT COUNT(*) FROM Stops WHERE zespol = ? AND slupek = ? AND nazwa_zespolu = ? AND id_ulicy = ? AND szer_geo = ? AND dlug_geo = ? AND kierunek = ? AND obowiazuje_od = ?",
                    (row['zespol'], row['slupek'], row['nazwa_zespolu'], row['id_ulicy'], row['szer_geo'], row['dlug_geo'], row['kierunek'], row['obowiazuje_od']))
        result = cursor.fetchone()

        if result[0] == 0:
            # Insert the record if it doesn't exist
            cursor.execute("INSERT INTO Stops (zespol, slupek, nazwa_zespolu, id_ulicy, szer_geo, dlug_geo, kierunek, obowiazuje_od) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (row['zespol'], row['slupek'], row['nazwa_zespolu'], row['id_ulicy'], row['szer_geo'], row['dlug_geo'], row['kierunek'], row['obowiazuje_od']))

    conn.commit()
    cursor.close()
    conn.close()