import datetime
import time
import threading
from tkinter import *
from playsound import playsound  

# Function to play alarm sound
def play_sound():
    playsound("Alarm clock/alarm.mp3")  


def alarm():
    while True:
        set_time = f"{hour.get()}:{minute.get()}:{second.get()}"
        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        if current_time == set_time:
            print("🔔 Wake up!")
            play_sound()
            break
        time.sleep(1)


def start_alarm():
    t1 = threading.Thread(target=alarm)
    t1.start()

# ----------------- GUI -----------------
root = Tk()
root.title("⏰ Alarm Clock")
root.geometry("400x300")
root.config(bg="#1e1e2e")

Label(root, text="Alarm Clock", font=("Arial", 20, "bold"), bg="#1e1e2e", fg="white").pack(pady=10)

# Current Time Display
def update_time():
    current = datetime.datetime.now().strftime("%H:%M:%S")
    lbl_time.config(text=f"Current Time: {current}")
    lbl_time.after(1000, update_time)

lbl_time = Label(root, font=("Arial", 14), bg="#1e1e2e", fg="cyan")
lbl_time.pack(pady=5)
update_time()

# Frame for time inputs
frame = Frame(root, bg="#1e1e2e")
frame.pack(pady=10)

hour = StringVar()
minute = StringVar()
second = StringVar()

Entry(frame, textvariable=hour, width=5, font=("Arial", 14), justify="center").grid(row=0, column=0, padx=5)
Entry(frame, textvariable=minute, width=5, font=("Arial", 14), justify="center").grid(row=0, column=1, padx=5)
Entry(frame, textvariable=second, width=5, font=("Arial", 14), justify="center").grid(row=0, column=2, padx=5)

Label(frame, text="HH", bg="#1e1e2e", fg="gray").grid(row=1, column=0)
Label(frame, text="MM", bg="#1e1e2e", fg="gray").grid(row=1, column=1)
Label(frame, text="SS", bg="#1e1e2e", fg="gray").grid(row=1, column=2)

Button(root, text="Set Alarm", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", command=start_alarm).pack(pady=15)

root.mainloop()
