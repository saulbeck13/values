from flask import Flask, render_template, request, redirect, url_for, session
import csv
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/', methods=['GET', 'POST'])
def survey():
    if 'current_question' not in session:
        session['current_question'] = 0

    if 'survey_results' not in session:
        session['survey_results'] = []

    questions = load_questions_from_csv('question_bank/questions.csv')
    current_question = session['current_question']
    survey_results = session['survey_results']

    if request.method == 'POST':
        # Process the submitted survey form and store the ratings
        question_id = request.form['question_id']
        conservation_rating = request.form['conservation']
        self_transcendence_rating = request.form['self_transcendence']
        openness_to_change_rating = request.form['openness_to_change']
        self_enhancement_rating = request.form['self_enhancement']

        # Store the question_id and rating as desired
        survey_results.append({
            'question_id': question_id,
            'conservation': conservation_rating,
            'self_transcendence': self_transcendence_rating,
            'openness_to_change': openness_to_change_rating,
            'self_enhancement': self_enhancement_rating
        })

        if current_question == len(questions) - 1:
            # If the last question has been answered, show the thank you page
            save_survey_results_to_csv('survey_results.csv', survey_results)
            session.pop('survey_results')  # Remove survey results from session
            return redirect(url_for('thank_you'))
        else:
            # After processing the submission, increment the current question
            session['current_question'] += 1
            return redirect(url_for('survey'))

    else:
        if current_question < 0:
            current_question = 0
        elif current_question >= len(questions):
            # If the current question exceeds the question count, redirect to the last question
            return redirect(url_for('survey'))

        question = questions[current_question]

        # Render the survey page with the current question
        return render_template('survey.html', random_question=question)


@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html', survey_results=session.get('survey_results', []))


def load_questions_from_csv(file_path):
    questions = []
    main_values = set()  # Set to store unique main values

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file, delimiter="\t")
        for row in reader:
            questions.append(row)
            main_values.add(row['main_value'])

    # Randomly select two questions for each main value
    selected_questions = []
    for value in main_values:
        value_questions = [q for q in questions if q['main_value'] == value]
        selected = random.sample(value_questions, 1)
        selected_questions.extend(selected)

    return selected_questions



def save_survey_results_to_csv(file_path, results):
    fieldnames = ['question_id', 'conservation', 'self_transcendence', 'openness_to_change', 'self_enhancement']

    # Check if the file already exists
    file_exists = os.path.isfile(file_path)

    with open(file_path, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header only if the file doesn't exist
        if not file_exists:
            writer.writeheader()

        writer.writerows(results)


if __name__ == '__main__':
    app.run()
