# from flask import Flask, request, redirect, session,url_for,render_template,flash,jsonify
# from user.models import User, Permission
# from flask import Blueprint
#
#
# userlogin_bpt = Blueprint('userlogin_bpt', __name__, template_folder='./templates/')
#
#
# @userlogin_bpt.route('/', methods=['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         return render_template('login.html')
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         print(username, password)
#         if User.query.filter(username=username, password=password):
#             session['username'] = username
#             session['password'] = password
#             return render_template('login.html')
