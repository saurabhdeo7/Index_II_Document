from django.db import models
import uuid

# from FindIndexIIWebsite import settings

from django.conf import settings

# Create your models here.

from users.models import CustomUser

LANGS = [('English', 'eng'), ]
STATES = [('', ''),('maharashtra', 'maharashtra'), ('andhra pradesh', 'andhra pradesh'), ('arunachal pradesh ', 'arunachal pradesh '), ('assam', 'assam'), ('bihar', 'bihar'), ('chhattisgarh', 'chhattisgarh'), ('goa', 'goa'), ('gujarat', 'gujarat'), ('haryana', 'haryana'), ('himachal pradesh', 'himachal pradesh'), ('jammu and kashmir', 'jammu and kashmir'), ('jharkhand', 'jharkhand'), ('karnataka', 'karnataka'), ('kerala', 'kerala'), ('madhya pradesh', 'madhya pradesh'), ('manipur', 'manipur'), ('meghalaya', 'meghalaya'), ('mizoram', 'mizoram'), ('nagaland', 'nagaland'), ('odisha', 'odisha'), ('punjab', 'punjab'), ('rajasthan', 'rajasthan'), ('sikkim', 'sikkim'), ('tamil nadu', 'tamil nadu'), ('telangana', 'telangana'), ('tripura', 'tripura'), ('uttar pradesh', 'uttar pradesh'), ('uttarakhand', 'uttarakhand'), ('west bengal', 'west bengal'), ('andaman and nicobar islands', 'andaman and nicobar islands'), ('chandigarh', 'chandigarh'), ('dadra and nagar haveli', 'dadra and nagar haveli'), ('daman and diu', 'daman and diu'), ('lakshadweep', 'lakshadweep'), ('national capital territory of delhi', 'national capital territory of delhi'), ('puducherry', 'puducherry')]

# from django.core.files.storage import FileSystemStorage
#
# upload_storage = FileSystemStorage(location=settings.UPLOAD_ROOT)

class IndexIIdoc(models.Model):
    Doc_ID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        auto_created=True,
    )
    #  TODO: FileField
    fileIn=models.CharField(max_length=200,blank=True)
    # fileIn = models.FileField(upload_to='uploadedfiles')
    serialNo = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=500, blank=True)
    vilagename = models.CharField(max_length=200, blank=True)
    subdistrict = models.CharField(max_length=200, blank=True)
    district = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True, choices=STATES,default=("maharashtra"))
    # pincode=models.IntegerField(blank=True)
    language = models.CharField(max_length=100, choices=LANGS, default=('English', 'eng'))
    # added_by = models.CharField(max_length=200, default="admin")
    added_by= models.ForeignKey(CustomUser , on_delete=models.CASCADE,related_name='owner')

