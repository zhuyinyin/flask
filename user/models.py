from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# 班级模型
class Grade(db.Model):
    __tablename__ = 'grade'
    g_id = db.Column(db.Integer, primary_key=True)
    g_name = db.Column(db.String(20), unique=True)
    g_create_time = db.Column(db.DateTime, default=datetime.now)
    students = db.relationship('Student', backref='grade')


# 学生模型
class Student(db.Model):
    __tablename__ = 'student'
    s_id = db.Column(db.Integer, primary_key=True)
    s_name = db.Column(db.String(16), unique=True)
    s_sex = db.Column(db.Integer)
    gread_id = db.Column(db.Integer, db.ForeignKey('grade.g_id'), nullable=True)


# 用户模型
class User(db.Model):
    __tablename__ = 'user'
    u_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True)
    password = db.Column(db.String(250))
    u_create_time = db.Column(db.DateTime, default=datetime.now)
    role_id = db.Column(db.Integer, db.ForeignKey('role.r_id'))


# 角色模型
class Role(db.Model):
    __tablename__ = 'role'
    r_id = db.Column(db.Integer, primary_key=True)
    r_name = db.Column(db.String(10))
    users = db.relationship('User', backref='role')


# 角色和权限(多对多)关联表
# r_p为关联表的表名
r_p = db.Table('r_p',
               db.Column('role_id', db.Integer, db.ForeignKey('role.r_id'), primary_key=True),
               db.Column('permission_id', db.Integer, db.ForeignKey('permission.p_id'), primary_key=True)
               )


# 权限模型
class Permission(db.Model):
    __tablename__ = 'permission'
    p_id = db.Column(db.Integer, primary_key=True)
    p_name = db.Column(db.String(16), unique=True)
    p_er = db.Column(db.String(16), unique=True)
    roles = db.relationship('Role', secondary=r_p, backref=db.backref('permission', lazy=True))
