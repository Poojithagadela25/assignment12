from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# In-Memory Data Store
books = [
    {'id': 1, 'title': 'The Pragmatic Programmer', 'author': 'Andrew Hunt'},
    {'id': 2, 'title': 'Clean Code', 'author': 'Robert C. Martin'},
    {'id': 3, 'title': 'Introduction to Algorithms', 'author': 'Thomas H. Cormen'}
]

# Route to get all books or search by title and author
@app.route('/api/books', methods=['GET'])
def get_books():
    """
    Get the list of all books or search by title and/or author.
    """
    # Retrieve optional query parameters for title and author
    title = request.args.get('title')
    author = request.args.get('author')
    
    # Start with all books
    filtered_books = books
    
    # If a title is provided, filter the books by title (case-insensitive)
    if title:
        filtered_books = [book for book in filtered_books if title.lower() in book['title'].lower()]
    
    # If an author is provided, filter the books by author (case-insensitive)
    if author:
        filtered_books = [book for book in filtered_books if author.lower() in book['author'].lower()]
    
    # Return the filtered list of books in JSON format
    return jsonify({'books': filtered_books})

# Route to get a book by its ID
@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """
    Get a single book by ID.
    """
    # Search for the book in the list
    book = next((book for book in books if book['id'] == book_id), None)
    if book is None:
        # If the book is not found, return a 404 response
        abort(404)
    return jsonify({'book': book})

# Route to create a new book
@app.route('/api/books', methods=['POST'])
def create_book():
    """
    Create a new book.
    """
    # Check if the request contains JSON data and required fields
    if not request.json or not 'title' in request.json or not 'author' in request.json:
        # Bad request if 'title' or 'author' is missing in the request
        abort(400)
    # Create a new book object
    new_book = {
        'id': books[-1]['id'] + 1 if books else 1,  # Incremental ID
        'title': request.json['title'],
        'author': request.json['author']
    }
    books.append(new_book)
    # Return the new book with 201 Created status
    return jsonify({'book': new_book}), 201

# Route to update an existing book
@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """
    Update a book by ID.
    """
    # Find the book to update
    book = next((book for book in books if book['id'] == book_id), None)
    if book is None:
        # If the book is not found, return a 404 response
        abort(404)
    if not request.json:
        # Bad request if no JSON data is provided
        abort(400)
    # Update the book's title and author if provided in the request
    book['title'] = request.json.get('title', book['title'])
    book['author'] = request.json.get('author', book['author'])
    return jsonify({'book': book})

# Route to delete a book
@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """
    Delete a book by ID.
    """
    # Find the book to delete
    book = next((book for book in books if book['id'] == book_id), None)
    if book is None:
        # If the book is not found, return a 404 response
        abort(404)
    books.remove(book)
    # Return an empty response with 204 No Content status
    return '', 204

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    """
    Custom 404 error handler.
    """
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    """
    Custom 400 error handler.
    """
    return jsonify({'error': 'Bad request'}), 400

# Starting the Application
if __name__ == '_main_':
    app.run(debug=True)