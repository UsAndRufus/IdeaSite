#idea & user models
from django.db import models
from django.contrib.auth.models import User
from ideamanager.models import Idea, Tag, IdeaTag, IdeaLink

from django.db.models import Count

from collections import OrderedDict


def FetchRelated(idea1):
    '''
    try:
        found_idea = Idea.objects.get(name__iexact=idea)
    except Idea.DoesNotExist:
        error = ['no idea found']
        return error
    '''
    
    idea_id=idea1.global_idea_id
    
    
    linked = IdeaLink.objects.filter(idea1=idea_id)
    #this returns a list of dictionary objects with idea1 and idea2 fields
    

    
    return(linked)
    
def CalculateBestMatch(idea1):
    #excludes private ideas
    
    
    #gets related ideas
    linked = FetchRelated(idea1)
    
    
    linknames = []
    for item in linked:
        if item.idea2.is_private == False:
            linknames.append(item.generateLinkName())
        
    
    checked = []
    weighting_dict = {}
    
    
    for item in linked:
        if item.generateLinkName() not in checked:
            if item.idea2.is_private == False:
                weighting = CalculateWeighting(item.generateLinkName(),linknames)
                weighting_dict[item.idea2] = weighting
                
            checked.append(item.generateLinkName())
    
    
    
    return(weighting_dict)

def CalculateWeighting(item,linknames):
    weighting = 0
    for i in linknames:
        if item == i:
            weighting = weighting + 1

    
    return(weighting)
    
'''    
def GetAuthorUsers(linked):
    
    authorUsers = []
    
    for item in linked:
        currentUser = item
'''


def GetLinkedUsers(user):
    userIdeas = Idea.objects.filter(user_id=user.id)
    relatedUsers = {}
    
    for idea in userIdeas:
        weighting_dict = CalculateBestMatch(idea)
        for key, value in weighting_dict.items():
            u = key.user_id
            if u not in relatedUsers:
                relatedUsers[u]=0

            relatedUsers[u] += value  
    
    return(relatedUsers)




