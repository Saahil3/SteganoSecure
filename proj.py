from tkinter import *
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk
import os
from stegano import lsb
import uuid
import hashlib

root = Tk()
root.title("CSS Project")
root.geometry("700x500+150+180")
root.resizable(False, False)

lbl = None  # Define lbl as a global variable
text1 = None  # Define text1 as a global variable

# Function to prompt user for password
def prompt_for_password():
    password = simpledialog.askstring("Password", "Enter your password:", show='*')
    return password

def showImage():
    global filename
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title='Select Image File',
                                          filetype=(("PNG file", "*.png"),
                                                    ("JPG File", "*.jpg"),
                                                    ("All file", "*.*")))
    img = Image.open(filename)
    img = ImageTk.PhotoImage(img)

    lbl.configure(image=img, width=250, height=250)
    lbl.image = img

def hide():
    global secret
    message = text1.get(1.0, END)

    # Prompt for password
    password = prompt_for_password()
    if password is None:
        return  # User canceled

    # Encrypt password
    encrypted_password = hashlib.sha256(password.encode()).hexdigest()

    # Save encrypted password to file
    with open('password.txt', 'w') as f:
        f.write(encrypted_password)

    # Hide text in the image
    secret = lsb.hide(str(filename), message)

def show():
    # Prompt for password
    password = prompt_for_password()
    if password is None:
        return  # User canceled

    # Read stored encrypted password from file
    with open('password.txt', 'r') as f:
        stored_encrypted_password = f.read()

    # Encrypt entered password
    entered_encrypted_password = hashlib.sha256(password.encode()).hexdigest()

    # Compare entered password with stored password
    if entered_encrypted_password == stored_encrypted_password:
        clear_message = lsb.reveal(filename)
        text1.delete(1.0, END)
        text1.insert(END, clear_message)
    else:
        messagebox.showerror("Error", "Incorrect password!")

def save():
    unique_filename = str(uuid.uuid4()) + ".png"
    secret.save(unique_filename)
    lbl.configure(image=None)
    lbl.image = None
    text1.delete(1.0, END)

def main_menu():
    # Clear existing widgets
    global bg_image, bg_label
    for widget in root.winfo_children():
        widget.destroy()

    # Add background image
    bg_image = Image.open("webapp/Templates/pngtree-matrix-data-code-hacker-background-image_908351.png")
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = Label(root, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)
    # Label(root, text="StegoSecure", fg="black", font="arial 25 bold").place(x=200, y=3)

    # Title
    Label(root, text="StegoSecure", fg="black", font="arial 25 bold").place(x=200, y=4)

    # Encode Text Button
    Button(text="Encode Text", width=10, height=2, font="arial 14 bold", command=encode_screen).place(x=150, y=200)

    # Decode Text Button
    Button(text="Decode Text", width=10, height=2, font="arial 14 bold", command=decode_screen).place(x=350, y=200)

# Now you can call the main_menu() function whenever you want to return to the main menu.

def encode_screen():
    global bg_image,bg_label
    global lbl, text1  # Define lbl and text1 as global variables
    # Clear existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Add background image
    bg_image = Image.open("webapp/Templates/pngtree-matrix-data-code-hacker-background-image_908351.png")
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = Label(root, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)

    # Title
    Label(root, text="StegoSecure", fg="black", font="arial 25 bold").place(x=200, y=4)

    # First Frame
    f = Frame(root, bd=3, bg="black", width=340, height=280, relief=GROOVE)
    f.place(x=10, y=80)

    lbl = Label(f, bg="black")
    lbl.place(x=40, y=10)

    # Second Frame
    frame2 = Frame(root, bd=3, width=340, height=280, bg="white", relief=GROOVE)
    frame2.place(x=350, y=80)

    text1 = Text(frame2, font="Roboto 20", bg="white", fg="black", relief=GROOVE, wrap=WORD)
    text1.place(x=0, y=0, width=320, height=295)

    scrollbar1 = Scrollbar(frame2)
    scrollbar1.place(x=320, y=0, height=300)

    scrollbar1.configure(command=text1.yview)
    text1.configure(yscrollcommand=scrollbar1.set)


    Button(root, text="Open Image", width=10, height=2, font="arial 14 bold", command=showImage).place(x=20, y=380)
    Button(root, text="Save Image", width=10, height=2, font="arial 14 bold", command=save).place(x=180, y=380)


    Button(root, text="Hide Text", width=10, height=2, font="arial 14 bold", command=hide).place(x=380, y=380)
    Button(root, text="Back", width=10, height=2, font="arial 14 bold", command=main_menu).place(x=540, y=380)

def decode_screen():
    global bg_image,bg_label

    global lbl, text1  # Define lbl and text1 as global variables
    # Clear existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Add background image
    bg_image = Image.open("webapp/Templates/pngtree-matrix-data-code-hacker-background-image_908351.png")
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = Label(root, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)

    # Title
    Label(root, text="StegoSecure", fg="black", font="arial 25 bold").place(x=200, y=4)

    # First Frame
    f = Frame(root, bd=3, bg="black", width=340, height=280, relief=GROOVE)
    f.place(x=10, y=80)

    lbl = Label(f, bg="black")
    lbl.place(x=40, y=10)

    # Second Frame
    frame2 = Frame(root, bd=3, width=340, height=280, bg="white", relief=GROOVE)
    frame2.place(x=350, y=80)

    text1 = Text(frame2, font="Roboto 20", bg="white", fg="black", relief=GROOVE, wrap=WORD)
    text1.place(x=0, y=0, width=320, height=295)

    scrollbar1 = Scrollbar(frame2)
    scrollbar1.place(x=320, y=0, height=300)

    scrollbar1.configure(command=text1.yview)
    text1.configure(yscrollcommand=scrollbar1.set)

    # Third Frame
    # frame3 = Frame(root, bd=3, width=330, height=100, relief=GROOVE)
    # frame3.place(x=10, y=370)

    Button(root, text="Open Image", width=10, height=2, font="arial 14 bold", command=showImage).place(x=20, y=380)
    Button(root, text="Save Image", width=10, height=2, font="arial 14 bold", command=save).place(x=180, y=380)


    Button(root, text="Show Text", width=10, height=2, font="arial 14 bold", command=show).place(x=380, y=380)
    Button(root, text="Back", width=10, height=2, font="arial 14 bold", command=main_menu).place(x=540, y=380)


bg_image = Image.open("webapp/Templates/pngtree-matrix-data-code-hacker-background-image_908351.png")
bg_image = ImageTk.PhotoImage(bg_image)
bg_label = Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)
Label(root,text="StegoSecure",fg="black",font="arial 25 bold").place(x=200,y=3)


Button(text="Encode Text",width=10, height=2, font="arial 14 bold",command=encode_screen).place(x=150,y=200)
Button(text="Decode Text",width=10, height=2, font="arial 14 bold",command=decode_screen).place(x=350,y=200)

root.mainloop()
