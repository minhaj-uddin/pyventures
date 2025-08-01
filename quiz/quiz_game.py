import os
import json
import random
from termcolor import cprint

QUIZ_FILE = 'quiz_game.json'

QUESTION = 'question'
OPTIONS = 'options'
ANSWER = 'answer'


def ask_question(index, question, options):
    print(f'Question {index}: {question}')
    for option in options:
        print(option)

    return input('Your answer: ').upper().strip()


def run_quiz(quiz):
    print("Available categories:")
    for category in quiz.keys():
        print(f"- {category.capitalize()}")

    selected_category = input("Please choose a category: ").lower()
    if selected_category in quiz:
        score = 0
        random.shuffle(quiz[selected_category])
        questions = quiz[selected_category]

        for index, item in enumerate(questions, 1):
            answer = ask_question(index, item["QUESTION"], item["OPTIONS"])

            if answer == item["ANSWER"]:
                cprint('Correct!', 'green')
                score += 1
            else:
                cprint(f'Wrong! The correct answer is {item["ANSWER"]}', 'red')

            print()

        print(
            f'Quiz over! Your final score is {score} out of {len(questions)}')
    else:
        print("Invalid category selected.")


def main():
    if not os.path.exists(QUIZ_FILE):
        print(f"Error: File '{QUIZ_FILE}' not found.")
        exit()

    try:
        with open(QUIZ_FILE, "r") as file:
            content = file.read()
            if not content.strip():
                print(f"Error: File '{QUIZ_FILE}' is empty.")
                exit()
            quiz = json.loads(content)
    except json.JSONDecodeError:
        print(f"Error: File '{QUIZ_FILE}' contains invalid JSON.")
        exit()

    run_quiz(quiz)


if __name__ == '__main__':
    main()
