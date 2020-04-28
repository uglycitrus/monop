from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('games/', include('game.urls')),
    path('payments/', include('payment.urls')),
    path('card/', include('deck.urls')),
    path('turn/', include('turn.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]

