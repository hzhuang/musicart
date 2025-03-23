# # Simple in-memory database (no SQL)
# terms = [
#     {"id": 1, "name": "Sonata", "definition": "Multi-movement work"},
#     {"id": 2, "name": "Nocturne", "definition": "Night-inspired piece"}
# ]

# composers = [
#     {"id": 1, "name": "Beethoven", "era": "Classical/Romantic"},
#     {"id": 2, "name": "Chopin", "era": "Romantic"}
# ]

# review_list = []  # Will store term IDs


import sqlite3

def get_terms(search=None):
    conn = sqlite3.connect('music.db')
    c = conn.cursor()
    c.execute("SELECT * FROM terms")
    terms = c.fetchall()
    conn.close()
    return terms

def insert_term(term, definition):
    conn = sqlite3.connect('music.db')
    c = conn.cursor()
    c.execute("INSERT INTO terms (term, definition) VALUES (?, ?);", (term, definition))
    conn.commit()  # Ensure the insertion is saved
    return c.lastrowid  # Get the auto-generated ID of the inserted row

def get_composers():
    conn = sqlite3.connect('music.db')
    c = conn.cursor()
    c.execute("SELECT * FROM composers")
    composers = c.fetchall()
    conn.close()
    return composers


def insert_composer(name, bio, audio_path):
    conn = sqlite3.connect('music.db')
    c = conn.cursor()
    c.execute("INSERT INTO composers (name, bio, audio_path) VALUES (?, ?, ?);", (name, bio, audio_path))
    conn.commit()  # Ensure the insertion is saved
    return c.lastrowid  # Get the auto-generated ID of the inserted row

def get_term_by_id(term_id):
    conn = sqlite3.connect('music.db')
    c = conn.cursor()
    c.execute("SELECT * FROM terms WHERE id=?", (term_id,))
    term = c.fetchone()
    conn.close()
    return term

def get_composer_by_id(composer_id):
    conn = sqlite3.connect('music.db')
    c = conn.cursor()
    c.execute("SELECT * FROM composers WHERE id=?", (composer_id,))
    composer = c.fetchone()
    conn.close()
    return composer

def insert_to_review(reference_id, category, term_name, definition_bio, your_answer):
    conn = sqlite3.connect('music.db')
    c = conn.cursor()
    c.execute("INSERT INTO review_list (reference_id, category, term_name, definition_bio, your_answer) VALUES (?, ?, ?, ?, ?);", (reference_id, category, term_name, definition_bio, your_answer))
    conn.commit()  # Ensure the insertion is saved
    return c.lastrowid  # Get the auto-generated ID of the inserted row


def get_reviews():
    conn = sqlite3.connect('music.db')
    c = conn.cursor()
    c.execute("SELECT * FROM review_list")
    reviews = c.fetchall()
    conn.close()
    return reviews

def delete_review(review_id):
    conn = sqlite3.connect('music.db')
    c = conn.cursor()
    print(f"Checking: {review_id}")
    c.execute("DELETE FROM review_list WHERE id = ?", (review_id,))
    conn.commit()
    conn.close()