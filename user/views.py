from flask import Flask, request, redirect, session,url_for,render_template,flash,jsonify
from user.models import User, Permission, Grade, Student,Role,r_p
from flask import Blueprint
from utils.ch_login import is_login
import datetime
from user.models import db


userlogin_bpt = Blueprint('userlogin_bpt', __name__, template_folder='../templates/')


@userlogin_bpt.route('/', methods=['GET', 'POST'])
@userlogin_bpt.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not all([username, password]):
            msg = '*请填写完整的信息'
            return render_template('login.html', msg=msg)
        if User.query.filter_by(username=username, password=password).first():
            session['username'] = username
            session['password'] = password
            return redirect('/user/index')
        else:
            msg = '* 用户名或者密码不一致'
            return render_template('login.html', msg=msg)


@userlogin_bpt.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['pwd2']
        time = datetime.datetime.now()
        db.session.add(User(username=username, password=password, u_create_time=time, role_id=2))
        db.session.commit()
        return redirect('/user/login')


@userlogin_bpt.route('/logout', methods=['GET', 'POST'])
@is_login
def logout():
    if request.method == 'GET':
        session.clear()
        return redirect('/user/login')


@userlogin_bpt.route('/index', methods=['GET', 'POST'])
@is_login
def index():
    if request.method == 'GET':
        return render_template('index.html')
    # if request.method == 'POST':
    #     return render_template('index.html')


@userlogin_bpt.route('/head', methods=['GET', 'POST'])
@is_login
def head():
    if request.method == 'GET':
        return render_template('head.html', user=session.get('username'))


@userlogin_bpt.route('/left', methods=['GET', 'POST'])
@is_login
def left():
    if request.method == 'GET':
        user = User.query.filter_by(username=session.get('username')).first()
        permissions = user.role.permission
        return render_template('left.html', permissions=permissions)


@userlogin_bpt.route('/grade', methods=['GET', 'POST'])
@is_login
def grade():
    if request.method == 'GET':
        user = User.query.filter_by(username=session.get('username')).first()
        BJLB = None
        for i in user.role.permission:
            if i.p_id == 3:
                BJLB = i.p_id
        if BJLB:
            # grades = Grade.query.all()
            page = int(request.args.get('page', 1))
            per_page = 4
            paginate = Grade.query.paginate(page, per_page, error_out=False)
            return render_template('grade.html', paginate=paginate)


@userlogin_bpt.route('/addgrade', methods=['GET', 'POST'])
@is_login
def addgrade():
    if request.method == 'GET':
        return render_template('addgrade.html')
    if request.method == 'POST':
        g_name = request.form['g_name']
        time = datetime.datetime.now()
        db.session.add(Grade(g_name=g_name, g_create_time=time))
        db.session.commit()
        return redirect('/user/grade')


@userlogin_bpt.route('/grade_student/<g_id>', methods=['GET', 'POST'])
@is_login
def grade_student(g_id):
    if request.method == 'GET':
        gid = int(g_id)
        stus = Student.query.filter_by(gread_id=gid)
        page = int(request.args.get('page', 1))
        per_page = 10
        paginate = stus.paginate(page, per_page, error_out=False)
        return render_template('student2.html', paginate=paginate)


@userlogin_bpt.route('/g_del/<g_id>', methods=['GET', 'POST'])
@is_login
def g_del(g_id):
    if request.method == 'GET':
        Student.query.filter_by(gread_id=g_id).delete()
        Grade.query.filter_by(g_id=g_id).delete()
        db.session.commit()
        return redirect('/user/grade')


@userlogin_bpt.route('/s_del/<s_id>', methods=['GET', 'POST'])
@is_login
def s_del(s_id):
    if request.method == 'GET':
        Student.query.filter_by(s_id=s_id).delete()
        db.session.commit()
        return redirect('/user/student')


@userlogin_bpt.route('/student', methods=['GET', 'POST'])
@is_login
def student():
    if request.method == 'GET':
        stus = Student.query.all()
        # for i in stus:
        #     print(i.s_id, i.s_name)
        page = int(request.args.get('page', 1))
        per_page = 2
        paginate = Student.query.paginate(page, per_page, error_out=False)
        return render_template('student.html', stus=stus, paginate=paginate)


@userlogin_bpt.route('/addstu', methods=['GET', 'POST'])
@is_login
def addstu():
    if request.method == 'GET':
        grades = Grade.query.all()
        return render_template('addstu.html', grades=grades)
    if request.method == 'POST':
        s_name = request.form['s_name']
        s_sex = request.form['s_sex']
        gread_id = request.form['g_name']
        db.session.add(Student(s_name=s_name, s_sex=s_sex, gread_id=gread_id))
        db.session.commit()
        return redirect('/user/student')


@userlogin_bpt.route('/roles', methods=['GET', 'POST'])
@is_login
def roles():
    if request.method == 'GET':
        roles = Role.query.all()
        return render_template('roles.html', roles=roles)


@userlogin_bpt.route('/userperlist/<r_id>', methods=['GET', 'POST'])
@is_login
def userperlist(r_id):
    if request.method == 'GET':
        role = Role.query.filter_by(r_id=r_id).first()
        pers = role.permission
        return render_template('user_per_list.html', pers=pers)


@userlogin_bpt.route('/adduserper/<r_id>', methods=['GET', 'POST'])
@is_login
def adduserper(r_id):
    if request.method == 'GET':
        permissions = Permission.query.all()
        return render_template('add_user_per.html', permissions=permissions)
    if request.method == 'POST':
        role = Role.query.filter_by(r_id=r_id).first()
        p_id = request.form['p_id']
        # print(p_id)
        permission = Permission.query.filter_by(p_id=p_id).first()
        permission.roles.append(role)
        permission.roles.remove(role)
        db.session.add(permission)
        db.session.commit()
        return redirect('/user/roles')


@userlogin_bpt.route('/addroles', methods=['GET', 'POST'])
@is_login
def addroles():
    if request.method == 'GET':
        return render_template('addroles.html')


@userlogin_bpt.route('/permissions', methods=['GET', 'POST'])
@is_login
def permissions():
    if request.method == 'GET':
        permissions = Permission.query.all()
        return render_template('permissions.html', permissions=permissions)


@userlogin_bpt.route('/addpermission', methods=['GET', 'POST'])
@is_login
def addpermission():
    if request.method == 'GET':
        # per =的的 达瓦
        return render_template('addpermission.html')


@userlogin_bpt.route('/changepwd', methods=['GET', 'POST'])
@is_login
def changepwd():
    if request.method == 'GET':
        username = session.get('username')
        # print(username)
        user = User.query.filter_by(username=username).first()
        return render_template('changepwd.html', user=user)
