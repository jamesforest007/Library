from flask import Blueprint, render_template, redirect, url_for, request, abort, current_app, send_file, jsonify
from flask_login import login_required, current_user
from app.models import Company, db, User, TEAM_CHOICES
from werkzeug.security import generate_password_hash
from app.utils import admin_required
from functools import wraps
import datetime

# Define sector and industry choices
SECTOR_CHOICES = {
    'Manufacturing': [
        'Automotive',
        'Electronics',
        'Food & Beverage',
        'Textiles',
        'Machinery'
    ],
    'Technology': [
        'Software',
        'Hardware',
        'IT Services',
        'Telecommunications',
        'Cloud Computing'
    ],
    'Healthcare': [
        'Hospitals',
        'Pharmaceuticals',
        'Medical Devices',
        'Biotechnology',
        'Healthcare Services'
    ],
    'Financial Services': [
        'Banking',
        'Insurance',
        'Investment',
        'Fintech',
        'Asset Management'
    ]
}

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
        }
    ]
    return render_template('index.html', menu_items=menu_items)


@main.route('/dashboard')
@login_required
def dashboard():  
    return redirect(url_for('main.index'))


def team_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        company_id = kwargs.get('id')
        if company_id:
            company = Company.query.get_or_404(company_id)
            if not current_user.same_team(company):
                abort(403)
        return f(*args, **kwargs)
    return decorated_function

@main.route('/companies')
@login_required
def companies():
    search = request.args.get('search', '')
    query = Company.query
    
    if not current_user.is_admin:
        # Get the first team from user's team list for filtering
        user_teams = current_user.team_list
        if user_teams:
            query = query.filter(Company.teams.in_(user_teams))
    
    if search:
        search_term = f"%{search}%"
        companies = query.filter(
            db.or_(
                Company.name.ilike(search_term),
                Company.sector.ilike(search_term),
                Company.industry.ilike(search_term),
                Company.location.ilike(search_term),
                Company.contact_person.ilike(search_term)
            )
        ).all()
    else:
        companies = query.all()
    return render_template('companies.html', companies=companies)

@main.route('/companies/add', methods=['GET', 'POST'])
@login_required
def add_company():
    if request.method == 'POST':
        company = Company(
            name=request.form['name'],
            sector=request.form['sector'],
            industry=request.form['industry'],
            team=current_user.team_list[0] if current_user.team_list else None,  # Use first team
            created_by=current_user.id,
            location=request.form['location'],
            contact_person=request.form['contact_person'],
            email=request.form['email'],
            phone=request.form['phone'],
            status='Active'
        )
        db.session.add(company)
        db.session.commit()
        return redirect(url_for('main.companies'))
    return render_template('add_company.html', 
                         sectors=SECTOR_CHOICES.keys(),
                         sectors_json=SECTOR_CHOICES)

@main.route('/companies/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@team_required
def edit_company(id):
    company = Company.query.get_or_404(id)
    if request.method == 'POST':
        company.name = request.form['name']
        company.sector = request.form['sector']
        company.industry = request.form['industry']
        company.location = request.form['location']
        company.contact_person = request.form['contact_person']
        company.email = request.form['email']
        company.phone = request.form['phone']
        db.session.commit()
        return redirect(url_for('main.companies'))
    return render_template('edit_company.html', 
                          company=company,
                          sectors=SECTOR_CHOICES.keys(),
                          sectors_json=SECTOR_CHOICES)

@main.route('/companies/delete/<int:id>')
@login_required
@team_required
def delete_company(id):
    company = Company.query.get_or_404(id)
    db.session.delete(company)
    db.session.commit()
    return redirect(url_for('main.companies'))

@main.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@main.route('/users/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    if request.method == 'POST':
        selected_teams = request.form.getlist('teams')
        user = User(
            username=request.form['username'],
            password=generate_password_hash(request.form['password']),
            teams=','.join(selected_teams),
            is_active=True,
            is_admin=request.form.get('is_admin', False) == 'on'
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.users'))
    return render_template('add_user.html', teams=TEAM_CHOICES)

@main.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.username = request.form['username']
        selected_teams = request.form.getlist('teams')
        user.teams = ','.join(selected_teams)
        if request.form['password']:
            user.password = generate_password_hash(request.form['password'])
        user.is_admin = request.form.get('is_admin', False) == 'on'
        db.session.commit()
        return redirect(url_for('main.users'))
    return render_template('edit_user.html', user=user, teams=TEAM_CHOICES)

@main.route('/users/toggle/<int:id>')
@login_required
@admin_required
def toggle_user(id):
    user = User.query.get_or_404(id)
    user.is_active = not user.is_active
    db.session.commit()
    return redirect(url_for('main.users'))

@main.route('/example')
def example():
    # Access config values
    secret = current_app.config['SECRET_KEY']
    db_uri = current_app.config['SQLALCHEMY_DATABASE_URI']
    
    # Use in pagination
    page_size = current_app.config['ITEMS_PER_PAGE']
    return f"Config values: {secret}, {db_uri}, {page_size}"

@main.route('/company/download-excel')
@login_required
def download_company_excel():
    # Generate Excel file
    excel_data = Company.export_to_excel()
    
    # Create response with Excel file
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'companies_{timestamp}.xlsx'
    
    return send_file(
        excel_data,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename  # For newer Flask versions
    )

@main.route('/company/upload-excel', methods=['POST'])
@login_required
def upload_company_excel():
    if 'excel_file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    excel_file = request.files['excel_file']
    
    if excel_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    # Check if file is an Excel file
    if not excel_file.filename.endswith(('.xls', '.xlsx')):
        return jsonify({'error': 'File is not an Excel file'}), 400
    
    try:
        # Process the Excel file
        Company.import_from_excel(excel_file)
        return jsonify({'success': 'Company data has been updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500 