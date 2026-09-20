import tkinter as tk
from tkinter import messagebox


# ---------------------------------------------------------
# Vigenere Cipher Functions
# ---------------------------------------------------------

def vigenere_encrypt(text, key):
    """
    Encrypt text using the Vigenere Cipher.
    Spaces and punctuation are preserved.
    Only alphabetic characters are encrypted.
    """

    text = text.upper()
    key = key.upper()

    # Keep only alphabetic characters in the key
    key = ''.join(ch for ch in key if ch.isalpha())

    if not key:
        raise ValueError("Key must contain at least one alphabetic character.")

    result = ""
    key_index = 0

    for char in text:

        if char.isalpha():
            # Convert A-Z to 0-25
            text_value = ord(char) - ord('A')
            key_value = ord(key[key_index % len(key)]) - ord('A')

            # Vigenere encryption
            encrypted_value = (text_value + key_value) % 26

            result += chr(encrypted_value + ord('A'))

            key_index += 1

        else:
            # Preserve spaces, numbers and punctuation
            result += char

    return result


def vigenere_decrypt(text, key):
    """
    Decrypt text using the Vigenere Cipher.
    Spaces and punctuation are preserved.
    """

    text = text.upper()
    key = key.upper()

    # Keep only alphabetic characters in the key
    key = ''.join(ch for ch in key if ch.isalpha())

    if not key:
        raise ValueError("Key must contain at least one alphabetic character.")

    result = ""
    key_index = 0

    for char in text:

        if char.isalpha():

            text_value = ord(char) - ord('A')
            key_value = ord(key[key_index % len(key)]) - ord('A')

            # Vigenere decryption
            decrypted_value = (text_value - key_value) % 26

            result += chr(decrypted_value + ord('A'))

            key_index += 1

        else:
            # Preserve spaces, numbers and punctuation
            result += char

    return result


# ---------------------------------------------------------
# Encrypt Button
# ---------------------------------------------------------

def encrypt_button():

    plaintext = plaintext_box.get("1.0", tk.END).strip()
    key = key_entry.get().strip()

    if not plaintext:
        messagebox.showwarning(
            "Input Error",
            "Please enter plaintext."
        )
        return

    if not key:
        messagebox.showwarning(
            "Input Error",
            "Please enter a key."
        )
        return

    try:

        ciphertext = vigenere_encrypt(
            plaintext,
            key
        )

        # Display encrypted text
        ciphertext_box.delete("1.0", tk.END)
        ciphertext_box.insert(
            tk.END,
            ciphertext
        )

        # Clear previous decrypted text
        decrypted_box.delete("1.0", tk.END)

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


# ---------------------------------------------------------
# Decrypt Button
# ---------------------------------------------------------

def decrypt_button():

    ciphertext = ciphertext_box.get(
        "1.0",
        tk.END
    ).strip()

    key = key_entry.get().strip()

    if not ciphertext:
        messagebox.showwarning(
            "Input Error",
            "Please enter ciphertext or encrypt some plaintext first."
        )
        return

    if not key:
        messagebox.showwarning(
            "Input Error",
            "Please enter a key."
        )
        return

    try:

        plaintext = vigenere_decrypt(
            ciphertext,
            key
        )

        # Display decrypted plaintext
        decrypted_box.delete(
            "1.0",
            tk.END
        )

        decrypted_box.insert(
            tk.END,
            plaintext
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


# ---------------------------------------------------------
# Clear Button
# ---------------------------------------------------------

def clear_all():

    plaintext_box.delete(
        "1.0",
        tk.END
    )

    key_entry.delete(
        0,
        tk.END
    )

    ciphertext_box.delete(
        "1.0",
        tk.END
    )

    decrypted_box.delete(
        "1.0",
        tk.END
    )


# ---------------------------------------------------------
# Main Tkinter Window
# ---------------------------------------------------------

root = tk.Tk()

root.title("Vigenère Cipher")
root.geometry("800x650")

root.resizable(False, False)


# ---------------------------------------------------------
# Title
# ---------------------------------------------------------

title_label = tk.Label(
    root,
    text="VIGENÈRE CIPHER",
    font=("Arial", 24, "bold")
)

title_label.pack(pady=15)


subtitle_label = tk.Label(
    root,
    text="Encryption and Decryption using Vigenère Algorithm",
    font=("Arial", 11)
)

subtitle_label.pack(pady=5)


# ---------------------------------------------------------
# Key Input
# ---------------------------------------------------------

key_frame = tk.Frame(root)

key_frame.pack(pady=15)


key_label = tk.Label(
    key_frame,
    text="Key:",
    font=("Arial", 12, "bold")
)

key_label.pack(
    side=tk.LEFT,
    padx=10
)


key_entry = tk.Entry(
    key_frame,
    width=40,
    font=("Arial", 12)
)

key_entry.pack(
    side=tk.LEFT
)


# ---------------------------------------------------------
# Plaintext Input
# ---------------------------------------------------------

plaintext_label = tk.Label(
    root,
    text="Plaintext:",
    font=("Arial", 12, "bold")
)

plaintext_label.pack(
    anchor="w",
    padx=50
)


plaintext_box = tk.Text(
    root,
    width=80,
    height=6,
    font=("Consolas", 12)
)

plaintext_box.pack(
    pady=5
)


# ---------------------------------------------------------
# Buttons
# ---------------------------------------------------------

button_frame = tk.Frame(root)

button_frame.pack(
    pady=15
)


encrypt_btn = tk.Button(
    button_frame,
    text="ENCRYPT",
    width=15,
    font=("Arial", 11, "bold"),
    command=encrypt_button
)

encrypt_btn.pack(
    side=tk.LEFT,
    padx=10
)


decrypt_btn = tk.Button(
    button_frame,
    text="DECRYPT",
    width=15,
    font=("Arial", 11, "bold"),
    command=decrypt_button
)

decrypt_btn.pack(
    side=tk.LEFT,
    padx=10
)


clear_btn = tk.Button(
    button_frame,
    text="CLEAR",
    width=15,
    font=("Arial", 11, "bold"),
    command=clear_all
)

clear_btn.pack(
    side=tk.LEFT,
    padx=10
)


# ---------------------------------------------------------
# Ciphertext Output
# ---------------------------------------------------------

ciphertext_label = tk.Label(
    root,
    text="Ciphertext:",
    font=("Arial", 12, "bold")
)

ciphertext_label.pack(
    anchor="w",
    padx=50
)


ciphertext_box = tk.Text(
    root,
    width=80,
    height=5,
    font=("Consolas", 12)
)

ciphertext_box.pack(
    pady=5
)


# ---------------------------------------------------------
# Decrypted Plaintext Output
# ---------------------------------------------------------

decrypted_label = tk.Label(
    root,
    text="Decrypted Plaintext:",
    font=("Arial", 12, "bold")
)

decrypted_label.pack(
    anchor="w",
    padx=50
)


decrypted_box = tk.Text(
    root,
    width=80,
    height=5,
    font=("Consolas", 12)
)

decrypted_box.pack(
    pady=5
)


# ---------------------------------------------------------
# Start Application
# ---------------------------------------------------------

root.mainloop()