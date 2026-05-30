from django.urls import path
from . import views
from .views import generate_resume


urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_user, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),  # <-- NEW
    path("logout/", views.logout_user, name="logout"), 
    path("resend-activation/", views.resend_activation, name="resend_activation"),
    path("generate-resume/", generate_resume, name="generate_resume"),
    path(
        "activate/<uidb64>/<token>/",
        views.activate,
        name="activate"
    ),
    path("resend-activation/", views.resend_activation, name="resend_activation"),
    path("generate-resume/", views.generate_resume, name="generate_resume"),
    path("download-pdf/", views.download_resume_pdf, name="download_resume_pdf"),



]
