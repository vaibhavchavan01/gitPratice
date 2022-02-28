# from django.contrib.auth.forms import UsernameField
# from . import forms
from datetime import timedelta
from django.views import View
from pyexpat.errors import messages
import uuid
from django.contrib.auth.hashers import make_password
from django.views.generic import TemplateView
from .models import Artist, Genre, Movie, MovieArtist, User
from django.shortcuts import render, redirect
from .forms import UserCreateForm, UserForm
from .emailSetup import forget_password_mail
from .backends import CustomBackend
from django.contrib.auth import authenticate


class SignUpView(TemplateView):       
    form_class = UserCreateForm
    template_name = "signup.html"
    def getUser(request):
        if request.method=='POST':
            userData = User(
                firstname = request.POST.get('fname'),
                lastname = request.POST.get('lname'),       
                email = request.POST.get('email'),
                mobile = request.POST.get('mobile'),
                password = make_password(request.POST.get('psw')),
                confirm_password = make_password(request.POST.get('psw-repeat'))
            )
            # userData.is_superuser=True
            userData.save()
            return render(request, 'login.html')
        


class LoginCheckView(TemplateView):
    form_class = UserForm
    # template_name = 'login.html'   
       
    def check_login(request):
        user = ''
        if request.method == 'POST':
            login_user = request.POST.get('uname')
            login_password = request.POST.get('psw')
            try:
                user = authenticate(request, email =  login_user, password = login_password)
            except Exception as e:
                return render(request, 'login.html')
            request.session['user'] = user.id
            if user.is_superuser:
                request.session['is_superuser'] = True
                return redirect('demoApp:home',)
            else:
                return redirect('demoApp:home')

class ForgetPasswordView(TemplateView):

    template_name = 'forget_password.html'
    def get_link(request):
        token = str(uuid.uuid4())
        if request.method == 'POST':
            email = request.POST.get('uname')
            print('email_valid:',email)
            
            # global Email
            # Email = email  
            try:
                user = User.objects.get(email=email)  
            except:
                pass
            data = {"email":email}  
            if email == user.email:
                forget_password_mail(email, token)
                # Email = email
                return render(request, 'forget_password.html', data)
            else:
                return messages.success(request, 'User not found with this username')

class ResetPasswordView(ForgetPasswordView, TemplateView):
    def resetPassord(request, token, email):
        return render(request, 'reset_password.html',{'newEmail':email})
    def after_reset_Password(request):
        
        if request.method == 'POST':
            try:
                userData = User.objects.get(email=request.POST.get('email'))
                password = request.POST.get('psw')
                confirm_password =request.POST.get('cpsw')                
                if password == confirm_password:
                    userData.password = make_password(password)
                    userData.confirm_password = make_password(confirm_password)
                    userData.save()
                    return render(request, 'login.html')
                else:
                    return render(request, 'reset_password.html', {'message':"password not match"})  

            except:
                pass
            
                
class HomepageView(TemplateView):
    template_name = "homepage.html"
    def get(self, request):
        genre = Genre.objects.all()
        movie = Movie.objects.all()
        movie_artist = MovieArtist.objects.all()
        artist = Artist.objects.all()
        return render(request, 'homepage.html', {"movie":movie, "movie_artist":movie_artist, "artist":artist,"genre":genre})
       
class AfterLoginView(View):
    def get(self, request):
        dict = {}
        genre = Genre.objects.all()
        movie = Movie.objects.all()
        movie_artist = MovieArtist.objects.all()
        artist = Artist.objects.all()
        dict = {"movie":movie, "movie_artist":movie_artist, "artist":artist, "genre":genre}
        return render(request, 'index.html', {"movie":movie, "movie_artist":movie_artist, "artist":artist,"genre":genre})
       
def GetDetail(request,id):
    if request.session.get('user'):
        data = MovieArtist.objects.get(pk=id)
        return render(request,'index.html',{'movie_artist':data})
    else:
        return render(request,'login.html',{'message':"Please Login First"})

def Logout(request):
    request.session.clear()
    return redirect("/")

class AddDetailsView(TemplateView):
    template_name = 'addData.html'
    def add_details(request):
        if request.method == 'POST':
            duration = request.POST.get('duration')
            duration = duration.split(':') 
            AddGenreDetails = Genre(
                name = request.POST.get('genre')
            )            
            AddGenreDetails.save()
            AddMovieDetails = Movie(
                title = request.POST.get('title'),
                language = request.POST.get('language'),
                duration = timedelta(hours = int(duration[0]),minutes= int(duration[1])),
                release = request.POST.get('release'),
                country = request.POST.get('country'),
                description = request.POST.get('description'),
                genre = AddGenreDetails,
                image = request.FILES['img']
            )
            AddMovieDetails.save()
            AddArtistDetails = Artist(
                name = request.POST.get('artist')
            )
            AddArtistDetails.save()
            AddMovieArtistDetails = MovieArtist(
                a_type = request.POST.get('artist type'),
                movie = AddMovieDetails,
                artist = AddArtistDetails
            )
            AddMovieArtistDetails.save()
            
        return redirect('demoApp:home')
class DeleteRecord(TemplateView):
    pass
def delete_record(request, id):
    record = MovieArtist.objects.get(pk=id)
    record.delete()
    return redirect('demoApp:home')

def edit_record(request, id):
    record = MovieArtist.objects.get(pk=id)
    print(record.movie.description)
    return render(request, 'edit.html', {'data':record})

def update_record(request, ma_id, m_id, a_id, g_id):
    duration = request.POST.get('duration')
    duration = duration.split(':') 
    AddGenreDetails = Genre.objects.get(pk=g_id)
    AddGenreDetails.name = request.POST.get('genre')          
    AddGenreDetails.save()

    AddMovieDetails = Movie.objects.get(pk=m_id)
    AddMovieDetails.title = request.POST.get('title')
    AddMovieDetails.language = request.POST.get('language')
    AddMovieDetails.duration = timedelta(hours = int(duration[0]),minutes= int(duration[1]))
    AddMovieDetails.release = request.POST.get('release')
    AddMovieDetails.country = request.POST.get('country')
    AddMovieDetails.description = request.POST.get('description')
    AddMovieDetails.genre = AddGenreDetails
    AddMovieDetails.image = request.FILES['img']
    
    AddMovieDetails.save()
    AddArtistDetails = Artist.objects.get(pk=a_id)
    AddArtistDetails.name = request.POST.get('artist')
    AddArtistDetails.save()

    AddMovieArtistDetails = MovieArtist.objects.get(pk=ma_id)
    AddMovieArtistDetails.a_type = request.POST.get('artist type')
    AddMovieArtistDetails.movie = AddMovieDetails
    AddMovieArtistDetails.artist = AddArtistDetails
    AddMovieArtistDetails.save()
    
    return redirect('demoApp:home')
