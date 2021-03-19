from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from newsapi.newsapi_client import NewsApiClient
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template
from .utils import account_activation_token

from main.decorators import unauthenticated_user
from .forms import UserRegisterForm

@unauthenticated_user
def index(request):

    newsapi = NewsApiClient(api_key="a59e5f24831a4322b535578654582973")
    topheadlines = newsapi.get_top_headlines(category='business', country='in')
    articles = topheadlines['articles']

    desc = []
    news = []
    img = []
    author = []
    publishedAt = []
    url = []

    for i in range(len(articles)):
        myarticles = articles[i]

        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
        author.append(myarticles['author'])
        publishedAt.append(myarticles['publishedAt'])
        url.append(myarticles['url'])

    mylist = zip(news[:3], desc, img, author, publishedAt, url)

    return render(request, 'accounts/index.html', context={"mylist": mylist})

def contact(request):
    if request.method == 'POST':
        contact_name = request.POST.get('name')
        contact_email = request.POST.get('email')
        contact_subject = request.POST.get('subject')
        contact_content = request.POST.get('body')

        template = get_template('accounts/contact_form.txt')
        context = {
            'contact_name': contact_name,
            'contact_email': contact_email,
            'contact_subject': contact_subject,
            'contact_content': contact_content,
        }

        content = template.render(context)

        email = EmailMessage(
            contact_subject,
            content,
            "InvestInIt" + '',
            ['datafeed0@gmail.com'],
            headers={'Reply To': contact_email}
        )

        email.send()

        messages.success(request, "Thank you ! your message has been sent.")
        return redirect('contact')

    return render(request,'accounts/contact.html')

@unauthenticated_user
def pricing(request):

    return render(request,'accounts/pricing.html')

@unauthenticated_user
def terms(request):

    return render(request,'accounts/terms.html')

@unauthenticated_user
def disclosure(request):

    return render(request, 'accounts/disclosure.html')

def faq(request):

    return render(request, 'accounts/faq.html')

@unauthenticated_user
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email_id = request.POST.get('email')
            user.is_active = False
            user.save()

            current_site = get_current_site(request)

            email_subject = "Confirm your account on InvestInIt"
            email_body = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }
            link = reverse('activate', kwargs={
                'uidb64': email_body['uid'], 'token': email_body['token']})
            activate_url = 'http://'+current_site.domain+link

            email = EmailMessage(
                email_subject,
                'Hi '+user.username + ',\n\nThanks for signing up with Invest In It! You must follow this link to activate your account: \n'+activate_url 
                + '\n\nHave fun, and don''t hesitate to contact us with your feedback.\nInvest In It Team \nhttp://www.investinit.ml',
               'datafeed0@gmail.com',
               [email_id],
            )
            
            email.send(fail_silently=False)
            

            messages.success(request, 'Account created successfully')
            messages.success(request, 'Please verify your E-Mail')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form':form })

class emailVerification(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account Activated Successfully')
            return redirect('login')

        except Exception as ex:
            print(ex)

        return redirect('login')


@unauthenticated_user
def login_view(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        raw_password = request.POST.get('password')

        try:
            user = authenticate(
                request, username=username, password=raw_password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.warning(
                    request, "Username or Password is incorrect")
        except (ValueError):
            messages.warning(request, "Please enter a valid username")

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
