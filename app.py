from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://aditijagdale:AditiJagdale12@cluster1.4lmvqqz.mongodb.net/library_db?retryWrites=true&w=majority"

mongo = PyMongo(app)
books_collection = mongo.db.books

# Home route for rendering HTML page
@app.route('/')
def index():
    books = list(books_collection.find())
    return render_template('index.html', books=books)

# API: Get all books
@app.route('/api/books', methods=['GET'])
def get_books():
    books = []
    for book in books_collection.find():
        book['_id'] = str(book['_id'])
        books.append(book)
    return jsonify(books)

# API: Get book by ID
@app.route('/api/books/<id>', methods=['GET'])
def get_book(id):
    book = books_collection.find_one({'_id': ObjectId(id)})
    if book:
        book['_id'] = str(book['_id'])
        return jsonify(book)
    return jsonify({'message': 'Book not found'}), 404

# API: Add new book
@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.get_json()
    if not data.get('title') or not data.get('isbn'):
        return jsonify({'error': 'Title and ISBN required'}), 400
    book_id = books_collection.insert_one({
        'title': data['title'],
        'author': data.get('author', ''),
        'year': data.get('year', 0),
        'isbn': data['isbn']
    }).inserted_id
    return jsonify({'message': 'Book added successfully', 'book_id': str(book_id)}), 201

# API: Update book
@app.route('/api/books/<id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()
    result = books_collection.update_one({'_id': ObjectId(id)}, {'$set': data})
    if result.matched_count:
        return jsonify({'message': 'Book updated successfully'})
    return jsonify({'message': 'Book not found'}), 404

# API: Delete book
@app.route('/api/books/<id>', methods=['DELETE'])
def delete_book(id):
    result = books_collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count:
        return jsonify({'message': 'Book deleted successfully'})
    return jsonify({'message': 'Book not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)





