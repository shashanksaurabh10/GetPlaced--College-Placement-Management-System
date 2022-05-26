from flask import Flask, render_template, request, session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime
from flask_mail import Mail
from werkzeug.utils import secure_filename
import re
import os
import json
from sqlalchemy.sql import func


with open("config.json", "r") as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['UPLOAD_FOLDER'] = params['upload_location']
'''app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD=  params['gmail-password']
)
mail = Mail(app)'''
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

class Student(db.Model):

    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    usn = db.Column(db.String(10), nullable=False)
    branch= db.Column(db.String(4), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phoneno = db.Column(db.String(10), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    avg_sgpa = db.Column(db.String(20), nullable=False)
    internship = db.Column(db.String(20), nullable=False)
    specialization = db.Column(db.String(20), nullable=False)
    pref_company = db.Column(db.String(20), nullable=False)


class Company(db.Model):
    company_id = db.Column(db.Integer, primary_key=True)
    companyname = db.Column(db.String(50),nullable=False)
    job_position = db.Column(db.String(50),nullable=False)
    skill_req = db.Column(db.String(200),nullable=False)
    annual_package = db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(50),nullable=False)

class Placement_record(db.Model):
    stu_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    branch = db.Column(db.String(10),nullable=False)
    company = db.Column(db.String(50),nullable=False)
    yearofplacement = db.Column(db.String(20),nullable=False)
    package = db.Column(db.String(20),nullable=False)

class Contact_admin(db.Model):
    contact_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    usn = db.Column(db.String(20), nullable=False)
    branch= db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    problem = db.Column(db.String(200), nullable=False)

class Placement_administrator(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    deptname = db.Column(db.String(20), nullable=False)
    yearofexp = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phoneno = db.Column(db.String(20), nullable=False)
    bio = db.Column(db.String(5000), nullable=False)


@app.route("/studentdatabase",methods=['GET','POST'])
def hello1():
    '''usn0 = request.form.get('usn')
    post = Student.query.filter_by(usn=usn0).first()'''

    if ('user' in session and session['user'] == params['usn']):
        post = Student.query.filter_by().all()
        return render_template('student_database.html',params=params,post=post)

    if request.method == 'POST':
        usn0 = request.form.get('usn')
        password0 = request.form.get('password0')
        if (usn0 == params['usn'] and password0 == params['login_password']):
            session['user'] = usn0
            post = Student.query.filter_by().all()
            return render_template('student_database.html',params=params,post=post)

    return render_template('studentlogin.html',params=params,post=post)

@app.route("/admindatabase",methods=['GET','POST'])
def admin():
    '''usn0 = request.form.get('usn')
    post = Student.query.filter_by(usn=usn0).first()'''

    if ('user' in session and session['user'] == params['admin_username']):
        post = Student.query.filter_by().all()
        return render_template('admin_database.html',params=params,post=post)

    if request.method == 'POST':
        usn0 = request.form.get('usn')
        password0 = request.form.get('password0')
        if (usn0 == params['admin_username'] and password0 == params['admin_password']):
            session['user'] = usn0
            post = Student.query.filter_by().all()
            return render_template('admin_database.html',params=params,post=post)

    return render_template('placementadminlogin.html',params=params,post=post)

@app.route("/principaldatabase",methods=['GET','POST'])
def principal():
    '''usn0 = request.form.get('usn')
    post = Student.query.filter_by(usn=usn0).first()'''

    if ('user' in session and session['user'] == params['prin_username']):
        admin = Placement_administrator.query.filter_by().all()
        return render_template('admin_details.html',params=params,admin=admin)

    if request.method == 'POST':
        username0 = request.form.get('username0')
        password0 = request.form.get('password0')
        if (username0 == params['prin_username'] and password0 == params['prin_password']):
            session['user'] = username0
            admin = Placement_administrator.query.filter_by().all()
            return render_template('admin_details.html',params=params,admin=admin)

    return render_template('principallogin.html',params=params,admin=admin)


@app.route("/filter9",methods=['GET'])
def filter9():
    post = Student.query.filter(Student.avg_sgpa>=9.0)
    return render_template('filter9.html',params=params,post=post)

@app.route("/filter8",methods=['GET'])
def filter8():
    post = Student.query.filter(Student.avg_sgpa>=8.0)
    return render_template('filter8.html',params=params,post=post)

@app.route("/filter7",methods=['GET'])
def filter7():
    post = Student.query.filter(Student.avg_sgpa>=7.0)
    return render_template('filter7.html',params=params,post=post)

@app.route("/filter6",methods=['GET'])
def filter6():
    post = Student.query.filter(Student.avg_sgpa>=6.0)
    return render_template('filter6.html',params=params,post=post)

@app.route("/companydetails",methods=['GET'])
def hello2():
    company = Company.query.filter_by().all()
    return render_template('company_details.html',params=params,company=company)

@app.route("/admincompanydetails",methods=['GET'])
def admincompanydetails():
    company = Company.query.filter_by().all()
    return render_template('admin_companydetails.html',params=params,company=company)

@app.route("/placementhistory",methods=['GET'])
def hello3():
    placement = Placement_record.query.order_by(desc(Placement_record.yearofplacement)).all()
    avg = Placement_record.query.with_entities(func.avg(Placement_record.package)).scalar()
    return render_template('placement_history.html',params=params,placement=placement,avg=avg)

@app.route("/adminplacementhistory",methods=['GET'])
def adminplacement():
    placement = Placement_record.query.order_by(desc(Placement_record.yearofplacement)).all()
    avg = Placement_record.query.with_entities(func.avg(Placement_record.package)).scalar()
    return render_template('admin_placement.html',params=params,placement=placement,avg=avg)

@app.route("/principalplacementhistory",methods=['GET'])
def principalplacement():
    placement = Placement_record.query.order_by(desc(Placement_record.yearofplacement)).all()
    return render_template('principalplacement.html',params=params,placement=placement)


@app.route("/query",methods=['GET'])
def query():
    query = Contact_admin.query.order_by(desc(Contact_admin.contact_id)).all()
    return render_template('query.html',params=params,query=query)

@app.route("/adminblog",methods=['GET'])
def adminblog():
    admin = Placement_administrator.query.filter_by().all()
    return render_template('adminblog.html',params=params,admin=admin)

@app.route("/contactadmin", methods=['GET','POST'])
def hello4():

    if(request.method=='POST'):
        name = request.form.get('name')
        usn = request.form.get('usn')
        branch = request.form.get('branch')
        email = request.form.get('email')
        problem = request.form.get('problem')
        entry = Contact_admin(name=name, usn = usn, branch = branch, email = email, problem = problem)
        db.session.add(entry)
        db.session.commit()
        '''mail.send_message('New message from ' + name,
                          sender=email,
                          recipients = [params['gmail-user']],
                          body = problem + "\n" + usn
                          )'''

    return render_template('contact_admin.html',params=params)

@app.route("/principalcontactadmin", methods=['GET','POST'])
def princontactadmin():

    if(request.method=='POST'):
        name = request.form.get('name')
        usn = request.form.get('usn')
        branch = request.form.get('branch')
        email = request.form.get('email')
        problem = request.form.get('problem')
        entry = Contact_admin(name=name, usn = usn, branch = branch, email = email, problem = problem)
        db.session.add(entry)
        db.session.commit()
        '''mail.send_message('New message from ' + name,
                          sender=email,
                          recipients = [params['gmail-user']],
                          body = problem + "\n" + usn
                          )'''

    return render_template('prin_contactadmin.html',params=params)


@app.route("/")
def hello():
    return render_template('try1.html',params=params)

@app.route("/about")
def harry():
    return render_template('about.html',params=params)

@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if(request.method=='POST'):
        name = request.form.get('name')
        usn = request.form.get('usn')
        branch = request.form.get('branch')
        sem = request.form.get('sem')
        email = request.form.get('email')
        phoneno = request.form.get('phoneno')
        dob = request.form.get('dob')
        avgsgpa = request.form.get('avgsgpa')
        internship = request.form.get('internship')
        specialization = request.form.get('specialization')
        prefcompany = request.form.get('prefcompany')
        entry = Student(name=name, usn = usn, branch = branch, semester = sem , email = email, phoneno = phoneno  , dob = dob , avg_sgpa = avgsgpa , internship = internship, specialization = specialization, pref_company = prefcompany )
        db.session.add(entry)
        db.session.commit()


    return render_template('registration.html',params=params)

@app.route("/loginstudent",methods=['GET','POST'])
def run2():
    
    return render_template('studentlogin.html',params=params)

@app.route("/loginadmin")
def run3():
    return render_template('placementadminlogin.html',params=params)


@app.route("/loginprincipal")
def run5():
    return render_template('principallogin.html',params=params)

@app.route("/upload",methods=['GET','POST'])
def upload():
    if('user' in session and session['user'] == params['usn']):
        if(request.method == 'POST'):
            f = request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return render_template('submit.html',params=params)
    return render_template('student_database.html',params=params)

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/loginstudent')

@app.route("/adminlogout")
def logoutadmin():
    session.pop('user')
    return redirect('/loginadmin')

@app.route("/principallogout")
def logoutprincipal():
    session.pop('user')
    return redirect('/loginprincipal')


@app.route("/edit/<string:student_id>",methods=['GET','POST']) 
def edit(student_id):
    if('user' in session and session['user'] == params['usn']):
        if(request.method == 'POST'):
            name = request.form.get('name')
            usn = request.form.get('usn')
            branch = request.form.get('branch')
            sem = request.form.get('sem')
            email = request.form.get('email')
            phoneno = request.form.get('phoneno')
            dob = request.form.get('dob')
            avgsgpa = request.form.get('avgsgpa')
            internship = request.form.get('internship')
            specialization = request.form.get('specialization')
            prefcompany = request.form.get('prefcompany')

            if student_id == '0':
                entry = Student(name=name, usn = usn, branch = branch, semester = sem , email = email, phoneno = phoneno  , dob = dob , avg_sgpa = avgsgpa , internship = internship, specialization = specialization, pref_company = prefcompany)
                db.session.add(entry)
                db.session.commit()
            else:
                post = Student.query.filter_by(student_id=student_id).first()
                post.name = name
                post.usn = usn
                post.branch= branch
                post.semester = sem
                post.email = email
                post.phoneno = phoneno
                post.dob = dob
                post.avg_sgpa = avgsgpa
                post.internship = internship
                post.specialization = specialization
                post.pref_company = prefcompany
                db.session.commit()
                return redirect('/edit/'+student_id)
        post = Student.query.filter_by(student_id=student_id).first()
        return render_template('edit.html',params=params,post=post,student_id=student_id)

@app.route("/companyedit/<string:company_id>",methods=['GET','POST']) 
def companyedit(company_id):
    if('user' in session and session['user'] == params['admin_username']):
        if(request.method == 'POST'):
            companyname = request.form.get('companyname')
            job_position = request.form.get('job_position')
            skill_req = request.form.get('skill_req')
            annual_package = request.form.get('annual_package')
            email = request.form.get('email')

            if company_id == '0':
                entry = Company(companyname=companyname, job_position = job_position, skill_req = skill_req, annual_package = annual_package , email = email)
                db.session.add(entry)
                db.session.commit()
            else:
                company = Company.query.filter_by(company_id=company_id).first()
                company.companyname = companyname
                company.job_position = job_position
                company.skill_req= skill_req
                company.annual_package = annual_package
                company.email = email
                db.session.commit()
                return redirect('/companyedit/'+company_id)
        company = Company.query.filter_by(company_id=company_id).first()
        return render_template('companyedit.html',params=params,company=company,company_id=company_id)


@app.route("/placementedit/<string:stu_id>",methods=['GET','POST']) 
def placementedit(stu_id):
    if('user' in session and session['user'] == params['admin_username']):
        if(request.method == 'POST'):
            name = request.form.get('name')
            branch = request.form.get('branch')
            company = request.form.get('company')
            yop = request.form.get('yop')
            package = request.form.get('package')

            if stu_id == '0':
                entry = Placement_record(name=name, branch = branch, company = company, yearofplacement = yop , package = package)
                db.session.add(entry)
                db.session.commit()
            else:
                placement = Placement_record.query.filter_by(stu_id=stu_id).first()
                placement.name = name
                placement.branch = branch
                placement.company= company
                placement.yearofplacement = yop
                placement.package = package
                db.session.commit()
                return redirect('/placementedit/'+stu_id)
        placement = Placement_record.query.filter_by(stu_id=stu_id).first()
        return render_template('placementedit.html',params=params,placement=placement,stu_id=stu_id)

@app.route("/adminedit/<string:admin_id>",methods=['GET','POST']) 
def adminedit(admin_id):
    if('user' in session and session['user'] == params['prin_username']):
        if(request.method == 'POST'):
            name = request.form.get('name')
            deptname = request.form.get('deptname')
            yoe = request.form.get('yoe')
            email = request.form.get('email')
            phoneno = request.form.get('phoneno')
            bio = request.form.get('bio')

            if admin_id == '0':
                entry = Placement_administrator(name=name, deptname = deptname, yearofexp = yoe, email = email , phoneno = phoneno, bio=bio)
                db.session.add(entry)
                db.session.commit()
            else:
                admin = Placement_administrator.query.filter_by(admin_id=admin_id).first()
                admin.name = name
                admin.deptname = deptname
                admin.yearofexp= yoe
                admin.email = email
                admin.phoneno = phoneno
                admin.bio = bio
                db.session.commit()
                return redirect('/adminedit/'+admin_id)
        admin = Placement_administrator.query.filter_by(admin_id=admin_id).first()
        return render_template('adminedit.html',params=params,admin=admin,admin_id=admin_id)



@app.route("/delete/<string:student_id>",methods=['GET','POST']) 
def delete(student_id):
    if('user' in session and session['user'] == params['usn']):
        post = Student.query.filter_by(student_id=student_id).first()
        db.session.delete(post)
        db.session.commit()
    return redirect('/studentdatabase')

@app.route("/companydelete/<string:company_id>",methods=['GET','POST']) 
def companydelete(company_id):
    if('user' in session and session['user'] == params['admin_username']):
        company = Company.query.filter_by(company_id=company_id).first()
        db.session.delete(company)
        db.session.commit()
    return redirect('/admincompanydetails')

@app.route("/placementdelete/<string:stu_id>",methods=['GET','POST']) 
def placementdelete(stu_id):
    if('user' in session and session['user'] == params['admin_username']):
        placement = Placement_record.query.filter_by(stu_id=stu_id).first()
        db.session.delete(placement)
        db.session.commit()
    return redirect('/adminplacementhistory')

@app.route("/admindelete/<string:admin_id>",methods=['GET','POST']) 
def admindelete(admin_id):
    if('user' in session and session['user'] == params['prin_username']):
        admin = Placement_administrator.query.filter_by(admin_id=admin_id).first()
        db.session.delete(admin)
        db.session.commit()
    return redirect('/principaldatabase')


app.run(debug=True)