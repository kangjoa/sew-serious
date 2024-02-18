from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from sewing_app.models import Fabric, Pattern
from sewing_app.forms import FabricForm, PatternForm

# Import app and db from events_app package so that we can run app
from sewing_app.extensions import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################


@main.route('/')
def homepage():
    all_fabrics = Fabric.query.all()
    all_fabrics_names = ', '.join([fabric.name for fabric in all_fabrics])
    print(f"All fabric names: {all_fabrics_names}")
    return render_template('home.html', all_fabrics=all_fabrics)


@main.route('/new_fabric', methods=['GET', 'POST'])
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
def new_pattern():
    # Create a PatternForm
    form = PatternForm()

    # If form was submitted and was valid:
    # - create a new Pattern object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the pattern detail page.
    if form.validate_on_submit():
        new_pattern = Pattern(
            name=form.name.data,
            category=form.category.data,
            photo_url=form.photo_url.data,
        )

        fabrics = form.fabrics.data
        for fabric_id in fabrics:
            fabric = Fabric.query.get(fabric_id)
            new_pattern.fabrics.append(fabric)
            if fabric:
                new_pattern.fabrics.append(fabric)

        db.session.add(new_pattern)
        db.session.commit()

        flash('New pattern was created successfully!')
        return redirect(url_for('main.pattern_detail', pattern_id=new_pattern.id))

    # Send the form to the template and use it to render the form fields
    return render_template('new_pattern.html', form=form)


@main.route('/fabric/<fabric_id>', methods=['GET', 'POST'])
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
