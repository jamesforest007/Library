from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required
from app.models import Book, db
from pdb import set_trace

# Create a blueprint named 'main'
# This blueprint will handle all the main routes of our application
main = Blueprint('main', __name__)

# Routes in this blueprint start with '/'
@main.route('/')
@login_required
def index():
    menu_items = [
        {
            'id': 1,
            'name': 'Dashboard',
            'link': 'dashboard',
            'icon': 'fa fa-dashboard',
            'priority': 500,
            'parent_menu': '',
            'status': 'Active'
        },
        # Add more menu items here
    ]
    return render_template('index.html', menu_items=menu_items)


@main.route('/dashboard')
@login_required
def dashboard():  
    return redirect(url_for('main.index'))


@main.route('/books')
@login_required
def books():
   
    books = Book.query.all()
    return render_template('books.html', books=books)

@main.route('/books/add', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        book = Book(
            title=request.form['title'],
            author=request.form['author'],
            category=request.form['category'],
            rack=request.form['rack'],
            available=True
        )
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('main.books'))
    return render_template('add_book.html')

@main.route('/books/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_book(id):
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.category = request.form['category']
        book.rack = request.form['rack']
        db.session.commit()
        return redirect(url_for('main.books'))
    return render_template('edit_book.html', book=book)

@main.route('/books/delete/<int:id>')
@login_required
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('main.books')) 