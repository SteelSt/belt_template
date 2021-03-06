#import needed django modules
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib import auth

#import bcrypt
import bcrypt

#  import our db(s)
from .models import User

#This is our index page and contains login and registration forms
def loginandreg(request):
    return render(request,'python_belt_exam_app/loginandreg.html')

#Processes information from the registration form
def process_register(request, methods=['POST']):
    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = User.objects.register_validator(request.POST)
    # check if the errors object has anything in it
    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
            print("WEVE HIT AN ERROR")
        # redirect the user back to the form to fix the errors
        return redirect('/', id)
    else:
        # if the errors object is empty, that means there were no errors!
        # add our new record to the table , push what we need to session,
        # and redirect to /landing to render our final page
        User.objects.create(first_name=request.POST['input_first_name'], last_name=request.POST['input_last_name'], email=request.POST['input_email'], password=bcrypt.hashpw(request.POST['input_password'].encode('utf8'), bcrypt.gensalt()))
        request.session['user_id'] = User.objects.last().id
        request.session['isloggedin'] = True
        request.session['user_email'] = request.POST['input_email']
        request.session['welcomename'] = request.POST['input_first_name']
        request.session['welcomemessage'] = 'Successfully registered!'
        request.session['errors'] = ""
        return redirect('/landing')

def process_login(request, methods=['POST']):
    # Query the data we need
        query = User.objects.all().values('id', 'email', 'first_name', 'password')
        # Iterate through query until we find user email then verify password is legit
        for row in query:
            if row['email'] == request.POST['login_email'] and bcrypt.checkpw(request.POST['login_password'].encode(), row['password'].encode()): 
                request.session['isloggedin'] = True
                request.session['user_id'] = row['id']
                request.session['user_email'] = row['email']
                request.session['welcomename'] = row['first_name']
                request.session['welcomemessage'] = 'Successfully logged in!'
                request.session['errors'] = ""
                return redirect('/landing')
        #if a matching email addy and pass is not found return to index w/ an error message in session
        request.session['errors'] = "• Please Try Again"
        return redirect('/')

#This is the landing page that the user arrives at after registering or logging in
def landing(request):
    # If the user has a isLoggedin session
    query = User.objects.filter(id=request.session['user_id']).values('id', 'email')
    if 'isloggedin' in request.session:
        for row in query:
            print("ITERATING...")
            if request.session['user_id'] == row['id'] and request.session['user_email'] == row['email']:
                return render(request,'python_belt_exam_app/landing.html')
            else:
                return redirect('/')
    else:
        return redirect('/')

# Clears out session / logs out the user
def logout(request):
    auth.logout(request)
    return redirect('/')