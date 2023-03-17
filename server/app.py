from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# tell browser to give permission to make request to the server using JS
CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


# GET request to show all the messages in '/messages' route
@app.route('/messages', methods=["GET", "POST"])
def messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()

    if request.method == "GET":
        messages_dict = [message.to_dict() for message in messages]
        response = make_response(messages_dict, 200)
        return response
    
    elif request.method == "POST":
        message_body = Message(
            body=request.get_json()['body'],
            username=request.get_json()["username"]
        )
        db.session.add(message_body)
        db.session.commit()
        response = make_response(message_body.to_dict(), 201)
        return response
    
    def __repr__(self):
        return f"""<Message {self.id}: {self.body}, username:{self.username}"""
    

@app.route('/messages/<int:id>', methods=["GET", "DELETE", "PATCH"])
def messages_by_id(id):

    message = Message.query.filter_by(id=id).first()

    if not message:
        response_body = {
            "message": "This message does not exist. Please try again."
        }
        response = make_response(jsonify(response_body), 404)
        return response
    else:
        if request.method == "GET":
            message_dict = message.to_dict()
            response = make_response(message_dict, 200)
            return response
        elif request.method == "DELETE":
            db.session.delete(message)
            db.session.commit()

            response_body = {
                "delete_successful": True,
                "message": "Message deleted."
            }
            response = make_response(response_body, 200)
            return response
        elif request.method == "PATCH":
            # message = Message.query.filter_by(id=id).first()
            # request.get_json() -> Parses the incoming JSON request data and returns it.
            # convert json data into python data.
            for attr in request.get_json():
                setattr(message, attr, request.get_json()[attr])
            db.session.add(message)
            db.session.commit()
            response = make_response(message.to_dict(), 200)
            return response
            



if __name__ == '__main__':
    app.run(port=5555)
