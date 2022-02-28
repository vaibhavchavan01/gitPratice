from django.contrib import admin

# Register your models here.
from .models import Genre, Movie, Artist, MovieArtist, User
# from .forms import UserCreateForm
from django.contrib.auth.admin import UserAdmin

class admingenre(admin.ModelAdmin):
    list_display = ["name"]
class adminmovie(admin.ModelAdmin):
    list_display = ["title","language","release","country","image"]
class adminartist(admin.ModelAdmin):
    list_display = ["name"]
class adminmovie_artist(admin.ModelAdmin):
    list_display = ["movie","artist","a_type"]
class adminuser(admin.ModelAdmin):
    list_display = ["firstname","lastname","mobile","email","is_superuser"]

admin.site.register(Movie,adminmovie)
admin.site.register(Genre,admingenre)
admin.site.register(Artist,adminartist)
admin.site.register(MovieArtist,adminmovie_artist)
admin.site.register(User,adminuser)

# class MyUserAdmin(UserAdmin):
#     add_form = UserCreateForm
#     model = User
#     list_display = ['username', 'mobile', 'email']
#     fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('mobile', 'email')}),
#     ) #this will allow to change these fields in admin module