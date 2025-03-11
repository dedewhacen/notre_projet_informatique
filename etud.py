from flask import Flask, render_template, redirect, url_for, request
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Connexion à la base de données
conn = mysql.connector.connect(
    host="localhost",
    user="root",       # Remplace par ton utilisateur MySQL
    password="",       # Remplace par ton mot de passe MySQL
    database="gestion_des_reclamation"
)
cursor = conn.cursor()

@app.route('/')
def accueil():
    return render_template('hom.html')

@app.route('/etudiant', methods=['GET', 'POST'])
def etudiant():
    if request.method == 'POST':
        matricule = request.form['matricule']
        email = request.form['email']
        licence = request.form['licence']
        semestre = request.form['semestre']
        departement = request.form['departement']
        matiere = request.form['matiere']
        objet_rec = request.form['objet']
        details = request.form['details']
        moment_de_reclamation = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Insertion dans la table 'etudiant'
        cursor.execute("""
            INSERT INTO etudiant (matricule_etd, Email, Licence, Semestre, Departement) 
            VALUES (%s, %s, %s, %s, %s) 
            ON DUPLICATE KEY UPDATE Email=VALUES(Email), Licence=VALUES(Licence), Semestre=VALUES(Semestre), Departement=VALUES(Departement)
        """, (matricule, email, licence, semestre, departement))
        conn.commit()

        # Insérer la matière si elle n'existe pas déjà
        cursor.execute("""
            INSERT IGNORE INTO matiér (code_mat, nom_mat) VALUES (%s, %s)
        """, (matiere, matiere))
        conn.commit()

        # Insertion de la réclamation
        cursor.execute("""
            INSERT INTO réclamation (Détails, Objet_rec, moment_de_creation, matricule_etd, code_mat) 
            VALUES (%s, %s, %s, %s, %s)
        """, (details, objet_rec, moment_de_reclamation, matricule, matiere))
        conn.commit()

        # Redirige vers la page de suivi des réclamations
        return redirect(url_for('suivi_reclamations_etud'))

    return render_template('page_etud.html')

@app.route('/suivi_reclamations_etud')
def suivi_reclamations_etud():
    # Récupérer toutes les réclamations
    cursor.execute("SELECT id_rec, Détails, Objet_rec, moment_de_creation, matricule_etd, code_mat FROM réclamation")
    reclamations = cursor.fetchall()
    return render_template('suivi_reclamations_etud.html', reclamations=reclamations)

@app.route('/supprimer_reclamation/<int:id_rec>', methods=['POST'])
def supprimer_reclamation(id_rec):
    cursor.execute("DELETE FROM réclamation WHERE id_rec = %s", (id_rec,))
    conn.commit()
    return redirect(url_for('suivi_reclamations_etud'))

@app.route('/modifier_reclamation_etud/<int:id_rec>', methods=['GET', 'POST'])
def modifier_reclamation_etud(id_rec):
    if request.method == 'POST':
        objet_rec = request.form['objet_rec']
        details = request.form['details']
        # Mettre à jour le moment de modification
        moment_de_reclamation = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("""
            UPDATE réclamation
            SET Objet_rec = %s, Détails = %s, moment_de_creation = %s
            WHERE id_rec = %s
        """, (objet_rec, details, moment_de_reclamation, id_rec))
        conn.commit()
        return redirect(url_for('suivi_reclamations_etud'))
    else:
        cursor.execute("SELECT id_rec, Détails, Objet_rec FROM réclamation WHERE id_rec = %s", (id_rec,))
        reclamation = cursor.fetchone()
        return render_template('modifier_reclamation_etud.html', reclamation=reclamation)

if __name__ == '__main__':
    app.run(debug=True)
