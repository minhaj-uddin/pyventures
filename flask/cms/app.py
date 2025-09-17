from flask import Flask
from flask_cors import CORS
from models import db
from routes import articles, comments, tags

app = Flask(__name__)
app.config.from_object("config.Config")

CORS(app)
db.init_app(app)

app.register_blueprint(articles.bp, url_prefix='/api/articles')
app.register_blueprint(comments.bp, url_prefix='/api/comments')
app.register_blueprint(tags.bp, url_prefix='/api/tags')


@app.route('/')
def home():
    return {"message": "Flask SPA CMS backend is running"}


if __name__ == "__main__":
    app.run(debug=True)
