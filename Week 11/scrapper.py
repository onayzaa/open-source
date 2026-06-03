import requests
from bs4 import BeautifulSoup
import csv
import os

car=input("Enter name :")
url=f'https://www.pakwheels.com/new-cars/pricelist/{car}'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}
response=requests.get(url, headers=headers)


if response.status_code==200:
    soup=BeautifulSoup(response.text,'html.parser')
    tables=soup.find_all('table')
    if not tables:
        print("No tables found on the webpage.")
    for table in tables:
        rows=table.find_all('tr')
        for row in rows:
            cols=row.find_all('td')
            if len(cols)>= 2:
                name=cols[0].get_text()
                price=cols[1].get_text()
                print(f"Name: {name}, Price: {price}")
            
        
else:
    print("Failed to retrieve the webpage.")    


#create a function to scrape data from the webpage, the above code can be used inside the function




def scrapper(car: str) -> list[dict]:
    """
    Scrapes car price data from PakWheels for the given car name.
    Returns a list of dicts with 'name' and 'price' keys.
    """
    url = f'https://www.pakwheels.com/new-cars/pricelist/{car}'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/121.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table')

    if not tables:
        print("No tables found on the webpage.")
        return []

    data = []
    for table in tables:
        for row in table.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) >= 2:
                name  = cols[0].get_text(strip=True)
                price = cols[1].get_text(strip=True)
                if name and price:                  # skip empty rows
                    data.append({"name": name, "price": price})
                    print(f"Name: {name}, Price: {price}")

    return data


def save_to_file(data: list[dict], filename: str) -> None:
    """
    Saves a list of {'name', 'price'} dicts to a CSV file.
    Creates the file (or overwrites it) at the given path.
    """
    if not data:
        print("No data to save.")
        return

    # Ensure parent directory exists
    parent = os.path.dirname(filename)
    if parent:
        os.makedirs(parent, exist_ok=True)

    fieldnames = list(data[0].keys())          # derive columns from first record

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"Data saved to '{filename}' ({len(data)} rows).")


# ── entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    car_name = input("Enter car name (e.g. toyota, honda, suzuki): ").strip().lower()
    results  = scrapper(car_name)

    if results:
        output_file = f"{car_name}_prices.csv"
        save_to_file(results, output_file)