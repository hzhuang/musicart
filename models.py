import sqlite3

def get_composers():
    conn = sqlite3.connect('music_terms.db')
    c = conn.cursor()
    c.execute("SELECT * FROM composers")
    composers = [{'id': row[0], 'name': row[1], 'bio': row[2]} for row in c.fetchall()]
    conn.close()
    return composers

def get_review_terms():
    conn = sqlite3.connect('music_terms.db')
    c = conn.cursor()
    c.execute('''SELECT review_list.*, terms.term, terms.definition 
               FROM review_list 
               JOIN terms ON review_list.term_id = terms.id''')
    reviews = [dict(row) for row in c.fetchall()]
    conn.close()
    return reviews