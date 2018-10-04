"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, redirect, url_for, request
from Mount_Farmer import app
import config_cosmos_db
import pydocumentdb.document_client as document_client
from forms import realm_form, char_form, validators
from functions import check_mounts, get_model_list, get_mounts, get_faction

@app.route('/')
def index():
    return redirect(url_for('home'))
@app.route('/home', methods=['GET', 'POST'])
def home():
    """Renders the home page."""
    chars_form = char_form()
    realms_form = realm_form()    
    if realms_form.validate_on_submit():
        if chars_form.validate_on_submit():
            character_name =  chars_form.charname.data
            realm_name = realms_form.realm_select.data
            return redirect(url_for('results', character_name=character_name,realm_name=realm_name))
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        realms_form=realms_form,
        chars_form=chars_form
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message="If you need to contact me"
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='World of Warcraft Mount Farmer providers an easy way to check what your most common missing mounts are.'
    )

@app.route('/model')
def model():
    """Renders the model page."""
    model_list = get_model_list()
    model_list_len = range(len(model_list))
    #mount_id = Match_Mount_ID()
    return render_template(
        'model.html',
        title='Mount Model',
        message='Below is a list of every mount in World of Warcraft and the approximated percentage of the player base that owns it.',
        model_list=model_list,
        model_list_len=model_list_len,
        year=datetime.now().year,
    )

@app.route('/results', methods=['GET', 'POST'])
def results():
    """Renders the results page."""
    character_name = request.args['character_name']
    realm_name = request.args['realm_name']
    realm_name = realm_name[:-5]
    user_mounts = get_mounts(character_name, realm_name)
    user_faction = get_faction(character_name, realm_name)
    user_mount_match = check_mounts(user_mounts, user_faction)
    user_mount_top10 = user_mount_match[:20]
    user_mount_top10_len = range(len(user_mount_top10))
    return render_template(
        'results.html',
        message='Below is a list of the top 10 mounts you have not obtained when compared to the most acquired mounts',
        title='Results',
        user_mount_top10=user_mount_top10,
        user_mount_top10_len=user_mount_top10_len,
        year=datetime.now().year,
    )