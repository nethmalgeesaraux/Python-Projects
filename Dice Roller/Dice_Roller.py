import tkinter as tk
import random

# Function to roll the dice
def roll_dice():
    dice_number = random.randint(1, 6)
    label_result.config(text=f"🎲 You rolled: {dice_number}")

# Create main window
root = tk.Tk()
root.title("Dice Roller 🎲")
root.geometry("300x250")
root.config(bg="#222")

# Heading
label_title = tk.Label(root, text="🎲 Dice Roller", font=("Arial", 20, "bold"), bg="#222", fg="white")
label_title.pack(pady=10)

# Result Label
label_result = tk.Label(root, text="Click 'Roll' to start", font=("Arial", 16), bg="#222", fg="lightgreen")
label_result.pack(pady=20)

# Roll Button
btn_roll = tk.Button(root, text="Roll Dice", command=roll_dice, font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", padx=20, pady=10)
btn_roll.pack(pady=10)

# Exit Button
btn_exit = tk.Button(root, text="Exit", command=root.quit, font=("Arial", 12, "bold"), bg="#E53935", fg="white", padx=15)
btn_exit.pack(pady=10)

root.mainloop()
