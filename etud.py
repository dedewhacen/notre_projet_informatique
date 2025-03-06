from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
def accueil():
    return render_template('hom.html')

@app.route('/etudiant', methods=['GET'])
def etudiant():
    # Redirection directe sans vérification
    return render_template('page_etud.html')

@app.route('/formulaire', methods=['POST'])
def formulaire():
        # Ajouter ici le traitement des données...
        return redirect(url_for('etudiant'))

if __name__ == '__main__':
    app.run(debug=True)