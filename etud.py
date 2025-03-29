from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
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

        # D'abord, on vérifie dans la table etudiant
        cursor.execute("SELECT Email, pwd FROM etudiant WHERE Email = %s AND pwd = %s", (email, pwd))
        user = cursor.fetchone()
        if user:
            session['logged_in'] = True
            session['user_email'] = email
            session['role'] = 'etudiant'
            return redirect(url_for('suivi_reclamations_etud'))

        # Sinon, on vérifie dans la table user pour les administrateurs
        cursor.execute("SELECT email_admin, pwd_admin FROM user WHERE email_admin = %s AND pwd_admin = %s",
                       (email, pwd))
        admin = cursor.fetchone()
        if admin:
            session['logged_in'] = True
            session['user_email'] = email
            session['role'] = 'admin'
            return redirect(
                url_for('admin_dashboard'))  # Assure-toi d'avoir une route admin_dashboard qui affiche admin.html

        # Si aucun identifiant ne correspond, afficher un message d'erreur
        flash("Identifiants invalides. Veuillez réessayer.", "danger")

    return render_template('login.html')


@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('logged_in') or session.get('role') != 'admin':
        flash("Accès réservé aux administrateurs.", "danger")
        return redirect(url_for('login'))

    # Exécuter la requête SQL pour récupérer les données souhaitées
    query = """
    SELECT 
    e.Email AS 'Email_etudiant',
    e.matricule_etd AS 'Matricule',
    m.nom_mat AS 'Matiere_reclamee',
    e.Departement AS 'Departement',
    e.Licence AS 'Niveau',
    r.statut AS 'Statut',
    r.moment_de_creation AS 'Date_creation',
    r.Objet_rec AS 'Objet_reclamation',
    r.Détails AS 'Details_reclamation'
FROM 
    etudiant e 
JOIN 
    réclamation r ON e.matricule_etd = r.matricule_etd 
JOIN 
    matiér m ON r.code_mat = m.code_mat;
    """
    cursor.execute(query)
    # Récupère toutes les lignes ; chaque ligne est un tuple
    results = cursor.fetchall()

    # Optionnel : pour plus de lisibilité, tu peux construire une liste de dictionnaires
    reclamations = []
    for row in results:
        reclamations.append({
            'email': row[0],
            'matricule': row[1],
            'matiere': row[2],
            'departement': row[3],
            'niveau': row[4],
            'statut': row[5],
            'date_creation': row[6],
            'objet': row[7],
            'details': row[8]
        })

    return render_template('admin.html', reclamations=reclamations)


@app.route('/suivi_reclamations_etud')
def suivi_reclamations_etud():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Récupérer le matricule via l'email de session
    email = session['user_email']
    cursor.execute("SELECT matricule_etd FROM etudiant WHERE Email = %s", (email,))
    matricule = cursor.fetchone()[0]  # [0] car fetchone() retourne un tuple

    # Filtrer par matricule
    cursor.execute("""
        SELECT id_rec, Détails, Objet_rec, moment_de_creation, matricule_etd, code_mat 
        FROM réclamation 
        WHERE matricule_etd = %s
    """, (matricule,))

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


@app.route('/etudiant', methods=['GET', 'POST'])


def etudiant():
    email = session.get('user_email')
    message = None
    category = 'success'

    # Récupération des données étudiant
    cursor.execute("SELECT matricule_etd, Email, Licence, Departement FROM etudiant WHERE Email = %s",
                   (email,))
    etudiant_data = cursor.fetchone()

    if request.method == 'POST':
        try:
            matricule = request.form['matricule']
            matiere = request.form['matiere']
            objet_rec = request.form.getlist('objet')
            details = request.form['details']
            moment_de_reclamation = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            objets_str = ','.join(objet_rec)

            # Vérification existence de la matière
            cursor.execute("INSERT IGNORE INTO matiér (code_mat, nom_mat) VALUES (%s, %s)",
                           (matiere, matiere))

            # Insertion réclamation avec vérification unicité
            cursor.execute("""
                INSERT INTO réclamation (Détails, Objet_rec, moment_de_creation, matricule_etd, code_mat) 
                VALUES (%s, %s, %s, %s, %s)
            """, (details, objets_str, moment_de_reclamation, matricule, matiere))

            conn.commit()
            flash("Réclamation soumise avec succès!", "success")
            return redirect(url_for('suivi_reclamations_etud'))

        except mysql.connector.IntegrityError as e:
            conn.rollback()
            if 'unique_reclamation' in str(e):
                flash("Vous avez déjà une réclamation pour cette matière et cet objet", "danger")
            else:
                flash("Une erreur est survenue lors de la soumission", "danger")

    return render_template('page_etud.html',
                           etudiant=etudiant_data,
                           message=message,
                           category=category)


@app.route('/get_claimed_matieres')
def get_claimed_matieres():
    if not session.get('logged_in'):
        return jsonify([])

    email = session['user_email']
    cursor.execute("""
        SELECT r.code_mat 
        FROM réclamation r
        JOIN etudiant e ON r.matricule_etd = e.matricule_etd 
        WHERE e.Email = %s
    """, (email,))

    result = cursor.fetchall()
    claimed_matieres = [row[0] for row in result]
    return jsonify(claimed_matieres=claimed_matieres)

@app.route('/parametres', methods=['GET'])
def parametres():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Supposons que l'email stocké dans la session identifie l'utilisateur.
    email = session['user_email']
    cursor.execute("SELECT email,pwd FROM etudiant WHERE email = %s", (email,))
    user = cursor.fetchone()

    return render_template('parametres.html', user=user)

@app.route('/parametres_admin')
def parametres_admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Supposons que l'email stocké dans la session identifie l'utilisateur.
    email = session['user_email']
    cursor.execute("SELECT email_admin,pwd_admin FROM user WHERE email_admin = %s", (email,))
    user_A = cursor.fetchone()

    return render_template('parametres_admin.html',user_A=user_A)
@app.route('/change_password', methods=['POST'])
def change_password():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    email = session['user_email']
    old_password = request.form['old_password']
    new_password = request.form['new_password']

    # Vérifier que l'ancien mot de passe est correct
    cursor.execute("SELECT pwd FROM etudiant WHERE email = %s", (email,))
    result = cursor.fetchone()

    if result and result[0] == old_password:  # Pour une meilleure sécurité, vous devriez stocker un hash
        # Mettre à jour le mot de passe
        cursor.execute("UPDATE etudiant SET pwd = %s WHERE email = %s", (new_password, email))
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