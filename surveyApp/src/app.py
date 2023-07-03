from flask import Flask, render_template, request, redirect, url_for
import csv
import random 
import os


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        # Process the submitted survey form and store the ratings
        # Retrieve the ratings for each story and store them as desired

        # After processing the submission, redirect to the next story
        return redirect(url_for('survey'))

    else:
        # Read the questions from the CSV file
        questions = []
        with open('question_bank/questions.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                questions.append(row)
                

        # Randomly select a question for each main value
        main_values = set([question['main_value'] for question in questions])
        random_questions = []

        for main_value in main_values:
            filtered_questions = [question for question in questions if question['main_value'] == main_value]
            random_question = random.choice(filtered_questions)
            random_questions.append(random_question)

        print(random_questions)

        # Render the survey start page with the next story
        return render_template('survey_start.html', random_questions=random_questions)

