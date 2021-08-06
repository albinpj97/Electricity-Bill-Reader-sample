"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,request,redirect
from Main_Project_Flask import app
from Main_Project_Flask.extraction import textExtraction

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
            'index.html',
            title='Home')
    
@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Corporate Headquarters'
    )
@app.route('/result',methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        #return render_template('result.html',title='Result')
        if 'file' not in request.files:
            return render_template('index.html',title='Home',name = "Home Page")
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            #flash('No selected file')
            return render_template('index.html',title='Home',name = "Home Page")
        if file:  
            #image = file.read()
            cn,dd,dis_d,pay=textExtraction(file)
            if(cn==0 and dd==0 and dis_d==0 and pay==0):
                return render_template('retake.html',title='Result',name = "Invalid Input")
            else:
                return render_template('result.html',title='Result',cons_num = cn, dued  = dd, disc = dis_d ,probsd = pay )
@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='This Application help to read Electricity Bill'
    )
