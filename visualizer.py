import matplotlib.pyplot as plt
import seaborn as sns

class Visualizer:
    def __init__(self, df):
        self.df = df

    def create_plots(self, team_name):
        sns.set_style("whitegrid")

        # Graphique 1 : Évolution des victoires par année
        plt.figure(figsize=(10, 5))
        sns.lineplot(x='Year', y='Wins', data=self.df, marker='o', color='b')
        plt.title(f'Évolution des victoires pour {team_name}', fontsize=16)
        plt.xlabel('Année', fontsize=14)
        plt.ylabel('Nombre de victoires', fontsize=14)
        plt.savefig(f'static/{team_name}_wins_evolution.png')
        plt.close()

        # Graphique 2 : Comparaison du nombre de buts marqués par année (histogramme)
        plt.figure(figsize=(10, 5))
        sns.histplot(self.df['Goals For (GF)'], bins=10, kde=True, color='green')
        plt.title(f'Distribution des buts marqués pour {team_name}', fontsize=16)
        plt.xlabel('Buts marqués (GF)', fontsize=14)
        plt.ylabel('Fréquence', fontsize=14)
        plt.savefig(f'static/{team_name}_goals_histogram.png')
        plt.close()

        # Graphique 3 : Boxplot des victoires par équipe
        plt.figure(figsize=(10, 5))
        sns.boxplot(x='Team Name', y='Wins', data=self.df, palette='Set2')
        plt.title(f'Boxplot des victoires pour {team_name}', fontsize=16)
        plt.xlabel('Équipe', fontsize=14)
        plt.ylabel('Nombre de victoires', fontsize=14)
        plt.xticks(rotation=45)
        plt.savefig(f'static/{team_name}_wins_boxplot.png')
        plt.close()