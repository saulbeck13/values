from flask import Flask, render_template, request
import csv
import random 
import os


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def survey():
    # ...
    
    # Read the questions from the CSV file
    questions = []
    with open('question_bank/question_bank.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            questions.append(row)

    # Randomly select one question
    random_question = random.choice(questions)

    # Render the survey form template with the randomly selected question
    return render_template('survey_form.html', random_question=random_question)
