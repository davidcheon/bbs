from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
import views
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bbs.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$',views.index),
    url(r'^index(.html)?/$',views.index),
    url(r'^bbs_detail/(\d+)/',views.bbs_detail),
    url(r'^bbs_news/$',views.bbs_news),
    url(r'^bbs_sports/$',views.bbs_sports),
    url(r'^bbs_men/$',views.bbs_men),
    url(r'^registerdetail/(.*/)?$',views.registerdetail),
    url(r'^loginout/$',views.loginout),
    url(r'^login/(.*?/)?$',views.login),
    url(r'^updateuser/$',views.updateuser),
    url(r'^bbs_pub/(\d+)/$',views.bbs_pub),
    url(r'^add_sub_comment/$',views.add_sub_comment),
    url(r'user_bbs/(.*/)?$',views.user_bbs),
    url(r'^user_comments/(.*/)?$',views.user_comments),
    url(r'^getonlineusers/(.*/)?$',views.getonlineusers),
    url(r'^chatroom/(.*/)?$',views.chatroom),
    url(r'^getchatcontent/(.*/)?',views.getchatcontent),
    url(r'^sendmessage/(.*/)?',views.sendmessage),
    url(r'^bbs_remove/(\d+)/$',views.bbs_remove),
)