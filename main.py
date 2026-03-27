import mysql.connector
import random
import sys

mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password", # Replace with your MySQL password
            database="online_quiz"
        )

def get_random_question(cursor):
    cursor.execute("SELECT * FROM questions ORDER BY RAND() LIMIT 1")
    question = cursor.fetchone()
    return question

def run_quiz():
    mycursor = mydb.cursor()
    score = 0
    print
    print("Welcome to the Online Quiz Portal!")
    user_name = input("Enter your name: ")

    # Fetch a question
    question_data = get_random_question(mycursor)

    if question_data:
        qid, q_text, op_a, op_b, op_c, op_d, correct_ans = question_data

        print(f"\nQuestion: {q_text}")
        print(f"A. {op_a}")
        print(f"B. {op_b}")
        print(f"C. {op_c}")
        if op_c: print(f"C. {op_c}")
        if op_d: print(f"D. {op_d}")

        user_answer = input("Enter your answer (e.g., 'Paris'): ")

        if user_answer.strip().lower() == correct_ans.strip().lower():
            print("Correct answer!")
            score += 1
        else:
            print(f"Wrong answer. The correct answer was: {correct_ans}")
    else:
        print("No questions found in the database.")

    print(f"\nQuiz finished, {user_name}! Your final score is {score}.")
    
    # Store score in the database (optional, requires a scores table)

    mycursor.close()
    mydb.close()


run_quiz()
