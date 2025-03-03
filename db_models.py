import json
import sqlite3
from datetime import datetime

def init_db():
    """ Crée les tables dans la base de données si elles n'existent pas """
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()

    # Table pour stocker tous les messages
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            role TEXT,
            message TEXT,
            timestamp TEXT
        )
    ''')

    # Table pour stocker uniquement les événements choquants
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detection_tls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            role_detection TEXT,
            event_type TEXT,
            message TEXT,
            timestamp TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS maladie_tbl (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            maladie_txt TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS liste_maladie_tbl (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            maladie_txt TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Appeler cette fonction une fois au démarrage
init_db()



def save_to_db(user_id, role, message):
    """ Enregistre un message dans la base de données """
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO messages (user_id, role, message, timestamp) VALUES (?, ?, ?, ?)", 
                   (user_id, role, message, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def save_detection_db(user_id, role_detection, message, event_type):
    """ Enregistre un événement choquant dans la base de données """
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO detection_tls (user_id, role_detection, event_type, message, timestamp) VALUES (?, ?, ?, ?, ?)", 
                   (user_id,role_detection, event_type, message, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

# def get_chat_maladie(user_id):
#     """ Récupère l'historique des messages d'un utilisateur pour les maladies détectées,
#         sans doublons, et construit une chaîne de texte.
#     """
#     conn = sqlite3.connect("chat_history.db")
#     cursor = conn.cursor()
    
#     cursor.execute(
#         "SELECT role, message, timestamp FROM messages WHERE user_id = ? AND role = 'MALADIE' ORDER BY timestamp", 
#         (user_id,)
#     )
#     history = cursor.fetchall()
#     list_maladie_potentielle = None

#     if history:
#         # Utiliser une liste pour conserver l'ordre d'apparition et un set pour détecter les doublons (insensible à la casse)
#         unique_maladies = []
#         seen = set()
#         for row in history:
#             maladie = row[1].strip()
#             key = maladie.lower()  # pour ignorer la casse lors de la comparaison
#             if key not in seen:
#                 seen.add(key)
#                 unique_maladies.append(maladie)
        
#         # Construire la chaîne de résultat
#         list_maladie_potentielle = "Prenez en considération la liste des maladies potentielles suivantes, que l'utilisateur peut avoir:"
#         for maladie in unique_maladies:
#             list_maladie_potentielle += f"\n- {maladie}"
    
#     conn.close()
#     return list_maladie_potentielle

def save_maladie_db(user_id,maladie):
    """ Enregistre une maladie de dans la base de données """
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO maladie_tbl (user_id, maladie_txt) VALUES (?, ?)", 
                   (user_id,maladie))
    
    conn.commit()
    conn.close()

def save_maladie_potentiel_db(user_id,maladie):
    """ Enregistre une maladie de dans la base de données """
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO liste_maladie_tbl (user_id, maladie_txt) VALUES (?, ?)", 
                   (user_id,maladie))
    
    conn.commit()
    conn.close()


def get_choc(user_id):
    """ Récupère l'historique des choques émotionnel de  l'utilisateur """
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT event_type, message, timestamp FROM detection_tls WHERE user_id = ? AND role_detection = 'CHOC' ORDER BY timestamp;", (user_id,))
    history = cursor.fetchall()
    list_choque_emotionnelle = None
    if history:
        list_choque_emotionnelle = "\nVoici la liste des choques émotionnel déja déclaré par l'utilisateur trié par date: "
        for row in history:
            list_choque_emotionnelle += f"\n- Date  : {row[2]}, Type de choc : {row[0]}, Message : {row[1]}"
        
    conn.close()
    return list_choque_emotionnelle or ''

def get_souvenir(user_id):
    """ Récupère l'historique des choques émotionnel de  l'utilisateur """
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT event_type, message, timestamp FROM detection_tls WHERE user_id = ? AND role_detection = 'SOUVENIR' ORDER BY timestamp;", (user_id,))
    history = cursor.fetchall()
    list_choque_emotionnelle = None
    if history:
        list_choque_emotionnelle = "\nVoici la liste des souvenir déja déclaré par l'utilisateur trié par date: "
        for row in history:
            list_choque_emotionnelle += f"\n- Date  : {row[2]}, Type de choc : {row[0]}, Message : {row[1]}"
        
    conn.close()
    return list_choque_emotionnelle or ''

def get_preference(user_id):
    """ Récupère l'historique des choques émotionnel de  l'utilisateur """
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT event_type, message, timestamp FROM detection_tls WHERE user_id = ? AND role_detection = 'PREFERENCE' ORDER BY timestamp;", (user_id,))
    history = cursor.fetchall()
    list_choque_emotionnelle = None
    if history:
        list_choque_emotionnelle = "\nVoici la liste des préférences déja déclaré par l'utilisateur trié par date: "
        for row in history:
            list_choque_emotionnelle += f"\n- Date  : {row[2]}, Type de choc : {row[0]}, Message : {row[1]}"
        
    conn.close()
    return list_choque_emotionnelle or ''

def get_maladie(user_id):
    """ Récupère l'historique des choques émotionnel de  l'utilisateur """
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT event_type, message, timestamp FROM detection_tls WHERE user_id = ? AND role_detection = 'MALADIE' ORDER BY timestamp;", (user_id,))
    history = cursor.fetchall()
    list_choque_emotionnelle = None
    if history:
        list_choque_emotionnelle = "\n Prenez en considération la liste des maladies potentielles suivantes, que l'utilisateur peut avoir: "
        for row in history:
            list_choque_emotionnelle += f"\n- Date  : {row[2]}, Type de choc : {row[0]}, Message : {row[1]}"
        
    conn.close()
    return list_choque_emotionnelle or ''

import sqlite3

def get_chat_history(user_id):
    """ Fetch the chat history for a user from the database. """
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()

    cursor.execute("SELECT role, message, timestamp FROM messages WHERE user_id = ? ORDER BY timestamp;", (user_id))
    history = cursor.fetchall()
    
    conn.close()

    # Convert to a list of dictionaries
    return [{"role": row[0], "message": row[1], "timestamp": row[2]} for row in history]


def get_last_history(user_id):
    """ Récupère l'historique des110 derniers messages entre l'utilisateur et le bot """
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT role, message, timestamp FROM (SELECT role, message, timestamp FROM messages WHERE user_id = ? ORDER BY timestamp DESC LIMIT 10) sub ORDER BY timestamp;", (user_id,))
    history = cursor.fetchall()
    list_choque_emotionnelle = None
    if history:
        list_choque_emotionnelle = "\n Voici les dix derniers messages échangés entre l'utilisateur et vous: "
        for row in history:
            list_choque_emotionnelle += f"\n- Role  : {row[0]}, Message : {row[1]}"
        
    conn.close()
    return list_choque_emotionnelle or ''

def get_desease(user_id):
    """ Récupère la maladie de l'utilisateur """
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT maladie_txt FROM maladie_tbl WHERE user_id = ? ORDER BY id DESC LIMIT 1;", 
        (user_id,)
    )
    dernier_maladie = cursor.fetchone()  # Récupérer le dernier enregistrement
    conn.close()
    return dernier_maladie[0] if dernier_maladie else ""

def get_maladie_potentiel(user_id):
    """ Récupère la liste des maladies potentiel de l'utilisateur """
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT maladie_txt FROM liste_maladie_tbl WHERE user_id = ?", (user_id,)) 
    history = cursor.fetchall()
    list_maladie_potentiel= history
    conn.close()
    return list_maladie_potentiel or []

def delete_list_maladie(user_id,maladie):
    """ Supprime la liste des maladies potentiel de l'utilisateur """
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM liste_maladie_tbl WHERE user_id = ? and maladie_txt <> ?", (user_id,maladie)) 
    conn.commit()
    conn.close()


def get_count_potential_desease(user_id):
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) from liste_maladie_tbl lmt WHERE user_id = ?;", (user_id,))
    history = cursor.fetchall()
    conn.commit()
    conn.close()
    return history[0][0] if history else ""

def get_top_desease(user_id):
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()

    query = """
    WITH maladie_counts AS (
        SELECT maladie_txt, COUNT(*) AS occurrence
        FROM liste_maladie_tbl
        WHERE user_id = ?
        GROUP BY maladie_txt
    )
    SELECT maladie_txt, occurrence
    FROM maladie_counts;
    """

    cursor.execute(query, (user_id,))
    history = cursor.fetchall()
    conn.close()

    if not history:
        return ""

    # Trouver le maximum d'occurrences
    max_occurrence = max(history, key=lambda x: x[1])[1]

    # Filtrer les maladies qui ont ce maximum
    top_diseases = [row[0] for row in history if row[1] == max_occurrence]

    # Retourner la maladie seulement s'il y en a une seule en tête
    return top_diseases[0] if len(top_diseases) == 1 else "not yet"


