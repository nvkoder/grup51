import requests
import sqlite3
from datetime import datetime, timedelta

# Definér API URL'er
api_urls = [
    "https://www.elprisenligenu.dk/api/v1/prices/2024/04-14_DK2.json",
    "https://www.elprisenligenu.dk/api/v1/prices/2024/04-15_DK2.json"
]

# Opret forbindelse til SQLite databasen
db_connection = sqlite3.connect("electricity_prices.db")
cursor = db_connection.cursor()

# Opret ElectricityPrices tabellen, hvis den ikke eksisterer
cursor.execute('''CREATE TABLE IF NOT EXISTS ElectricityPrices (
                    id INTEGER PRIMARY KEY,
                    DKK_per_kWh REAL,
                    time_start TEXT,
                    time_end TEXT
                )''')

# Loop gennem API URL'erne
for api_url in api_urls:
    # Foretag API forespørgslen
    response = requests.get(api_url)

    # Tjek om forespørgslen var vellykket
    if response.status_code == 200:
        data = response.json()

        # Indsæt data i databasen
        for entry in data:
            DKK_per_kWh = entry["DKK_per_kWh"]
            time_start = entry["time_start"]
            time_end = entry["time_end"]

            # Indsæt data i databasen
            cursor.execute('''INSERT INTO ElectricityPrices 
                            (DKK_per_kWh, time_start, time_end) 
                            VALUES (?, ?, ?)''', 
                            (DKK_per_kWh, time_start, time_end))

# Commit ændringerne og luk forbindelsen til databasen
db_connection.commit()

# Slet duplikater ved hjælp af ROWID
cursor.execute('''DELETE FROM ElectricityPrices 
                  WHERE ROWID NOT IN (SELECT MIN(ROWID) 
                                      FROM ElectricityPrices 
                                      GROUP BY DKK_per_kWh, time_start, time_end)''')


import sqlite3

# Opret forbindelse til SQLite databasen
db_connection = sqlite3.connect("electricity_prices.db")
cursor = db_connection.cursor()

# Find den billigste elpris og tilhørende tidspunkter
cursor.execute("SELECT DKK_per_kWh, time_start, time_end FROM ElectricityPrices WHERE DKK_per_kWh = (SELECT MIN(DKK_per_kWh) FROM ElectricityPrices)")

# Hent resultatet af forespørgslen
cheapest_price_data = cursor.fetchone()

if cheapest_price_data:
    cheapest_price, time_start, time_end = cheapest_price_data

    # Udskriv den billigste elpris og tidspunkterne
    print("Den billigste elpris er:", cheapest_price, "DKK per kWh")
    print("Tidspunktet for den billigste elpris er fra", time_start, "til", time_end)
else:
    print("Ingen data fundet.")

# Luk forbindelsen til databasen
db_connection.close()


