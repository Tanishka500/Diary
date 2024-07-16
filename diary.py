import tkinter as tk
from tkinter import simpledialog, messagebox
from cryptography.fernet import Fernet
import os

def load_key():
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
    else:
        with open("secret.key", "rb") as key_file:
            key = key_file.read()
    return key

key = load_key()
cipher = Fernet(key)

def save_note():
    note = text.get("1.0", tk.END).strip()
    if note:
        encrypted_note = cipher.encrypt(note.encode())
        with open("diary.dat", "wb") as file:
            file.write(encrypted_note)
        messagebox.showinfo("Info", "Note saved successfully!")
    else:
        messagebox.showinfo("Info", "No note to save!")

def load_note():
    if os.path.exists("diary.dat"):
        with open("diary.dat", "rb") as file:
            encrypted_note = file.read()
        decrypted_note = cipher.decrypt(encrypted_note).decode()
        text.delete("1.0", tk.END)
        text.insert(tk.END, decrypted_note)
    else:
        messagebox.showinfo("Info", "No saved notes found!")

def authenticate():
    user_password = simpledialog.askstring("Password", "Enter password:", show='*')
    if user_password == "Tanishka_Chitti1": 
        messagebox.showinfo("Info", "Access Granted")
        load_note()
    else:
        messagebox.showerror("Error", "Access Denied")
        root.destroy()

root = tk.Tk()
root.title("Secure Personal Diary")

background_canvas = tk.Canvas(root, width=800, height=600, bg="#F5DEB3")
background_canvas.pack()

background_canvas.create_text(400, 50, text="My Diary", font=("Arial", 24, "bold"), fill="black")

background_canvas.create_line(70, 120, 70, 580, fill="red")

text_frame_width = 660
text_frame_height = 460
canvas_width = 800
canvas_height = 600

text_frame_x = (canvas_width - text_frame_width) / 2
text_frame_y = (canvas_height - text_frame_height) / 2

text_frame = tk.Frame(root, width=text_frame_width, height=text_frame_height, bg="white")
text_frame.place(x=text_frame_x, y=text_frame_y)

text = tk.Text(text_frame, wrap=tk.WORD, font=("Comic Sans MS", 12), width=70, height=24, bg="white", fg="black", padx=10, pady=10)
text.pack(expand=True, fill=tk.BOTH)

save_button = tk.Button(root, text="Save", command=save_note, bg="lightgreen", fg="black")
save_button.place(x=700, y=560)

root.after(100, authenticate)

root.mainloop()
