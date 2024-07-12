from flask import Flask, render_template, request, flash, redirect, url_for
from PIL import Image
from stegano import lsb
import os
import hashlib
import uuid

from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
# Define the upload folder
app.config['UPLOAD_FOLDER'] = "images"

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
# Function to prompt user for password
def prompt_for_password():
    password = request.form['password']
    return password

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encode', methods=['GET', 'POST'])
def encode():
    if request.method == 'POST':
        # Check if all required fields are filled
        if 'image' not in request.files or 'message' not in request.form or 'password' not in request.form:
            flash('Please fill all fields!', 'error')
            return redirect(request.url)

        # Get image file
        image = request.files['image']
        if image.filename == '':
            flash('No selected file!', 'error')
            return redirect(request.url)

        # Prompt for password
        password = prompt_for_password()
        if password is None:
            return  # User canceled

        # Encrypt password
        encrypted_password = hashlib.sha256(password.encode()).hexdigest()

        # Save encrypted password to file
        with open('password.txt', 'w') as f:
            f.write(encrypted_password)

        if not password:
            flash('Please enter a password!', 'error')
            return redirect(request.url)

        # Check if image file is valid
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Hide text in the image
            message = request.form['message']
            secret = lsb.hide(os.path.join(app.config['UPLOAD_FOLDER'], filename), message)

            # Save the modified image
            unique_filename = str(uuid.uuid4()) + ".png"
            secret.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))

            # flash('Message encoded successfully!', 'success')
            return redirect(url_for('index'))

    return render_template('encode.html')

@app.route('/decode', methods=['GET', 'POST'])
def decode():
    if request.method == 'POST':
        # Check if all required fields are filled
        if 'image' not in request.files or 'password' not in request.form:
            flash('Please fill all fields!', 'error')
            return redirect(request.url)

        # Get image file
        image = request.files['image']
        if image.filename == '':
            flash('No selected file!', 'error')
            return redirect(request.url)

        # Prompt for password
        password = prompt_for_password()
        if not password:
            flash('Please enter a password!', 'error')
            return redirect(request.url)

        # Check if image file is valid
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Check password and reveal message
            if verify_password(password):
                clear_message = lsb.reveal(image_path)
                flash('Message decoded successfully!', 'success')
                return render_template('decode.html', message=clear_message)
            else:
                flash('Incorrect password!', 'error')
                return redirect(request.url)

    return render_template('decode.html')

# Function to verify password
def verify_password(password):
    # Read stored encrypted password from file
    with open('password.txt', 'r') as f:
        stored_encrypted_password = f.read()

    # Encrypt entered password
    entered_encrypted_password = hashlib.sha256(password.encode()).hexdigest()

    # Compare entered password with stored password
    return entered_encrypted_password == stored_encrypted_password

# Function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

if __name__ == '__main__':
    app.run(debug=True)
