from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config
from datetime import datetime
import pytz

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)

    sr_code = db.Column(db.String(50), unique=True)

    password = db.Column(db.String(255))

    full_name = db.Column(db.String(255))

    program = db.Column(db.String(100))

    section_name = db.Column(db.String(100))

class Admin(db.Model):

    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100))

    password = db.Column(db.String(100))

class Log(db.Model):

    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)

    log_code = db.Column(db.String(100))

    student_id = db.Column(
        db.Integer,
        db.ForeignKey('students.id')
    )

    instructor = db.Column(db.String(255))

    laboratory = db.Column(db.String(255))

    start_time = db.Column(db.String(50))

    end_time = db.Column(db.String(50))

    timestamp = db.Column(
        db.String(50)
    )

    student = db.relationship('Student')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    message = None
    error = None

    if request.method == 'POST':

        sr_code = request.form['sr_code']
        password = request.form['password']

        student = Student.query.filter_by(
            sr_code=sr_code,
            password=password
        ).first()

        if student:

            session['student_id'] = student.id

            return render_template(
                'dashboard.html',
                student=student
            )

        else:

            error = "Invalid SR-Code or Password"

    if request.args.get('deleted'):

        message = "Log Successfully Deleted"

    elif request.args.get('next'):

        message = "Ready for Next Student"

    return render_template(
        'login.html',
        message=message,
        error=error
    )

@app.route('/logout')
def logout():

    session.clear()

    return redirect(
        '/login?next=1'
    )

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        admin = Admin.query.filter_by(
            username=username,
            password=password
        ).first()

        if admin:

            session['admin_id'] = admin.id

            return redirect('/admin_dashboard')

        else:

            return render_template(
                'admin_login.html',
                error='Invalid Username or Password'
            )

    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():

    search = request.args.get('search')

    filter_date = request.args.get('filter_date')

    query = Log.query.join(Student)

    # SEARCH FILTER
    if search:

        query = query.filter(

            (Student.sr_code.contains(search)) |

            (Student.full_name.contains(search)) |

            (Log.instructor.contains(search)) |

            (Log.laboratory.contains(search))

        )

    if filter_date:

        query = query.filter(
            db.func.date(Log.timestamp) == filter_date
        )


    # SORT BY TIMESTAMP
    logs = query.order_by(Log.timestamp.asc()).all()

    # TOTAL LOGS TODAY
    today = datetime.now(
        pytz.timezone('Asia/Manila')
    ).date()

    total_logs_today = Log.query.filter(
        db.func.date(Log.timestamp) == today
    ).count()

    # CURRENT DATE/TIME
    current_datetime = datetime.now(
        pytz.timezone('Asia/Manila')
    ).strftime("%B %d, %Y — %I:%M %p")

    # MOST USED LABORATORY
    most_used_lab = db.session.query(
        Log.laboratory,
        db.func.count(Log.id)
    ).group_by(
        Log.laboratory
    ).order_by(
        db.func.count(Log.id).desc()
    ).first()

    # MOST ACTIVE STUDENT
    most_active_student = db.session.query(
        Student.full_name,
        db.func.count(Log.id)
    ).join(Log).group_by(
        Student.full_name
    ).order_by(
        db.func.count(Log.id).desc()
    ).first()

    # MOST SELECTED INSTRUCTOR
    most_selected_instructor = db.session.query(
        Log.instructor,
        db.func.count(Log.id)
    ).group_by(
        Log.instructor
    ).order_by(
        db.func.count(Log.id).desc()
    ).first()

    return render_template(

        'admin_dashboard.html',

        logs=logs,

        total_logs=total_logs_today,

        current_datetime=current_datetime,

        most_used_lab=most_used_lab,

        most_active_student=most_active_student,

        most_selected_instructor=most_selected_instructor

    )

@app.route('/admin_logout')
def admin_logout():

    session.pop('admin_id', None)

    return redirect('/')

@app.route('/dashboard')
def dashboard():

    if 'student_id' not in session:

        return redirect('/login')

    student = Student.query.get(
        session['student_id']
    )

    return render_template(
        'dashboard.html',
        student=student
    )

@app.route('/submit_log', methods=['POST'])
def submit_log():

    if 'student_id' not in session:

        return redirect('/login')

    laboratory = request.form['laboratory']

    # DATE FORMAT
    today = datetime.now().strftime('%Y%m%d')

    # GET LAB NUMBER
    lab_number = laboratory.replace('Laboratory ', '')

    # COUNT EXISTING LOGS FOR SAME LAB
    existing_logs = Log.query.filter_by(
        laboratory=laboratory
    ).count()

    # NEXT NUMBER
    sequence = existing_logs + 1

    # GENERATE LOG CODE
    generated_log_code = f"{today}L{lab_number}-{sequence}"

    # CONVERT TIME TO 12-HOUR FORMAT
    start_time_24 = request.form['start_time']
    end_time_24 = request.form['end_time']

    start_dt = datetime.strptime(start_time_24, "%H:%M")
    end_dt = datetime.strptime(end_time_24, "%H:%M")

    start_time_12 = start_dt.strftime("%I:%M").lstrip("0") + " " + start_dt.strftime("%p")
    end_time_12 = end_dt.strftime("%I:%M").lstrip("0") + " " + end_dt.strftime("%p")

    log = Log(

        log_code=generated_log_code,

        student_id=session['student_id'],

        instructor=request.form['instructor'],

        laboratory=laboratory,

        start_time=start_time_12,

        end_time=end_time_12,

        timestamp=datetime.now(
            pytz.timezone('Asia/Manila')
        ).strftime("%Y-%m-%d %I:%M:%S %p")

    )

    db.session.add(log)

    db.session.commit()

    student = Student.query.get(
        session['student_id']
    )

    return render_template(

        'review_log.html',

        student=student,

        formatted_start=log.start_time,

        formatted_end=log.end_time,

        log=log,

        message="Log Successfully Submitted"

    )

@app.route('/delete_log/<int:log_id>')
def delete_log(log_id):

    log = Log.query.get_or_404(log_id)

    db.session.delete(log)

    db.session.commit()

    return redirect('/login?deleted=1')

@app.route('/update_log/<int:log_id>', methods=['GET', 'POST'])
def update_log(log_id):

    if 'student_id' not in session:
        return redirect('/login')

    log = Log.query.get(log_id)

    if request.method == 'POST':

        # UPDATE INSTRUCTOR
        log.instructor = request.form['instructor']

        # UPDATED LABORATORY
        updated_lab = request.form['laboratory']
        log.laboratory = updated_lab

        # GENERATE NEW LOG CODE
        lab_number = updated_lab.replace('Laboratory ', '')

        today = datetime.now().strftime('%Y%m%d')

        existing_logs = Log.query.filter(
            Log.laboratory == updated_lab,
            Log.id != log.id
        ).count()

        sequence = existing_logs + 1

        log.log_code = f"{today}L{lab_number}-{sequence}"

        # TIME CONVERSION
        start_time_24 = request.form['start_time']
        end_time_24 = request.form['end_time']

        start_dt = datetime.strptime(start_time_24, "%H:%M")
        end_dt = datetime.strptime(end_time_24, "%H:%M")

        log.start_time = (
            start_dt.strftime("%I:%M").lstrip("0")
            + " "
            + start_dt.strftime("%p")
        )

        log.end_time = (
            end_dt.strftime("%I:%M").lstrip("0")
            + " "
            + end_dt.strftime("%p")
        )

        db.session.commit()

        student = Student.query.get(log.student_id)

        formatted_start = log.start_time
        formatted_end = log.end_time

        return render_template(
            'review_log.html',
            student=student,
            log=log,
            formatted_start=formatted_start,
            formatted_end=formatted_end,
            message="Log Updated Successfully"
        )

    return render_template(
        'update_log.html',
        log=log
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
