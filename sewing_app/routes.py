from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from sewing_app.models import Fabric, Pattern, User
from sewing_app.forms import FabricForm, PatternForm, SignUpForm, LoginForm

# Import app and db from sewing_app package so that we can run app
from sewing_app.extensions import app, db, bcrypt

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)

##########################################
#           Routes                       #
##########################################


@main.route('/')
def homepage():
    all_fabrics = Fabric.query.all()
    all_fabrics_names = ', '.join([fabric.name for fabric in all_fabrics])
    print(f"All fabric names: {all_fabrics_names}")
    return render_template('home.html', all_fabrics=all_fabrics)


@main.route('/patterns')
def patterns():
    all_patterns = Pattern.query.all()
    return render_template('patterns.html', all_patterns=all_patterns)


@main.route('/new_fabric', methods=['GET', 'POST'])
@login_required
def new_fabric():
    # Create a FabricForm
    form = FabricForm()

    # If form was submitted and was valid:
    if form.validate_on_submit():
        # create a new Fabric object and save it to the database
        new_fabric = Fabric(
            name=form.name.data,
            color=form.color.data,
            quantity=form.quantity.data,
            photo_url=form.photo_url.data
        )
        db.session.add(new_fabric)
        db.session.commit()

        # flash a success message, and
        # redirect the user to the fabric detail page.
        flash('New fabric was created successfully!')
        return redirect(url_for('main.fabric_detail', fabric_id=new_fabric.id))
    # Send the form to the template and use it to render the form fields
    return render_template('new_fabric.html', form=form)


@main.route('/new_pattern', methods=['GET', 'POST'])
@login_required
def new_pattern():
    # Create a PatternForm
    form = PatternForm()

    # If form was submitted and was valid:
    # - create a new Pattern object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the pattern detail page.
    if form.validate_on_submit():
        # Extract fabric IDs from form data
        fabric_ids = [fabric.id for fabric in form.fabrics.data]

        # Retrieve Fabric objects based on extracted IDs
        fabrics = [Fabric.query.get(id) for id in fabric_ids]
        new_pattern = Pattern(
            name=form.name.data,
            category=form.category.data,
            photo_url=form.photo_url.data,
            fabrics=fabrics
        )

        db.session.add(new_pattern)
        db.session.commit()

        flash(f'New pattern "{new_pattern.name}" was created successfully!')
        return redirect(url_for('main.pattern_detail', pattern_id=new_pattern.id))

    # Send the form to the template and use it to render the form fields
    return render_template('new_pattern.html', form=form)


@main.route('/fabric/<fabric_id>', methods=['GET', 'POST'])
@login_required
def fabric_detail(fabric_id):
    fabric = Fabric.query.get(fabric_id)
    # Create a FabricForm and pass in `obj=fabric`
    form = FabricForm(obj=fabric)

    # If form was submitted and was valid:
    # - update the Fabric object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the fabric detail page.
    if form.validate_on_submit():
        form.populate_obj(fabric)
        db.session.commit()

        flash('Fabric was updated successfully!')
        return redirect(url_for('main.fabric_detail', fabric_id=fabric.id))

    # Send the form to the template and use it to render the form fields
    fabric = Fabric.query.get(fabric_id)
    return render_template('fabric_detail.html', fabric=fabric, form=form)


@main.route('/pattern/<pattern_id>', methods=['GET', 'POST'])
@login_required
def pattern_detail(pattern_id):
    pattern = Pattern.query.get(pattern_id)
    # Create a PatternForm and pass in `obj=pattern`
    form = PatternForm(obj=pattern)

    # If form was submitted and was valid:
    # - update the Pattern object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the pattern detail page.
    if form.validate_on_submit():
        form.populate_obj(pattern)
        db.session.commit()

        flash('Pattern was updated successfully!')
        return redirect(url_for('main.pattern_detail', pattern_id=pattern.id))

    # Send the form to the template and use it to render the form fields
    pattern = Pattern.query.get(pattern_id)
    return render_template('pattern_detail.html', pattern=pattern, form=form)


@main.route('/add_to_patterns_list/<pattern_id>', methods=['POST'])
@login_required
def add_to_patterns_list(pattern_id):
    """Add a pattern to the logged in user's patterns list."""
    pattern = Pattern.query.get(pattern_id)
    current_user.patterns_list_items.append(pattern)
    db.session.commit()
    flash(f'Pattern "{pattern.name}" was added to your patterns list!')
    return redirect(url_for('main.patterns_list'))


@main.route('/remove_from_patterns_list/<pattern_id>', methods=['POST'])
@login_required
def remove_from_patterns_list(pattern_id):
    """Remove a pattern from the logged in user's patterns list."""
    pattern = Pattern.query.get(pattern_id)
    current_user.patterns_list_items.remove(pattern)
    db.session.commit()
    flash(f'Pattern "{pattern.name}" was removed from your patterns list!')
    return redirect(url_for('main.patterns_list'))


@main.route('/patterns_list')
@login_required
def patterns_list():
    """Get logged in user's patterns list and display in a template."""
    patterns_list = current_user.patterns_list_items
    return render_template('patterns_list.html', patterns_list=patterns_list)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))
