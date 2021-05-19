from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import get_all_bhav, get_single_bhav


urlpatterns = {
    path('bhavcopy/', get_all_bhav),
    path('bhavcopy/<slug:key>', get_single_bhav)
}

urlpatterns = format_suffix_patterns(urlpatterns)