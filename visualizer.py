import matplotlib
matplotlib.use('Agg')  # Utiliser le backend non interactif
import matplotlib.pyplot as plt
import seaborn as sns


class Visualizer:
    def __init__(self, df):
        self.df = df

    def create_plots(self, team_name):
        try:
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

            # Graphique 4 : Heatmap des performances moyennes par année
            plt.figure(figsize=(10, 5))
            df_pivot = self.df.pivot_table(index='Year', columns='Team Name', values='Wins', aggfunc='mean')
            sns.heatmap(df_pivot, annot=True, cmap='YlGnBu', fmt='.1f')
            plt.title(f'Heatmap des performances moyennes par année pour {team_name}', fontsize=16)
            plt.xlabel('Équipe', fontsize=14)
            plt.ylabel('Année', fontsize=14)
            plt.savefig(f'static/{team_name}_performance_heatmap.png')
            plt.close()

            # Graphique 5 : Scatter plot entre le nombre de buts marqués et le pourcentage de victoires
            plt.figure(figsize=(10, 5))
            sns.scatterplot(x='Goals For (GF)', y='Win %', data=self.df, hue='Team Name', palette='viridis')
            plt.title(f'Scatter plot : Buts marqués vs Pourcentage de victoires pour {team_name}', fontsize=16)
            plt.xlabel('Buts marqués (GF)', fontsize=14)
            plt.ylabel('Pourcentage de victoires', fontsize=14)
            plt.savefig(f'static/{team_name}_goals_vs_win_percentage.png')
            plt.close()

            # Graphique 6 : Distribution des performances des équipes pour une année donnée
            plt.figure(figsize=(10, 5))
            sns.kdeplot(self.df['Wins'], fill=True, color='blue')  # Remplace `shade=True` par `fill=True`
            plt.title(f'Distribution des performances pour {team_name}', fontsize=16)
            plt.xlabel('Nombre de victoires', fontsize=14)
            plt.ylabel('Densité', fontsize=14)
            plt.savefig(f'static/{team_name}_performance_distribution.png')
            plt.close()

        except Exception as e:
            print(f"Erreur lors de la création des graphiques : {e}")

    def create_comparison_plots(self, teams, start_year, end_year):
        try:
            sns.set_style("whitegrid")

            # Graphique 1 : Comparaison des victoires par année
            plt.figure(figsize=(10, 5))
            sns.lineplot(x='Year', y='Wins', hue='Team Name', data=self.df, marker='o')
            plt.title(f'Comparaison des victoires ({start_year}-{end_year})', fontsize=16)
            plt.xlabel('Année', fontsize=14)
            plt.ylabel('Nombre de victoires', fontsize=14)
            plt.savefig(f'static/comparison_wins_{start_year}_{end_year}.png')
            plt.close()

            # Graphique 2 : Comparaison des buts marqués par année
            plt.figure(figsize=(10, 5))
            sns.lineplot(x='Year', y='Goals For (GF)', hue='Team Name', data=self.df, marker='o')
            plt.title(f'Comparaison des buts marqués ({start_year}-{end_year})', fontsize=16)
            plt.xlabel('Année', fontsize=14)
            plt.ylabel('Buts marqués (GF)', fontsize=14)
            plt.savefig(f'static/comparison_goals_{start_year}_{end_year}.png')
            plt.close()

        except Exception as e:
            print(f"Erreur lors de la création des graphiques de comparaison : {e}")