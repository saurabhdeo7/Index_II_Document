# django_project/main/views.py
from django.db.models import Q
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from indexIIdocument.models import STATES, IndexIIdoc
from users.models import CustomUser
from django.core.paginator import Paginator

mydata=""
uploadedCount , downloadedCount = 0 , 0
# Create your views here.
def aboutpage(request):
    return render(request=request,
                  template_name="main/about.html")

def homepage(request):
    mydata=""
    if request.method == 'POST' and request.POST.get('searchDoc') == 'searchDoc':
        # Subject.objects.filter(Q(user__in=["John", "Brad"]) | Q(user__isnull=True))
        village = str(request.POST.get('village')).lower().strip()
        state = str(request.POST['state']).lower().strip()
        district = str(request.POST['district']).lower().strip()
        subdistrict = str(request.POST['subdistrict']).lower().strip()
        PropertyNo = str(request.POST['PropertyNo']).lower().strip()
        if state != "":
            messages.info(request, "Showing All Documents from State : " + state)
        else :
            messages.info(request, "Showing All Available Documents")


        mydata = IndexIIdoc.objects.filter(Q(state__icontains=state) | Q(state__in=state) | Q(state__isnull=True),
                                           Q(vilagename__icontains=village) | Q(vilagename__in=village) | Q(
                                               vilagename__isnull=True),
                                           Q(district__icontains=district) | Q(district__in=district) | Q(
                                               district__isnull=True),
                                           Q(subdistrict__icontains=subdistrict) | Q(subdistrict__in=subdistrict) | Q(
                                               subdistrict__isnull=True),
                                           Q(serialNo__icontains=PropertyNo) | Q(serialNo__in=PropertyNo) | Q(
                                               serialNo__isnull=True)).values()
        
        Query = CustomUser.objects.filter(Q(username = request.user)).values_list()
        
        uploadedCount = 0
        #downloadedCount = Query[0][15]
        #print(mydata[0])
        if village is None:
            print("village search:none" + village)

        if(str(request.user) != "AnonymousUser" and str(request.user.is_superuser) != "True"):  #Changed By MSc CS Team
            mydata = mydata.filter(~Q(added_by = request.user)).values()                        #Changed By MSc CS Team

    paginator = Paginator(mydata,10)
    pagenumber = request.GET.get("page")
    myFinalData = paginator.get_page(pagenumber)

    return render(request=request,
                  template_name='main/home.html',
                  context={"objects": "dummy",
                           "STATES": STATES,
                            "mydata":myFinalData,
                           }
                  )


    # return HttpResponse("This is our homepage! It works!")

