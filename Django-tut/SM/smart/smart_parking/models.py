from django.db import models

# Create your models here.
class slot(models.Model):
	slot_name = models.CharField(max_length=200)
	slot_status = models.CharField(max_length=100,default='free')
	
	def __str__(self):
		return  (self.slot_name)

class Order (models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_id = models.ForeignKey(slot)
    payment_option = models.CharField(max_length=50)
    