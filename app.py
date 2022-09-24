from flask import Flask, request
from controller.userController import signup, signin, infoUserToken 

app = Flask(__name__)

app.add_url_rule('/api/reg/', view_func=signup, methods=['POST'])
app.add_url_rule('/api/login/', view_func=signin, methods=['POST'])
app.add_url_rule('/api/infoUserToken/', view_func=infoUserToken, methods=['GET'])

if __name__ == "__main__":
    app.run()