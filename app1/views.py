#!coding:utf-8
from django.views.decorators.cache import cache_page
from django.shortcuts import render, render_to_response
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.
import models,json,threading,time
from django import forms
from django.contrib import auth
from datetime import datetime, timedelta
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import thread
# from app1 import server
class MyThread(threading.Thread):
    t=None
    def __init__(self):
        super(MyThread,self).__init__()
        self.status=True
    @staticmethod
    def getInstance():
        if MyThread.t==None:
            MyThread.t=MyThread()
        return MyThread.t 
    def run(self):
        while self.status:
            time.sleep(10)
            ds=[]
            now=datetime.now()
            oneday=timedelta(days=1)
            standard=(now-oneday).strftime('%s')
            cs=models.ChatContent.objects.order_by('pubdate')
            for c in cs:
                if c.pubdate.strftime('%s')<standard:
                    ds.append(c)
            for d in ds:
                d.delete()
            print '----run-----',self.status
    
    def setstatus(self,value):
        self.status=value
    def getstatus(self):
        return self.status
class SendMessageForm(forms.Form):
    content=forms.CharField(label="留言",widget=forms.Textarea)
class ChatForm(forms.Form):
    content=forms.CharField(label='聊天内容',widget=forms.Textarea)
class userdetail(forms.Form):
    username=forms.CharField(max_length=50)
    email=forms.CharField(max_length=100)
    bbs_signature=forms.CharField(max_length=100)
    bbs_user_photo=forms.FileField()
class commentform(forms.Form):
    comment_content=forms.CharField(label='留言内容',widget=forms.Textarea)
class registerform(forms.Form):
    username=forms.CharField(max_length=50)
    password=forms.CharField(widget=forms.PasswordInput)
    password2=forms.CharField(widget=forms.PasswordInput)
    email=forms.CharField(max_length=100)
    bbs_user_signature=forms.CharField(max_length=100)
    bbs_user_photo=forms.FileField()
class loginform(forms.Form):
    username=forms.CharField(max_length=50)
    password=forms.CharField(widget=forms.PasswordInput)
def getstatus(request):
    information={}
    username=request.session.get('username','anonymous')
    action1='logout' if username!='anonymous' else 'login'
    action2='detail' if username!='anonymous' else 'register'
    information['username']=username
    information['action1']=action1
    information['action2']=action2
    return information
def updateuserdate(request):
    pass

def addtoonlineuser(request,username):
    if request.META.has_key('HTTP_X_FORWARD_FOR'):
        ip=request.META['HTTP_X_FORWARD_FOR']
    else:
        ip=request.META['REMOTE_ADDR']
#     user=models.BBS_User.objects.filter(bbs_user=user)[0]
    s=cache.get('username',set())
    s.add(username)
    cache.set('username',s)
#     models.OnlineUser.objects.create(ip=ip,user=user,login_date=datetime.now())
def removeonlineuser(request,username):
    if request.META.has_key('HTTP_X_FORWARD_FOR'):
        ip=request.META['HTTP_X_FORWARD_FOR']
    else:
        ip=request.META['REMOTE_ADDR']
    us=cache.get('username',set())
    if us!=set():
        us.remove(username)
    cache.set('username',us)
#     models.OnlineUser.objects.filter(user=user).delete()
t=MyThread()
# @cache_page(20*1)
# @csrf_exempt
def index(request):
#     if request.META.has_key('HTTP_X_FORWARD_FOR'):
#         print cache.get(request.META['HTTP_X_FORWARD_FOR'],None)
#     else:
#         print cache.get(request.META['REMOTE_ADDR'],None)
    if request.session.get('username','anonymous')!='anonymous':
        t=globals()['t'] if 't' in globals().keys() else MyThread()
        globals()['t']=t
        if not t.getstatus():
            t.setstatus(True)
            if not t.isAlive():
                t.start()
        else:
            if not t.isAlive():
                t.start()
       
    bbs_list=cache.get('bbs_list') if cache.get('bbs_list')!=None else models.BBS.objects.all()
    cache.set('bbs_list',bbs_list,10)
    return render_to_response('index.html',{'bbs_list':bbs_list,'information':getstatus(request),'onlineusers':json.loads(getonlineuser(request)),'order':0},
                              context_instance=RequestContext(request))
def bbs_detail(request,bbs_id):
    cf=commentform()
    if request.method=='POST':
        user=request.session.get('username','anonymous')
        if user=='anonymous':
            return HttpResponseRedirect('/login/')
        q={}
        q['comment_content']=request.POST['comment_content']
        q['comment_to_bbs']=models.BBS.objects.get(id=bbs_id)
        q['comment_from_user']=models.BBS_User.objects.get(bbs_user__username__exact=user)
        q['comment_create_date']=datetime.now()
        models.BBS_Comment.objects.create(comment_content=q['comment_content'],
                                         comment_to_bbs=q['comment_to_bbs'],
                                         comment_from_user=q['comment_from_user'],
                                         comment_create_date=q['comment_create_date'] )
    bbs=models.BBS.objects.get(id=bbs_id)
    comments=models.BBS_Comment.objects.filter(comment_to_bbs__id=bbs_id).all()
    comments=list(comments)
    comments.reverse()
    com_to_com={}
    for com in comments:
        cs=models.BBS_Comment_To_Comment.objects.filter(comment_to_comment_to_comment__id=com.id).all()
        com_to_com[com.id]=cs
    return render_to_response('bbs_detail.html',{'bbs':bbs,'comments':comments,'com_to_com':com_to_com,'cf':cf,'information':getstatus(request),
                                                 },context_instance=RequestContext(request))
def bbs_men(request):
    if cache.get('bbs_men_list')!=None:
        bbs_list=cache.get('bbs_men_list')
    else:
        bbs_list=models.BBS.objects.filter(bbs_in_category__category_name__exact='men').all()
    cache.set('bbs_men_list',bbs_list,10)
    return render_to_response('bbs_men.html',{'bbs_list':bbs_list,'information':getstatus(request),'order':3},
                              context_instance=RequestContext(request))
def bbs_sports(request):
    if cache.get('bbs_men_list')!=None:
        bbs_list=cache.get('bbs_men_list')
    else:
        bbs_list=models.BBS.objects.filter(bbs_in_category__category_name__exact='sports').all()
    cache.set('bbs_men_list',bbs_list,10)
    return render_to_response('bbs_sports.html',{'bbs_list':bbs_list,'information':getstatus(request),'order':2},
                              context_instance=RequestContext(request))
def bbs_news(request):
    if cache.get('bbs_men_list')!=None:
        bbs_list=cache.get('bbs_men_list')
    else:
        bbs_list=models.BBS.objects.filter(bbs_in_category__category_name__exact='news').all()
    cache.set('bbs_men_list',bbs_list,10)
    return render_to_response('bbs_news.html',{'bbs_list':bbs_list,'information':getstatus(request),'order':1},
                              context_instance=RequestContext(request))
def registerdetail(request,name=None):
    
    if request.method=='POST':
        rf=registerform(request.POST,request.FILES)
        if rf.is_valid():
            u=User.objects.filter(username=rf.cleaned_data['username'])
            if u:
                return render_to_response('register.html',{'rf':registerform(),'information':getstatus(request),'error':'username is already existed'})
            ps1=rf.cleaned_data['password']
            ps2=rf.cleaned_data['password2']
            if ps1!=ps2:
                return render_to_response('register.html',{'rf':registerform(),'information':getstatus(request),'error':'password is not same'})
            user=User()
            user.username=rf.cleaned_data['username']
            user.set_password(ps1)
            user.email=rf.cleaned_data['email']
            user.save()
            if user:
                buser=models.BBS_User.objects.create(bbs_user=user,bbs_user_signature=rf.cleaned_data['bbs_user_signature'],
                                                     bbs_user_photo=rf.cleaned_data['bbs_user_photo'])
                if buser:
                    request.session['username']=user.username
                    if request.META.has_key('HTTP_X_FORWARD_FOR'):
                        ip=cache.get(request.META['HTTP_X_FORWARD_FOR'],None)
                    else:
                        ip=cache.get(request.META['REMOTE_ADDR'],None)
                    models.BBS_User_Loginout_Infor.objects.create(user=buser,ip=ip)
                    return HttpResponseRedirect('/')
    else:
#         if request.session.get('username','anonymous')=='anonymous':
#             return HttpResponseRedirect('/login/')
        user=name.strip('/') if name!=None else request.session.get('username','anonymous')
        if user!='anonymous':
            buser=models.BBS_User.objects.get(bbs_user__username__exact=user)
            bs=models.BBS.objects.filter(bbs_from_user=buser)
            luser=models.BBS_User_Loginout_Infor.objects.filter(user=buser)
            lastlogin=None
            lastlogout=None
            if len(luser)!=0:
                luser=luser[0]
                lastlogin=luser.login_date
                lastlogout=luser.logout_date
            items=models.SendMessage.objects.filter(touser__exact=user)
            ud={}
            ud['items']=items
            ud['bs']=bs
            ud['username']=buser.bbs_user.username
            ud['email']=buser.bbs_user.email
            ud['bbs_signature']=buser.bbs_user_signature
            ud['bbs_user_photo']=buser.bbs_user_photo
            ud['user']=user
            ud['lastlogin']=lastlogin
            ud['lastlogout']=lastlogout
#             request.session['temp']=user
            return render_to_response('userdetail.html',{'ud':ud,'information':getstatus(request),'onlineusers':json.loads(getonlineuser(request)),
                                                         'sendmessageform':SendMessageForm()},
                                      context_instance=RequestContext(request))
        else:
            rf=registerform()
            return render_to_response('register.html',{'rf':rf,'information':getstatus(request)})
def user_comments(request,name=None):
    if request.method=='GET':
#         user=request.session['temp'] if request.session.get('temp','anon')!='anon' else 'anonymous'
        if request.session.get('username','anonymous')=='anonymous':
            return HttpResponseRedirect('/login/')
        user=name.strip('/') if name !=None else 'anonymous'
        if user!='anonymous':
            try:
                ud={}
                buser=models.BBS_User.objects.get(bbs_user__username__exact=user)
            except Exception,e:
                ud['cs']=None
            else:
                cs=models.BBS_Comment.objects.filter(comment_from_user=buser)
                ud['cs']=cs
                ud['user']=user
            return render_to_response('user_comments.html',{'ud':ud,'information':getstatus(request)},
                                      context_instance=RequestContext(request))
    return HttpResponseRedirect('/')
def user_bbs(request,name=None):
    if request.method=='GET':
#         user=request.session['temp'] if request.session.get('temp','anon')!='anon' else 'anonymous'
        if request.session.get('username','anonymous')=='anonymous':
            return HttpResponseRedirect('/login/')
        user=name.strip('/') if name !=None else 'anonymous'
        if user!='anonymous':
            try:
                ud={}
                buser=models.BBS_User.objects.get(bbs_user__username__exact=user)
            except Exception,e:
                ud['bs']=None
            else:
                bs=models.BBS.objects.filter(bbs_from_user=buser)
                ud['bs']=bs
                ud['user']=user
            return render_to_response('user_bbs.html',{'ud':ud,'information':getstatus(request)},
                                      context_instance=RequestContext(request))
    return HttpResponseRedirect('/')
def loginout(request):
    #user=request.session.get('username','anonymous')
    user=request.session.get('username','anonymous')
    if request.session.exists('temp'):
        request.session['temp'].delete()
    if  user=='anonymous':
        return HttpResponseRedirect('/login/')
    else:
        del request.session['username']
        loginuser=models.BBS_User_Loginout_Infor.objects.filter(user__bbs_user__username__exact=user).update(logout_date=datetime.now())
#         if loginuser[0]:
#             print dir(loginuser[0])
#             loginuser[0].update(logout_date=datetime.now())
        auth.logout(request)
        if t.getstatus():
            t.setstatus(False)
            del globals()['t']
       
#         u=models.BBS_User.objects.filter(bbs_user__username__exact=user)
        removeonlineuser(request,user)
#         addtoonlineuser(request, user).delete()
        return HttpResponseRedirect('/')
@csrf_protect
def login(request,next):
    if request.method=='GET':
        return render_to_response('login.html',{'lf':loginform(),'information':getstatus(request)},
                                  context_instance=RequestContext(request))
    else:
        lf=loginform(request.POST)
        if lf.is_valid():
            #user=User.objects.filter(username=lf.cleaned_data['username'],password=make_password(password=lf.cleaned_data['password'], salt='a', hasher='pbkdf2_sha256'))
            user=auth.authenticate(username=lf.cleaned_data['username'],password=lf.cleaned_data['password'])
            if user:
                request.session['username']=user.username
                addtoonlineuser(request,user.username)
                if request.META.has_key('HTTP_X_FORWARD_FOR'):
                    ip=cache.get(request.META['HTTP_X_FORWARD_FOR'],None)
                else:
                    ip=cache.get(request.META['REMOTE_ADDR'],None)
                finduser=models.BBS_User_Loginout_Infor.objects.filter(user=user)
                if finduser:
                    finduser.update(login_date=datetime.now(),logout_date=None)
                else:                    
                    models.BBS_User_Loginout_Infor.objects.create(user=models.BBS_User.objects.filter(bbs_user=user)[0],
                                                              ip=ip)
#                 t=globals()['t'] if 't' in globals().keys()else MyThread()
#                 globals()['t']=t
#                 if not t.getstatus():
#                     t.setstatus(True)
#                     if not t.isAlive():
#                         t.start()
#                 else:
#                     t.start()
                if not next:
                    return HttpResponseRedirect('/')
#                     return render_to_response('index.html',context_instance=RequestContext(request))
                else:
                    return HttpResponseRedirect('/'+next)
            else:
                return render_to_response('login.html',{'error':'username or password is wrong','lf':loginform()})
def updateuser(request):
    if request.method=='POST':
        ud=userdetail(request.POST,request.FILES)
        if ud.is_valid():
            user=User.objects.get(username__exact=request.user.username)
            user.username=ud.cleaned_data['username']
            user.email=ud.cleaned_data['email']
            uus=models.BBS_User.objects.get(bbs_user__username__exact=request.user.username)
            uus.bbs_user_signature=ud.cleaned_data['bbs_signature']
            uus.bbs_user_photo=ud.cleaned_data['bbs_user_photo']
            user.save()
            uus.save()
            request.session['username']=user.username
            return HttpResponseRedirect('/')
        else:
            return render_to_response('userdetail.html',{'error':'update failed','information':getstatus(request),
                                                         },
                                      context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')
def bbs_pub(request,cate_id):
    username=request.session['username']
    if request.method=='GET':
        if username=='anonymous':
            return HttpResponseRedirect('/login')
        else:
            cats={'1':'Sports Pub','2':'News Pub','3':'Men Pub'}
            return render_to_response('bbs_pub.html',{'information':getstatus(request),'cate':cats[str(cate_id)]},
                                      context_instance=RequestContext(request))
    else:
        if username!='anonymous':
            title=request.POST.get('bbs_title','no title')
            content=request.POST.get('bbs_content','no content')
            summary=request.POST.get('bbs_summary','no summary')
            from_user=models.BBS_User.objects.get(bbs_user__username__exact=username)
            cate=models.Category.objects.get(id=cate_id)
            bbs=models.BBS.objects.create(bbs_title=title,bbs_content=content,
                                          bbs_summary=summary,bbs_from_user=from_user,
                                          bbs_in_category=cate)
            if bbs:
                return HttpResponseRedirect('/')
            else:
                return render_to_response('bbs_pub.html',{'error':'pub error'})
        else:
            return render_to_response('bbs_pub.html',{'information':getstatus(request),'error':'login first'})
def add_sub_comment(request):
    if request.method=='POST':
        from_user=request.session.get('username','anonymous')
        next=request.POST['cate']+request.POST['id']+'/'
        if from_user=='anonymous':return HttpResponseRedirect('/login'+next)
        content=request.POST['comment_to_comment_content']
        from_user=models.BBS_User.objects.filter(bbs_user__username__exact=from_user)[0]
        comment_to_comment_to_comment=models.BBS_Comment.objects.filter(id=request.POST['tocommentid'])[0]
        com=models.BBS_Comment_To_Comment.objects.create(comment_to_comment_content=content,
                                                        comment_to_comment_from_user=from_user,
                                                        comment_to_comment_to_comment=comment_to_comment_to_comment,)
        com.save()
        return HttpResponseRedirect(next)
    else:
        return HttpResponseRedirect('/')
def getonlineuser(request):
#     us=models.OnlineUser.objects.all()
    us=cache.get('username',set())
    users=[]
    if len(us)==0:
        users.append('nobody online')
    elif len(us)==1:
        users.append('only myself')
    else:
        for u in us:
            if u!=request.session.get('username','anonymous'):
                users.append(u)
    return json.dumps(users)
def getonlineusers(request,args=None):
    return  HttpResponse(getonlineuser(request))
def chatroom(request,args=None):
    if not request.session.has_key('username'):
        return HttpResponseRedirect('/')
    if request.method=='POST':
        chatform=ChatForm(request.POST)
        if chatform.is_valid():
            content=chatform.cleaned_data['content']
            fromuser=models.BBS_User.objects.filter(bbs_user__username__exact=request.session['username'])[0]
            models.ChatContent.objects.create(content=content,fromuser=fromuser)
            return HttpResponse('success')
    elif request.method=='GET':
        counts= models.ChatContent.objects.count()
        request.session['lastchatdatetime']=datetime.now().strftime('%s')
        if counts<15:
#             if counts<1:
#                 return HttpResponse('no content')
#             else:
            cs=models.ChatContent.objects.all()
            return render_to_response('chatroom.html',{'information':getstatus(request),'onlineusers':json.loads(getonlineuser(request)),'chatcontents':cs,
                                               'chatform':ChatForm(),'order':4},context_instance=RequestContext(request))
        else:
#             chats=models.ChatContent.objects.all()[counts-10 if counts>10 else counts-1:counts]
            cs=models.ChatContent.objects.all()[counts-15:counts]
            chs=[]
#             onehourago=(datetime.now()-timedelta(hours=1)).strftime('%s')
#             for c in cs:
#                 if c.pubdate.strftime('%s')>onehourago:
#                     chs.append(c)
            return render_to_response('chatroom.html',{'information':getstatus(request),'onlineusers':json.loads(getonlineuser(request)),'chatcontents':cs,
                                               'chatform':ChatForm(),'order':4},context_instance=RequestContext(request))
    return HttpResponse('invalid request')
def chatcontent(request):
    lastdatetime=request.session['lastchatdatetime']
    counts= models.ChatContent.objects.count()
    chats=models.ChatContent.objects.all()[counts-3 if counts>3 else counts-1:counts]
    contents=[]
    for chat in chats:
        if chat.pubdate.strftime('%s')>lastdatetime:
#             contents[chat.fromuser.bbs_user.username]=chat.content
#             contents['']({'pubdate':chat.pubdate,'content':chat.content,'fromuser':chat.fromuser})
            contents.append({'pubdate':str(chat.pubdate),'content':chat.content,'fromuser':chat.fromuser.bbs_user.username})
    if len(contents)>=1:
        request.session['lastchatdatetime']=chats[len(chats)-1].pubdate.strftime('%s')
        return json.dumps(contents)
    else:
        return 'None'
def getchatcontent(request,args=None):
    return HttpResponse(chatcontent(request))
def sendmessage(request,username=None):
    if request.method=='GET':
        return render_to_response('sendmessage.html',{'information':getstatus(request),'sendmessageform':SendMessageForm()},context_instance=RequestContext(request))
    elif request.method=='POST':
        touser=request.POST['touser']
        content=request.POST['content']
        fromuser=models.BBS_User.objects.filter(bbs_user__username__exact=request.session['username'])[0]
        us=models.SendMessage()
        us.fromuser=fromuser
        us.touser=touser
        us.content=content
        us.save()
#         senddate=models.SendMessage.objects.filter(touser=t)
        u={'touser':touser,'content':content,'fromuser':fromuser.bbs_user.username,'senddate':str(us.senddate)}
#         u.append({'content':content})
#         u.append({'fromuser':fromuser.bbs_user.username})
#         u='<p>'+content+'</p>'
        return HttpResponse(json.dumps(u))
    else:
        return HttpResponse('invalid request')
def bbs_remove(request,bbs_id):
    if request.method=='GET':
        models.BBS.objects.filter(id=bbs_id).delete()
        return HttpResponse('success')
    return HttpResponse('error')