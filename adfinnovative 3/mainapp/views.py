from django.shortcuts import render, redirect
from .forms import UserForm,LoginForm,OtpForm, SearchForm
from django.http import HttpResponse,HttpResponseRedirect
from .models import User, Product
from django.core.mail import send_mail
import math, random
from reportlab.pdfgen import canvas
from django.contrib import messages
from django.views import View
from django.http import FileResponse
import requests 
from bs4 import BeautifulSoup 
import nltk
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from io import BytesIO
#import nltk
# nltk.download('punkt')
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('corpus')
# Create your views here.
#nltk.download()
def generate_pdf(request):
    response = FileResponse(generate_pdf_file(), 
                            as_attachment=True, 
                            filename='order_details.pdf')
    return response
 
 
def generate_pdf_file():
    
 
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
 
    # Create a PDF document
    prods = Product.objects.all()
    p.drawString(100, 750, "Order Details")
    p.drawString(100, 700, f"Username : {prods[0].user}")
 
    y = 700
    sum_total=0
    for i in prods:
        sum_total+=i.value

    for i in prods:
        # p.drawString(100, y, f"Username : {i.user}")
        p.drawString(100, y - 20, f"Product Name : {i.name}")
        p.drawString(100, y - 40, f"Product Price: {i.value}")
        y -= 60

    p.drawString(100, y, f"Order Total : {sum_total}")
 
    p.showPage()
    p.save()
 
    buffer.seek(0)
    return buffer

def generateOTP() :
    digits = "0123456789"
    OTP = ""
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

global otp
otp=""    

def Otp(request):
    global otp
    if request.method == 'POST':
        form = OtpForm(request.POST)
        if form.is_valid():
            test = form.cleaned_data
            u = test.get("verify")
            if u==otp:
                return HttpResponseRedirect("login")
            else:
                return HttpResponse("Invalid OTP")
    form1 = OtpForm()
    context={'form':form1}
    return render(request,"otp.html",context)

def register(request):
    global otp
    if request.method=="POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            data = form.cleaned_data
            temp_mail = data.get("email")
            otp = generateOTP()
            send_mail("Verification Email","Your OTP = "+str(otp),"pachchigar1912@gmail.com",[temp_mail])
            f2 = OtpForm()
            return render(request,"otp.html",{'form':f2})
    form1 = UserForm()
    context={'form':form1}
    return render(request,"reg_form.html",context)

def login(request):
    if request.method == 'POST':
        form2 = LoginForm(request.POST)
        if form2.is_valid():
            test = form2.cleaned_data
            u = test.get("username")
            # print(u)
            p = test.get("password")
            username = test.get("username") 
            # print(p)
            try:
                a = User.objects.raw("SELECT username,password,first_name FROM mainapp_user WHERE username=%s and password=%s",[str(u),str(p)])
                fname = a[0].first_name
                if a[0].password==p:
                    context={'first_name':fname}
                    form = SearchForm()
                    context['form'] = form
                    request.session['fname'] = fname
                    request.session['username'] = username
                    return redirect("home")
            except:
                return HttpResponse("Invalid Username or Password")
        else:
            return HttpResponse("Invalid!")
    else:
        form3 = LoginForm()
        context={'log':form3}
        return render(request,"login_form.html",context)
    
class login_home(View): 
    def get(self, request):
        context = {}
        form = SearchForm()
        context['form'] = form
        context['fname'] = request.session.get('fname')
        context['username'] = request.session.get('username')
        context['searched'] = False
        return render(request,"login_home.html", context)
    
    def post(self, request):
        stri = request.POST['instr'] 
        print(stri)
        product = ajiov(stri)
        nykaprod = nykaav(stri)
        lifestyle1 = lifestyle(stri)
        context = {}
        form = SearchForm()
        context['form'] = form
        context['fname'] = request.session.get('fname')
        context['username'] = request.session.get('username')
        print(product)
        context['productname'] = product['name']
        context['productimg'] = product['img']
        context['productprice'] = product['price']
        # print(nykaprod)
        context['nykname'] = nykaprod['name']
        context['nykprice'] = nykaprod['price']
        context['nykimg'] = nykaprod['img']
        print(lifestyle)
        context['lifename'] = lifestyle1['name']
        context['lifeprice'] = lifestyle1['price']
        context['lifeimg'] = lifestyle1['img']

        context['searched'] = True
        context['searchterm'] = stri
        # context['link'] = product['url']
        return render(request,"login_home.html", context)



def ajiov(stri): 
    #stop_words = set(stopwords.words('english'))
     
    txt = stri
    # tokenized = sent_tokenize(txt) 
    # for i in tokenized:
    #     wordList = nltk.word_tokenize(i)
    #     wordList = [w for w in wordList]
    #     tagged = nltk.pos_tag(wordList)
    # if(tagged[-1][1]=='JJ'):
    colorstr='query=%3Aprce-asc%3Averticalcolorfamily%3A'+txt.split(' ')[-1].title()+'&'
    # else:
    #     colorstr=''
    urlstr='https://www.ajio.com/search/?'+colorstr+'text='+ stri
    print(urlstr)
    r = requests.get(urlstr) 
    soup = BeautifulSoup(r.content, 'html.parser') 
    s = soup.find_all('script', type="application/ld+json") [-1]
    data = json.loads(s.text)
    ldeal=data['itemListElement'][0]
    print(ldeal)
    ajioname=ldeal['name']
    ajioimg=ldeal['image']
    ajiopri=ldeal['url']
    r2 = requests.get(ajiopri) 
    print(r2)
    product = {}
    product['name'] = ajioname
    product['img'] = ajioimg
    
    # product['url']

    # Parsing the HTML 
    soup2 = BeautifulSoup(r2.content, 'html.parser') 
    s2 = soup2.find_all('script', type="application/ld+json")[-1]
    data2 = json.loads(s2.text)
    ajiopri=data2['offers']['price']

    print(ajioname)
    print(ajioimg)
    print(ajiopri)
    product['price'] = ajiopri
    return product
# # Parsing the HTML 
#     soup2 = BeautifulSoup(r2.content, 'html.parser') 
#     s2 = soup2.find_all('script', type="application/ld+json")[-1]
#     data2 = json.loads(s2.text)
#     ajiopri=data2['offers']['price']
class orderConfirmed(View):
    def get(self, request):
        return render(request, "orderConfirmed")


def nykaav(stri):

    # stri=input('enter a prompt:-')
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    r = requests.get('https://www.shoppersstop.com/search/?text='+stri+'&sort=price-asc', headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser') 
    s2=soup.find_all('input', class_='listProductUrl', type='hidden')
    sdeep=s2[0]['value']
    r = requests.get('https://www.shoppersstop.com'+sdeep, headers=headers)

    soup2 = BeautifulSoup(r.content, 'html.parser') 
    sdeep2 = soup2.find_all('script', type='application/ld+json') 
    json_content = json.loads(sdeep2[1].string)
    shsttit=json_content['name']
    shstpri=json_content['offers']['price']
    sdeep3 = soup2.find_all('picture') 
    first_link = sdeep3[2].find('source')
    shstimg=first_link['data-srcset']
    print(shsttit)
    print(shstpri)
    print(shstimg)
    product = {}
    product['name'] = shsttit
    product['img'] = shstimg
    product['price'] = shstpri
    return product

def lifestyle(stri):
    urlstr='https://www.lifestylestores.com/in/en/search?q='+stri+'%3Aindex%3Aprice%3Acolor.en%3A'+stri.split(' ')[-1]
    #urlstr='https://www.lifestylestores.com/in/en/SHOP-Levi%27s-Red-LEVI%27S-Men-Typographic-Printed-Crew-Neck-T-shirt/p/1000012345581-Red-Red'
    r = requests.get(urlstr) 
    soup = BeautifulSoup(r.content, 'html.parser') 
    s = soup.find_all('script')
    data = json.loads(s[4].text)
    lifename=data['props']['initialState']['algoliaProductReducer']['init']['_rawResults'][0]['hits'][0]['name']['en']
    lifepri=data['props']['initialState']['algoliaProductReducer']['init']['_rawResults'][0]['hits'][0]['price']
    lifeimg=data['props']['initialState']['algoliaProductReducer']['init']['_rawResults'][0]['hits'][0]['gallaryImages'][0]
    product = {}
    product['name'] = lifename
    product['img'] = lifeimg
    product['price'] = lifepri
    return product

class cart_page(View):
    def get(self,request): 
        # context={'price':request.session.get('price')}
        # print(context)
        return render(request,"cartPage.html")
    
    def post(self,request):
        # print(request.POST['cartinput'])
        # print(json.loads(request.POST['cartinput'])[0])
        for object in json.loads(request.POST['cartinput']):
            user = request.session.get('username')
            Product(user=user,name = object['name'], value = object['value']).save()
            # print(object['name'])
        return render(request,"orderConfirmed.html")
    
class orderConfirmed(View):
    def get(self, request):
        return render(request,"orderConfirmed.html")