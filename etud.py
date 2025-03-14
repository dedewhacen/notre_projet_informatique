from flask import Flask, render_template, redirect, url_for, request, session, flash
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete'  # IMPORTANT : définissez ici une clé secrète pour les sessions

# Connexion à la base de données
conn = mysql.connector.connect(
    host="localhost",
    user="root",       # Remplacez par votre utilisateur MySQL
    password="",       # Remplacez par votre mot de passe MySQL
    database="gestion_des_reclamation"
)
cursor = conn.cursor()

# Route de connexion (page de login)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['pwd']
        # Vérifier dans la table 'user'
        cursor.execute("SELECT * FROM user WHERE email = %s AND pwd = %s", (email, pwd))
        user = cursor.fetchone()
        if user:
            session['logged_in'] = True
            session['user_email'] = email
            return redirect(url_for('suivi_reclamations_etud'))
        else:
            flash("Identifiants invalides. Veuillez réessayer.")
    return render_template('login.html')

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


@app.route('/parametres', methods=['GET'])
def parametres():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Supposons que l'email stocké dans la session identifie l'utilisateur.
    email = session['user_email']
    cursor.execute("SELECT email, nom, prenom FROM user WHERE email = %s", (email,))
    user = cursor.fetchone()

    return render_template('parametres.html', user=user)


@app.route('/update_profile', methods=['POST'])
def update_profile():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    email = session['user_email']
    nom = request.form['nom']
    prenom = request.form['prenom']

    # Mise à jour des champs dans la table user
    cursor.execute("UPDATE user SET nom = %s, prenom = %s WHERE email = %s", (nom, prenom, email))
    conn.commit()

    flash("Profil mis à jour avec succès.", "success")
    return redirect(url_for('parametres'))


@app.route('/change_password', methods=['POST'])
def change_password():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    email = session['user_email']
    old_password = request.form['old_password']
    new_password = request.form['new_password']

    # Vérifier que l'ancien mot de passe est correct
    cursor.execute("SELECT pwd FROM user WHERE email = %s", (email,))
    result = cursor.fetchone()

    if result and result[0] == old_password:  # Pour une meilleure sécurité, vous devriez stocker un hash
        # Mettre à jour le mot de passe
        cursor.execute("UPDATE user SET pwd = %s WHERE email = %s", (new_password, email))
        conn.commit()
        flash("Mot de passe changé avec succès.", "success")
    else:
        flash("Ancien mot de passe incorrect.", "danger")

    return redirect(url_for('parametres'))

@app.route('/logout')
def logout():
    session.pop('username', None)  # Supprime la session
    return redirect(url_for('login'))  # Redirige vers l'accueil
if __name__ == '__main__':
    app.run(debug=True)
