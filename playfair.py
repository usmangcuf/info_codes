import tkinter as tk
from tkinter import messagebox


# ---------------------------------------------------------
# Playfair Cipher Functions
# ---------------------------------------------------------

def prepare_key(key):
    """
    Prepare the key:
    - Convert to uppercase
    - Replace J with I
    - Keep only alphabetic characters
    - Remove duplicate characters
    """
    key = key.upper().replace("J", "I")

    result = ""
    for ch in key:
        if ch.isalpha() and ch not in result:
            result += ch

    return result


def create_matrix(key):
    """
    Create the 5x5 Playfair matrix.
    I and J are combined.
    """

    key = prepare_key(key)

    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

    combined = key

    for ch in alphabet:
        if ch not in combined:
            combined += ch

    matrix = []

    for i in range(0, 25, 5):
        matrix.append(list(combined[i:i + 5]))

    return matrix


def display_matrix(matrix):
    """
    Display matrix in the GUI.
    """
    for widget in matrix_frame.winfo_children():
        widget.destroy()

    for r in range(5):
        for c in range(5):
            label = tk.Label(
                matrix_frame,
                text=matrix[r][c],
                width=4,
                height=2,
                font=("Arial", 14, "bold"),
                relief="solid",
                borderwidth=1
            )
            label.grid(row=r, column=c, padx=2, pady=2)


def find_position(matrix, letter):
    """
    Find row and column of a character in the matrix.
    """
    if letter == "J":
        letter = "I"

    for row in range(5):
        for col in range(5):
            if matrix[row][col] == letter:
                return row, col

    return None


def prepare_plaintext(text):
    """
    Prepare plaintext for Playfair encryption.

    Rules:
    - Convert J -> I
    - Remove spaces and non-alphabetic characters
    - Split into pairs
    - If both letters in a pair are the same,
      insert X between them.
    - If one letter remains at the end, add X.
    """

    text = text.upper().replace("J", "I")

    # Keep only alphabets
    text = "".join(ch for ch in text if ch.isalpha())

    pairs = []
    i = 0

    while i < len(text):

        first = text[i]

        if i + 1 < len(text):
            second = text[i + 1]

            if first == second:
                pairs.append(first + "X")
                i += 1
            else:
                pairs.append(first + second)
                i += 2
        else:
            pairs.append(first + "X")
            i += 1

    return pairs


def encrypt_pair(pair, matrix):
    """
    Encrypt one pair using Playfair rules.
    """

    a, b = pair

    row1, col1 = find_position(matrix, a)
    row2, col2 = find_position(matrix, b)

    # Same row
    if row1 == row2:
        a = matrix[row1][(col1 + 1) % 5]
        b = matrix[row2][(col2 + 1) % 5]

    # Same column
    elif col1 == col2:
        a = matrix[(row1 + 1) % 5][col1]
        b = matrix[(row2 + 1) % 5][col2]

    # Rectangle
    else:
        a = matrix[row1][col2]
        b = matrix[row2][col1]

    return a + b


def decrypt_pair(pair, matrix):
    """
    Decrypt one pair using Playfair rules.
    """

    a, b = pair

    row1, col1 = find_position(matrix, a)
    row2, col2 = find_position(matrix, b)

    # Same row
    if row1 == row2:
        a = matrix[row1][(col1 - 1) % 5]
        b = matrix[row2][(col2 - 1) % 5]

    # Same column
    elif col1 == col2:
        a = matrix[(row1 - 1) % 5][col1]
        b = matrix[(row2 - 1) % 5][col2]

    # Rectangle
    else:
        a = matrix[row1][col2]
        b = matrix[row2][col1]

    return a + b


def encrypt_text(plaintext, key):
    """
    Encrypt complete plaintext.
    """

    matrix = create_matrix(key)

    pairs = prepare_plaintext(plaintext)

    ciphertext = ""

    for pair in pairs:
        ciphertext += encrypt_pair(pair, matrix)

    return ciphertext, matrix


def decrypt_text(ciphertext, key):
    """
    Decrypt complete ciphertext.
    """

    matrix = create_matrix(key)

    # Convert J to I and remove non-alphabetic characters
    ciphertext = ciphertext.upper().replace("J", "I")
    ciphertext = "".join(ch for ch in ciphertext if ch.isalpha())

    # Ciphertext should have even number of characters
    if len(ciphertext) % 2 != 0:
        raise ValueError("Ciphertext must contain an even number of letters.")

    plaintext = ""

    for i in range(0, len(ciphertext), 2):
        pair = ciphertext[i:i + 2]
        plaintext += decrypt_pair(pair, matrix)

    return plaintext, matrix


# ---------------------------------------------------------
# Button Functions
# ---------------------------------------------------------

def encrypt_button():
    plaintext = plaintext_box.get("1.0", tk.END).strip()
    key = key_entry.get().strip()

    if not plaintext:
        messagebox.showwarning("Input Error", "Please enter plaintext.")
        return

    if not key:
        messagebox.showwarning("Input Error", "Please enter a key.")
        return

    try:
        ciphertext, matrix = encrypt_text(plaintext, key)

        ciphertext_box.delete("1.0", tk.END)
        ciphertext_box.insert(tk.END, ciphertext)

        display_matrix(matrix)

        # Clear previous decrypted text
        decrypted_box.delete("1.0", tk.END)

    except Exception as e:
        messagebox.showerror("Error", str(e))


def decrypt_button():
    ciphertext = ciphertext_box.get("1.0", tk.END).strip()
    key = key_entry.get().strip()

    if not ciphertext:
        messagebox.showwarning(
            "Input Error",
            "Please encrypt some plaintext first or enter ciphertext."
        )
        return

    if not key:
        messagebox.showwarning("Input Error", "Please enter a key.")
        return

    try:
        plaintext, matrix = decrypt_text(ciphertext, key)

        decrypted_box.delete("1.0", tk.END)
        decrypted_box.insert(tk.END, plaintext)

        display_matrix(matrix)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---------------------------------------------------------
# Tkinter GUI
# ---------------------------------------------------------

root = tk.Tk()
root.title("Playfair Cipher - I/J Combined")
root.geometry("800x800")
root.resizable(False, False)


# Title
title_label = tk.Label(
    root,
    text="PLAYFAIR CIPHER",
    font=("Arial", 22, "bold")
)
title_label.pack(pady=15)


subtitle = tk.Label(
    root,
    text="I/J are combined — J is automatically converted to I",
    font=("Arial", 11)
)
subtitle.pack(pady=2)


# ---------------------------------------------------------
# Key
# ---------------------------------------------------------

key_frame = tk.Frame(root)
key_frame.pack(pady=15)

tk.Label(
    key_frame,
    text="Key:",
    font=("Arial", 12, "bold")
).pack(side=tk.LEFT, padx=10)

key_entry = tk.Entry(
    key_frame,
    width=45,
    font=("Arial", 12)
)
key_entry.pack(side=tk.LEFT)


# ---------------------------------------------------------
# Plaintext
# ---------------------------------------------------------

tk.Label(
    root,
    text="Plaintext:",
    font=("Arial", 12, "bold")
).pack(anchor="w", padx=50)

plaintext_box = tk.Text(
    root,
    width=80,
    height=5,
    font=("Consolas", 12)
)
plaintext_box.pack(pady=5)


# ---------------------------------------------------------
# Buttons
# ---------------------------------------------------------

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

encrypt_btn = tk.Button(
    button_frame,
    text="ENCRYPT",
    width=15,
    font=("Arial", 11, "bold"),
    command=encrypt_button
)
encrypt_btn.pack(side=tk.LEFT, padx=10)

decrypt_btn = tk.Button(
    button_frame,
    text="DECRYPT",
    width=15,
    font=("Arial", 11, "bold"),
    command=decrypt_button
)
decrypt_btn.pack(side=tk.LEFT, padx=10)


# ---------------------------------------------------------
# Ciphertext
# ---------------------------------------------------------

tk.Label(
    root,
    text="Ciphertext:",
    font=("Arial", 12, "bold")
).pack(anchor="w", padx=50)

ciphertext_box = tk.Text(
    root,
    width=80,
    height=4,
    font=("Consolas", 12)
)
ciphertext_box.pack(pady=5)


# ---------------------------------------------------------
# Decrypted Plaintext
# ---------------------------------------------------------

tk.Label(
    root,
    text="Decrypted Plaintext:",
    font=("Arial", 12, "bold")
).pack(anchor="w", padx=50)

decrypted_box = tk.Text(
    root,
    width=80,
    height=4,
    font=("Consolas", 12)
)
decrypted_box.pack(pady=5)


# ---------------------------------------------------------
# Playfair Matrix
# ---------------------------------------------------------

tk.Label(
    root,
    text="Playfair Matrix",
    font=("Arial", 13, "bold")
).pack(pady=(10, 5))

matrix_frame = tk.Frame(root)
matrix_frame.pack()


# Start GUI
root.mainloop()