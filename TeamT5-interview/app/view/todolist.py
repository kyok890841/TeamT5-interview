from flask import Flask, flash, render_template, redirect, url_for, request, session, Blueprint, make_response
from flask_restful import Api, Resource, reqparse

from marshmallow import ValidationError

from ..model.todo import TodoModel, TodoSchema
from .. import db
from .abort_msg import abort_msg

todo = Blueprint('todolist', __name__)
api = Api(todo)

todo_schema = TodoSchema()

class AddTodo(Resource):
    def post(self):
        try:
            print(request.form)
            print(session.get('username'))
            todo_data = todo_schema.load(request.form)
            new_todo = TodoModel(todo_data,username=session.get('username'))
            new_todo.save_db()
            new_todo.save_session()
            return redirect(url_for('todolist.showtodo', user=session.get('username')))

        except ValidationError as error:
            return {'errors': error.messages}, 400

        except Exception as e:
            return {'errors': abort_msg(e)}, 500
    def get(self):
        return make_response(render_template('add_todo.html', user=session.get('username')))

class ShowTodo(Resource):
    def get(self):
        user = session.get('username')
        query = TodoModel.get_todo_by_user(user)
        return make_response(render_template('todo.html', items=query, user=user))
class EditTodo(Resource):
    def post(self):
        print(request.args.get("items"))
        print(request.args.get("expire_time"))
        print(type(request.args.get("id")))
        id = request.args.get("id")
        items = request.args.get("items")
        expire_time = request.args.get("expire_time")
        return make_response(render_template('edit_todo.html',id=id, items=items, expire_time=expire_time))

class EditPost(Resource):
    def post(self):
        print(request.args)
        todo_data = todo_schema.load(request.form)
        print(todo_data)
        items = todo_data['items']
        expire_time = todo_data['expire_time']
        todo = TodoModel(todo_data,username=session.get('username'))
        todo.update_db(request.args.get('id'), items, expire_time)
        return redirect(url_for('todolist.showtodo'))

class DeleteTodo(Resource):
    def post(self):
        id = request.args.get("id")
        todo = TodoModel
        todo.delete_db(id)
        return redirect(url_for('todolist.showtodo'))


api.add_resource(AddTodo, '/todoo')
api.add_resource(ShowTodo, '/show')
api.add_resource(EditTodo,'/edit')
api.add_resource(EditPost,'/editpost')
api.add_resource(DeleteTodo,'/deletetodo')