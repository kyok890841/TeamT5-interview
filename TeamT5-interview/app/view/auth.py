from flask import Flask, render_template, redirect, url_for, request, session, Blueprint, make_response, flash
from flask_restful import Api, Resource, reqparse

from marshmallow import ValidationError

from ..model.user import UserModel, UserSchema
from .. import db
from .abort_msg import abort_msg

auth = Blueprint('auth', __name__)
api = Api(auth)

users_schema = UserSchema()


class Signup(Resource):
    def post(self):
        try:
            # 資料驗證
            print(request.form)
            user_data = users_schema.load(request.form)
            # 註冊
            new_user = UserModel(user_data)
            new_user.save_db()
            new_user.save_session()
            flash('You were successfully sign-up!')
            return redirect(url_for('auth.login'))

            

        except ValidationError as error:
            return {'errors': error.messages}, 400

        except Exception as e:
            return {'errors': abort_msg(e)}, 500

    def get(self):
        return make_response(render_template('signup.html'))


class Login(Resource):
    def post(self):
        try:
            # 資料驗證
            user_data = users_schema.load(request.form)
            name = user_data['name']
            password = user_data['password']

            # 登入
            query = UserModel.get_user(name)
            if query != None and query.verify_password(password):
                query.save_session()
                return redirect(url_for('todolist.showtodo', user=name))
            else:
                return {'errors': 'incorrect username or password'}, 400

        except ValidationError as error:
            return {'errors': error.messages}, 400

        except Exception as e:
            return {'errors': abort_msg(e)}, 500

    def get(self):
        return make_response(render_template('login.html'))


class Logout(Resource):
    def get(self):
        UserModel.remove_session()
        return make_response(render_template('login.html'))


api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
