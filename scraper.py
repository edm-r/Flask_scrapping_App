import requests
from bs4 import BeautifulSoup
import pandas as pd

class Scraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def scrape_team_data(self, team_name):
        try:
            url = f"{self.base_url}?q={team_name}"
            response = requests.get(url)
            response.raise_for_status()  # Lève une exception si le statut n'est pas 200

            soup = BeautifulSoup(response.text, 'html.parser')

            # Trouver le tableau des données
            table = soup.find('table', class_='table')
            if not table:
                raise ValueError("Tableau des données non trouvé sur la page.")

            rows = table.find_all('tr')[1:]  # Ignorer la première ligne (en-tête)

            data = []
            for row in rows:
                cols = row.find_all('td')
                if len(cols) < 8:
                    continue  # Ignorer les lignes incomplètes
                data.append({
                    'Team Name': cols[0].text.strip(),
                    'Year': cols[1].text.strip(),
                    'Wins': cols[2].text.strip(),
                    'Losses': cols[3].text.strip(),
                    'OT Losses': cols[4].text.strip(),
                    'Win %': cols[5].text.strip(),
                    'Goals For (GF)': cols[6].text.strip(),
                    'Goals Against (GA)': cols[7].text.strip()
                })

            if not data:
                raise ValueError("Aucune donnée trouvée pour cette équipe.")

            # Convertir en DataFrame Pandas
            df = pd.DataFrame(data)
            return df

        except requests.exceptions.RequestException as e:
            print(f"Erreur de connexion : {e}")
            return pd.DataFrame()  # Retourne un DataFrame vide en cas d'erreur
        except Exception as e:
            print(f"Erreur lors du scraping : {e}")
            return pd.DataFrame()  # Retourne un DataFrame vide en cas d'erreur