# app.py
# Run: python app.py
# Prereqs: pip install Flask Flask-SQLAlchemy PyMySQL fpdf2

from flask import Flask, render_template, request, redirect, url_for, send_file
from models import db, Student, Department, Payment   # import models
from invoice_generator import generate_invoice        # import invoice logic
import datetime
import os



app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/studentdb'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Admin%401234@localhost:3306/studentdb'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

db.init_app(app)

# -----------------------------------------------------------------------------
# Seed departments
# -----------------------------------------------------------------------------
def seed_departments():
    if Department.query.count() == 0:
        deps = ['Computer Science', 'Data Analytics', 'Management']
        for name in deps:
            db.session.add(Department(Dept_Name=name))
        db.session.commit()

# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------
@app.route('/')
def home():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        depts = Department.query.order_by(Department.Dept_Name).all()
        return render_template('register.html', depts=depts)

    name = request.form['name'].strip()
    email = request.form.get('email', '').strip() or None
    dob_raw = request.form.get('dob', '').strip()
    dept_id_raw = request.form.get('dept_id', '').strip()

    dob = None
    if dob_raw:
        try:
            dob = datetime.datetime.strptime(dob_raw, '%Y-%m-%d').date()
        except ValueError:
            dob = None

    dept_id = int(dept_id_raw) if dept_id_raw else None

    student = Student(Name=name, Email=email, DOB=dob, Dept_ID=dept_id)
    db.session.add(student)
    db.session.commit()
    return redirect(url_for('payment', student_id=student.Student_ID))

@app.route('/payment/<int:student_id>', methods=['GET', 'POST'])
def payment(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == 'GET':
        return render_template('payment.html', student=student)

    amount_raw = request.form['amount'].strip()
    try:
        amount = float(amount_raw)
    except ValueError:
        amount = 0.0

    pay = Payment(
        Student_ID=student.Student_ID,
        Amount=amount,
        Status='Paid',
        Date=datetime.date.today()
    )
    db.session.add(pay)
    db.session.commit()

    # Fetch department name for invoice
    dept_name = "-"
    if student.Dept_ID:
        dept = Department.query.get(student.Dept_ID)
        if dept:
            dept_name = dept.Dept_Name

    pdf_path = generate_invoice(student, pay, department_name=dept_name)
    return send_file(pdf_path, as_attachment=True)

# -----------------------------------------------------------------------------
# Bootstrap
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_departments()
    app.run(debug=True)

#------------------------------------------------------------------------------------------------------------------------------
#export SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:AjDCrMtgfiuALEEitqHWxQXRzUPTDWVI@mainline.proxy.rlwy.net:16132/railway"
#------------------------------------------------------------------------------------------------------------------------------