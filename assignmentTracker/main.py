# app.py

from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory  
import os

app = Flask(__name__)

# Dummy data for demonstration purposes
students = [
    {"username": "student1", "password": "password1", "assignments": []},
    {"username": "student2", "password": "password2", "assignments": []},
      {"username": "student3", "password": "password3", "assignments": []}
]

teachers = [
    {"username": "teacher1", "password": "password1"},
    {"username": "teacher2", "password": "password2"}
]

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Landing page
@app.route('/')
def index():
    return render_template('index.html')

# Student login page
@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for student in students:
            if student['username'] == username and student['password'] == password:
                return redirect(url_for('student_dashboard', username=username))
        return render_template('login.html', message='Invalid username or password')
    return render_template('login.html')

# Teacher login page
@app.route('/teacher_login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for teacher in teachers:
            if teacher['username'] == username and teacher['password'] == password:
                return redirect(url_for('teacher_dashboard', username=username))
        return render_template('login.html', message='Invalid username or password')
    return render_template('login.html')

# Student dashboard
@app.route('/student_dashboard/<username>')
def student_dashboard(username):
    student = next((s for s in students if s['username'] == username), None)
    if student:
        return render_template('student_dashboard.html', student=student)
    return redirect(url_for('student_login'))

# Teacher dashboard
@app.route('/teacher_dashboard/<username>', methods=['GET', 'POST'])
def teacher_dashboard(username):
    teacher = next((t for t in teachers if t['username'] == username), None)
    if teacher:
        if request.method == 'POST':
            student_username = request.form['student_username']
            student = next((s for s in students if s['username'] == student_username), None)
            if student:
                file = request.files['assignment']
                filename = file.filename
                if file:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    student['assignments'].append(filename)
        return render_template('teacher_dashboard.html', teacher=teacher, students=students)
    return redirect(url_for('teacher_login'))

# Route to handle assignment assignment
@app.route('/assign_assignment/<teacher_username>/<student_username>', methods=['POST'])
def assign_assignment(teacher_username, student_username):
    teacher = next((t for t in teachers if t['username'] == teacher_username), None)
    if teacher:
        student = next((s for s in students if s['username'] == student_username), None)
        if student:
            file = request.files['assignment']
            filename = file.filename
            if file:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                student['assignments'].append(filename)
    return redirect(url_for('teacher_dashboard', username=teacher_username))


@app.route('/uploads/<path:filename>')
def download_file(filename):
    uploads_dir = 'uploads'  # Directory where PDF files are stored
    return send_from_directory('uploads/', path=filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)