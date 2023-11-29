from flask import Blueprint, render_template

main = Blueprint("main", __name__)

@main.route('/')
def index():
    if('options' in locals()):
        return render_template('mixview.html',title='Personal Mixer',content = "Body goes here!")
    
    else:
        return render_template('mixview.html',title='Personal Mixer',content = "Body goes here!")

@main.route('/about')
def description():
    return "<body><p>\
    this is a desription</p></body>"


@main.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404