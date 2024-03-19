import json
import random


def load_questions(filename):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Add cake points information to each question
    for question in data["questions"]:
        question["cake_points"] = 1000  # Initial cake points for each question

    return data["questions"]


def select_question(questions):
    return random.choice(questions)

def check_answer(question, player_answer):
    return player_answer.lower() == question["correct answer"]
