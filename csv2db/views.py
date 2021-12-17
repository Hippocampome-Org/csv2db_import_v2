from django.shortcuts import render
from .forms import UploadFileForm
from .lib.map import Map
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import zipfile
import time
import os
from django.core.management import call_command
from krasnow import settings
import subprocess
from django.http import HttpResponse
from django.http import JsonResponse
DATABASES = settings.DATABASES
name = DATABASES['default']['NAME']
passwd = DATABASES['default']['PASSWORD']
user = DATABASES['default']['USER']
def load(request):
    if request.method == "POST":
        try:
                file = request.FILES['file']
                fs = FileSystemStorage()
                timestr = time.strftime("%Y%m%d-%H%M%S")
                filename = fs.save(timestr+"-"+file.name, file)
                with zipfile.ZipFile("filedownloads/"+timestr+"-"+file.name, "r") as z:
                    z.extractall("iconv_autoingestion/latin1/"+timestr+"-"+file.name)
                directory = "iconv_autoingestion/latin1/"+timestr+"-"+file.name+"/"+str(file.name).split(".")[0]
                outputdirectory = "iconv_autoingestion/utf8/"
                outputdirectory_packetnotes = "iconv_autoingestion/utf8/packet_notes/"
                for filename in os.listdir(directory):
                    print(filename)
                    if os.path.isfile(os.path.join(directory, filename)) and filename.endswith(".csv"):
                        cmd = "iconv -f latin1 -t UTF-8 {0} > {1}".format(os.path.join(directory, filename),os.path.join(outputdirectory,filename))
                        print(cmd)
                        os.system(cmd)
                    elif os.path.isdir(os.path.join(directory, filename)):
                        direc = os.path.join(directory, filename)
                        for fn in os.listdir(direc):
                            cmd = "iconv -f latin1 -t UTF-8 {0} > {1}".format(os.path.join(direc, fn),os.path.join(outputdirectory_packetnotes,fn))
                            print(cmd)
                            os.system(cmd)
                os.system("cp -vr iconv_autoingestion/utf8/ static/csv2db/dat/")
                call_command('makemigrations')
                call_command('migrate')
                call_command('flush','--noinput')
                call_command('load')
                file = open(os.getcwd()+"/mysqldump/backup.sql", 'w+')
                if passwd!="":
                    proc = subprocess.Popen(["mysqldump","-u",user,"-p"+passwd,name],stdout=file,
                                      stderr=subprocess.STDOUT)
                else:
                    proc = subprocess.Popen(["mysqldump","-u",user,name],stdout=file,
                                      stderr=subprocess.STDOUT)
                proc.wait()
                proc.communicate()
                file.close()
                def download_helper():
                    file_path = os.getcwd()+"/mysqldump/backup.sql"
                    if os.path.exists(file_path):
                            with open(file_path, 'rb') as fh:
                                    response = HttpResponse(fh.read(), content_type="application/sql")
                                    response['Content-Disposition'] = 'inline; filename=backup.sql'
                                    return response
                    else:
                            return HttpResponse('Cannot find file')
                return download_helper()
        except Exception as e:
            print(e)
            return HttpResponse('Error')
    else:
        return render(request,'csv2db/load.html')

def index(request):
    return render(request, 'csv2db/index.html')

def import_all(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Map(request).all_to_all()
                return render(request, 'csv2db/done.html')
            except KeyError:
                return render(request, 'csv2db/error.html')
        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()
    return render(request, 'csv2db/import_all.html', {'form': form})

def import_article(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Map(request).article_to_article() # and article_to_author
                return render(request, 'csv2db/done.html')
            except KeyError:
                return render(request, 'csv2db/error.html')
        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()
    return render(request, 'csv2db/import_article.html', {'form': form})

def import_attachment(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Map(request).attachment_to_attachment()
                return render(request, 'csv2db/done.html')
            except KeyError:
                return render(request, 'csv2db/error.html')
        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()
    return render(request, 'csv2db/import_attachment.html', {'form': form})

def import_connection(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Map(request).connection_to_connection()
                return render(request, 'csv2db/done.html')
            except KeyError:
                return render(request, 'csv2db/error.html')
        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()
    return render(request, 'csv2db/import_connection.html', {'form': form})

def import_epdata(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Map(request).epdata_to_epdata()
                return render(request, 'csv2db/done.html')
            except KeyError:
                return render(request, 'csv2db/error.html')
        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()
    return render(request, 'csv2db/import_epdata.html', {'form': form})

def import_fragment(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Map(request).fragment_to_fragment()
                return render(request, 'csv2db/done.html')
            except KeyError:
                return render(request, 'csv2db/error.html')
        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()
    return render(request, 'csv2db/import_fragment.html', {'form': form})

def import_markerdata(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Map(request).markerdata_to_markerdata()
                return render(request, 'csv2db/done.html')
            except KeyError:
                return render(request, 'csv2db/error.html')
        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()
    return render(request, 'csv2db/import_markerdata.html', {'form': form})

def import_morphdata(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Map(request).morphdata_to_morphdata()
                return render(request, 'csv2db/done.html')
            except KeyError:
                return render(request, 'csv2db/error.html')
        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()
    return render(request, 'csv2db/import_morphdata.html', {'form': form})

def import_notes(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Map(request).notes_to_type()
                return render(request, 'csv2db/done.html')
            except KeyError:
                return render(request, 'csv2db/error.html')
        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()
    return render(request, 'csv2db/import_notes.html', {'form': form})

def import_synonym(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Map(request).synonym_to_synonym()
                return render(request, 'csv2db/done.html')
            except KeyError:
                return render(request, 'csv2db/error.html')
        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()
    return render(request, 'csv2db/import_synonym.html', {'form': form})

def import_term(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Map(request).term_to_term()
                return render(request, 'csv2db/done.html')
            except KeyError:
                return render(request, 'csv2db/error.html')
        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()
    return render(request, 'csv2db/import_term.html', {'form': form})

def import_type(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                dev = 'false'
                Map(request).type_to_type(dev)
                return render(request, 'csv2db/done.html')
            except KeyError:
                return render(request, 'csv2db/error.html')
        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()
    return render(request, 'csv2db/import_type.html', {'form': form})

def import_type_dev(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                dev = 'true'
                Map(request).type_to_type(dev)
                return render(request, 'csv2db/done.html')
            except KeyError:
                return render(request, 'csv2db/error.html')
        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()
    return render(request, 'csv2db/import_type_dev.html', {'form': form})
