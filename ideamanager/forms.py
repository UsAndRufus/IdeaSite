from django import forms #importing Django's forms module
from django.db import models
from django.contrib.auth.models import User #importing the Django User object
from ideamanager.models import * #importing my custom models from models.py


class RegisterForm(forms.Form):#this is the form used in registraton
    username = forms.CharField(max_length=20)
    password1=forms.CharField(max_length=30,widget=forms.PasswordInput())
    password2=forms.CharField(max_length=30,widget=forms.PasswordInput())
    email=forms.EmailField(max_length=30)
    
    
    
    
    def check_username(self): # check if username does not exist
        try:
            User.objects.get(username=self.cleaned_data['username']) #get user from user model
        except User.DoesNotExist:#if the user does not exist, return the data to say so
            return self.cleaned_data['username']
        
        raise forms.ValidationError("User already exists")#if the user does exist, return an error message
    
    
    def check_password(self): # checking if password1 and password2 match each other
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:#check if both pass first validation
            if self.cleaned_data['password1'] != self.cleaned_data['password2']: # check if they match each other
                raise forms.ValidationError("Passwords do not match")#if the match, return a validation error
       
        return self.cleaned_data
    
    def save(self): # used to save the idea
        new_user=User.objects.create_user(self.cleaned_data['username'],
                                          self.cleaned_data['email'],
                                          self.cleaned_data['password1'])
        new_user.save()

class AddIdeaForm(forms.Form):#this is the form used in idea creation
    title = forms.CharField(max_length = 30)
    text = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField()
    private = forms.BooleanField(required=False)
    
    '''def check_idea_exists(user,self):#check if user already has an idea with that name
        try:
            Idea.objects.get(title=self.cleaned_data['title'], user_id=user.id)
        except Idea.DoesNotExist:
        pass
    '''#already have this in views, to save time I'm going to leave it there (for now at least) rather than adding to the form validation logic here
    
    
    
