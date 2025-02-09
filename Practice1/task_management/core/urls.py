from rest_framework.routers import DefaultRouter 

from .views import UserViewSet, ProjectViewSet, CategoryViewSet, PriorityViewSet, TaskViewSet, share_cv_email 

from django.urls import path 

from .views import contact_view, create_cv, cv_list

from django.conf import settings 

from django.conf.urls.static import static 

router = DefaultRouter() 

router.register(r'users', UserViewSet) 

router.register(r'projects', ProjectViewSet) 

router.register(r'categories', CategoryViewSet) 

router.register(r'priorities', PriorityViewSet) 

router.register(r'tasks', TaskViewSet) 

urlpatterns = router.urls
urlpatterns += [ 

    path('contact/', contact_view, name='contact'), 
    path('cv/create/', create_cv, name='cv'),
    path('cv-list/', cv_list, name='cv_list'),
    path('share/email/<int:cv_id>/', share_cv_email, name='share_cv_email'), 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)