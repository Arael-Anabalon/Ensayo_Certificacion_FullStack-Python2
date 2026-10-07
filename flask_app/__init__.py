from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "52004134eb2b6940f0f5bf14adfede8b8ff53bb91dd005b71ae9519d8fe29739"
bcrypt = Bcrypt(app)