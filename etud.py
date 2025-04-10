from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify,abort
import mysql.connector
from datetime import datetime, timezone, timedelta
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = 'votre_cle_secrete_tres_secrete'

# Connexion à la base de données
conn = mysql.connector.connect(
    host="localhost",
    user="root",       # Remplacez par votre utilisateur MySQL
    password="",       # Remplacez par votre mot de passe MySQL
    database="gestion_des_reclamation"
)
cursor = conn.cursor()
# Configuration du scheduler pour la suppression automatique
scheduler = BackgroundScheduler()
scheduler.start()

def delete_expired_configs():
    with app.app_context():
        now = datetime.now(timezone.utc)
        cursor.execute("DELETE FROM configuration_reclamation WHERE date_fermeture <= %s", (now,))
        conn.commit()
        print(f"Suppression automatique effectuée à {now}")

scheduler.add_job(delete_expired_configs, 'interval', minutes=1)
atexit.register(lambda: scheduler.shutdown())
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
        r.id_rec,
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
            'id_rec':row[0],
            'email': row[1],
            'matricule': row[2],
            'matiere': row[3],
            'departement': row[4],
            'niveau': row[5],
            'statut': row[6],
            'date_creation': row[7],
            'objet': row[8],
            'details': row[9]
        })

    cursor.execute("SELECT DISTINCT code_mat FROM reclamation")
    matieres = [row[0] for row in cursor.fetchall()]

    return render_template('admin.html',
                           reclamations=reclamations,
                           matieres=matieres)

@app.route('/suivi_reclamations_etud')
def suivi_reclamations_etud():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    email = session.get('user_email')
    if not email:
        flash("Erreur : aucune session utilisateur détectée.", "danger")
        return redirect(url_for('login'))

    # Récupération des infos étudiant
    cursor.execute("SELECT matricule_etd, Licence FROM etudiant WHERE Email = %s", (email,))
    result = cursor.fetchone()
    if not result:
        flash("Aucun étudiant trouvé avec cet email.", "warning")
        return redirect(url_for('login'))

    matricule, niveau_etudiant = result

    # Récupération des réclamations
    cursor.execute("""
        SELECT id_rec, Détails, Objet_rec, moment_de_creation, code_mat, statut 
        FROM reclamation 
        WHERE matricule_etd = %s
    """, (matricule,))
    reclamations = cursor.fetchall()

    # Configuration active
    cursor.execute("""
        SELECT date_fermeture 
        FROM configuration_reclamation 
        WHERE niveau = %s 
        AND date_fermeture > NOW()
        ORDER BY date_fermeture DESC 
        LIMIT 1
    """, (niveau_etudiant,))
    config_active = cursor.fetchone()

    date_fermeture = config_active[0] if config_active else None
    now = datetime.now(timezone.utc)
    is_expired = True  # Par défaut considéré comme expiré

    if date_fermeture:
        # Conversion en datetime aware si nécessaire
        if date_fermeture.tzinfo is None:
            date_fermeture = date_fermeture.replace(tzinfo=timezone.utc)
        is_expired = now > date_fermeture

    return render_template('suivi_reclamations_etud.html',
                           reclamations=reclamations,
                           date_fermeture=date_fermeture,
                           is_expired=is_expired)


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
    if not email or 'user_email' not in session:
        return redirect(url_for('login'))

    try:
        # Récupération des infos étudiant
        cursor.execute(
            "SELECT matricule_etd, Email, Licence, Departement FROM etudiant WHERE Email = %s",
            (email,)
        )
        etudiant_data = cursor.fetchone()
        if not etudiant_data:
            flash("Profil étudiant introuvable", "danger")
            return redirect(url_for('login'))

        matricule, _, niveau, departement = etudiant_data

        # Récupération des matières déjà réclamées
        cursor.execute(
            "SELECT code_mat FROM reclamation WHERE matricule_etd = %s",
            (matricule,)
        )
        claimed_matieres = [row[0] for row in cursor.fetchall()]

        # Récupération des matières disponibles
        available_matieres = []
        cursor.execute(
            """SELECT code_mat FROM configuration_reclamation
            WHERE niveau = %s ORDER BY date_fermeture DESC LIMIT 1""",
            (niveau,)
        )
        config = cursor.fetchone()

        if config and config[0]:
            matieres_list = config[0].split(',')
            placeholders = ','.join(['%s'] * len(matieres_list))

            cursor.execute(
                f"""SELECT m.code_mat, m.dept_mat 
                FROM matiere m
                WHERE m.code_mat IN ({placeholders})
                AND (m.dept_mat = %s OR m.dept_mat = 'COMN')
                AND m.niveau_de_licence = %s""",
                (*matieres_list, departement, niveau)
            )
            for row in cursor.fetchall():
                available_matieres.append({
                    'code': row[0],
                    'dept': row[1],
                    'claimed': row[0] in claimed_matieres
                })

        # Traitement du formulaire
        if request.method == 'POST':
            matiere_code = request.form.get('matiere')
            objet = request.form.get('objet')

            # Vérification préalable de la matière
            if not matiere_code or matiere_code in claimed_matieres:
                flash("Cette matière a déjà fait l'objet d'une réclamation", "danger")
                return redirect(url_for('etudiant'))

            # Validation des champs
            required_fields = ['matricule', 'details']
            if not all(request.form.get(field) for field in required_fields):
                flash("Tous les champs obligatoires doivent être remplis", "danger")
                return redirect(url_for('etudiant'))

            # Validation du type de réclamation
            cursor.execute(
                "SELECT dept_mat FROM matiere WHERE code_mat = %s",
                (matiere_code,)
            )
            matiere_dept = cursor.fetchone()

            if not matiere_dept:
                flash("Matière invalide", "danger")
                return redirect(url_for('etudiant'))

            matiere_dept = matiere_dept[0]
            allowed_types = ['Devoir', 'Examen', 'TP'] if matiere_dept in ('GCGP', 'GEER') else ['Devoir', 'Examen']

            if objet not in allowed_types:
                flash("Type de réclamation non autorisé pour cette matière", "danger")
                return redirect(url_for('etudiant'))

            # Insertion en base
            try:
                cursor.execute(
                    """INSERT INTO reclamation 
                    (Détails, Objet_rec, moment_de_creation, matricule_etd, code_mat)
                    VALUES (%s, %s, %s, %s, %s)""",
                    (request.form['details'],
                     objet,
                     datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                     matricule,
                     matiere_code)
                )
                conn.commit()
                flash("Réclamation enregistrée avec succès!", "success")
                return redirect(url_for('suivi_reclamations_etud'))

            except mysql.connector.IntegrityError as e:
                conn.rollback()
                if 'unique_reclamation' in str(e):
                    flash("Une réclamation existe déjà pour cette matière", "danger")
                else:
                    flash("Erreur de base de données", "danger")
                return redirect(url_for('etudiant'))

        return render_template(
            'page_etud.html',
            etudiant=etudiant_data,
            matieres=available_matieres,
            claimed_matieres=claimed_matieres,
            current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

    except Exception as e:
        conn.rollback()
        flash(f"Erreur inattendue: {str(e)}", "danger")
        app.logger.error(f"Erreur dans /etudiant: {str(e)}")
        return redirect(url_for('etudiant'))


# Modification de la route /save-config
# Route pour sauvegarder les configurations
@app.route('/save-config', methods=['POST'])
def save_config():
    if not session.get('logged_in') or session.get('role') != 'admin':
        return jsonify(error="Accès non autorisé"), 403

    try:
        configs = request.get_json()
        print("Données reçues:", configs)  # Debug
        current_time = datetime.now(timezone.utc)
        errors = []
        saved_configs = []

        for config in configs:
            # Extraction des paramètres avec vérification
            config_id = config.get('id')
            niveau = config.get('niveau')
            matieres = config.get('matieres', [])
            date_fermeture_str = config.get('date_fermeture')



            # Validation basique
            if not niveau or not matieres or not date_fermeture_str:
                errors.append("Champs manquants dans la configuration")
                continue

            # Conversion de la date
            try:
                new_close_date = datetime.fromisoformat(date_fermeture_str.replace('Z', '+00:00')).astimezone(
                    timezone.utc)
            except ValueError:
                try:
                    # Fallback pour les dates sans timezone
                    new_close_date = datetime.fromisoformat(date_fermeture_str).replace(tzinfo=timezone.utc)
                except ValueError:
                    errors.append(f"Format de date invalide pour {niveau}")
                    continue

            # Vérification durée minimale
            if new_close_date < current_time + timedelta(minutes=10):
                errors.append(f"Date trop proche pour {niveau} (min. 10 minutes)")
                continue

            # Vérification durée précédente
            cursor.execute("""
                SELECT date_fermeture 
                FROM configuration_reclamation 
                WHERE niveau = %s
                AND (%s IS NULL OR id != %s)
                ORDER BY date_fermeture DESC 
                LIMIT 1
            """, (niveau, config_id, config_id))

            last_config = cursor.fetchone()
            if last_config:
                last_close_date = last_config[0]
                if new_close_date >= last_close_date:
                    remaining_time = last_close_date - current_time
                    errors.append(
                        f"Durée pour {niveau} doit être plus courte que précédente "
                        f"({remaining_time.days} jours {remaining_time.seconds // 3600} heures)"
                    )
                    continue

            # Construction de la requête SQL
            if config_id:
                print(f"Mise à jour configuration {config_id}")  # D
                # Mode mise à jour
                cursor.execute("""
                            UPDATE configuration_reclamation 
                            SET niveau = %s,
                                code_mat = %s,
                                date_fermeture = %s
                            WHERE id = %s
                        """, (niveau, ','.join(matieres), new_close_date, config_id))
                action = "updated"
            else:
                print("Nouvelle configuration")
                # Nouvelle configuration
                cursor.execute("""
                    INSERT INTO configuration_reclamation 
                    (niveau, code_mat, date_fermeture)
                    VALUES (%s, %s, %s)
                """, (niveau, ','.join(matieres), new_close_date))
                config_id = cursor.lastrowid
                action = "created"

            saved_configs.append({"id": config_id, "action": action})

        if errors:
            conn.rollback()
            return jsonify({"status": "error", "errors": errors}), 400

        conn.commit()
        return jsonify({
            "status": "success",
            "message": f"{len(saved_configs)} configuration(s) sauvegardée(s)",
            "configs": saved_configs
        })

    except Exception as e:
        conn.rollback()
        app.logger.error(f"Erreur sauvegarde configuration: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Erreur serveur",
            "debug": str(e)
        }), 500


# Route pour supprimer une configuration
@app.route('/delete-config/<int:id>', methods=['POST'])
def delete_config(id):
    if not session.get('logged_in') or session.get('role') != 'admin':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(error="Accès non autorisé"), 403
        flash("Accès non autorisé", "danger")
        return redirect(url_for('login'))

    try:
        cursor.execute("DELETE FROM configuration_reclamation WHERE id = %s", (id,))
        conn.commit()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(success=True)
        else:
            flash("Configuration supprimée", "success")
            return redirect(url_for('parametres_admin'))

    except Exception as e:
        conn.rollback()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(error=str(e)), 500
        flash(f"Erreur : {str(e)}", "danger")
        return redirect(url_for('parametres_admin'))


@app.route('/last-duration/<niveau>')
def get_last_duration(niveau):
    cursor.execute("""
        SELECT date_fermeture 
        FROM configuration_reclamation 
        WHERE niveau = %s 
        ORDER BY date_fermeture DESC 
        LIMIT 1
    """, (niveau,))
    result = cursor.fetchone()

    if result:
        duration = result[0] - datetime.now(timezone.utc)
        return jsonify({
            'days': duration.days,
            'hours': duration.seconds // 3600
        })
    return jsonify({})
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
        FROM reclamation r
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
    if not session.get('logged_in') or session.get('role') != 'admin':
        return redirect(url_for('login'))

    email = session['user_email']
    cursor.execute("SELECT email_admin, pwd_admin FROM user WHERE email_admin = %s", (email,))
    user_A = cursor.fetchone()

    edit_id = request.args.get('edit_id')
    editing_config = None
    if edit_id:
        cursor.execute("""
                SELECT id, niveau, code_mat, date_fermeture 
                FROM configuration_reclamation 
                WHERE id = %s
            """, (edit_id,))
        config_row = cursor.fetchone()
        if config_row:
            editing_config = {
                'id': config_row[0],
                'niveau': config_row[1],
                'matieres': config_row[2].split(','),
                'date_fermeture': config_row[3].strftime('%Y-%m-%dT%H:%M')
            }

    # Récupération des données structurées depuis la base
    cursor.execute("""
        SELECT code_mat, dept_mat, niveau_de_licence, semestre 
        FROM matiere
        WHERE niveau_de_licence IS NOT NULL 
          AND semestre IS NOT NULL
          AND dept_mat IS NOT NULL
    """)
    matieres_data = cursor.fetchall()

    # Structure des données avec validation
    structured_data = {
        'L1': {'S1': [], 'S2': []},
        'L2': {'S3': [], 'S4': []},
        'L3': {'S5': []}
    }

    valid_semestres = {
        'L1': {'S1', 'S2'},
        'L2': {'S3', 'S4'},
        'L3': {'S5'}
    }

    for row in matieres_data:
        code_mat, dept_mat, niveau, semestre = row

        # Validation des données
        if niveau not in valid_semestres:
            continue
        if semestre not in valid_semestres[niveau]:
            continue

        # Extraction du numéro de matière depuis code_mat
        try:
            _, code_part = code_mat.split('_')
            numero = code_part[1] if len(code_part) > 1 else '0'
        except (ValueError, IndexError):
            numero = '0'

        structured_data[niveau][semestre].append({
            'code': code_mat,
            'dept': dept_mat,
            'numero': numero
        })
        # In parametres_admin route
        cursor.execute("""
            SELECT id, niveau, code_mat, date_fermeture 
            FROM configuration_reclamation 
            WHERE date_fermeture > %s
        """, (datetime.now(timezone.utc),))

        active_configs = []
        for row in cursor.fetchall():
            active_configs.append({
                'id': row[0],
                'niveau': row[1],
                'matieres': row[2].split(','),
                'date_fermeture': row[3]
            })

        edit_id = request.args.get('edit_id')
        editing_config = None
        if edit_id:
            cursor.execute("""
                    SELECT id, niveau, code_mat, date_fermeture 
                    FROM configuration_reclamation 
                    WHERE id = %s
                """, (edit_id,))
            config_row = cursor.fetchone()
            if config_row:
                editing_config = {
                    'id': config_row[0],
                    'niveau': config_row[1],
                    'matieres': config_row[2].split(','),
                    'date_fermeture': config_row[3].strftime('%Y-%m-%dT%H:%M')
                }

    return render_template('parametres_admin.html',
                           matieres=structured_data,
                           user_A=user_A,
                           active_configs=active_configs,datetime=datetime,editing_config=editing_config,
                           timedelta=timedelta)


@app.template_filter('time_remaining')
def time_remaining_filter(dt):
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    diff = dt - now
    if diff.total_seconds() <= 0:
        return "Expiré"
    hours = diff.seconds // 3600
    minutes = (diff.seconds % 3600) // 60
    return f"{hours}h {minutes:02d}m {diff.seconds % 60:02d}s restantes"
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


@app.route('/update_status', methods=['POST'])
def update_status():
    if not session.get('logged_in') or session.get('role') != 'admin':
        return jsonify(success=False, error="Unauthorized"), 403

    data = request.get_json()
    rec_id = data.get('reclamation_id')
    new_status = data.get('new_status')

    try:
        cursor.execute("""
            UPDATE reclamation 
            SET statut = %s 
            WHERE id_rec = %s
        """, (new_status, rec_id))
        conn.commit()
        return jsonify(success=True)
    except Exception as e:
        conn.rollback()
        return jsonify(success=False, error=str(e)), 500

@app.route('/logout')
def logout():
    # Supprime toutes les données de session
    session.clear()
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(debug=True)