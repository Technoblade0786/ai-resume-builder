from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.http import FileResponse
from django.urls import reverse

from .forms import RegisterForm, ResumeInputForm
from .utils import generate_resume_pdf

from openai import OpenAI


# ======================================================
# SEND ACTIVATION EMAIL ✅ FIXED
# ======================================================
def send_activation_email(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    activation_url = request.build_absolute_uri(
        reverse("activate", kwargs={"uidb64": uid, "token": token})
    )

    context = {
        "user": user,
        "activation_url": activation_url,
    }

    subject = "Activate your AI Resume Builder account"

    text_content = render_to_string(
        "users/emails/activation_email.txt", context
    )
    html_content = render_to_string(
        "users/emails/activation_email.html", context
    )

    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)

        print("✅ Activation email sent to:", user.email)

    except Exception as e:
        print("❌ Email sending failed:", str(e))
        raise e


# ======================================================
# ACTIVATE ACCOUNT
# ======================================================
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Account activated successfully. Please login.")
        return redirect("login")

    return render(request, "users/activation_invalid.html")


# ======================================================
# RESEND ACTIVATION
# ======================================================
def resend_activation(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()

        if not user:
            messages.error(request, "No account found with that email.")
            return redirect("resend_activation")

        if user.is_active:
            messages.info(request, "Account already activated.")
            return redirect("login")

        send_activation_email(user, request)
        messages.success(request, "Activation email resent successfully.")
        return redirect("login")

    return render(request, "users/resend_activation.html")


# ======================================================
# REGISTER
# ======================================================
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            print("FORM VALID")

            user = form.save(commit=False)
            user.is_active = False
            user.save()

            send_activation_email(user, request)

            messages.success(
                request,
                "Registration successful. Check your email to activate your account.",
            )
            return redirect("login")

        else:
            print(form.errors)

    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})


# ======================================================
# LOGIN
# ======================================================
def login_user(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )

        if user:
            if not user.is_active:
                messages.error(request, "Please activate your account first.")
                return redirect("login")

            login(request, user)
            return redirect("dashboard")

        messages.error(request, "Invalid username or password.")

    return render(request, "users/login.html")


# ======================================================
# LOGOUT
# ======================================================
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")


# ======================================================
# DASHBOARD
# ======================================================
@login_required(login_url="login")
def dashboard(request):
    return render(request, "users/dashboard.html")


# ======================================================
# GENERATE RESUME
# ======================================================
@login_required
def generate_resume(request):
    if request.method == "POST":
        form = ResumeInputForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            template_choice = data.get("template", "modern")
            use_ai = data.get("use_ai")
            api_key = data.get("openai_api_key")

            context = {
                "full_name": data["full_name"],
                "job_title": data["job_title"],
                "skills": data["skills"].split(","),
                "experience": data["experience"],
                "projects": data["projects"],
                "education": data["education"],
                "ai_used": False,
            }

            template_map = {
                "modern": "users/resume_templates/modern.html",
                "simple": "users/resume_templates/simple.html",
                "ats": "users/resume_templates/ats.html",
            }

            template_name = template_map.get(
                template_choice, template_map["modern"]
            )

            if use_ai and api_key:
                client = OpenAI(api_key=api_key)

                prompt = f"""
Create a professional ATS-friendly resume.

Name: {data['full_name']}
Job Title: {data['job_title']}
Skills: {data['skills']}
Experience: {data['experience']}
Projects: {data['projects']}
Education: {data['education']}
"""

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                )

                context["ai_resume"] = response.choices[0].message.content
                context["ai_used"] = True

            resume_html = render_to_string(template_name, context)
            request.session["resume_html"] = resume_html

            return render(
                request,
                "users/resume_result.html",
                {"resume_html": resume_html, "ai_used": context["ai_used"]},
            )

    else:
        form = ResumeInputForm()

    return render(request, "users/resume_form.html", {"form": form})


# ======================================================
# DOWNLOAD PDF
# ======================================================
@login_required
def download_resume_pdf(request):
    html = request.session.get("resume_html")

    if not html:
        messages.error(request, "No resume found to download.")
        return redirect("generate_resume")

    edited_html = request.POST.get("edited_resume")
    if edited_html:
        html = edited_html

    pdf_buffer = generate_resume_pdf(html)

    return FileResponse(
        pdf_buffer,
        as_attachment=True,
        filename="resume.pdf",
    )
