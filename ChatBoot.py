import tkinter as tk
from tkinter import scrolledtext, messagebox
import random
import datetime

class ChatBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Chat Bot")
        self.root.geometry("500x600")
        self.root.configure(bg='#f0f0f0')
        
        self.bot_name = "ChatBot"
        self.setup_responses()
        self.create_widgets()
        
    def setup_responses(self):
        self.responses = {
            "greeting": [
                "Hello! How can I help you today?",
                "Hi there! What's on your mind?",
                "Hey! Nice to talk to you!"
            ],
            "how_are_you": [
                "I'm doing great, thanks for asking!",
                "I'm just a program, but I'm functioning perfectly!",
                "All systems go! How are you?"
            ],
            "goodbye": [
                "Goodbye! Have a great day!",
                "See you later!",
                "Bye! Come back anytime!"
            ],
            "help": [
                "I can chat with you about simple topics. Try asking how I am or just say hello!",
                "I'm a simple bot. You can greet me, ask how I am, or say goodbye!"
            ],
            "time": [
                f"The current time is {datetime.datetime.now().strftime('%H:%M')}",
                f"It's {datetime.datetime.now().strftime('%I:%M %p')} right now"
            ],
            "joke": [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the scarecrow win an award? He was outstanding in his field!",
                "What do you call a fake noodle? An impasta!"
            ],
            "default": [
                "That's interesting! Tell me more.",
                "I see. What else would you like to talk about?",
                "Interesting! Could you elaborate?"
            ]
        }
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Python Chat Bot", 
                              font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#333')
        title_label.pack(pady=10)
        
        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, 
                                                     width=50, height=20,
                                                     font=('Arial', 11),
                                                     bg='white', fg='#333')
        self.chat_display.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg='#f0f0f0')
        input_frame.pack(padx=20, pady=10, fill=tk.X)
        
        # Message entry
        self.message_entry = tk.Entry(input_frame, font=('Arial', 12), 
                                     bg='white', fg='#333', width=40)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.message_entry.bind('<Return>', lambda event: self.send_message())
        
        # Send button
        send_button = tk.Button(input_frame, text="Send", 
                               font=('Arial', 10, 'bold'),
                               bg='#4CAF50', fg='white',
                               command=self.send_message)
        send_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Clear button
        clear_button = tk.Button(self.root, text="Clear Chat", 
                                font=('Arial', 10),
                                bg='#ff9800', fg='white',
                                command=self.clear_chat)
        clear_button.pack(pady=5)
        
        # Welcome message
        self.add_message(self.bot_name, "Hello! I'm your Python chat bot. Type 'help' to see what I can do!")
    
    def get_bot_response(self, user_input):
        user_input = user_input.lower()
        
        if any(word in user_input for word in ['hello', 'hi', 'hey']):
            return random.choice(self.responses["greeting"])
        
        elif any(word in user_input for word in ['how are you', 'how do you do']):
            return random.choice(self.responses["how_are_you"])
        
        elif any(word in user_input for word in ['bye', 'goodbye', 'see you']):
            return random.choice(self.responses["goodbye"])
        
        elif any(word in user_input for word in ['help', 'what can you do']):
            return random.choice(self.responses["help"])
        
        elif any(word in user_input for word in ['time', 'clock']):
            return random.choice(self.responses["time"])
        
        elif any(word in user_input for word in ['joke', 'funny']):
            return random.choice(self.responses["joke"])
        
        else:
            return random.choice(self.responses["default"])
    
    def add_message(self, sender, message):
        self.chat_display.config(state=tk.NORMAL)
        
        # Add sender tag
        if sender == self.bot_name:
            self.chat_display.insert(tk.END, f"{sender}: ", 'bot_name')
        else:
            self.chat_display.insert(tk.END, f"{sender}: ", 'user_name')
        
        # Add message
        self.chat_display.insert(tk.END, f"{message}\n\n")
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def send_message(self):
        user_message = self.message_entry.get().strip()
        
        if user_message:
            # Add user message
            self.add_message("You", user_message)
            
            # Clear input
            self.message_entry.delete(0, tk.END)
            
            # Get and add bot response
            bot_response = self.get_bot_response(user_message)
            self.add_message(self.bot_name, bot_response)
    
    def clear_chat(self):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.add_message(self.bot_name, "Chat cleared! How can I help you?")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatBotGUI(root)
    root.mainloop()