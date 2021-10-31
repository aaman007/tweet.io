from django.urls import path, include

app_name = 'core-api'

urlpatterns = [
    path('v1/', include('core.api.v1.urls'))
]
