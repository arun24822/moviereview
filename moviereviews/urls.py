from django.contrib import admin
from django.urls import path, include
from movie import views as movieViews
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', movieViews.home, name='home'),
    path('signup/', movieViews.signup, name='signup'),
    path('news/', include('news.urls')), #project -level url
    path('movie/', include('movie.urls')),
    path('', include('accounts.urls')),
]

#for media files enetered by user in django admin
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)