from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from backend.appAPI.chatbot_with_retriever import chatbot_knowledge_retriever
from backend.appAPI.coding_assistant import coding_assistant
from backend.appAPI.project_requirement import project_generator
from backend.appAPI.title_generation import title_generator
from backend.appAPI.utils import get_secret
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os 

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

load_dotenv()

app.config['AWS_ACCESS_KEY_ID'] = os.getenv('AWS_ACCESS_KEY_ID')
app.config['AWS_SECRET_ACCESS_KEY'] = os.getenv('AWS_SECRET_ACCESS_KEY')
app.config['CO_API_KEY'] = os.getenv('CO_API_KEY')


@app.route('/')

def home():
    return render_template('loginPage.html')

@app.route('/about')
def about():
    return render_template("aboutPage.html")

@app.route('/ai')
def ai():
    return render_template("index.html")

@app.route('/profile')
def profile():
    return render_template("profilePage.html")

@app.route('/canvas')
def canvas():
    return render_template("canvasPage.html")

@app.route('/chatbot', methods=['POST'])
def get_response_from_ai(): #General Chat Bot
    data = request.get_json()
    print(data)
    user_input = data.get('input')
    session_id = data.get("sessionID")

    if not user_input:
        return jsonify({'error': 'No input provided'}), 400
    result = chatbot_knowledge_retriever(session_id=session_id, query=user_input)

    return jsonify({'result': result}), 200

@app.route('/codingchatbot', methods=['POST'])
def get_coding_assistant(): # Coding Assistant
    data = request.get_json()
    user_input = data.get("input")
    session_id = data.get("sessionID")
    project_requirement = data.get("pr")
    if not user_input:
        return jsonify({'error': 'No input provided'}), 400
    result = coding_assistant(session_id=session_id, query=user_input, project=project_requirement)

    return jsonify({'result': result})

@app.route("/gtitle", methods=["POST"])
def generate_title(): # Title Generation for Chat Conversation
    data=request.get_json()
    session_id= data.get("sessionID")
    user_input= data.get("input")
    if not user_input:
        return jsonify({'error': 'No input provided'}), 400
    result = title_generator(session_id=session_id, query=user_input)
    return jsonify({'result': result})

@app.route("/gproject", methods=["POST"])
def generate_project_requirement(): # Project Requirement and Description
    data=request.get_json()
    session_id= data.get("sessionID")
    level = data.get("level")
    target_alg = data.get("alg")
    application = data.get("application")

    result = project_generator(session_id=session_id, ML_Past_Experience=level, Application_of_the_project=application, Algorithm_Wanted_to_try=target_alg )

    return jsonify({"result": result})

db = None
collection = None

def connect():
    db_name = "MLHorizon"
    collection_name = "MLUserDataStorage"
    uri = get_secret("mongodb_connection_url")
    #"mongodb+srv://zeyucai:1234567890@mldatabase.36zie.mongodb.net/?retryWrites=true&w=majority&appName=MLDatabase"
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    global db 
    db = client[db_name]
    global collection 
    collection = db[collection_name]

connect()
# Endpoint to get all users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = list(collection.find({}))
        data = {}
        # Convert MongoDB documents to JSON format
        for user in users:
            user['_id'] = str(user['_id'])  # Convert ObjectId to string
            data[user["googleID"]] = user
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to add a new user
@app.route('/users', methods=['POST'])
def add_user():
    new_user = request.get_json()
    unique_id = new_user.get("USERID")

    try:
        existing_user = collection.find_one({"USERID": unique_id})
        if not existing_user:
            new_user['chatBotConversations'] = []
            new_user['canvasConversations'] = []
            collection.insert_one(new_user)  # Add new user
            return jsonify({'message': 'User added successfully!'}), 201
        else:
            # Update the existing user
            collection.update_one(
                {"USERID": unique_id},
                {"$set": {"chatBotConversations": new_user['chatBotConversations']}}
            )
            return jsonify({'message': 'User updated successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/users', methods=['PUT'])
def replace_user():
    replace_data = request.get_json()
    replace_data["_id"] = ""
    unique_id = replace_data.get("USERID")
    try:
        user_data = collection.find_one({"USERID": unique_id})
        for info in user_data:
            if info not in replace_data:
                replace_data[info] = user_data[info]
        # Update the existing user
        collection.update_one(
            {"USERID": unique_id},
            {"$set": {
                "googleID": replace_data["googleID"],
                "firstName": replace_data["firstName"],
                "lastName" : replace_data["lastName"],
                "emial": replace_data["email"],
                "chatBotConversations": replace_data['chatBotConversations'],
                "canvasConversations" : replace_data["canvasConversations"]
                }})
        return jsonify({'message': 'User updated successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)