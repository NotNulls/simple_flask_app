from email.message import Message
from dubinsko import app, mail
from flask import current_app, render_template, request
from dubinsko.email import send_email
from dubinsko.forms import ContactForm


@app.route("/",methods=["GET","POST"])
@app.route("/home", methods=["GET","POST"])
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