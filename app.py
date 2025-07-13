from flask import Flask, render_template, request, redirect, session, url_for, flash
from oauth import authorize_user, get_gmail_service
from send import send_bulk_emails
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "supersecretkey")

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'xlsx', 'html'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename, allowed):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed

@app.route('/')
def index():
    if 'credentials' not in session:
        return render_template('index.html', logged_in=False)
    return render_template('index.html', logged_in=True)

@app.route('/authorize')
def authorize():
    return authorize_user()

@app.route('/oauth2callback')
def oauth2callback():
    return authorize_user(callback=True)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/send', methods=['POST'])
def send():
    if 'credentials' not in session:
        return redirect('/')

    delay = int(request.form.get("delay", 2))
    html_file = request.files.get("html_file")
    excel_file = request.files.get("excel_file")

    if not html_file or not allowed_file(html_file.filename, {'html'}):
        flash("Invalid HTML file.")
        return redirect('/')
    if not excel_file or not allowed_file(excel_file.filename, {'xlsx'}):
        flash("Invalid Excel file.")
        return redirect('/')

    html_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(html_file.filename))
    excel_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(excel_file.filename))
    html_file.save(html_path)
    excel_file.save(excel_path)

    creds = session['credentials']
    service = get_gmail_service(creds)
    count = send_bulk_emails(service, excel_path, html_path, delay)

    return render_template('result.html', count=count)

if __name__ == "__main__":
    app.run(debug=True)