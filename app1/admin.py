from django.contrib import admin
from app1 import models
class BBS_User_Admin(admin.ModelAdmin):
    list_display=('bbs_user','bbs_user_signature','bbs_user_photo',)
class Category_Admin(admin.ModelAdmin):
    list_display=('category_name','category_manager',)
class BBS_Admin(admin.ModelAdmin):
    list_display=('bbs_title','bbs_summary','bbs_from_user','signature','bbs_create_date','bbs_in_category',)
    list_filter=('bbs_create_date',)
    search_fields=('bbs_title','bbs_from_user__bbs_user__username','bbs_summary',)
    def signature(self,obj):
        return obj.bbs_from_user.bbs_user_signature
    signature.short_description='user_description'
class BBS_Comment_Admin(admin.ModelAdmin):
    list_display=('comment_to_bbs','comment_from_user','comment_create_date',)
class BBS_Comment_To_Comment_Admin(admin.ModelAdmin):
    list_display=('comment_to_comment_to_comment','comment_to_comment_content','comment_to_comment_from_user',
                  'comment_to_comment_create_date',)
class OnlineUser_Admin(admin.ModelAdmin):
    list_display=('ip','user','login_date')
class Chatroom_Admin(admin.ModelAdmin):
    list_display=('fromuser','content','pubdate')
class SendMessage_Admin(admin.ModelAdmin):
    list_display=('fromuser','content','senddate')
class BBS_User_Loginout_Infor_Admin(admin.ModelAdmin):
    list_display=('user','ip','login_date','logout_date')
# Register your models here.
admin.site.register(models.BBS,BBS_Admin)
admin.site.register(models.BBS_Comment,BBS_Comment_Admin)
admin.site.register(models.BBS_User,BBS_User_Admin)
admin.site.register(models.Category,Category_Admin)
admin.site.register(models.BBS_Comment_To_Comment,BBS_Comment_To_Comment_Admin)
admin.site.register(models.OnlineUser,OnlineUser_Admin)
admin.site.register(models.ChatContent,Chatroom_Admin)
admin.site.register(models.SendMessage,SendMessage_Admin)
admin.site.register(models.BBS_User_Loginout_Infor,BBS_User_Loginout_Infor_Admin)