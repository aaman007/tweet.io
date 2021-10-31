from django.urls import path, include

app_name = 'tweets-api'

urlpatterns = [
    path('v1/', include('tweets.api.v1.urls'))
]
