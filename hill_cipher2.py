#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 20:56:34 2025

@author: mac
"""

import tkinter as tk
from tkinter import messagebox
import numpy as np

# Function to compute modular inverse of a number under mod 26
def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

# Prepare text: uppercase letters, preserve spaces
def prepare_text(text):
    text = text.upper()
    letters_only = [c for c in text if c.isalpha()]
    if len(letters_only) % 2 != 0:
        text += 'X'  # pad at the end if needed
    return text

# Encryption
def encrypt():
    try:
        key = np.array([
            [int(e1.get()), int(e2.get())],
            [int(e3.get()), int(e4.get())]
        ])
        
        text = input_text.get("1.0", tk.END).strip().upper()
        text = prepare_text(text)

        encrypted = ""
        buffer = []

        for char in text:
            if char == " ":
                # process existing buffer before appending space
                if len(buffer) == 2:
                    pair = np.array([[ord(buffer[0]) - 65], [ord(buffer[1]) - 65]])
                    result = np.dot(key, pair) % 26
                    encrypted += chr(result[0][0] + 65) + chr(result[1][0] + 65)
                    buffer = []
                encrypted += " "
            else:
                buffer.append(char)
                if len(buffer) == 2:
                    pair = np.array([[ord(buffer[0]) - 65], [ord(buffer[1]) - 65]])
                    result = np.dot(key, pair) % 26
                    encrypted += chr(result[0][0] + 65) + chr(result[1][0] + 65)
                    buffer = []

        encrypted_text.delete("1.0", tk.END)
        encrypted_text.insert(tk.END, encrypted)

    except Exception as ex:
        messagebox.showerror("Error", f"Encryption failed: {ex}")

# Decryption
def decrypt():
    try:
        key = np.array([
            [int(e1.get()), int(e2.get())],
            [int(e3.get()), int(e4.get())]
        ])

        # determinant
        det = int(np.round(np.linalg.det(key))) % 26
        det_inv = mod_inverse(det, 26)
        if det_inv is None:
            messagebox.showerror("Error", "Key matrix is not invertible under mod 26")
            return

        # adjugate matrix
        adj = np.array([[key[1][1], -key[0][1]],
                        [-key[1][0], key[0][0]]])
        
        # modular inverse matrix
        inv_key = (det_inv * adj) % 26

        text = encrypted_text.get("1.0", tk.END).strip().upper()
        decrypted = ""
        buffer = []

        for char in text:
            if char == " ":
                # process buffer first
                if len(buffer) == 2:
                    pair = np.array([[ord(buffer[0]) - 65], [ord(buffer[1]) - 65]])
                    result = np.dot(inv_key, pair) % 26
                    decrypted += chr(result[0][0] + 65) + chr(result[1][0] + 65)
                    buffer = []
                decrypted += " "
            else:
                buffer.append(char)
                if len(buffer) == 2:
                    pair = np.array([[ord(buffer[0]) - 65], [ord(buffer[1]) - 65]])
                    result = np.dot(inv_key, pair) % 26
                    decrypted += chr(result[0][0] + 65) + chr(result[1][0] + 65)
                    buffer = []

        decrypted_text.delete("1.0", tk.END)
        decrypted_text.insert(tk.END, decrypted)

    except Exception as ex:
        messagebox.showerror("Error", f"Decryption failed: {ex}")

# Exit
def close_app():
    root.destroy()

# GUI Setup
root = tk.Tk()
root.title("Hill Cipher (2x2) with Spaces")
root.geometry("500x200")

# Input Text
tk.Label(root, text="Input Text:").grid(row=0, column=0, sticky="w")
input_text = tk.Text(root, height=2, width=40)
input_text.grid(row=0, column=1, columnspan=4)

# Key Matrix
tk.Label(root, text="Key Matrix (2x2):").grid(row=1, column=0, sticky="w")

e1 = tk.Entry(root, width=5)
e1.grid(row=1, column=1)
e2 = tk.Entry(root, width=5)
e2.grid(row=1, column=2)
e3 = tk.Entry(root, width=5)
e3.grid(row=2, column=1)
e4 = tk.Entry(root, width=5)
e4.grid(row=2, column=2)

# Encrypted Text
tk.Label(root, text="Encrypted Text:").grid(row=3, column=0, sticky="w")
encrypted_text = tk.Text(root, height=2, width=40)
encrypted_text.grid(row=3, column=1, columnspan=4)

# Decrypted Text
tk.Label(root, text="Decrypted Text:").grid(row=4, column=0, sticky="w")
decrypted_text = tk.Text(root, height=2, width=40)
decrypted_text.grid(row=4, column=1, columnspan=4)

# Buttons
tk.Button(root, text="Encrypt", command=encrypt, bg="lightgreen").grid(row=5, column=1)
tk.Button(root, text="Decrypt", command=decrypt, bg="lightblue").grid(row=5, column=2)
tk.Button(root, text="Exit", command=close_app, bg="lightcoral").grid(row=5, column=3)

root.mainloop()
