#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 00:05:18 2025

@author: mac
"""

import tkinter as tk
from tkinter import messagebox

# Caesar Cipher Encryption
def encrypt(text, key):
    result = ""
    for char in text:
        if char.isalpha():  # process only letters
            shift = 65 if char.isupper() else 97
            result += chr((ord(char) - shift + key) % 26 + shift)
        else:
            result += char
    return result

# Caesar Cipher Decryption
def decrypt(text, key):
    return encrypt(text, -key)

# Encrypt button function
def encrypt_text():
    try:
        key = int(key_entry.get())
        text = input_entry.get("1.0", tk.END).strip()
        encrypted = encrypt(text, key)
        encrypt_entry.delete("1.0", tk.END)
        encrypt_entry.insert(tk.END, encrypted)
    except ValueError:
        messagebox.showerror("Invalid Input", "Key must be an integer.")

# Decrypt button function
def decrypt_text():
    try:
        key = int(key_entry.get())
        text = encrypt_entry.get("1.0", tk.END).strip()
        decrypted = decrypt(text, key)
        decrypt_entry.delete("1.0", tk.END)
        decrypt_entry.insert(tk.END, decrypted)
    except ValueError:
        messagebox.showerror("Invalid Input", "Key must be an integer.")

# GUI setup
root = tk.Tk()
root.title("Caesar Cipher GUI")
root.geometry("600x500")

# Input label and text box
tk.Label(root, text="Enter Text:").pack(pady=5)
input_entry = tk.Text(root, height=3, width=40)
input_entry.pack(pady=5)

# Key input
tk.Label(root, text="Enter Key (integer):").pack(pady=5)
key_entry = tk.Entry(root, width=10)
key_entry.pack(pady=5)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

encrypt_button = tk.Button(button_frame, text="Encrypt", command=encrypt_text, width=10)
encrypt_button.grid(row=0, column=0, padx=5)

decrypt_button = tk.Button(button_frame, text="Decrypt", command=decrypt_text, width=10)
decrypt_button.grid(row=0, column=1, padx=5)

exit_button = tk.Button(button_frame, text="Exit", command=root.quit, width=10, fg="red")
exit_button.grid(row=0, column=2, padx=5)

# Output label and text box
tk.Label(root, text="Encrypt Result:").pack(pady=5)
encrypt_entry = tk.Text(root, height=3, width=40)
encrypt_entry.pack(pady=5)
tk.Label(root, text="Decrypt Result:").pack(pady=5)
decrypt_entry = tk.Text(root, height=3, width=40)
decrypt_entry.pack(pady=5)

root.mainloop()
