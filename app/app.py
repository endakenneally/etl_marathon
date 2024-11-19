from flask import Flask
from routes import api_blueprint

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(api_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
