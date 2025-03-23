from flask import Flask, render_template, request, redirect, url_for, session
import database
import random
from initialize_db import init_database
from routing import main

app = Flask(__name__)
app.secret_key = "super_secret_key"

init_database()

app.register_blueprint(main)

# Routes for static pages
@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/composer/<int:composer_id>')
def composer_detail(composer_id):
    composer = database.get_composer_by_id(composer_id)
    return render_template('composer_detail.html', composer=composer)

# Quiz Routes
@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/quiz/terms')
def quiz_terms():
    terms = database.get_terms()
    current_term = random.choice(terms)
    return render_template('quiz_terms.html', current_term=current_term)

@app.route('/quiz/composers')
def quiz_composers():
    composers = database.get_composers()
    current_composer = random.choice(composers)
    return render_template('quiz_composers.html', current_composer=current_composer)

@app.route('/quiz/terms', methods=['POST'])
def check_term_answer():
    user_answer = request.form.get('answer')
    term_id = request.form.get('term_id')
    term = database.get_term_by_id(term_id)
    
    if user_answer.lower() != term[1].lower():
        session.setdefault('review', []).append({
            'type': 'term',
            'term': term,
            'user_answer': user_answer
        })
    
    return redirect(url_for('quiz_terms'))

@app.route('/quiz/composers', methods=['POST'])
def check_composer_answer():
    user_answer = request.form.get('answer')
    composer_id = request.form.get('composer_id')
    composer = database.get_composer_by_id(composer_id)
    
    if user_answer.lower() != composer[1].lower():
        session.setdefault('review', []).append({
            'type': 'composer',
            'composer': composer,
            'user_answer': user_answer
        })
    
    return redirect(url_for('quiz_composers'))



if __name__ == '__main__':
    app.run(debug=True)






# Quiz system
@app.route('/quiz')
def quiz_start():
    session.clear()
    return render_template('quiz_start.html')

@app.route('/quiz/terms', methods=['GET', 'POST'])
def terms_quiz():
    if 'terms_queue' not in session:
        all_terms = [t[0] for t in database.get_terms()]
        random.shuffle(all_terms)
        session['terms_queue'] = all_terms
        session['terms_answered'] = []
        session['score'] = 0

    if request.method == 'POST':
        term_id = int(request.form['term_id'])
        user_answer = request.form['answer'].strip()
        term = database.get_term_by_id(term_id)
        
        session['terms_answered'].append({
            'term_id': term_id,
            'correct': user_answer.lower() == term[1].lower(),
            'user_answer': user_answer
        })
        
        if user_answer.lower() == term[1].lower():
            session['score'] += 1
        else:
            session.setdefault('review', []).append({
                'type': 'term',
                'term_id': term_id,
                'user_answer': user_answer
            })
        
        session['terms_queue'].remove(term_id)
    
    if session['terms_queue']:
        current_id = session['terms_queue'][0]
        return render_template('quiz_terms.html',
                             term=database.get_term_by_id(current_id),
                             progress=len(session['terms_answered']),
                             total=len(session['terms_answered']) + len(session['terms_queue']))
    else:
        score = session['score']
        total = len(session['terms_answered'])
        session.clear()
        return render_template('quiz_complete.html', score=score, total=total)

# Review system
@app.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == 'POST':
        index = int(request.form['index'])
        if 'review' in session and index < len(session['review']):
            del session['review'][index]
            session.modified = True
    return render_template('review.html', review_items=session.get('review', []))