from email.message import Message
from dubinsko import app, mail
from flask import current_app, render_template, request, redirect, g, abort, url_for
from dubinsko.email import send_email
from dubinsko.forms import ContactForm
from dubinsko import app
from flask import session


@app.before_request
def before():
    if request.view_args and 'lang_code' in request.view_args:
        if request.view_args['lang_code'] not in ('en','rs'):
            return abort(404)
        g.current_lang = request.view_args['lang_code']
        request.view_args.pop('lang_code')

@app.route("/<lang_code>",methods=["GET","POST"])
@app.route("/home", methods=["GET","POST"])
@app.route("/", methods=["GET","POST"])
def home_page():
    form = ContactForm()
    
    
    if request.method == "POST":
        name = form.name.data
        email = form.email_address.data
        message = form.message.data


        try:
             send_email(
                 subject=name,
                 sender=email,
                 recipients=current_app.config['MAIL_USERNAME'],
                 text_body=message,
                
             )

        except:
             return render_template('index.html', form = form)
    
    return render_template('index.html', form = form)


@app.route('/onama')
def about_page():
    render_template('about_us.html')


@app.route('/<lang_code>/about')
def index():
    return render_template('about_us.html')

@app.route('/language=<language>')
def set_language(language=None):
    session['language'] = language
    return redirect(url_for('home_page'))