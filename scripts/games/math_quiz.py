#l0tr1k math quiz   
#version 1.0

import random
import time

# Funkcia na generovanie matematickej úlohy
def generate_question():
    operations = ['+', '-', '*', '/']
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)
    operation = random.choice(operations)

    # Zabezpečenie, aby delenie dávalo celé číslo
    if operation == '/':
        num1 = num1 * num2

    question = f"{num1} {operation} {num2}"
    answer = eval(question)  # Vypočíta správnu odpoveď
    return question, answer

# Hlavná funkcia hry
def main():
    print("Vitajte v logickej hre! Vašou úlohou je vyriešiť 20 matematických príkladov.")
    print("Na každú úlohu máte 3 sekundy. Začnime!")

    correct_answers = 0
    total_questions = 20

    for i in range(total_questions):
        question, answer = generate_question()
        print(f"Úloha {i+1}: Koľko je {question}?")

        start_time = time.time()
        try:
            user_input = input("Vaša odpoveď: ")
            elapsed_time = time.time() - start_time

            if elapsed_time > 3:
                print("Čas vypršal!")
            elif float(user_input) == answer:
                print("Správne!")
                correct_answers += 1
            else:
                print("Nesprávne!")
        except ValueError:
            print("Nesprávny vstup! Pokračujeme ďalšou úlohou.")

    print(f"Hra skončila! Správne odpovede: {correct_answers} z {total_questions}")

# Spustenie programu
if __name__ == "__main__":
    main()