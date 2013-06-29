from ideamanager.models import Idea, Tag, IdeaTag, IdeaLink
from django.contrib import admin

admin.site.register(Idea)
admin.site.register(Tag)
admin.site.register(IdeaTag)
admin.site.register(IdeaLink)