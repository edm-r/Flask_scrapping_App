from flask import Flask, render_template, request, send_file, flash, redirect
from scraper import Scraper
from analyzer import Analyzer
from visualizer import Visualizer
import pandas as pd

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Clé secrète pour Flask Flash

# Initialiser le scraper avec l'URL de base
scraper = Scraper(base_url="https://www.scrapethissite.com/pages/forms/")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    team_name = request.form.get('team_name', '').strip()
    if not team_name:
        flash("Veuillez entrer un nom d'équipe.", 'error')
        return redirect('/')

    try:
        # Scraper les données
        df = scraper.scrape_team_data(team_name)
        if df.empty:
            flash(f"Aucune donnée trouvée pour l'équipe : {team_name}", 'error')
            return redirect('/')

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

    except Exception as e:
        flash(f"Une erreur s'est produite : {e}", 'error')
        return redirect('/')

@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

@app.route('/compare', methods=['POST'])
def compare():
    teams = request.form.get('teams', '').strip()
    start_year = request.form.get('start_year', '').strip()
    end_year = request.form.get('end_year', '').strip()

    if not teams or not start_year or not end_year:
        flash("Veuillez remplir tous les champs du formulaire.", 'error')
        return redirect('/')

    try:
        start_year = int(start_year)
        end_year = int(end_year)
        teams = [team.strip() for team in teams.split(',') if team.strip()]

        if not teams:
            flash("Veuillez entrer au moins une équipe.", 'error')
            return redirect('/')

        # Scraper les données pour chaque équipe
        all_data = []
        for team in teams:
            df = scraper.scrape_team_data(team)
            if df.empty:
                flash(f"Aucune donnée trouvée pour l'équipe : {team}", 'error')
                continue
            df['Year'] = df['Year'].astype(int)
            df = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
            all_data.append(df)

        if not all_data:
            flash("Aucune donnée trouvée pour les équipes et la période spécifiées.", 'error')
            return redirect('/')

        combined_df = pd.concat(all_data)

        # Visualiser les données comparées
        visualizer = Visualizer(combined_df)
        visualizer.create_comparison_plots(teams, start_year, end_year)

        # Sauvegarder les données comparées en CSV
        filename = f"comparison_{'_'.join(teams)}_{start_year}_{end_year}.csv"
        combined_df.to_csv(filename, index=False)

        return render_template('comparison.html', teams=teams, start_year=start_year, end_year=end_year, data=combined_df.to_dict('records'))

    except ValueError as e:
        flash(f"Erreur de saisie : {e}", 'error')
        return redirect('/')
    except Exception as e:
        flash(f"Une erreur s'est produite : {e}", 'error')
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)