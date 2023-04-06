from django.db import models

# Create your models here.

class Timings(models.Model):
	Stime = models.TimeField(max_length = 100,default=None,null = True)
	ETime = models.TimeField(max_length=200,default=None,null = True)
	P1Stime = models.TimeField(max_length=200,default=None,null = True)
	P1Etime = models.TimeField(max_length=200,default=None,null = True)
	P2Stime = models.TimeField(max_length=20,default=None,null = True)
	P2Etime = models.TimeField(max_length=100,default=None,null = True)
	Date_0 = models.DateField(default = None)

	class Meta:
		db_table = "Timings"


class Booths(models.Model):
	Type_of_booth = models.CharField(max_length = 100,default=None,null = True)
	Price_NA = models.BigIntegerField(default=None,null = True)
	Price_PA = models.BigIntegerField(default=None,null = True)
	Duration = models.BigIntegerField(default=None,null = True)
	Status = models.CharField(max_length=20,default=None,null = True)
	Date_1 = models.DateField(default = None)
	Max_Cars = models.CharField(max_length=20,default=None,null = True)
	countdown = models.DateTimeField(default = None)
	

 
	class Meta:
		db_table = "Booths"


class Simulation(models.Model):
	Bid = models.ForeignKey(Booths, on_delete=models.CASCADE,default=None,null = True)
	Cars_done =  models.CharField(max_length = 100,default=None,null = True)
	Cars_remaining = models.BigIntegerField(default=None,null = True)
	Amount_collected = models.BigIntegerField(default=None,null = True)
	Total_time_taken =  models.DateTimeField(max_length = 100,default=None,null = True)
	Date = models.DateField(default = None)
	Total_time_min = models.BigIntegerField(default=None,null = True)

	class Meta:
		db_table = "Simulation"