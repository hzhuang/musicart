from flask import Blueprint, jsonify, session, render_template, request, redirect, url_for
from database import *
import random

main = Blueprint('main', __name__)

@main.route("/terms")
def terms():
    terms = get_terms()
    return render_template("terms.html", terms=terms)

@main.route("/add_term", methods=["POST"])
def add_term():
    term = request.form.get("term")
    definition = request.form.get("definition")

    if term and definition:
        insert_term(term, definition)
    return redirect(url_for("main.terms"))


@main.route('/quiz/terms')
def quiz_terms():
    terms = get_terms()
    selected_terms = random.sample(terms, 2)
    
    # Store the selected terms and current index in the session
    session['selected_terms'] = selected_terms
    session['current_term_index'] = 0
    session['user_term_answers'] = []  # Initialize an empty list to store user answers
    
    return render_template('quiz_term_question.html')

@main.route('/quiz/submit_term_answer', methods=['POST'])
def submit_term_answer():
    # Get the user's answer and term ID from the form
    user_answer = request.form.get('answer')
    term_id = request.form.get('term_id')
    
    print(f"Received answer: {user_answer}, term ID: {term_id}")  # Debugging output

    # Save the user's answer in the session
    session['user_term_answers'].append({
        'term_id': term_id,
        'user_answer': user_answer
    })
    
    print(f"Before appending: {session['user_term_answers']}")  # Debugging output
    
    # Move to the next term
    session['current_term_index'] += 1
    if(session['current_term_index'] < len(session['selected_terms'])):
        # Redirect to display the next term
        return render_template('quiz_term_question.html')
    return redirect(url_for('main.display_term_answer'))

@main.route('/quiz/display_term_answer')
def display_term_answer():
    # Get the selected terms and current index from the session
    selected_terms = session.get('selected_terms', [])
    user_term_answers = session.get('user_term_answers', [])
    # Calculate correct answers
    correct_answer = 0
    for i, term in enumerate(selected_terms):
        if i < len(user_term_answers) and user_term_answers[i]["user_answer"] == term[1]:
            correct_answer += 1
    print(f"Checking: {correct_answer}")         
    print(f"Checking: {session['user_term_answers']}")  # Debugging output
    # Render the template with the current term
    return render_template('quiz_term_answer_display.html', terms=selected_terms, answers = user_term_answers, correct_answer=correct_answer)


#composers
@main.route("/composers")
def composers():
    composers = get_composers()
    return render_template("composers.html", composers=composers)

@main.route("/add_composer", methods=["POST"])
def add_composer():
    name = request.form.get("name")
    bio = request.form.get("bio")
    audio_path = request.form.get("audio_path")

    if name and bio and audio_path:
        insert_composer(name, bio, audio_path)
    return redirect(url_for("main.composers"))

@main.route('/quiz/composers')
def quiz_composers():
    composers = get_composers()
    selected_composers = random.sample(composers, 2)
    
    # Store the selected composers and current index in the session
    session['selected_composers'] = selected_composers
    session['current_composer_index'] = 0
    session['user_composer_answers'] = []  # Initialize an empty list to store user answers
    
    return render_template('quiz_composer_question.html')

@main.route('/quiz/submit_composer_answer', methods=['POST'])
def submit_answer():
    # Get the user's answer and composer ID from the form
    user_answer = request.form.get('answer')
    composer_id = request.form.get('composer_id')
    
    print(f"Received answer: {user_answer}, Composer ID: {composer_id}")  # Debugging output

    # Save the user's answer in the session
    session['user_composer_answers'].append({
        'composer_id': composer_id,
        'user_answer': user_answer
    })
    
    print(f"Before appending: {session['user_composer_answers']}")  # Debugging output
    
    # Move to the next composer
    session['current_composer_index'] += 1
    if(session['current_composer_index'] < len(session['selected_composers'])):
        # Redirect to display the next composer
        return render_template('quiz_composer_question.html')
    return redirect(url_for('main.display_composer_answer'))

@main.route('/quiz/display_composer_answer')
def display_composer_answer():
    # Get the selected composers and current index from the session
    selected_composers = session.get('selected_composers', [])
    user_composer_answers = session.get('user_composer_answers', [])
    
    print(f"Checking: {session['user_composer_answers']}")  # Debugging output
    # Render the template with the current composer
    return render_template('quiz_composer_answer_display.html', composers=selected_composers, answers = user_composer_answers)

@main.route('/add_to_review', methods=['POST'])
def add_to_review():
    data = request.get_json()
    reference_id = data.get('reference_id')
    category = data.get('category')
    term_name = data.get('term_name')
    definition_bio = data.get('definition_bio')
    your_answer = data.get('your_answer')
    
    print(f"Checking: {category}{term_name}")  # Debugging output
      
    try:
        if not (reference_id and category and term_name and definition_bio):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Insert into the database (ensure this function returns a success JSON)
        success = insert_to_review(reference_id, category, term_name, definition_bio, your_answer)

        if success:
            return jsonify({'success': True, 'message': 'Added to review successfully'}), 200
        else:
            return jsonify({'success': False, 'message': 'Database insertion failed'}), 500

    except Exception as e:
        print(f"Error: {str(e)}")  # Debugging output
        return jsonify({'success': False, 'error': str(e)}), 500


# Review Routes
@main.route('/review')
def review():
    review_list = get_reviews()
    print(f"Checking: {review_list}")  # Debugging output
    return render_template('review.html', review_list=review_list)

@main.route('/remove_review/<int:id>', methods=['POST'])
def remove_review(id):
    print(f"delete_review: {id}")  # Debugging output
    delete_review(id)
    return redirect(url_for('main.review'))