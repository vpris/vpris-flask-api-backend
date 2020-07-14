from database_setup import Base, Article
from flask import Flask, request, render_template, url_for, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///blog.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/posts')
def posts():
    articles = session.query(Article).order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/posts/<int:id>')
def post_detail(id):
    article = session.query(Article).get(id)
    return render_template("post_detail.html", article=article)


@app.route('/posts/<int:id>/del', methods=['GET', 'POST'])
def post_delete(id):
    article = session.query(Article).filter_by(id=id).one()

    if request.method == 'POST':
        session.delete(article)
        session.commit()
        return redirect(url_for('posts', article=id))
    else:
        return redirect(url_for('posts', article=id))


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = session.query(Article).filter_by(id=id).one()

    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        session.commit()
        return redirect('/posts')
    else:
        return "При редактировании статьи произошла ошибка!"


@app.route('/create_article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        article = Article(title=request.form['title'],
                          intro=request.form['intro'],
                          text=request.form['text'])
        session.add(article)
        session.commit()
        return redirect(url_for('posts'))
    else:
        return render_template("create_article.html")


"""
api functions
"""
from flask import jsonify


def get_posts():
    posts = session.query(Article).all()
    return jsonify(posts=[a.serialize for a in posts])


def get_post(id):
    posts = session.query(Article).filter_by(id=id).one()
    return jsonify(posts=posts.serialize)


def makeANewPost(title, intro, text):
    addedarticle = Article(title=title, intro=intro, text=text)
    session.add(addedarticle)
    session.commit()
    return jsonify(Article=addedarticle.serialize)


def updatePost(id, title, intro, text):
    updatedPost = session.query(Article).filter_by(id=id).one()
    if not title:
        updatedPost.title = title
    if not intro:
        updatedPost.intro = intro
    if not text:
        updatedPost.text = text
    session.add(updatedPost)
    session.commit()
    return 'Updated a Book with id %s' % id


def deleteAPost(id):
    postToDelete = session.query(Article).filter_by(id=id).one()
    session.delete(postToDelete)
    session.commit()
    return 'Removed Post with id %s' % id


@app.route('/')
@app.route('/api', methods=['GET', 'POST'])
def postsFunction():
    if request.method == 'GET':
        return get_posts()
    elif request.method == 'POST':
        title = request.args.get('title', '')
        intro = request.args.get('intro', '')
        text = request.args.get('text', '')
        return makeANewPost(title, intro, text)


@app.route('/api/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def postFunctionId(id):
    if request.method == 'GET':
        return get_post(id)

    elif request.method == 'PUT':
        title = request.args.get('title', '')
        intro = request.args.get('intro', '')
        text = request.args.get('text', '')
        return updatePost(id, title, intro, text)

    elif request.method == 'DELETE':
        return deleteAPost(id)


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port='2001')
