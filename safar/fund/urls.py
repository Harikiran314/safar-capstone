from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name="index"),
	path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('profile', views.profile, name="profile"),
    path('causes/', views.causes, name="causes"),
    path('causes/<str:pk>', views.causes_details, name="causes-details"),
    path('myRequest/<str:pk>', views.myRequest, name="myRequest"),
    path('sign-in', views.sign_in, name="Signin"),
    path('sign-up', views.sign_up, name="SignUp"),
    path('signout', views.sign_out, name="Signout"),
    path('admin/Signin', views.admin_sign_in, name="AdminSignin"),
    path('admin/Signout', views.admin_sign_out, name='AdminSignout'),
    path('admin', views.admin, name="Admin"),
    path('admin/profile', views.admin_profile, name="AdminProfile"),
    path('admin/requests', views.admin_requests, name="AdminRequests"),
    path('payment', views.payment, name="payment")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)