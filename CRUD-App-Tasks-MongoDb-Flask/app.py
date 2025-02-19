from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
import os

app = Flask(__name__)
title = "Tasks Organizer"
heading = "Tasks Organizer Application"

client = MongoClient("mongodb://mongo-service:27017")
db = client.mymongodb    #Select the database
todos = db.todo #Select the collection name

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

@app.route("/list")
def lists ():
	#Display the all Tasks
	todos_l = todos.find()
	a1="active"
	return render_template('index.html',a1=a1,todos=todos_l,t=title,h=heading)

@app.route("/")
@app.route("/uncompleted")
def tasks ():
	#Display the Uncompleted Tasks
	print("welcome to the app")
	todos_l = todos.find({"done":"no"})
	a2="active"
	return render_template('index.html',a2=a2,todos=todos_l,t=title,h=heading)


@app.route("/completed")
def completed ():
	#Display the Completed Tasks
	todos_l = todos.find({"done":"yes"})
	a3="active"
	return render_template('index.html',a3=a3,todos=todos_l,t=title,h=heading)


@app.route("/done")
def done():
	# Done-or-not ICON
	id = request.values.get("_id")
	task = todos.find_one({"_id": ObjectId(id)})  # Use find_one instead of find for a single document

	# Check and toggle the "done" status
	if task["done"] == "yes":
		todos.update_one({"_id": ObjectId(id)}, {"$set": {"done": "no"}})
	else:
		todos.update_one({"_id": ObjectId(id)}, {"$set": {"done": "yes"}})

	# Redirect after update
	return redirect(redirect_url())


@app.route("/action", methods=['POST'])
def action ():
	#Adding a Task
	name=request.values.get("name")
	desc=request.values.get("desc")
	date=request.values.get("date")
	pr=request.values.get("pr")
	todos.insert_one({ "name":name, "desc":desc, "date":date, "pr":pr, "done":"no"})
	return redirect("/list")

@app.route("/remove")
def remove():
    # Delete a task by ID
    id = request.values.get("_id")
    todos.delete_one({"_id": ObjectId(id)})  # Replace remove with delete_one
    return redirect("/")


@app.route("/update")
def update ():
	id=request.values.get("_id")
	task=todos.find({"_id":ObjectId(id)})
	return render_template('update.html',tasks=task,h=heading,t=title)


@app.route("/action3", methods=['POST'])
def action3():
	# Updating a Task with various references
	name = request.values.get("name")
	desc = request.values.get("desc")
	date = request.values.get("date")
	pr = request.values.get("pr")
	id = request.values.get("_id")

	# Update the task with new values
	todos.update_one(
		{"_id": ObjectId(id)},
		{"$set": {"name": name, "desc": desc, "date": date, "pr": pr}}
	)
	return redirect("/")


@app.route("/search", methods=['GET'])
def search():
	#Searching a Task with various references

	key=request.values.get("key")
	refer=request.values.get("refer")
	if(key=="_id"):
		todos_l = todos.find({refer:ObjectId(key)})
	else:
		todos_l = todos.find({refer:key})
	return render_template('searchlist.html',todos=todos_l,t=title,h=heading)

if __name__ == "__main__":

    app.run(host='0.0.0.0', port=5000)

