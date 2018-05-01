from django.conf.urls import url
from .views import RegisterKey,Sign,LogIn,LogOut, HomePage, PostOne, DeleteOne, UpdateOne, GetList,List, Delete, Patch, GetOne, ForgotKey, MailKey,LoginForm,Api

urlpatterns=[

    # Home Page
    url(r'^$',LogIn),

    


    # Generating django forms
    url(r'^registerkey/$',RegisterKey),
    url(r'^loginform$',LoginForm),
    url(r'^postone/$', PostOne),
    url(r'^getlist/$', GetList),
    url(r'^getone/$', GetOne),
    url(r'^deleteone/$', DeleteOne),
    url(r'^updateone/$', UpdateOne),
    url(r'^getfkey/', ForgotKey),


    # for saving users credential in db
    url(r'^sign/$', Sign),
    url(r'^login/$',LogIn),
    url(r'^logout$',LogOut),


    # made as per the instruction given in the article
    url(r'^list/$',List),

    # to handle request made by django forms
    url(r'^delete/$', Delete),
    url(r'^patch/$', Patch),
    url(r'^mailkey/', MailKey),

    url(r'^api/(?P<email>.+)/(?P<key>\w{0,50})$', Api)

]