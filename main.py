import mysql.connector
import random

# 1. Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Aswanth@2009",
    database="quiz_db"
)
cursor = db.cursor()

name = input("Enter your Name: ")

if name.lower() == "admin":
    q = input("Question: ")
    o1 = input("Option 1: ")
    o2 = input("Option 2: ")
    o3 = input("Option 3: ")
    o4 = input("Option 4: ")
    ans = input("Correct Option Text: ") 
    
    query = "INSERT INTO questions (qtext, opt1, opt2, opt3, opt4, ans) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (q, o1, o2, o3, o4, ans))
    db.commit()
    print("Question Saved.")

else:
    cursor.execute("SELECT * FROM questions")
    all_data = cursor.fetchall() 
    
    if len(all_data) < 10:
        print("Not enough questions in the database.")
    else:
        quiz_questions = random.sample(all_data, 10)
        
        score = 0
        for row in quiz_questions:
            print(row[1])
            print("1.", row[2], " 2.", row[3], " 3.", row[4], " 4.", row[5])
            
            choice = input("Enter Option Number (1, 2, 3, or 4): ")
            
            user_ans = ""
            if choice == "1": user_ans = row[2]
            elif choice == "2": user_ans = row[3]
            elif choice == "3": user_ans = row[4]
            elif choice == "4": user_ans = row[5]
            
            if user_ans.strip().lower() == row[6].strip().lower():
                print("Correct!")
                score += 1
            else:
                print("Wrong! Correct answer was:", row[6])
        
        perc = (score / 10) * 100
        
        cursor.execute("SELECT score FROM students WHERE name = %s", (name,))
        record = cursor.fetchone()
        
        if record == None:
            cursor.execute("INSERT INTO students VALUES (%s, %s)", (name, perc))
            db.commit()
            display_score = perc
        else:
            prev_best = record[0]
            if perc > prev_best:
                cursor.execute("UPDATE students SET score = %s WHERE name = %s", (perc, name))
                db.commit()
                display_score = perc
                print("New High Score!")
            else:
                print("You scored lower than your best.")
                display_score = prev_best
        
        print("\n------------------------------")
        print("          CERTIFICATE")
        print("------------------------------")
        print("Name:", name)
        print("Marks Scored:", score, "/ 10")
        print("High Score Percentage:", display_score, "%")
        print("------------------------------")

db.close()
