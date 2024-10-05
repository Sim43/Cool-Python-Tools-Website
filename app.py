from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from color_generator import generate_colors
import os
from flask import send_file
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
if os.getenv('VERCEL'):
    UPLOAD_FOLDER = '/tmp'
else:
    UPLOAD_FOLDER = 'static/assets/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Bootstrap5(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))


def delete_uploaded_files():
    """Delete all files in the upload folder."""
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted {file_path}")
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


@app.route('/', methods=['GET', 'POST'])
def home():
    image_path = 'static/assets/img/sample.jpg'
    n_colors = 10
    delta = 16

    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        n_colors = int(request.form['n_colors'])
        delta = int(request.form['delta'])
        # If user does not select file, browser also submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # Delete previous uploaded files
            delete_uploaded_files()
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)

    colors = generate_colors(image_path, n_colors, delta)
    print(colors)
    return render_template("index.html", colors=colors, filename=filename)


if __name__ == "__main__":
    app.run(debug=False, port=5001)
