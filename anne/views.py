from django.core import paginator
from django.template.loader import render_to_string

import urllib
import json
from django.http import JsonResponse
from django.core import serializers

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from .forms import SearchVideoForm #, ProfileForm
from anne import models

from django.contrib.auth import authenticate,login,logout
from .forms import LoginForm, RegisterForm, ProfileForm, ClusterForm, AddVideoForm, DeleteVideoForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
# from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

def shareVideo(request):
        if 'session_username' in request.session:
            user = models.CustomUser.objects.get(username = request.session['session_username'])
            clusters = models.Cluster.objects.filter(user = user)
            return render(request, 'anne/share.html', {'clusters': clusters})

     

#delete videos done also its select all option
@login_required(login_url='http://kudos02.pythonanywhere.com/login/')
def deleteVideos(request):
    if request.method == 'POST':
        vid_list = request.POST.getlist('vid')

        first_video = models.Video.objects.get(id = int(vid_list[0]))

        for v in vid_list:
                vd = models.Video.objects.get(id = int(v))
                vd.delete()

        cluster_id = first_video.cluster.id
        cluster = models.Cluster.objects.get(id = cluster_id)
        delete_form = DeleteVideoForm()
        obj = cluster.video_set.all()
        delete_form.videos = obj
        user = models.CustomUser.objects.get(username = request.session['session_username'])
        clusters = models.Cluster.objects.filter(user = user)
        cluster_form = ClusterForm(request.POST or None, instance=cluster)
        return render(request, 'anne/cluster.html', {'clusters':clusters,'delete_form':delete_form ,'cluster_form':cluster_form, 'obj':obj, 'cluster' : cluster, 'form' : SearchVideoForm()})

        


@login_required(login_url='http://kudos02.pythonanywhere.com/login/')
def deleteCluster(request):
    cluster_id = request.GET['cluster_id']
    
    cluster = models.Cluster.objects.get(id = cluster_id)
    cluster.delete()

    cluster_form = ClusterForm(request.POST or None, instance=cluster)
    return render(request, 'anne/cluster.html', {'cluster_form':cluster_form, 'cluster' : cluster})


def checkUsername(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        username = request.POST.get('username')

        u_bool = True
        users = models.CustomUser.objects.all()
        emails = []
        usernames = []
        
        for i in users:
            if username == i.username :
                u_bool = False

        if u_bool:
            form.save()       
            request.session['session_username'] = username
            return JsonResponse({"status":"username not registered"})   

        else:
            return JsonResponse({"status":"username registered"})        


def Login(request):
    if request.method == 'POST':
        email = request.POST.get('login_email')
        password = request.POST.get('login_password')
        try:
            user = authenticate(request, username = email, password = password)
        except:
            return JsonResponse({'status':'Invalid credentials'})
        if user is not None:
            login(request, user)
            request.session['session_username'] = user.username
            return JsonResponse({'status':'User Login Success'})
        else:
            return JsonResponse({'status':'Invaid Credentials'})  
    authform = LoginForm()
    registerform = RegisterForm()        
    return render(request,'anne/login.html', {'authform':authform, 'registerform':registerform})
     
def checkEmail(request):
    if request.method == 'POST':
        email_entered = request.POST.get('email_entered')
        e_bool = True
        users = models.CustomUser.objects.all()
        emails = []
        usernames = []
        for i in users:
            if email_entered == i.email :
                e_bool = False
        if e_bool:        
            return JsonResponse({"status":"email not registered"})    
        else:
            return JsonResponse({"status":"email registered"})        

@login_required(login_url='http://kudos02.pythonanywhere.com/login/')
def userLogout(request):
    logout(request)
    return HttpResponseRedirect('http://kudos02.pythonanywhere.com/login/')


# def searchUser(request):

#     if 'how_many_visits' in request.session:
#         request.session['how_many_visits'] += 1

#     else:
#         request.session.setdefault('how_many_visits', 1)
        
#     form = SearchVideoForm()
#     authform = LoginForm()
#     registerform = RegisterForm()
#     cluster_form = ClusterForm()
#     obj = list(models.Video.objects.all())

#     if(len(obj)/5 <= request.session['how_many_visits']):
#         request.session['how_many_visits'] = 1

#     obj = obj[5 * (request.session['how_many_visits'] - 1) : 5 * request.session['how_many_visits'] ]
#     site_d = models.SiteDesc.objects.all()
#     if 'session_username' in request.session:
#         user = models.CustomUser.objects.get(username = request.session['session_username'])
#         clusters = models.Cluster.objects.filter(user = user)
#         #return render(request,'anne/index.html', {'authform':authform, 'registerform':registerform,'obj':obj, 'site_des':set(site_d), 'form': form})
#         return render(request,'anne/index.html', {'cluster_form':cluster_form, 'add_video_form':AddVideoForm, 'authform':authform, 'registerform':registerform, 'obj':obj, 'form': form, 'clusters': clusters})
#     else:
#         #return render(request,'anne/index.html', {'authform':authform, 'registerform':registerform,'obj':obj, 'site_des':set(site_d), 'form': form})
#         return render(request,'anne/index.html', {'cluster_form':cluster_form, 'add_video_form':AddVideoForm, 'authform':authform, 'registerform':registerform, 'obj':obj, 'form': form})


NEWS_COUNT_PER_PAGE = 3

def searchUser(request):

    if 'how_many_visits' in request.session:
        request.session['how_many_visits'] += 1

    else:
        request.session.setdefault('how_many_visits', 1)

    page = int(request.GET.get('page', 1))   
    form = SearchVideoForm()
    authform = LoginForm()
    registerform = RegisterForm()
    cluster_form = ClusterForm()
    obj = list(models.Video.objects.all())


    # if(len(obj)/5 <= request.session['how_many_visits']):
    #     request.session['how_many_visits'] = 1

    # obj = obj[5 * (request.session['how_many_visits'] - 1) : 5 * request.session['how_many_visits'] ]
    
    p = paginator.Paginator(obj,
                            NEWS_COUNT_PER_PAGE)
    print(p)                        
    site_d = models.SiteDesc.objects.all()
    try:
        post_page = p.page(page)
    except paginator.EmptyPage:
        post_page = paginator.Page([], page, p)

    if not request.is_ajax():
        print("not ajax call ajax call")
        print("not ajax call ajax call")
        print("not ajax call ajax call")
        print("not ajax call ajax call")
        
        if 'session_username' in request.session:
            user = models.CustomUser.objects.get(username = request.session['session_username'])
            clusters = models.Cluster.objects.filter(user = user)
            context = {
              'obj': post_page,
              'cluster_form':cluster_form,
              'add_video_form':AddVideoForm,
              'authform':authform,
              'registerform':registerform,
              'form': form,
              'clusters': clusters,
              }
            
            #return render(request,'anne/index.html', {'authform':authform, 'registerform':registerform,'obj':obj, 'site_des':set(site_d), 'form': form})
            return render(request,'anne/index.html', context)
            
        else:
            context = {
              'obj': post_page,
              'cluster_form':cluster_form,
              'add_video_form':AddVideoForm,
              'authform':authform,
              'registerform':registerform,
              'form': form,
              }
            #return render(request,'anne/index.html', {'authform':authform, 'registerform':registerform,'obj':obj, 'site_des':set(site_d), 'form': form})
            return render(request,'anne/index.html', context)
                  
    else:
        print("ajax call ajax call")
        print("ajax call ajax call")
        print("ajax call ajax call")
        print("ajax call ajax call")
        content = ''
        for post in post_page:
            content += render_to_string('anne/post.html',
                                        {'i': post},
                                        request=request)
        return JsonResponse({
            "content": content,
            "end_pagination": True if page >= p.num_pages else False,
        })


def videoPlayer(request):
    video_id = request.GET['video_id']
    video = models.Video.objects.get(id=video_id)
    page = int(request.GET.get('page', 1))   
    form = SearchVideoForm()
    authform = LoginForm()
    registerform = RegisterForm()
    cluster_form = ClusterForm()
    obj = list(models.Video.objects.all())


    # if(len(obj)/5 <= request.session['how_many_visits']):
    #     request.session['how_many_visits'] = 1

    # obj = obj[5 * (request.session['how_many_visits'] - 1) : 5 * request.session['how_many_visits'] ]
    
    p = paginator.Paginator(obj,
                            NEWS_COUNT_PER_PAGE)
    print(p)                        
    site_d = models.SiteDesc.objects.all()
    try:
        post_page = p.page(page)
    except paginator.EmptyPage:
        post_page = paginator.Page([], page, p)

    if not request.is_ajax():
        print("not ajax call ajax call")
        print("not ajax call ajax call")
        print("not ajax call ajax call")
        print("not ajax call ajax call")
        
        if 'session_username' in request.session:
            user = models.CustomUser.objects.get(username = request.session['session_username'])
            clusters = models.Cluster.objects.filter(user = user)
            context = {
              'video_id': video_id,  
              'obj': post_page,
              'cluster_form':cluster_form,
              'add_video_form':AddVideoForm,
              'form': form,
              'form' : SearchVideoForm(),
              'clusters': clusters,
              'my_video': video,
              }
            
            #return render(request,'anne/index.html', {'authform':authform, 'registerform':registerform,'obj':obj, 'site_des':set(site_d), 'form': form})
            return render(request,'anne/video_player.html', context)
            
        else:
            context = {
              'video_id': video_id,
              'obj': post_page,
              'cluster_form':cluster_form,
              'add_video_form':AddVideoForm,
              'form' : SearchVideoForm(),
              'form': form,
              'my_video': video,
              }
            #return render(request,'anne/index.html', {'authform':authform, 'registerform':registerform,'obj':obj, 'site_des':set(site_d), 'form': form})
            return render(request,'anne/video_player.html', context)
                  
    else:
        print("ajax call ajax call")
        print("ajax call ajax call")
        print("ajax call ajax call")
        print("ajax call ajax call")
        content = ''
        for post in post_page:
            content += render_to_string('anne/post.html',
                                        {'i': post},
                                        request=request)
        return JsonResponse({
            "content": content,
            "end_pagination": True if page >= p.num_pages else False,
        })


# def videoPlayer(request):
#     clusters = models.Cluster.objects.all()
#     obj = models.Video.objects.all()
#     video_id = request.GET['video_id']
#     video = models.Video.objects.get(id=video_id)
#     for p in models.Profile.objects.all():
#         if video.cluster.user == p.user:
#             return render(request, 'anne/video_player.html', {'profile_pic':p.image, 'obj':obj, 'my_video':video, 'clusters':clusters, 'add_video_form':AddVideoForm, 'form' : SearchVideoForm()})
#     return render(request, 'anne/video_player.html', {'video_id': video_id, 'obj':obj, 'my_video':video, 'clusters':clusters, 'add_video_form':AddVideoForm, 'form' : SearchVideoForm()})
           

def searchVideo(request):
    if request.method=='POST':
        form = SearchVideoForm(request.POST)
        desc = form.data['desc'].lower()
        if 'desc' in request.session :
            del request.session['desc']
        request.session['desc'] = desc

        Videos = []
        for vid in models.Video.objects.all():
            if desc in vid.video_title.lower() or desc in vid.video_owner.lower() :
                Videos.append(vid)

        if len(Videos) == 0:
              for cluster in models.Cluster.objects.all():
                if "cars" or "songs" in cluster.cluster_hashtags :
                    obj = cluster.video_set.all()
                    for vid in obj:
                            Videos.append(vid)
        res = render(request,'anne/search_video.html',{'form':form,'Videos':Videos})
        return res

@login_required(login_url='http://kudos02.pythonanywhere.com/login/')
def deleteUser(request):
        if 'session_username' in request.session:
            user = models.CustomUser.objects.get(username = request.session['session_username'])
            user.delete()
        return render(request, 'anne/login.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            ##################################################################
            username = request.POST['username']
            request.session['session_username'] = username
            return render(request, 'anne/profile.html', {'username':username})
    else:
        form = RegisterForm()
        return render(request, 'anne/register.html', {'form': form, 'title':'register here'})


@login_required(login_url='http://kudos02.pythonanywhere.com/login/')
def addProfile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST or None, request.FILES)
        if form.is_valid():
            profile = models.Profile()
            username = request.session['session_username']
            user = models.CustomUser.objects.get(username=username)
            profile.user = user
            profile.about = form.data['about']
            profile.image = request.FILES['image']
            profile.website_name = form.data['website_name']
            profile.save()
            request.session['sess_profile_pic'] = profile.image.url
            request.session['sess_id'] = profile.id
            return render(request,'anne/profile.html',{'profile':profile, 'profile_form':form, 'cluster_form':ClusterForm, 'form' : SearchVideoForm()})
    else:
        if 'session_username' in request.session:
            user = models.CustomUser.objects.get(username = request.session['session_username'])
            clusters = models.Cluster.objects.filter(user = user)
        if 'sess_id' in request.session: 
            sess_id = request.session['sess_id']
            profile = models.Profile.objects.get(id = sess_id)
            profile_pic = profile.image
            profile_form = ProfileForm(request.POST or None, instance=profile)
            return render(request,'anne/profile.html', {'profile':profile, 'profile_form':profile_form, 'cluster_form':ClusterForm, 'clusters':clusters, 'form' : SearchVideoForm()})

        else:
            profile_form = ProfileForm()
        return render(request,'anne/profile.html', {'profile_form':profile_form, 'cluster_form':ClusterForm, 'clusters':clusters, 'form' : SearchVideoForm()})

@login_required(login_url='http://kudos02.pythonanywhere.com/login/')
def editProfile(request):
    if request.method == 'POST':
        if 'sess_id' in request.session:
            sess_id = request.session['sess_id']
            profile = models.Profile.objects.get(id = sess_id)
            clusters = models.Cluster.objects.filter(user = profile.user)
            form = ProfileForm(request.POST or None, request.FILES, instance=profile)
            
            
            form.save()
            return render(request,'anne/profile.html',{'clusters':clusters, 'profile':profile, 'profile_form':form, 'cluster_form':ClusterForm, 'form' : SearchVideoForm()})
    else:
        print("else")
        print("else")
        if 'sess_id' in request.session:
            print("else2")
            print("else2")
            sess_id = request.session['sess_id']
            profile = models.Profile.objects.get(id = sess_id)
            clusters = models.Cluster.objects.filter(user = profile.user)
            form = ProfileForm(request.POST or None, request.FILES, instance=profile)
            return render(request,'anne/profile.html',{'clusters':clusters, 'profile':profile, 'profile_form':form, 'cluster_form':ClusterForm, 'form' : SearchVideoForm()})


@login_required(login_url='http://kudos02.pythonanywhere.com/login/')
def viewProfile(request):
        if 'session_username' in request.session:
            user = models.CustomUser.objects.get(username = request.session['session_username'])
            clusters = models.Cluster.objects.filter(user = user)
        if 'sess_id' in request.session: 
            sess_id = request.session['sess_id']
            profile = models.Profile.objects.get(id = sess_id)
            profile_pic = profile.image
            profile_form = ProfileForm(request.POST or None, instance=profile)
            return render(request,'anne/profile.html', {'profile':profile, 'profile_form':profile_form, 'cluster_form':ClusterForm, 'clusters':clusters, 'form' : SearchVideoForm()})

        else:
            profile_form = ProfileForm()
        return render(request,'anne/profile.html', {'profile_form':profile_form, 'cluster_form':ClusterForm, 'clusters':clusters, 'form' : SearchVideoForm()})

def viewPublicProfile(request):
        
        user = models.CustomUser.objects.get(username = request.GET['handle'])
        clusters = models.Cluster.objects.filter(user = user)
        profile = models.Profile.objects.filter(user = user)
        profile = profile[:1].get()
        return render(request,'anne/public_profile.html', {'profile':profile, 'clusters':clusters, 'form' : SearchVideoForm()})


@login_required(login_url='http://kudos02.pythonanywhere.com/login/')
def viewProfileArrangeClusters(request):
        if 'session_username' in request.session:
            user = models.CustomUser.objects.get(username = request.session['session_username'])
            clusters = models.Cluster.objects.filter(user = user)
        
        my_clusters = [] 
        for i in clusters:
            my_clusters.append(i)   
        my_clusters.sort(key=lambda x: x.cluster_name) 

        if 'sess_id' in request.session: 
            sess_id = request.session['sess_id']
            profile = models.Profile.objects.get(id = sess_id)
            profile_form = ProfileForm(request.POST or None, instance=profile)
            return render(request,'anne/profile.html', {'profile':profile, 'profile_form':profile_form, 'cluster_form':ClusterForm, 'clusters':my_clusters, 'form' : SearchVideoForm()})

        else:
            profile_form = ProfileForm()
        return render(request,'anne/profile.html', {'profile_form':profile_form, 'cluster_form':ClusterForm, 'clusters':my_clusters, 'form' : SearchVideoForm()})

@login_required(login_url='http://kudos02.pythonanywhere.com/login/')
def addCluster(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        cluster = models.Cluster()
        cluster.cluster_name = form.data['cluster_name']  
        cluster.cluster_tags = form.data['cluster_hashtags'] 
        user = models.CustomUser.objects.get(username = request.session['session_username']) 
        cluster.user = user
        clusters = models.Cluster.objects.filter(user = user)

        if 'session_username' in request.session:
            user = models.CustomUser.objects.get(username = request.session['session_username'])
            clusters = models.Cluster.objects.filter(user = user)
            print(clusters)
            for c in clusters:
                if c.video_set.all().first():
                    print(c.video_set.all().first().video_thumbnail)

            clusters = models.Cluster.objects.values().filter(user = user)
            c_images = []

            cluster.save()
            list_clusters = list(clusters)
            return JsonResponse({"status":"cluster created", 'clusters': list_clusters}) 

@login_required(login_url='http://kudos02.pythonanywhere.com/login/')
def cluster(request):
    cluster_id = request.GET['cluster_id']
    cluster = models.Cluster.objects.get(id = cluster_id)
    delete_form = DeleteVideoForm()
    obj = cluster.video_set.all()
    delete_form.videos = obj
    user = models.CustomUser.objects.get(username = request.session['session_username'])
    clusters = models.Cluster.objects.filter(user = user)
    cluster_form = ClusterForm(request.POST or None, instance=cluster)
    return render(request, 'anne/cluster.html', {'clusters':clusters,'delete_form':delete_form ,'cluster_form':cluster_form, 'obj':obj, 'cluster' : cluster, 'form' : SearchVideoForm()})

@login_required(login_url='http://kudos02.pythonanywhere.com/login/')
def addVideo(request):
    if request.method == 'GET':
        print("is i am inside add Video Fn")
        cluster_id = request.GET['cluster_id']
        video = models.Video()
        video.video_platform_id = request.GET['video_platform_id']
        video.video_title = request.GET['video_title']
        video.video_description = request.GET['video_description']
        video.video_url = request.GET['video_url']
        video.video_thumbnail = request.GET['video_thumbnail']
        video.video_owner = request.session['session_username']
        cluster = models.Cluster.objects.get(id = cluster_id)
        video.cluster = cluster
        video.save()
        print("add video func")
        print("add video func")
        print("add video func")
        print("add video func")
        obj = cluster.video_set.all()
        
        return JsonResponse({'video':"video_saved"})

        # if 'sess_profile_pic' in request.session:
        #     video.video_owner_thumbnail = request.session['sess_profile_pic']
        # video.cluster = models.Cluster.objects.get(id = cluster_id)

        # for v in models.Video.objects.all():
        #     cluster = models.Cluster.objects.get(id = cluster_id)
        #     obj = cluster.video_set.all()
        #     if(models.Cluster.objects.get(id = cluster_id) and v.video_platform_id == video.video_platform_id): 
        #         return render(request, 'anne/cluster.html', {'cluster_form':ClusterForm, 'obj':obj, 'cluster' : cluster, 'form' : SearchVideoForm()})
        # video.save()
        # obj = cluster.video_set.all()
        # return render(request, 'anne/cluster.html', {'cluster_form':ClusterForm, 'obj':obj, 'cluster' : cluster, 'form' : SearchVideoForm()})


from django.forms.models import model_to_dict

@login_required(login_url='http://kudos02.pythonanywhere.com/login/')
def addVideoIndex(request):
    if request.method == 'GET':
        video_id = request.GET['video_id']
        
        video = models.Video.objects.values().filter(id = video_id)
        videos = list(video)
        return JsonResponse({"status":"cluster created", 'videos': videos}) 

      


