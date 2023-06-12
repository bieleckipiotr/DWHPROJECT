import pyodbc
import requests
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


# TODO: kluczyk też możesz zmienić jeśli chcesz :))
apikey = '' # KLUCZ DO API WARSZAWSKIEGO

if __name__ == "__main__":
    # aktualna pozycja pojazdów
    server = '' # WYPEŁNIĆ WŁASNYMI DANYMI
    database = '' # BAZA DOCELOWA
    username = ''
    password = ''
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    query = "select distinct linia from DimBuses"
    cursor.execute(query)
    rows = cursor.fetchall()
    dictionaries = []
    for row in rows:
        linia = row[0]
        url = f"https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id=f2e5503e927d-4ad3-9500-4ab9e55deb59&apikey={apikey}&type=1&line={linia}"
        response = requests.get(url)
        if response.status_code == 200:
            # Odpowiedź jest udana, można przetwarzać dane
            data = response.json()  # Jeśli odpowiedź jest w formacie JSON
        for i in range(len(data['result'])):
            dictionary = {"linia" : linia}
            # print(data['result'][i]['values'][j]['key'], data['result'][i]['values'][j]['value'])
            if type(data['result'][i]) == str:
                continue
            for c, v in data['result'][i].items():
                dictionary[c] = v
            dictionaries.append(dictionary)


    currentposition = pd.DataFrame(dictionaries)
    currentposition

    conn = connect()
    currentposition = currentposition.drop(columns=['Lines'])
    check_for_table(conn, 'CurrentPosition', currentposition.columns)
    cursor = conn.cursor()
    # Insert Dataframe into SQL Server:
    for index, row in currentposition.iterrows():
    # Check if the record already exists
        cursor.execute("SELECT COUNT(*) FROM CurrentPosition WHERE linia = ? AND Lon = ? AND Lat = ? AND VehicleNumber = ? AND Brigade = ? AND Time = ?",
                    (row['linia'], row['Lon'], row['Lat'], row['VehicleNumber'], row['Brigade'], row['Time']))
        result = cursor.fetchone()
        
        if result[0] == 0:
            # Insert the record if it doesn't exist
            cursor.execute("INSERT INTO CurrentPosition (linia, Lon, Lat, VehicleNumber, Brigade, Time) VALUES (?, ?, ?, ?, ?, ?)",
                        (row['linia'], row['Lon'], row['Lat'], row['VehicleNumber'], row['Brigade'], row['Time']))

    conn.commit()
    cursor.close()
    conn.close()
