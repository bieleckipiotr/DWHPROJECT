import pyodbc
import requests

def f(lat_bus, lon_bus, lat_stop, lon_stop):
    GOOGLE_KEY = "" # TU WSTAWIĆ NALEŻY KLUCZ DO DISTANCE MATRIX API GOOGLE
    destination = str(lat_stop).replace(',','.') + ',' + str(lon_stop).replace(',', '.')
    origin = str(lat_bus).replace(',','.') + ',' + str(lon_bus).replace(',', '.')
    # destination = "52.1968,20.925" # lat + lon DimStops
    # origin = "52.1968,20.920" # lat + lon FactDelays
    url = "https://maps.googleapis.com/maps/api/distancematrix/json" + f"?destinations={destination}" +  f"&origins={origin}" + f"&key={GOOGLE_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        # Odpowiedź jest udana, można przetwarzać dane
        data = response.json()  # Jeśli odpowiedź jest w formacie JSON
        return (data['rows'][0]['elements'][0]['distance']['value'], data['rows'][0]['elements'][0]['duration']['value'])
    else:
        return(-1,-1)

if __name__ == "__main__":
    server = '' # WYPEŁNIĆ WŁASNYMI DANYMI
    database = '' # BAZA DOCELOWA
    username = ''
    password = ''
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    # Nawiązanie połączenia do bazy danych
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    query = "Select f.bus_id, f.stop_id, f.scheduled_arr_id, f.Time_id, f.Date_id, f.lat, f.lon, s.lat, s.lon, sc.time_scheduled_id FROM FactDelays f JOIN DimStops s ON f.stop_id = s.stop_id JOIN DimTime t ON f.Time_id = t.TimeID join DimScheduledArr sc on f.scheduled_arr_id = sc.scheduled_arr_id where delay is NULL"
    cursor.execute(query)
    # Fetch all the rows from the result set
    rows = cursor.fetchall()
    cursor.close()

    for row in rows:
        (distance, time) = f(row[5],row[6], row[7], row[8]) #delay to nie delay tylko czas jaki nam zajmuje dojazd z obecnej pozycji autobusu do przystanku
        eta_id = row[3] + int(time/60)
        eta_id = eta_id % 1440
        delay_minutes = eta_id - row[9]
        cursor = conn.cursor()
        query = f"update FactDelays Set distance = {distance}, delay = {delay_minutes}, time_estimated_id = {eta_id} where bus_id = '{row[0]}' and stop_id = '{row[1]}' and scheduled_arr_id = '{row[2]}' and Time_id = {row[3]} and Date_id = {row[4]}"
        cursor.execute(query)
        cursor.close()
    conn.commit()
    conn.close()




    
    
    server = '' # WYPEŁNIĆ WŁASNYMI DANYMI
    database = '' # BAZA PRZEJŚCIOWA
    username = ''
    password = ''
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    # Nawiązanie połączenia do bazy danych
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    query = "Delete from CurrentPosition"
    cursor.execute(query)
    cursor.close()
    conn.commit()
    conn.close()