from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('ideamanager.views',
    # Examples:
    # url(r'^$', 'IdeaSite.views.home', name='home'),
    # url(r'^IdeaSite/', include('IdeaSite.foo.urls'))
    
    url(r'^$', 'index'),
    url(r'^idea/(?P<global_idea_id>\d+)/$', 'idea_detail'),
    url(r'^idea/all/$', 'idea_view_all'),
    url(r'^idea/creator/$', 'idea_creator'),
    url(r'^accounts/login/$', 'login_page'),
    url(r'^accounts/logout/logout_request/$', 'logout_request'),
    url(r'^accounts/register/$', 'register'),
    url(r'^accounts/register/success/$', 'register_success'),
    url(r'^accounts/user/(?P<user_id>\d+)/$', 'user_detail'),
    url(r'^tag/(?P<tag_name>\w+)/$', 'tag_detail'),
)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),#admin
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

#+-------------------------------------------------------------------------------------------------------------------------------+
#|**please note apps URLs are not decoupled from project - if I want to plug the app somewhere else I will need to change this!**|
#+-------------------------------------------------------------------------------------------------------------------------------+