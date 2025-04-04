from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
import mysql.connector
from datetime import datetime
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = 'votre_cle_secrete_tres_secrete'  # Clé complexe

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
    # Vérifier si l'admin est connecté
    if not session.get('logged_in') or session.get('role') != 'admin':
        flash("Accès réservé aux administrateurs.", "danger")
        return redirect(url_for('login'))

    # Connexion et exécution SQL sécurisée
    query= """
    SELECT 
        e.Email AS Email_etudiant,
        e.matricule_etd AS Matricule,
        m.code_mat AS Matiere_reclamee,
        e.Departement AS Departement,
        e.Licence AS Niveau,
        r.statut AS Statut,
        r.moment_de_creation AS Date_creation,
        r.Objet_rec AS Objet_reclamation,
        r.Détails AS Details_reclamation
    FROM 
        etudiant e 
    JOIN 
        reclamation r ON e.matricule_etd = r.matricule_etd 
    JOIN 
        matiere m ON r.code_mat = m.code_mat;
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
    email = session.get('user_email')  # Utilisation de .get() pour éviter KeyError
    if not email:
        flash("Erreur : aucune session utilisateur détectée.", "danger")
        return redirect(url_for('login'))

    cursor.execute("SELECT matricule_etd FROM etudiant WHERE Email = %s", (email,))
    result = cursor.fetchone()

    if not result:  # Vérifier si l'étudiant existe
        flash("Aucun étudiant trouvé avec cet email.", "warning")
        return redirect(url_for('login'))

    matricule = result[0]  # Récupérer la valeur correcte

    # Filtrer par matricule
    cursor.execute("""
        SELECT id_rec, Détails, Objet_rec, moment_de_creation, matricule_etd, code_mat, statut 
        FROM reclamation 
        WHERE matricule_etd = %s
    """, (matricule,))

    reclamations = cursor.fetchall()

    cursor.execute("SELECT MAX(date_fermeture) FROM configuration_reclamation")
    date_fermeture = cursor.fetchone()[0]
    return render_template('suivi_reclamations_etud.html', reclamations=reclamations,date_fermeture=date_fermeture)


@app.route('/supprimer_reclamation/<int:id_rec>', methods=['POST'])
def supprimer_reclamation(id_rec):
    cursor.execute("DELETE FROM reclamation WHERE id_rec = %s", (id_rec,))
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
            UPDATE reclamation
            SET Objet_rec = %s, Détails = %s, moment_de_creation = %s
            WHERE id_rec = %s
        """, (objet_rec, details, moment_de_reclamation, id_rec))
        conn.commit()
        return redirect(url_for('suivi_reclamations_etud'))
    else:
        cursor.execute("SELECT id_rec, Détails, Objet_rec FROM reclamation WHERE id_rec = %s", (id_rec,))
        reclamation = cursor.fetchone()
        return render_template('modifier_reclamation_etud.html', reclamation=reclamation)


@app.route('/etudiant', methods=['GET', 'POST'])
def etudiant():
    email = session.get('user_email')
    message = None
    category = 'success'

    # Récupération des données etudiant
    cursor.execute("SELECT matricule_etd, Email, Licence, Departement FROM etudiant WHERE Email = %s",
                   (email,))
    etudiant_data = cursor.fetchone()
    niveau_etudiant = etudiant_data[2]  # Licence est à l'index 2 (L1, L2, etc.)
    # Requête pour les matières configurées par l'admin
    cursor.execute("""
            SELECT m.code_mat 
            FROM configuration_reclamation c
            JOIN matiere m ON c.code_mat = m.code_mat 
            WHERE c.niveau = %s
        """, (niveau_etudiant,))

    matieres_autorisees = [row[0] for row in cursor.fetchall()]

    if request.method == 'POST':
        try:
            matricule = request.form['matricule']
            matiere = request.form['matiere']
            if matiere not in matieres_autorisees:
                flash("Cette matière n'est pas autorisée pour votre niveau", "danger")
                return redirect(url_for('etudiant'))
            objet_rec = request.form.getlist('objet')
            details = request.form['details']
            moment_de_reclamation = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            objets_str = ','.join(objet_rec)



            # Insertion réclamation avec vérification unicité
            cursor.execute("""
                INSERT INTO reclamation (Détails, Objet_rec, moment_de_creation, matricule_etd, code_mat) 
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


@app.route('/save-config', methods=['POST'])
def save_config():
    if not session.get('logged_in') or session.get('role') != 'admin':
        return jsonify(error="Accès non autorisé"), 403

    try:
        configs = request.get_json()
        if not isinstance(configs, list):
            return jsonify(error="Format de données invalide"), 400

        for config in configs:
            niveau = config.get('niveau')
            matieres = config.get('matieres')
            date_fermeture = config.get('date_fermeture')

            # Validation des champs
            if not all([niveau, matieres, date_fermeture]):
                continue  # Ignore les entrées invalides

            # Vérifier existence configuration
            cursor.execute("""
                SELECT id, code_mat 
                FROM configuration_reclamation 
                WHERE niveau = %s AND date_fermeture = %s
            """, (niveau, date_fermeture))
            existing = cursor.fetchone()

            if existing:
                # Fusionner les matières
                anciennes = existing[1].split(',') if existing[1] else []
                nouvelles = list(set(anciennes + matieres))

                cursor.execute("""
                    UPDATE configuration_reclamation 
                    SET code_mat = %s 
                    WHERE id = %s
                """, (','.join(nouvelles), existing[0]))
            else:
                # Nouvelle entrée
                cursor.execute("""
                    INSERT INTO configuration_reclamation 
                    (niveau, code_mat, date_fermeture)
                    VALUES (%s, %s, %s)
                """, (niveau, ','.join(matieres), date_fermeture))

        conn.commit()
        return jsonify(success=True)

    except Exception as e:
        conn.rollback()
        return jsonify(error=f"Erreur : {str(e)}"), 500
@app.route('/change_admin_password', methods=['POST'])
def change_admin_password():
    if not session.get('logged_in') or session.get('role') != 'admin':
        return jsonify(error="Accès non autorisé"), 403

    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')

    # Vérification des identifiants
    cursor.execute("SELECT pwd_admin FROM user WHERE email_admin = %s", (session['user_email'],))
    result = cursor.fetchone()

    if not result or not check_password_hash(result[0], old_password):
        return jsonify(error="Ancien mot de passe incorrect")

    # Mise à jour du mot de passe
    hashed_password = generate_password_hash(new_password)
    cursor.execute("UPDATE user SET pwd_admin = %s WHERE email_admin = %s",
                   (hashed_password, session['user_email']))
    conn.commit()

    return jsonify(success=True)
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

#parametres administrateur
@app.route('/parametres_admin')
def parametres_admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    email = session['user_email']
    cursor.execute("SELECT email_admin, pwd_admin FROM user WHERE email_admin = %s", (email,))
    user_A = cursor.fetchone()

    cursor.execute("SELECT code_mat FROM matiere")
    matieres = [row[0] for row in cursor.fetchall()]

    # Structure des matières organisées par niveau et semestre
    structured_data = {
        'L1': {'S1': [], 'S2': []},
        'L2': {'S3': [], 'S4': []},
        'L3': {'S5': []}  # Pas de S6
    }

    for matiere in matieres:
        # Identifier la partie lettre (département) et chiffres (code)
        dept = ''.join(filter(str.isalpha, matiere))  # Ex: "GCGP", "GEER", "ST"
        code = ''.join(filter(str.isdigit, matiere))  # Ex: "11", "31", "41"

        if len(code) < 2:
            continue  # Évite les erreurs si le code est mal formé

        semestre_num = int(code[0])  # Ex: 1 → S1, 3 → S3
        semestre = f'S{semestre_num}'
        niveau = f'L{(semestre_num + 1) // 2}'  # Ex: S1, S2 → L1 | S3, S4 → L2

        if niveau in structured_data and semestre in structured_data[niveau]:
            structured_data[niveau][semestre].append({
                'code': matiere,
                'dept': dept,
                'numero': code[1]  # Deuxième chiffre pour différencier les matières
            })

    return render_template('parametres_admin.html', matieres=structured_data, user_A=user_A)



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