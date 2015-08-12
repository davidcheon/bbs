from django.db import models
import bbs
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    category_name=models.CharField(max_length=20,unique=True)
    category_manager=models.ForeignKey('BBS_User')
    def __unicode__(self):
        return self.category_name
class BBS_User(models.Model):
    bbs_user=models.OneToOneField(User)
    bbs_user_signature=models.CharField(max_length=100,default="nothing to leave")
    bbs_user_photo=models.ImageField(upload_to=bbs.settings.BASE_DIR+"/upload_imgs",default=bbs.settings.BASE_DIR+"/upload_imgs/default.png")
    def __unicode__(self):
        return self.bbs_user.username
class BBS_Comment(models.Model):
    comment_content=models.TextField()
    comment_to_bbs=models.ForeignKey('BBS')
    comment_from_user=models.ForeignKey('BBS_User')
    comment_create_date=models.DateTimeField()
    def __unicode__(self):
        return 'Comment:'+self.comment_to_bbs.bbs_title
class BBS_Comment_To_Comment(models.Model):
    comment_to_comment_content=models.TextField()
    comment_to_comment_from_user=models.ForeignKey('BBS_User')
    comment_to_comment_create_date=models.DateTimeField(auto_now_add=True)
    comment_to_comment_to_comment=models.ForeignKey('BBS_Comment')
    def __unicode__(self):
        return 'Comment:'+self.comment_to_comment_to_comment.comment_from_user.bbs_user.username
    
class BBS(models.Model):
    bbs_title=models.CharField(max_length=30)
    bbs_content=models.TextField()
    bbs_summary=models.CharField(max_length=100,blank=True,null=True)
    bbs_create_date=models.DateTimeField(auto_now_add=True)
    bbs_from_user=models.ForeignKey('BBS_User')
    bbs_in_category=models.ForeignKey('Category')
    def __unicode__(self):
        return self.bbs_title
class OnlineUser(models.Model):
    ip=models.CharField(max_length=30)
    user=models.ForeignKey('BBS_User')
    login_date=models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.user.bbs_user.username
class ChatContent(models.Model):
    fromuser=models.ForeignKey('BBS_User')
    content=models.CharField(max_length=100,blank=True,null=True)
    pubdate=models.DateTimeField(auto_now_add=True)
    get_latest_by=['pubdate']
    def __unicode__(self):
        return self.fromuser.bbs_user.username+'@said@'+self.content
class SendMessage(models.Model):
    fromuser=models.ForeignKey('BBS_User')
    touser=models.CharField(max_length=30)
    content=models.CharField(max_length=100,blank=True,null=True)
    senddate=models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.fromuser.bbs_user.username+' send: '+self.content+' $to$ '+self.touser+' at '+str(self.senddate)
class BBS_User_Loginout_Infor(models.Model):
    user=models.ForeignKey('BBS_User')
    ip=models.CharField(max_length=60,blank=True,null=True)
    login_date=models.DateTimeField(auto_now_add=True)
    logout_date=models.DateTimeField(null=True,blank=True)
    def __unicode__(self):
        return self.user.bbs_user.username+':login:'+str(self.login_date)+' logout:'+str(self.logout_date)+' from '+self.ip
