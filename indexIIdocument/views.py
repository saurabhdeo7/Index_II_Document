import csv
import re
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator

# from FindIndexIIWebsite import settings
from django.conf import settings

from users.decorators import superuser_only
from .newOCR import getFullOCR

from .models import STATES, IndexIIdoc

from users.models import CustomUser

from django.contrib.auth.decorators import login_required
from users import decorators

from django.core.files import File
from django.shortcuts import render, get_object_or_404

# Create your views here.

fileCore = settings.CONTENT_DIR

dataToSend = {
    'village': '',
    'serialNo': '',
    'typeOfImg': '',
    'desc': '',
    'output_data': '',
    'uploaded_file_url': '',
    'STATES': STATES,
    'districtList': '',
    'subdistrictList': '',

}
myfile = ''

fileCore = settings.CONTENT_DIR


@login_required
def uploadDocument(request):
    print("in upload function")
    # if request.method == 'POST' and request.POST.get('searchDoc') == 'searchDoc':
    #     print("in search")
    #     # Subject.objects.filter(Q(user__in=["John", "Brad"]) | Q(user__isnull=True))
    #     village = str(request.POST['village']).lower().strip()
    #     state = str(request.POST['state']).lower().strip()
    #     district = str(request.POST['district']).lower().strip()
    #     subdistrict = str(request.POST['subdistrict']).lower().strip()
    #     PropertyNo = str(request.POST['PropertyNo']).lower().strip()
    #
    #     mydata = IndexIIdoc.objects.filter(state=state, vilagename=village, district=district, subdistrict=subdistrict,
    #                                        description__icontains=PropertyNo).values()
    #
    #     print("village search:"+village)
    #

    if request.method == 'POST' and request.POST.get('upload') == 'uploadFirst':
        myfile = request.FILES['inputFile']

        # validation for size of file
        if myfile.size > 2000000:
            messages.error(request, "File size too large.")
            return redirect('uploadDocument')
        # validation for file format
        file_name_suffix = myfile.name.split(".")[-1]
        if file_name_suffix not in ["jpg", "png", "gif", "jpeg", "pdf"]:
            messages.error(request, "Wrong file suffix , supported are .jpg, .png, .jpeg, .pdf")
            return redirect('uploadDocument')

        print("pathhhhhh:" + settings.UPLOAD_ROOT)
        # fs = FileSystemStorage(location=settings.UPLOAD_ROOT, base_url='')
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        dataToSend['uploaded_file_url'] = fs.url(filename)
        fname = fileCore + dataToSend['uploaded_file_url']

        # dataToSend['uploaded_file_url'] = fname

        # print(dataToSend['uploaded_file_url'])
        print("fname:" + fname)

        if fname.endswith('.pdf'):
            dataToSend['typeOfImg'] = 'pdf'
        else:
            dataToSend['typeOfImg'] = 'image'


        Outputfilename = getFullOCR(fname)
        # for whole OCR
        with open(Outputfilename, "r", encoding='utf-8') as f:
            dataToSend['output_data'] = str(f.read())
        f.close()

        dataToSend['desc'] = searchDesc(Outputfilename, "land")

        dataToSend['village'] = searchDesc(Outputfilename, "village name")
        print("%%%%" + dataToSend['village'])
        dataToSend['serialNo'] = searchDesc(Outputfilename, "serial number")

        # dataToSend['pincode']= searchDesc(Outputfilename,"pincode")

        # print(filename)
        # district list
        # districtList=IndexIIdoc.objects.order_by('disrict').values_list('district',flat=True).distinct()
        # print(type(districtList))
        dataToSend['districtList'] = list(set(IndexIIdoc.objects.values_list('district', flat=True)))
        dataToSend['subdistrictList'] = list(set(IndexIIdoc.objects.values_list('subdistrict', flat=True)))

        return render(request, template_name='indexIIdocument/indexIIDocumentUpload.html', context=dataToSend)
    elif request.method == 'POST' and request.POST.get('save') == 'save':
        serialNo = str(request.POST['serialNo']).lower().strip()
        village = str(request.POST['village']).lower().strip()
        state = str(request.POST['state']).lower().strip()
        district1 = str(request.POST.get('district1',False)).lower().strip()
        subdistrict1 = str(request.POST.get('subdistrict1',False)).lower().strip()

        district2 = str(request.POST.get('district2',False)).lower().strip()
        subdistrict2 = str(request.POST.get('subdistrict2',False)).lower().strip()

        if district1 is None:
            district= district2

        else:
            district=district1

        if subdistrict1 is None:
            subdistrict = subdistrict2
        else:
            subdistrict = subdistrict1

        desc = str(request.POST['desc']).lower().strip()

        # f =open(dataToSend['uploaded_file_url'] ,"r")

        # document.fileIn= fileCore+ dataToSend['uploaded_file_url']

        # f =open(dataToSend['uploaded_file_url'] )
        # doc.fileIn=f

        # doc.fileIn = File(open( dataToSend['uploaded_file_url'] ))

        if IndexIIdoc.objects.filter(serialNo=serialNo).exists():
            messages.warning(request, "Document Already available in database. You cannot upload this document")

        else:
            # TODO: Fielfield changes
            # f =File(dataToSend['uploaded_file_url'])
            # print(f)
            # doc.fileIn=f
            # from django.core.files import File
            # Open an existing file using Python's built-in open()
            # import os
            # dataToSend['uploaded_file_url'] = dataToSend['uploaded_file_url'].replace(os.sep, '/')

            # f = open(dataToSend['uploaded_file_url'], "r", encoding='utf-8')
            # print("f is :" + str(f))
            # myfile1 = File(f)
            # print("myfile1 " + str(myfile1))
            doc = IndexIIdoc(fileIn=dataToSend['uploaded_file_url'], serialNo=serialNo, description=desc,
                             vilagename=village, subdistrict=subdistrict, district=district, state=state,
                             added_by=request.user)
            print("filIn field: " + str(doc.fileIn))

            doc.save()
            # f.close()
            messages.success(request, "Document Added Successfully")

            valuer = CustomUser.objects.get(username=request.user)
            number_of_docs_uploaded = int(valuer.number_of_docs_uploaded)
            number_of_docs_uploaded = number_of_docs_uploaded + 1

            #By Abhi ----------!!!!!!
            num1 = int(valuer.number_of_docs_downloded)
            number_of_docs_loded = num1 + 1

            valuer.number_of_docs_downloded = number_of_docs_loded
            valuer.number_of_docs_uploaded = number_of_docs_uploaded
            valuer.save()

        # deleteTmp(settings.UPLOAD_ROOT)

        return redirect('uploadDocument')
    else:
        print("else")
        pass

    return render(request=request, template_name='indexIIdocument/indexIIDocumentUpload.html')


def searchDesc(Outputfilename, descTitle):
    descOutput = ''
    # opening the CSV file
    with open(Outputfilename, mode='r', encoding='utf-8') as file:

        # reading the CSV file
        csvFile = csv.DictReader(file)
        # print(str(csvFile))

        # displaying the contents of the CSV file
        for lines in csvFile:
            # print(lines)
            # Village Name :
            if descTitle == "village name":
                # print("vill:"+str.lower(lines['k']))
                fo = re.search(descTitle, str.lower(lines['k']))
                if fo is None:
                    descOutput = str(fo)
                    continue
                else:
                    descOutput = str.lower((lines['k']))[fo.end():]
                    # print("found vill:" + descOutput)

                    break

                print("found :" + descOutput)

            if descTitle == "serial number":
                pattern = "[:]{1}[ ]*[0-9]+[/]{1}[0-9]{4}"
                # print("may in:"+str(lines['k']))
                fo = re.search(pattern, str(lines['k']))
                # print(str(fo))
                if fo is None:
                    descOutput = str(fo)
                else:
                    descOutput = str(lines['k'])[fo.start() + 1:fo.end()]
                    print(descOutput)
                break

            # PINCODE FUNCTIONALITY MAY BE ADDED LATER
            # if descTitle=="pincode" :
            #     fo = re.search("^[0-9]{6}$", str(lines['k']))
            #     if fo is None:
            #         descOutput =str(fo)
            #     else:
            #
            #         descOutput = str(fo.group())
            # #     break;
            # '''     <div class="container md-2">
            #             <strong>Verify this pincode for filling other values automatially or put those values manually.</strong>
            #             <br>
            #             <label for="pincode"> pincode</label>
            #             <input type="text" id="pincode" name="pincode" value="">
            #             <button name="pincodeVerify">verify pincode</button>
            #         </div>'''

            if re.search(descTitle, str.lower(lines['k'])):
                # print("found")
                descOutput = str(lines['v'])
                break
    # print("v = " + descOutput)

    return descOutput


def deleteTmp(path):
    import os
    for file_name in os.listdir(path):
        # construct full file path
        file = path + file_name
        if os.path.isfile(file):
            print('Deleting file:', file)
            os.remove(file)


@superuser_only
def allDocument(request):
    mydata = IndexIIdoc.objects.all().values()
    paginator = Paginator(mydata,10)
    pagenumber = request.GET.get("page")
    myFinalData = paginator.get_page(pagenumber)
    context = {
        'mydata': myFinalData,
    }
    return render(request=request, template_name='indexIIdocument/dataview.html', context=context)


@login_required
def yourDocument(request):
    mydata = IndexIIdoc.objects.filter(added_by=request.user).values()
    paginator = Paginator(mydata,10)
    pagenumber = request.GET.get("page")
    myFinalData = paginator.get_page(pagenumber)
    yourDocument = 2
    context = {
        'mydata': myFinalData,
        'page' : yourDocument,
    }
    print(context['page'])
    return render(request=request, template_name='indexIIdocument/dataview.html', context=context)