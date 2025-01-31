import pandas as pd

class Analyzer:
    def __init__(self, df):
        self.df = df

    def convert_to_numeric(self):
        # Convertir les colonnes en type numérique
        self.df['Wins'] = pd.to_numeric(self.df['Wins'], errors='coerce')
        self.df['Losses'] = pd.to_numeric(self.df['Losses'], errors='coerce')
        self.df['OT Losses'] = pd.to_numeric(self.df['OT Losses'], errors='coerce')
        self.df['Win %'] = pd.to_numeric(self.df['Win %'], errors='coerce')
        self.df['Goals For (GF)'] = pd.to_numeric(self.df['Goals For (GF)'], errors='coerce')
        self.df['Goals Against (GA)'] = pd.to_numeric(self.df['Goals Against (GA)'], errors='coerce')
        self.df = self.df.dropna()  # Supprimer les lignes avec des valeurs manquantes

    def analyze(self):
        # Calculer des statistiques descriptives
        mean_wins = self.df['Wins'].mean()
        median_goals_for = self.df['Goals For (GF)'].median()
        std_losses = self.df['Losses'].std()
        correlation = self.df['Wins'].corr(self.df['Goals For (GF)'])

        return {
            'mean_wins': mean_wins,
            'median_goals_for': median_goals_for,
            'std_losses': std_losses,
            'correlation': correlation
        }