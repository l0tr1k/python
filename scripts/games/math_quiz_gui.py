#l0tr1k math quiz with simple GUI  
#version 1.0

import tkinter as tk
import random
import time

class MathQuizGUI:
    def __init__(self, master):
        self.master = master
        master.title("Math Quiz Game")
        
        # Game configuration
        self.total_questions = 20
        self.time_limit = 5
        self.current_question = 0
        self.correct_answers = 0
        
        # Create GUI elements
        self.question_label = tk.Label(master, font=('Arial', 24))
        self.question_label.pack(pady=20)
        
        self.answer_entry = tk.Entry(master, font=('Arial', 20), width=10)
        self.answer_entry.pack(pady=10)
        self.answer_entry.bind('<Return>', self.check_answer)
        
        # Add submit hint
        self.submit_hint = tk.Label(master, text="Press ENTER or click Submit to answer", 
                                  font=('Arial', 12), fg='gray')
        self.submit_hint.pack()
        
        self.submit_button = tk.Button(master, text="Submit", command=self.check_answer)
        self.submit_button.pack(pady=10)
        
        self.timer_label = tk.Label(master, font=('Arial', 16))
        self.timer_label.pack(pady=10)
        
        self.score_label = tk.Label(master, font=('Arial', 16))
        self.score_label.pack(pady=10)
        
        self.start_game()

    def generate_question(self):
        """Generate valid math question with single-digit operands"""
        operations = ['+', '-', '*', '/']
        num1 = random.randint(1, 9)
        num2 = random.randint(1, 9)
        op = random.choice(operations)

        if op == '/':
            num1 = num1 * num2  # Ensure integer division
        
        return f"{num1} {op} {num2}", eval(f"{num1} {op} {num2}")

    def start_game(self):
        """Initialize game state and start first question"""
        self.current_question = 0
        self.correct_answers = 0
        self.show_next_question()

    def show_next_question(self):
        """Display next question and start timer"""
        if self.current_question >= self.total_questions:
            self.end_game()
            return
            
        self.current_question += 1
        self.question, self.correct_result = self.generate_question()
        self.question_label.config(text=f"Question {self.current_question}: \n {self.question} = ?")
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus_set()  # Auto-focus on entry field
        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        """Update timer display and check timeout"""
        elapsed = time.time() - self.start_time
        remaining = max(self.time_limit - elapsed, 0)
        self.timer_label.config(text=f"Time remaining: {remaining:.1f}s")
        
        if remaining > 0:
            self.master.after(100, self.update_timer)
        else:
            self.handle_timeout()

    def handle_timeout(self):
        """Handle time expiration for current question"""
        self.timer_label.config(text="Time's up!")
        self.master.after(1000, self.show_next_question)

    def check_answer(self, event=None):
        """Validate user input using either ENTER key or button click"""
        user_answer = self.answer_entry.get()
        elapsed = time.time() - self.start_time
        
        try:
            if elapsed > self.time_limit:
                result_text = "Too late!"
            elif int(user_answer) == self.correct_result:
                self.correct_answers += 1
                result_text = "Correct!"
            else:
                result_text = "Incorrect!"
        except ValueError:
            result_text = "Invalid input!"
        
        self.score_label.config(text=result_text)
        self.master.after(1000, self.show_next_question)

    def end_game(self):
        """Show final results"""
        self.question_label.config(text="Game Over!")
        self.timer_label.config(text="")
        self.score_label.config(
            text=f"Final Score: {self.correct_answers}/{self.total_questions}",
            fg="blue"
        )
        self.answer_entry.config(state=tk.DISABLED)
        self.submit_button.config(state=tk.DISABLED)

# Create and run the GUI
root = tk.Tk()
root.geometry("600x400")
game = MathQuizGUI(root)
root.mainloop()

# Close the database connection 
conn.close()    
# Close the cursor  
cursor.close()