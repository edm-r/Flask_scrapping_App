from flask import Flask, render_template, request, send_file
from scraper import Scraper
from analyzer import Analyzer
from visualizer import Visualizer
import pandas as pd

app = Flask(__name__)

# Initialiser le scraper avec l'URL de base
scraper = Scraper(base_url="https://www.scrapethissite.com/pages/forms/")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    team_name = request.form['team_name']
    
    # Scraper les données
    df = scraper.scrape_team_data(team_name)
    
    # Analyser les données
    analyzer = Analyzer(df)
    analyzer.convert_to_numeric()
    analysis = analyzer.analyze()
    
    # Visualiser les données
    visualizer = Visualizer(df)
    visualizer.create_plots(team_name)
    
    # Sauvegarder les données en CSV
    filename = f"{team_name}_data.csv"
    df.to_csv(filename, index=False)
    
    return render_template('results.html', team_name=team_name, data=df.to_dict('records'), analysis=analysis)

@app.route('/compare', methods=['POST'])
def compare():
    teams = request.form['teams'].split(',')
    start_year = int(request.form['start_year'])
    end_year = int(request.form['end_year'])

    # Scraper les données pour chaque équipe
    all_data = []
    for team in teams:
        df = scraper.scrape_team_data(team)
        df['Year'] = df['Year'].astype(int)
        df = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
        all_data.append(df)
    
    combined_df = pd.concat(all_data)
    
    # Visualiser les données comparées
    visualizer = Visualizer(combined_df)
    visualizer.create_comparison_plots(teams, start_year, end_year)
    
    # Sauvegarder les données comparées en CSV
    filename = f"comparison_{'_'.join(teams)}_{start_year}_{end_year}.csv"
    combined_df.to_csv(filename, index=False)
    
    return render_template('comparison.html', teams=teams, start_year=start_year, end_year=end_year, data=combined_df.to_dict('records'))

if __name__ == '__main__':
    app.run(debug=True)