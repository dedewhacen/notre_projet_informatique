from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify,abort
import mysql.connector
from datetime import datetime, timezone, timedelta
from flask_wtf.csrf import CSRFProtect
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import bcrypt
import random
import logging
from flask_mail import Mail, Message
import smtplib
smtplib.SMTP_DEBUG = 1

app = Flask(__name__)
csrf = CSRFProtect(app)
# Configuration Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ismereclamation@gmail.com'
app.config['MAIL_PASSWORD'] = 'rtvi vxrd sqqm ohsu'
app.secret_key = 'votre_cle_secrete_tres_secrete'
mail = Mail(app)


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
        now = datetime.utcnow()
        # Supprimer uniquement les configurations expirées
        cursor.execute("DELETE FROM configuration_reclamation WHERE date_fermeture <= %s", (now,))
        conn.commit()
        print(f"Nettoyage des configurations à {now}")


scheduler.add_job(delete_expired_configs, 'interval', minutes=1)
atexit.register(lambda: scheduler.shutdown())
# Route de connexion (page de login)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['pwd']

        # Vérification dans la table user (admin)
        cursor.execute("SELECT email_admin, pwd_admin FROM user WHERE email_admin = %s", (email,))
        admin = cursor.fetchone()

        if admin and bcrypt.checkpw(pwd.encode('utf-8'), admin[1].encode('utf-8')):
            session['logged_in'] = True
            session['user_email'] = email
            session['role'] = 'admin'
            return redirect(url_for('admin_dashboard'))

        # Vérification dans la table etudiant (mot de passe en clair)
        cursor.execute("SELECT Email, pwd FROM etudiant WHERE Email = %s", (email,))
        user = cursor.fetchone()

        if user:
            stored_pwd = user[1]
            try:
                # Essai avec mot de passe hashé
                if bcrypt.checkpw(pwd.encode('utf-8'), stored_pwd.encode('utf-8')):
                    session['logged_in'] = True
                    session['user_email'] = email
                    session['role'] = 'etudiant'
                    return redirect(url_for('suivi_reclamations_etud'))
            except ValueError:
                # Si le mot de passe n'est pas hashé (en clair)
                if pwd == stored_pwd:
                    session['logged_in'] = True
                    session['user_email'] = email
                    session['role'] = 'etudiant'
                    return redirect(url_for('suivi_reclamations_etud'))

        # Si aucun ne correspond
        flash("Identifiants invalides. Veuillez réessayer.", "danger")

    return render_template('login.html')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

def email_exists(email):
    """Vérifie l'existence de l'email dans la base de données"""
    try:
        # Forcer la comparaison en lowercase
        cursor.execute("""
            SELECT LOWER(Email) FROM etudiant WHERE LOWER(Email) = LOWER(%s)
            UNION
            SELECT LOWER(email_admin) FROM user WHERE LOWER(email_admin) = LOWER(%s)
        """, (email, email))
        return cursor.fetchone() is not None
    except Exception as e:
        logging.error(f"Erreur base de données: {str(e)}")
        return False

# Modifier la fonction send_verification_email
def send_verification_email(email, otp):
    """Envoi d'email avec Flask-Mail"""
    try:

        msg = Message(
            subject="Réinitialisation de mot de passe - ISME",
            sender=("ISME Réclamations", app.config['MAIL_USERNAME']),  # Ajout du nom d'expéditeur
            recipients=[email],
            body=f"Votre code de vérification est : {otp}\nValable 10 minutes",
            html=f"""  # Ajout d'une version HTML
            <h3>Réinitialisation de mot de passe ISME</h3>
            <p>Votre code de vérification : <strong>{otp}</strong></p>
            <p>Valable pendant 10 minutes</p>
            """
        )
        mail.send(msg)
        logging.info(f"Email envoyé à {email}")
        return True
    except Exception as e:
        logging.error(f"Échec envoi email: {str(e)}", exc_info=True)  # Log détaillé
        return False


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()

        if not email:
            flash("Veuillez entrer une adresse email", "danger")
            return redirect(url_for('forgot_password'))

        if not email_exists(email):
            flash("Aucun compte associé à cette adresse email", "danger")
            return redirect(url_for('forgot_password'))

        # Génération et stockage OTP
        otp = ''.join(random.choices('0123456789', k=6))
        session.update({
            'reset_email': email,
            'reset_otp': otp,
            'reset_expires': (datetime.now() + timedelta(minutes=10)).isoformat(),
            'otp_verified': False
        })

        if send_verification_email(email, otp):
            flash("Code de vérification envoyé! Vérifiez vos emails.", "success")
            return redirect(url_for('verify_otp'))

        flash("Erreur lors de l'envoi du code. Veuillez réessayer.", "danger")

    return render_template('forgot_password.html')


@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    required_keys = ['reset_email', 'reset_otp', 'reset_expires']
    if not all(key in session for key in required_keys):
        flash("Session invalide. Veuillez recommencer.", "danger")
        return redirect(url_for('forgot_password'))

    try:
        expires = datetime.fromisoformat(session['reset_expires'])
        if datetime.now() > expires:
            session.clear()
            flash("Le code a expiré. Veuillez recommencer.", "danger")
            return redirect(url_for('forgot_password'))
    except ValueError:
        session.clear()
        flash("Erreur système. Veuillez réessayer.", "danger")
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        user_otp = request.form.get('otp', '').strip()

        if user_otp == session['reset_otp']:
            session['otp_verified'] = True
            session.pop('reset_otp')
            return redirect(url_for('reset_password'))

        flash("Code incorrect. Veuillez vérifier et réessayer.", "danger")

    remaining = (expires - datetime.now()).seconds // 60
    return render_template('verify_otp.html', remaining_time=remaining)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if not session.get('otp_verified'):
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        new_pwd = request.form.get('new_password')
        confirm_pwd = request.form.get('confirm_password')

        if new_pwd != confirm_pwd:
            flash("Les mots de passe ne correspondent pas", "danger")
            return redirect(url_for('reset_password'))

        hashed_pwd = bcrypt.hashpw(new_pwd.encode('utf-8'), bcrypt.gensalt())
        email = session['reset_email']

        try:
            # Mise à jour prioritaire admin
            cursor.execute("UPDATE user SET pwd_admin = %s WHERE email_admin = %s",
                           (hashed_pwd.decode('utf-8'), email))

            if cursor.rowcount == 0:
                cursor.execute("UPDATE etudiant SET pwd = %s WHERE Email = %s",
                               (hashed_pwd.decode('utf-8'), email))

            conn.commit()
            session.clear()
            flash("Mot de passe réinitialisé avec succès!", "success")
            return redirect(url_for('login'))

        except Exception as e:
            conn.rollback()
            logging.error(f"Erreur mise à jour mot de passe: {str(e)}")
            flash("Erreur lors de la mise à jour. Veuillez réessayer.", "danger")

    return render_template('reset_password.html')
#Espace de l'admin

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
        matiere m ON r.code_mat = m.code_mat ORDER BY r.moment_de_creation DESC;;
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

#statistique
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


@app.route('/get_stats')
def get_stats():
    if not session.get('logged_in') or session.get('role') != 'admin':
        abort(403)

    try:
        # 1. Comptes de base
        cursor.execute("SELECT COUNT(*) FROM reclamation")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT statut, COUNT(*) FROM reclamation GROUP BY statut")
        status_counts = {'Accepté': 0, 'Refusé': 0, 'En attente': 0}
        for status, count in cursor.fetchall():
            status_counts[status] = count

        # 2. Top matières par niveau et semestre
        def get_top_matieres(level, semestre=None, limit=10):
            query = """
                SELECT r.code_mat, COUNT(*) as count 
                FROM reclamation r
                JOIN matiere m ON r.code_mat = m.code_mat
                WHERE m.niveau_de_licence = %s
            """
            params = [level]

            if semestre:
                query += " AND m.semestre = %s"
                params.append(semestre)

            query += """
                GROUP BY r.code_mat 
                ORDER BY count DESC 
                LIMIT %s
            """
            params.append(limit)

            cursor.execute(query, tuple(params))
            return [{'code_mat': row[0], 'count': row[1]} for row in cursor.fetchall()]

        # Pour chaque niveau: semestre impair, pair et global
        stats = {
            'L1': {
                'impair': get_top_matieres('L1', 'S1', 5),
                'pair': get_top_matieres('L1', 'S2', 5),
                'global': get_top_matieres('L1', None, 5)
            },
            'L2': {
                'impair': get_top_matieres('L2', 'S3', 5),
                'pair': get_top_matieres('L2', 'S4', 5),
                'global': get_top_matieres('L2', None, 5)
            },
            'L3': {
                'impair': get_top_matieres('L3', 'S5', 5),
                'pair': [],  # L3 n'a pas de semestre pair
                'global': get_top_matieres('L3', None, 5)
            }
        }

        return jsonify({
            'total': total,
            'accepted': status_counts['Accepté'],
            'rejected': status_counts['Refusé'],
            'pending': status_counts['En attente'],
            'stats': stats
        })

    except Exception as e:
        app.logger.error(f"Error generating stats: {str(e)}")
        return jsonify({'error': 'Unable to generate statistics'}), 500
#parametre de l'dmin

# Paramètres du compte admin
@app.route('/parametres_compte_admin')
def parametres_compte_admin():
    cursor.execute("SELECT email_admin, pwd_admin FROM user WHERE email_admin = %s", (session['user_email'],))
    admin_data = cursor.fetchone()
    return render_template('parametres_compte_admin.html', admin=admin_data)


@app.route('/change_admin_password', methods=['POST'])
def change_admin_password():
    if 'user_email' not in session or session.get('role') != 'admin':
        flash("Accès non autorisé", "danger")
        return redirect(url_for('login'))

    old_pwd = request.form.get('old_password')
    new_pwd = request.form.get('new_password')
    confirm_pwd = request.form.get('confirm_password')

    # Vérification des champs
    if not all([old_pwd, new_pwd, confirm_pwd]):
        flash("Tous les champs sont requis", "danger")
        return redirect(url_for('parametres_compte_admin'))

    if new_pwd != confirm_pwd:
        flash("Les mots de passe ne correspondent pas", "danger")
        return redirect(url_for('parametres_compte_admin'))

    # Connexion à la base
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="gestion_des_reclamation"
        )
        cursor = conn.cursor()

        # Récupération du hash actuel
        cursor.execute("SELECT pwd_admin FROM user WHERE email_admin = %s", (session['user_email'],))
        result = cursor.fetchone()

        if not result:
            flash("Compte administrateur introuvable", "danger")
            return redirect(url_for('parametres_compte_admin'))

        current_hash = result[0]

        # Vérification ancien mot de passe
        if not bcrypt.checkpw(old_pwd.encode('utf-8'), current_hash.encode('utf-8')):
            flash("Ancien mot de passe incorrect", "danger")
            return redirect(url_for('parametres_compte_admin'))

        # Validation nouveau mot de passe
        if len(new_pwd) < 8 or not any(c.isupper() for c in new_pwd) or not any(c.isdigit() for c in new_pwd):
            flash("Le mot de passe doit contenir 8+ caractères, 1 majuscule et 1 chiffre", "danger")
            return redirect(url_for('parametres_compte_admin'))

        # Génération nouveau hash
        new_hash = bcrypt.hashpw(new_pwd.encode('utf-8'), bcrypt.gensalt())

        # Mise à jour
        cursor.execute(
            "UPDATE user SET pwd_admin = %s WHERE email_admin = %s",
            (new_hash.decode('utf-8'), session['user_email'])
        )

        if cursor.rowcount == 0:
            flash("Aucun compte trouvé pour la mise à jour", "danger")
        else:
            conn.commit()
            flash("Mot de passe mis à jour avec succès", "success")

    except mysql.connector.Error as err:
        flash(f"Erreur base de données: {err}", "danger")
        conn.rollback()
    except Exception as e:
        flash(f"Erreur inattendue: {str(e)}", "danger")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

    return redirect(url_for('parametres_compte_admin'))
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

#save configuration
@app.route('/save-config', methods=['POST'])
def save_config():
    if not session.get('logged_in') or session.get('role') != 'admin':
        return jsonify(error="Accès non autorisé"), 403

    try:
        configs = request.get_json()
        print("Données reçues:", configs)  # Debug
        current_time = datetime.utcnow()
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
                new_close_date = datetime.fromisoformat(
                    config['date_fermeture'].replace('Z', '')
                ).replace(tzinfo=None)
            except ValueError:
                try:
                    # Fallback pour les dates sans timezone
                    new_close_date = datetime.fromisoformat(date_fermeture_str).replace(tzinfo=timezone.utc)
                except ValueError:
                    errors.append(f"Format de date invalide pour {niveau}")
                    continue

            # Vérification durée minimale
            if new_close_date < current_time :
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
        # Étape 1 : Désassocier les réclamations de la configuration
        cursor.execute("""
            UPDATE reclamation 
            SET config_id = NULL 
            WHERE config_id = %s
        """, (id,))

        # Étape 2 : Supprimer la configuration
        cursor.execute("DELETE FROM configuration_reclamation WHERE id = %s", (id,))

        conn.commit()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(success=True)
        else:
            flash("Configuration supprimée (réclamations conservées)", "success")
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

#compt a rebous
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

#Espace etudiant
@app.route('/suivi_reclamations_etud')
def suivi_reclamations_etud():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    email = session.get('user_email')
    if not email:
        flash("Session invalide", "danger")
        return redirect(url_for('login'))

    # Récupération des infos étudiant
    cursor.execute(
        "SELECT matricule_etd, Email, Licence, Departement FROM etudiant WHERE Email = %s",
        (email,))
    etudiant_data = cursor.fetchone()

    if not etudiant_data:
        flash("Étudiant introuvable", "danger")
        return redirect(url_for('login'))

    matricule, email_etd, niveau, departement = etudiant_data

    # Récupération de la configuration active
    cursor.execute(
        """SELECT id, code_mat, date_fermeture 
        FROM configuration_reclamation 
        WHERE niveau = %s AND date_fermeture > NOW()
        ORDER BY date_fermeture DESC LIMIT 1""",
        (niveau,))
    config_active = cursor.fetchone()

    current_config_id = config_active[0] if config_active else None
    date_fermeture = config_active[2] if config_active else None
    matieres_config = config_active[1].split(',') if config_active else []

    # Calcul de l'expiration
    is_expired = True
    if date_fermeture:
        now = datetime.now(timezone.utc)
        if date_fermeture.tzinfo is None:
            date_fermeture = date_fermeture.replace(tzinfo=timezone.utc)
        is_expired = now > date_fermeture

    # Récupération des matières disponibles
    available_matieres = []
    claimed_matieres = []

    if config_active and matieres_config:
        placeholders = ','.join(['%s'] * len(matieres_config))
        cursor.execute(
            f"""SELECT m.code_mat, m.dept_mat 
            FROM matiere m
            WHERE m.code_mat IN ({placeholders})
            AND (m.dept_mat = %s OR m.dept_mat = 'COMN')
            AND m.niveau_de_licence = %s""",
            (*matieres_config, departement, niveau))

        available_mats = cursor.fetchall()
        available_codes = [row[0] for row in available_mats]
        dept_mapping = {row[0]: row[1] for row in available_mats}  # Stocke code_mat -> dept_mat

        # Récupération des réclamations existantes
        cursor.execute(
            """SELECT code_mat FROM reclamation 
            WHERE matricule_etd = %s AND config_id = %s""",
            (matricule, current_config_id))
        claimed_matieres = [row[0] for row in cursor.fetchall()]

        # Construction de la liste des matières
        for code in available_codes:
            available_matieres.append({
                'code': code,
                'dept': dept_mapping[code],  # Ajout du département
                'claimed': code in claimed_matieres
            })

    # Récupération des réclamations
    cursor.execute(
        """SELECT id_rec, Détails, Objet_rec, 
           moment_de_creation, code_mat, statut, config_id 
        FROM reclamation 
        WHERE matricule_etd = %s
        ORDER BY moment_de_creation DESC""",
        (matricule,))

    reclamations = []
    for rec in cursor.fetchall():
        reclamations.append({
            'id_rec': rec[0],
            'details': rec[1],
            'objet': rec[2],
            'date_creation': rec[3],
            'matiere': rec[4],
            'statut': rec[5],
            'config_id': rec[6],
            'is_current': rec[6] == current_config_id
        })

    return render_template(
        'suivi_reclamations_etud.html',
        etudiant=etudiant_data,
        matieres=available_matieres,
        claimed_matieres=claimed_matieres,
        reclamations=reclamations,
        current_config_id=current_config_id,
        is_expired=is_expired,
        date_fermeture=date_fermeture,
        current_time=datetime.now()
    )


@app.route('/supprimer_reclamation/<int:id_rec>', methods=['POST'])
def supprimer_reclamation(id_rec):
    cursor.execute("DELETE FROM reclamation WHERE id_rec = %s", (id_rec,))
    conn.commit()
    return redirect(url_for('suivi_reclamations_etud'))



@app.route('/etudiant', methods=['POST'])
def etudiant():
    if not session.get('logged_in') or session.get('role') != 'etudiant':
        flash("Accès non autorisé", "danger")
        return redirect(url_for('login'))

    try:
        # Récupération des infos étudiant
        email = session['user_email']
        cursor.execute(
            "SELECT matricule_etd, Licence, Departement FROM etudiant WHERE Email = %s",
            (email,))
        etudiant_data = cursor.fetchone()

        if not etudiant_data:
            flash("Profil étudiant introuvable", "danger")
            return redirect(url_for('suivi_reclamations_etud'))

        matricule, niveau, departement = etudiant_data

        # Vérification configuration active
        cursor.execute(
            """SELECT id, code_mat, date_fermeture 
            FROM configuration_reclamation 
            WHERE niveau = %s AND date_fermeture > UTC_TIMESTAMP()
            ORDER BY date_fermeture DESC LIMIT 1""",
            (niveau,))
        config_active = cursor.fetchone()

        if not config_active:
            flash("Aucune période de réclamation active", "danger")
            return redirect(url_for('suivi_reclamations_etud'))

        current_config_id, matieres_config, date_fermeture = config_active
        matieres_list = matieres_config.split(',')

        # Validation des données du formulaire
        matiere_code = request.form.get('matiere')
        objets = request.form.getlist('objet')  # Récupération multiple
        details = request.form.get('details', '').strip()

        # Vérification des champs obligatoires
        if not matiere_code or len(objets) == 0:
            flash("Tous les champs obligatoires doivent être remplis", "danger")
            return redirect(url_for('suivi_reclamations_etud'))

        # Conversion en chaîne séparée par des virgules
        objet_str = ', '.join(objets)

        # Vérification matière valide
        cursor.execute(
            """SELECT code_mat, dept_mat 
            FROM matiere 
            WHERE code_mat = %s 
            AND code_mat IN ({})
            AND (dept_mat = %s OR dept_mat = 'COMN')"""
            .format(','.join(['%s'] * len(matieres_list))),
            [matiere_code] + matieres_list + [departement])

        matiere = cursor.fetchone()
        if not matiere:
            flash("Matière non valide pour ce département", "danger")
            return redirect(url_for('suivi_reclamations_etud'))

        # Vérification types de réclamation autorisés
        dept_mat = matiere[1]
        types_autorises = ['Devoir', 'Examen', 'TP'] if dept_mat in ('GCGP', 'GEER') else ['Devoir', 'Examen']

        if not all(item in types_autorises for item in objets):
            flash(
                f"Type(s) de réclamation non autorisé(s) pour cette matière. Choix valides : {', '.join(types_autorises)}",
                "danger")
            return redirect(url_for('suivi_reclamations_etud'))

        # Vérification réclamation existante
        cursor.execute(
            """SELECT id_rec 
            FROM reclamation 
            WHERE matricule_etd = %s 
            AND code_mat = %s 
            AND config_id = %s""",
            (matricule, matiere_code, current_config_id))

        if cursor.fetchone():
            flash("Une réclamation existe déjà pour cette matière", "warning")
            return redirect(url_for('suivi_reclamations_etud'))

        # Insertion de la réclamation
        cursor.execute(
            """INSERT INTO reclamation 
            (Détails, Objet_rec, moment_de_creation,
             matricule_etd, code_mat, config_id, statut)
            VALUES (%s, %s, UTC_TIMESTAMP(), %s, %s, %s, 'En attente')""",
            (details, objet_str, matricule, matiere_code, current_config_id))

        conn.commit()
        flash("Réclamation enregistrée avec succès !", "success")

    except mysql.connector.Error as err:
        conn.rollback()
        app.logger.error(f"Erreur base de données: {err}")
        flash("Erreur lors de l'enregistrement de la réclamation", "danger")
    except Exception as e:
        conn.rollback()
        app.logger.error(f"Erreur inattendue: {str(e)}")
        flash("Une erreur critique est survenue", "danger")

    return redirect(url_for('suivi_reclamations_etud'))


@app.route('/modifier_reclamation/<int:id_rec>', methods=['POST'])
def modifier_reclamation(id_rec):
    if not session.get('logged_in') or session.get('role') != 'etudiant':
        flash("Accès non autorisé", "danger")
        return redirect(url_for('login'))

    try:
        # Vérifier la période de modification
        cursor.execute("""
            SELECT c.date_fermeture 
            FROM reclamation r
            LEFT JOIN configuration_reclamation c ON r.config_id = c.id
            WHERE r.id_rec = %s
        """, (id_rec,))
        result = cursor.fetchone()

        if result and result[0] < datetime.utcnow():
            flash("La période de modification est expirée", "danger")
            return redirect(url_for('suivi_reclamations_etud'))

        # Récupération des données
        nouvelle_matiere = request.form.get('matiere')
        nouveaux_details = request.form.get('details', '').strip()
        nouvel_objet = ', '.join(request.form.getlist('objet'))

        # Vérification de la matière
        cursor.execute("""
            SELECT code_mat 
            FROM matiere 
            WHERE code_mat = %s
            AND niveau_de_licence = (
                SELECT Licence FROM etudiant WHERE Email = %s
            )
        """, (nouvelle_matiere, session['user_email']))

        if not cursor.fetchone():
            flash("Matière non valide pour votre niveau", "danger")
            return redirect(url_for('suivi_reclamations_etud'))

        # Mise à jour
        cursor.execute("""
            UPDATE reclamation 
            SET code_mat = %s,
                Détails = %s,
                Objet_rec = %s 
            WHERE id_rec = %s
            AND matricule_etd = (SELECT matricule_etd FROM etudiant WHERE Email = %s)
        """, (nouvelle_matiere, nouveaux_details, nouvel_objet, id_rec, session['user_email']))

        if cursor.rowcount == 0:
            flash("Aucune modification effectuée", "warning")
        else:
            conn.commit()
            flash("Réclamation modifiée avec succès", "success")

    except mysql.connector.Error as err:
        conn.rollback()
        flash(f"Erreur base de données : {err.msg}", "danger")
    except Exception as e:
        conn.rollback()
        flash(f"Erreur inattendue : {str(e)}", "danger")

    return redirect(url_for('suivi_reclamations_etud'))
#parametre de compt etudiant
# Modifier la route existante
@app.route('/parametres', methods=['GET'])
def parametres():
    email = session.get('user_email')
    if not email or 'user_email' not in session:
        return redirect(url_for('login'))

    cursor.execute("SELECT Email, pwd FROM etudiant WHERE Email = %s", (session['user_email'],))
    user = cursor.fetchone()
    return render_template('parametres.html', user=user)


# Ajouter une nouvelle route pour le traitement
@app.route('/change_student_password', methods=['POST'])
def change_student_password():
    if 'user_email' not in session or session.get('role') != 'etudiant':
        flash("Accès non autorisé", "danger")
        return redirect(url_for('login'))

    old_pwd = request.form.get('old_password')
    new_pwd = request.form.get('new_password')
    confirm_pwd = request.form.get('confirm_password')

    if not all([old_pwd, new_pwd, confirm_pwd]):
        flash("Tous les champs sont requis", "danger")
        return redirect(url_for('parametres'))

    if new_pwd != confirm_pwd:
        flash("Les mots de passe ne correspondent pas", "danger")
        return redirect(url_for('parametres'))

    try:
        # Récupération du mot de passe actuel
        cursor.execute("SELECT pwd FROM etudiant WHERE Email = %s", (session['user_email'],))
        result = cursor.fetchone()

        if not result:
            flash("Compte étudiant introuvable", "danger")
            return redirect(url_for('parametres'))

        stored_pwd = result[0]

        # Vérification ancien mot de passe
        try:
            if not bcrypt.checkpw(old_pwd.encode('utf-8'), stored_pwd.encode('utf-8')):
                flash("Ancien mot de passe incorrect", "danger")
                return redirect(url_for('parametres'))
        except ValueError:
            # Gestion des mots de passe en clair
            if old_pwd != stored_pwd:
                flash("Ancien mot de passe incorrect", "danger")
                return redirect(url_for('parametres'))

        # Validation nouveau mot de passe
        if len(new_pwd) < 8 or not any(c.isupper() for c in new_pwd) or not any(c.isdigit() for c in new_pwd):
            flash("Le mot de passe doit contenir 8+ caractères, 1 majuscule et 1 chiffre", "danger")
            return redirect(url_for('parametres'))

        # Hashage et mise à jour
        new_hash = bcrypt.hashpw(new_pwd.encode('utf-8'), bcrypt.gensalt())
        cursor.execute(
            "UPDATE etudiant SET pwd = %s WHERE Email = %s",
            (new_hash.decode('utf-8'), session['user_email']))
        conn.commit()

        flash("Mot de passe mis à jour avec succès", "success")
        return redirect(url_for('parametres'))

    except Exception as e:
        conn.rollback()
        flash(f"Erreur : {str(e)}", "danger")
        return redirect(url_for('parametres'))





@app.route('/logout')
def logout():
    # Supprime toutes les données de session
    session.clear()
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(debug=True)