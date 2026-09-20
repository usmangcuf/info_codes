#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 28 20:01:36 2025

@author: mac
"""

import tkinter as tk
from tkinter import messagebox

def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def encrypt_affine(text, a, b):
    result = ""
    for char in text:
        if char.isalpha():
            if char.isupper():
                result += chr(((a * (ord(char) - 65) + b) % 26) + 65)
            else:
                result += chr(((a * (ord(char) - 97) + b) % 26) + 97)
        else:
            result += char
    return result

def decrypt_affine(text, a, b):
    result = ""
    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        messagebox.showerror("Error", "'a' is not coprime with 26, decryption not possible.")
        return ""
    for char in text:
        if char.isalpha():
            if char.isupper():
                result += chr(((a_inv * ((ord(char) - 65) - b)) % 26) + 65)
            else:
                result += chr(((a_inv * ((ord(char) - 97) - b)) % 26) + 97)
        else:
            result += char
    return result

def encrypt_text():
    plaintext = input_entry.get("1.0", tk.END).strip()
    try:
        a = int(a_entry.get())
        b = int(b_entry.get())
        encrypted = encrypt_affine(plaintext, a, b)
        encrypt_entry.delete("1.0", tk.END)
        encrypt_entry.insert(tk.END, encrypted)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid integers for a and b.")

def decrypt_text():
    ciphertext = encrypt_entry.get("1.0", tk.END).strip()
    try:
        a = int(a_entry.get())
        b = int(b_entry.get())
        decrypted = decrypt_affine(ciphertext, a, b)
        if decrypted:
            decrypt_entry.delete("1.0", tk.END)
            decrypt_entry.insert(tk.END, decrypted)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid integers for a and b.")
# GUI setup
root = tk.Tk()
root.title("Affine Cipher GUI")
root.geometry("600x500")
# Input label and text box
tk.Label(root, text="Enter Text:").pack(pady=5)
input_entry = tk.Text(root, height=3, width=40)
input_entry.pack(pady=5)

# A input
tk.Label(root, text="Enter A (Coprime 26):").pack(pady=5)
a_entry = tk.Entry(root, width=10)
a_entry.pack(pady=5)
# B input
tk.Label(root, text="Enter B(below 26):").pack(pady=5)
b_entry = tk.Entry(root, width=10)
b_entry.pack(pady=5)

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
