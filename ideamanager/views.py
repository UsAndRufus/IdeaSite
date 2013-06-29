#!/usr/bin/python2.7

#Imports

#General
from django.utils import timezone

#http
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404, get_list_or_404

#idea & user models
from django.db import models
from django.contrib.auth.models import User
from ideamanager.models import Idea, Tag, IdeaTag, IdeaLink


#idea routing
from ideamanager.idearouter import CalculateBestMatch, GetLinkedUsers

#forms
from ideamanager.forms import *

#login/logout
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required #login redirect

#extras, eg ordered dictionaries
from collections import OrderedDict

#forms
#from django.forms import widgets <-- not needed, at least I think :P





def index(request):
    latest_idea_list = Idea.objects.all().order_by('-date_created')[:5]
    is_public_ideas = False
    for idea in latest_idea_list:
        if idea.is_private == False:
            is_public_ideas = True
            
    #t = loader.get_template('ideamanager/index.html')
    #c = Context({
    #    'latest_idea_list': latest_idea_list,
    #    'is_public_ideas': is_public_ideas,
    #})
    #return HttpResponse(t.render(c))
    
    context_dict =  {'latest_idea_list': latest_idea_list,
                    'is_public_ideas': is_public_ideas, 
                    'user': request.user,}
    
    return render_to_response('ideamanager/index.html', context_dict)
    
def idea_detail(request, global_idea_id):
    i = get_object_or_404(Idea, pk=global_idea_id)
    
    it = get_list_or_404(IdeaTag, global_idea_id = global_idea_id)
    
    #IdeaLink stuff
    il = CalculateBestMatch(i)
    il_sorted = OrderedDict(sorted(il.items(), key=lambda x: x[1], reverse=True))
   
    return render_to_response('ideamanager/idea_detail.html', {'idea': i, 'idea_tag_list': it, 'weighting_dict': il_sorted, 'user':request.user,})
    
def idea_view_all(request):
    all_ideas = Idea.objects.all().order_by('-date_created')
    
    return render_to_response('ideamanager/view_all_ideas.html', {'all_ideas': all_ideas, 'user': request.user,})
    
    
@login_required
def idea_creator(request):
    
    exists=False
    
    if request.method == 'POST': # If the form has been submitted...
        form = AddIdeaForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            
            found_user=get_object_or_404(User, username__iexact=request.user)
            
            i = Idea(user_id=found_user, title=form.cleaned_data['title'], text=form.cleaned_data['text'], is_private=form.cleaned_data['private'], date_created=timezone.now())
            
            try:
                found_idea = Idea.objects.get(user_id=found_user,title__iexact=form.cleaned_data['title'])
            except Idea.DoesNotExist:#if there is not an idea in the database with that name created by that user then save it and the Tags, IdeaTags and IdeaLinks
                i.save()
                
                tags = form.cleaned_data['tags'].split()
                
                tag_list = []
                
                #working out if tags exist
                for t in tags:
                    try:
                        found_tag = Tag.objects.get(name__iexact=t)
                        #try finding tag in database
                    except Tag.DoesNotExist:
                        #if it doesn't, add it
                        tag_to_create=Tag(name=t)
                        tag_to_create.save()
                        found_tag = Tag.objects.get(name__iexact=t)
                        
                    #now that the tag is in the database, add it to a list of the tag objects (tag_list). 
                    #tags is just a list of names, tag_list is a list ofTag objects.
                    tag_list.append(found_tag)
            
            
                idea_tag_list = []
                
                #create IdeaTags
                for tag_item in tag_list:
                    idea_tag=IdeaTag(global_idea_id=i,tag_id=tag_item)
                    idea_tag_list.append(idea_tag)
                    idea_tag.save()
                
                
                #create IdeaLink records
                for idea_tag_item in idea_tag_list:
                    matching_idea_tags = []
                    matching_idea_tags = IdeaTag.objects.filter(tag_id=idea_tag_item.tag_id)
                    for match in matching_idea_tags:
                        if idea_tag_item.global_idea_id != match.global_idea_id:
                            idea_link = IdeaLink(idea1=idea_tag_item.global_idea_id, idea2=match.global_idea_id, tag=match.tag_id)
                            idea_link.save()
                            idea_link_backwards = IdeaLink(idea1=match.global_idea_id, idea2=idea_tag_item.global_idea_id, tag=match.tag_id)
                            idea_link_backwards.save()
                
                redirect = '/idea/' + str(i.global_idea_id) + '/'
                return HttpResponseRedirect(redirect)
            
            #if we get to here, the form was valid but the idea already existed and hence has not been saved. 
            #We thus need to redirect the user back to the homepage with an error message.
            exists=True
        else:
            pass

    else:
        form = AddIdeaForm() # An unbound form
    
    
    return render_to_response('ideamanager/add_idea.html',{'form': form,'exists':exists},context_instance=RequestContext(request))
    #request context parameter above is to handle csrf token on page
    

def login_page(request):
    
    invalid = False
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect('/')
            else:
                # Return a 'disabled account' error message
                return HttpResponse('account disabled')
        else:
            invalid = True
            return render_to_response('ideamanager/login.html',{'invalid': invalid}, context_instance=RequestContext(request))
    else:
        pass
    
    #if we get here, method is not post so we just show it the normal page
    return render_to_response('ideamanager/login.html',{'invalid':invalid},context_instance=RequestContext(request))
    #request context parameter above is to handle csrf token on page
    
'''
def login_request(request):
    
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            # Return a 'disabled account' error message
            return HttpResponse('account disabled')
    else:
        return HttpResponseRedirect('/accounts/login/')
'''


def logout_request(request):
    logout(request)
    return HttpResponseRedirect('/')    
    
def register(request):
    userexists = False
    passconflict = False
    valid = True

    if request.method == 'POST': # If the form has been submitted...
        form = RegisterForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            
            try:
                form.check_username()
            except forms.ValidationError:
                valid = False
                userexists=True
            
            try:
                form.check_password()
            except forms.ValidationError:
                valid = False
                passconflict=True

            if valid:
                form.save()
                return HttpResponseRedirect('/accounts/register/success/') # Redirect after POST

    else:
        form = RegisterForm() # An unbound form
    

    
    return render_to_response('ideamanager/register.html', {'form': form, 'userexists': userexists,'passconflict': passconflict,},context_instance=RequestContext(request))
    
def register_success(request):
    return HttpResponseRedirect('/')
    
    
def user_detail(request, user_id):
    user_viewing = User.objects.get(pk=user_id)
    user_ideas = Idea.objects.filter(user_id=user_id)
    
    related_users = GetLinkedUsers(user_viewing)
    
    ru_sorted = OrderedDict(sorted(related_users.items(), key=lambda x: x[1], reverse=True))
    
    
    return render_to_response('ideamanager/user_detail.html', {'ideas': user_ideas, 'user': request.user, 'user_viewing':user_viewing, 'related_users':ru_sorted,})
    

    
def tag_detail(request, tag_name):
    t = Tag.objects.get(name = tag_name)
    it_list = IdeaTag.objects.filter(tag_id = t)
    
    ideas = []
    
    for it in it_list:
        id = it.global_idea_id.global_idea_id
        i = Idea.objects.get(global_idea_id = id)
        ideas.append(i)
    
    return render_to_response('ideamanager/tag_detail.html', {'user': request.user, 'tag':t,'ideas': ideas,})
    
    
    
    

