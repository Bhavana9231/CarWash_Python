from django.shortcuts import render,redirect
from django.contrib import messages
import datetime
from datetime import datetime
from .models import *
from django.db.models import Max
from datetime import date
import datetime
from datetime import date,timedelta
# Create your views here.
def home(request):
	return render(request,'home.html',{})

def Simulation_dashboard(request):
	booth = Simulation.objects.all()
	return render(request,'Simulation_dashboard.html',{'booth':booth})

def base(request):
	return render(request,'base.html',{})
def test1(request):
	return render(request,'test1.html',{})
def test2(request):
	return render(request,'test2.html',{})
def Add_Timings(request):
	if request.method == "POST":
		Stime = request.POST['Stime']
		ETime = request.POST['ETime']
		P1Stime = request.POST['P1Stime']
		P1Etime = request.POST['P1Etime']
		P2Stime = request.POST['P2Stime']
		P2Etime = request.POST['P2Etime']
		#Date = request.POST['Date']
		now = datetime.datetime.now()
		today = date.today()

		time = Timings(Stime = Stime,ETime = ETime,P1Stime = P1Stime,P1Etime = P1Etime,P2Stime = P2Stime,P2Etime = P2Etime,Date_0 = today)
		time.save()
		return redirect('/')
	else:
		return render(request,'Add_Timings.html',{})


def Manage_Booths(request):
	booth = Booths.objects.all()
	return render(request,'Manage_Booths.html',{'booth':booth})



def Add_Booths(request):
	if request.method == "POST":
		users = Booths.objects.all()
		#next_id = users.aggregate(Max('id'))['id__max'] + 1 if users else 1
		#print(next_id)
		
		
		Type_of_booth = request.POST['Type_of_booth']
		Price_NA = request.POST['Price_NA']
		Price_PA = request.POST['Price_PA']
		car_count = request.POST['car_count']
		Status = request.POST['Status']
		Duration = request.POST['Duration']
		total_time = int(car_count) * (int(Duration))
		print(total_time)
		t = datetime.datetime.now()
		current_time =datetime.datetime.now()
		print(current_time)
		new_time = current_time + datetime.timedelta(seconds=total_time)
		print(new_time)
		
		booth = Booths(Type_of_booth = Type_of_booth,Price_NA = Price_NA,Price_PA = Price_PA,Status = Status,Date_1 = t,Duration = Duration,countdown = new_time)
		booth.save()
		users = Booths.objects.all()
		next_id = users.aggregate(Max('id'))['id__max'] + 1
		print(next_id)
		simulate = Simulation(Bid = booth,Cars_done = '0' ,Cars_remaining = car_count ,Amount_collected = '0',Total_time_taken = t,Date = t,Total_time_min = total_time)
		simulate.save()
		
		
		
		
		
		return redirect('/test2/')
	else:
		return redirect('/test2/')



def Update_Booth(request):
	if request.method == "POST":
		b_id = request.POST['1updateid']
		Type_of_booth = request.POST['1updatename']
		Price_NA = request.POST['1updateage']
		Price_PA = request.POST['1updatephone']
		Status = request.POST['1updateadd']
		Booths.objects.all().filter(id = b_id).update(Price_NA = Price_NA,Price_PA = Price_PA,Status = Status)
		return redirect('/Manage_Booths/')
	else:
		return redirect('/Manage_Booths/')

def performance_booth(request):
	return render(request,'performance_booth.html',{})