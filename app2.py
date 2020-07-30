from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restplus import Resource, Api, fields


# configuration
DEBUG = True

# instantiate the app2
app2 = Flask(__name__)
api = Api(app2)
app2.config.from_object(__name__)

# enable CORS
CORS(app2, resources={r'/*': {'origins': '*'}})

BOOKS = [
    {
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

VOTE_SEED = [
    {
        'id': 1,
        'title': 'Yellow Pail!!',
        'description': 'On-demand sand castle construction expertise.',
        'url': '#',
        'votes': 16,
        'avatar': 'public/images/avatars/daniel.jpg',
        'submissionImage': 'public/images/submissions/image-yellow.png',
    },
    {
        'id': 2,
        'title': 'Supermajority: The Fantasy Congress League',
        'description': 'Earn points when your favorite politicians pass legislation.',
        'url': '#',
        'votes': 11,
        'avatar': 'public/images/avatars/kristy.png',
        'submissionImage': 'public/images/submissions/image-rose.png',
    },
    {
        'id': 3,
        'title': 'Tinfoild: Tailored tinfoil hats',
        'description': 'We have your measurements and shipping address.',
        'url': '#',
        'votes': 17,
        'avatar': 'public/images/avatars/veronika.jpg',
        'submissionImage': 'public/images/submissions/image-steel.png',
    },
    {
        'id': 4,
        'title': 'Haught or Naught',
        'description': 'High-minded or absent-minded? You decide.',
        'url': '#',
        'votes': 9,
        'avatar': 'public/images/avatars/molly.png',
        'submissionImage': 'public/images/submissions/image-aqua.png',
    }
]

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return (VOTE_SEED)

@app2.route('/vote', methods=['GET', 'POST'])
def all_votes():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        VOTE_SEED.append({
            'id': post_data.get('id'),
            'title': post_data.get('title'),
            'description': post_data.get('description'),
            'url': post_data.get('url'),
            'votes': post_data.get('votes'),
            'avatar': post_data.get('avatar'),
            'submissionImage': post_data.get('submissionImage')
        })
        response_object['message'] = 'Post added!'
    else:
        response_object['articles'] = VOTE_SEED
    return jsonify(response_object)

@app2.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)

# sanity check route
@app2.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


if __name__ == '__main__':
    app2.run()