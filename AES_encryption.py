#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 15:30:22 2025

@author: mac
"""

import tkinter as tk
from tkinter import messagebox
from Crypto.Cipher import AES
import base64

def pad(text):
    # Pad to multiple of 16 bytes using PKCS7 padding
    pad_len = 16 - len(text) % 16
    return text + chr(pad_len) * pad_len

def encrypt():
    plaintext = plaintext_entry.get()
    key = key_entry.get()

    if len(key) != 16:
        messagebox.showerror("Error", "Key must be exactly 16 bytes!")
        return

    try:
        cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        padded_text = pad(plaintext)
        encrypted_bytes = cipher.encrypt(padded_text.encode('utf-8'))
        encoded_cipher = base64.b64encode(encrypted_bytes).decode('utf-8')
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, encoded_cipher)
    except Exception as e:
        messagebox.showerror("Encryption Error", str(e))

# GUI setup
root = tk.Tk()
root.title("AES Encryption Tool")
root.geometry("400x300")

tk.Label(root, text="Enter Text to Encrypt:").pack()
plaintext_entry = tk.Entry(root, width=40)
plaintext_entry.pack(pady=5)

tk.Label(root, text="Enter 16-byte Key:").pack()
key_entry = tk.Entry(root, width=40, show='*')
key_entry.pack(pady=5)

encrypt_button = tk.Button(root, text="Encrypt", command=encrypt)
encrypt_button.pack(pady=10)

tk.Label(root, text="Encrypted Output (Base64):").pack()
output_text = tk.Text(root, height=5, width=50)
output_text.pack(pady=5)

root.mainloop()
