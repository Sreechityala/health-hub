from flask import Flask,render_template,request,redirect,session
from pymongo import MongoClient
import smtplib
app = Flask(__name__)

server = smtplib.SMTP(host="smtp.gmail.com",port=587)

cluster = MongoClient('mongodb+srv://sreech5121:sreech@cluster0.pnddyvt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

db = cluster['health']
users = db['users']
appoints = db['appointments']
carts = db['carts']
labCart = db['labcart']
mediceineOrders = db['orders']

app.secret_key = "ItIsAsECrEt@123"
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard',methods=['get'])
def loaddash():
    return render_template('app.html')

@app.route('/login',methods=['get'])
def loadlogin():
    return render_template('login.html')

@app.route('/signup',methods=['get'])
def loadsign():
    return render_template('sign-up.html')

@app.route('/login',methods=['post'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = users.find_one({"email":email,"password":password})
    if not user:
        return render_template('login.html',status="You don't have an account with these credentials")
    session['email'] = email
   
    return redirect('/dashboard')

@app.route('/labtest')
def labtest():
    return render_template('lab-test.html')

@app.route('/doctors')
def doctors():
    return render_template('find-doctors.html')

@app.route('/medicine')
def medicine():
    return render_template('medicine.html')

@app.route('/article')
def article():
    return render_template('article.html')

@app.route('/order')
def order():
    return render_template('order.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/article1')
def article1():
    return render_template('walking-article.html')

@app.route('/article2')
def article2():
    return render_template('stop-smoking-article.html')

@app.route('/article3')
def article3():
    return render_template('menstrual-cramps-article.html')

@app.route('/article4')
def article4():
    return render_template('healthy-gut-article.html')

@app.route('/article5')
def article5():
    return render_template('antibiotics-article.html')

@app.route('/family')
def doctor1():
    return render_template('family-doctor.html')

@app.route('/nutritionist')
def doctor2():
    return render_template('nutritionist.html')

@app.route('/dentist')
def doctor3():
    return render_template('dentist.html')

@app.route('/surgeon')
def doctor4():
    return render_template('surgeon.html')

@app.route('/cardiologist')
def doctor5():
    return render_template('cardiologist.html')

@app.route('/deliver')
def orderDel():
    return render_template('delivery.html')

@app.route('/book',methods=['post'])
def book():
    user = session["email"]
    name = request.form['name']
    # email = request.form['email']
    number = request.form['number']
    date = request.form['date']
    time = request.form['timeslot']
    
    appoints.insert_one({"user":user,"name":name,"number":number,"date":date, "timeslot": time})
    msg = """Subject: Booking Confirmtion \n
    Hi {0}, Thanks for Booking. Appointment is confirmed on following date and time \n
    Date : {1} \n
    Time : {2} \n
    """.format(name,date,time)
    server.starttls()
    server.login('sreech5121@gmail.com','aobkftmbyeuwrgpd')
    server.sendmail('sreech5121@gmail.com',user,msg=msg)
    return render_template('app.html',status="Appointment booked")

@app.route('/submit-address', methods=['post'])
def deliver():
    user = session["email"]
    name = request.form['fullname']
    number = request.form['phone']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    zip = request.form['zip']
    country = request.form['country']
    date = request.form['date'] 
    
    mediceineOrders.insert_one({"user": user, "name": name, "number": number, "address": address, "city": city, "state": state, "zip": zip, "country": country, "date": date})
    server.starttls()
    server.login('sreech5121@gmail.com', 'aobkftmbyeuwrgpd')
    server.sendmail('sreech5121@gmail.com', user, 'Your Order has been Confirmed and it will deliver on ' +date)
    return render_template('app.html')


@app.route('/signup',methods=['post'])
def signup():
    name = request.form['username']
    email = request.form['email']
    phno = request.form['mobile']
    gender = request.form['gender']
    password = request.form['password']
    cpass = request.form['cpassword']
    if password!=cpass:
        return render_template('sign-up.html',status="Password does not match")
    user = users.find_one({"email":email})
    if user:
        return render_template('sign-up.html',status="Already exist with this email")
    doc = {"email":email,"name":name,"mobile":phno,"gender":gender,"password":password}
    users.insert_one(doc)
    return redirect('/login')

@app.route('/addcart',methods=['post'])
def cart():
    item = request.form['item']
    email = session['email']
    isCart = carts.find_one({'email':email})
    if isCart:
        carts.update_one({'email':email},{"$push":{"items":item}})
    else:
        carts.insert_one({"email":email,"items":[item]})  
    return render_template('medicine.html')  

@app.route('/orders')
def orders():
    data = carts.find_one({'email':session['email']})
    newData = []
    print(data['items'])
    for i in data['items']:
        c = {}
        b = i.split('$')
        c['item'] = b[0]
        c['cost'] = b[1]
        newData.append(c)
    return render_template('order.html',items=newData)

@app.route('/laborders')
def  laborders():
    email = session['email']
    data = labCart.find_one({'email':email})
    newData = []
    for i in data['items']:
        c = {}
        b = i.split('$')
        c['item'] = b[0]
        c['cost'] = b[1]
        newData.append(c)
    return render_template('laborders.html',items=newData)

@app.route('/labcart',methods=['post'])
def labcar():
    email = session['email']
    item = request.form['item']
    isLabCart = labCart.find_one({'email':email})
    if isLabCart:
        labCart.update_one({'email':email},{'$push':{'items':item}})
    else:
        labCart.insert_one({'email':email,'items':[item]})
    return render_template('lab-test.html')

if __name__=="__main__":
    app.run(debug=True)