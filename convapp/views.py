import os
import fnmatch
import shutil

import fitz
from PIL import Image
from fpdf import FPDF
from psd_tools import PSDImage

from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import datetime

from .serializers import ImageSerializer
from .models import FileModel,ImgModel

folder_time = datetime.datetime.now().strftime("%Y-%m-%d_%I-%M-%S_%p")
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=15)

class Fileupload(APIView):
    def post(self, request):
        if request.method == "POST":
            #saving user file in current format
            docfile = FileModel()
            docfile.file= request.FILES['filename']
            docfile.save()
	    
            #check the extension of uploaded file
            extension = str(docfile.file).split(".")[-1]
            name = str(docfile.file)
		
	    #if the extension is PDF or AI use this
            if extension == "pdf" or extension == "ai":
                for file in os.listdir('media'):
                    if fnmatch.fnmatch(file, name):
                        document = os.path.join('media', file)
                        doc = fitz.open(document)
                        for each in doc:
                            page_num = str(each).split()
                            current_page = int(page_num[1])
                            page = doc.loadPage(current_page)  # number of page
                            pix = page.get_pixmap()
                            output = name +'pg'+ str(page_num[1])+folder_time+ ".png"
                            pix.save(output)

                            for images in os.listdir('./'):
                                if fnmatch.fnmatch(images, '*.png'):
                                    shutil.move(images, settings.MEDIA_ROOT)

                            image = ImgModel()
                            image.file = docfile
                            image.img = output
                            image.save()

            #if it's image format or say extension is png/jpg/jpeg/tiff
            elif extension == "png" or extension == "jpg" or extension == "jpeg" or extension == "tiff":
                image = ImgModel()
                image.file = docfile
                image.img = request.FILES['filename']
                image.save()

            #if the extension is bmp
            elif extension =="bmp":
                img = Image.open(docfile.file)
                target_name = name + ".png"
                rgb_image = img.convert('RGB')
                rgb_image.save(target_name)
                for images in os.listdir('./'):
                    if fnmatch.fnmatch(images, '*.png'):
                        shutil.move(images, settings.MEDIA_ROOT)

                image = ImgModel()
                image.file = docfile
                image.img = target_name
                image.save()

            #if the extension is txt
            elif extension == "txt":
                # open the text file in read mode
                for file in os.listdir('media'):
                    if fnmatch.fnmatch(file, name):
                        document = os.path.join('media', file)
                        f = open(document, "r")

                        # insert the texts in pdf
                        for x in f:
                            pdf.cell(200, 10, txt=x, ln=1, align='L')

                        # save the pdf with name .pdf
                        pdf.output(name+".pdf")
                        new_doc = name+".pdf"

                        for images in os.listdir('./'):
                            if fnmatch.fnmatch(images, '*.pdf'):
                                shutil.move(images, settings.MEDIA_ROOT)

                        for file in os.listdir('media'):
                            if fnmatch.fnmatch(file, new_doc):
                                document = os.path.join('media', file)
                                doc = fitz.open(document)
                                for each in doc:
                                    page_num = str(each).split()
                                    current_page = int(page_num[1])
                                    page = doc.loadPage(current_page)  # number of page
                                    pix = page.get_pixmap()
                                    output = name + 'pg' + str(page_num[1]) + folder_time + ".png"
                                    pix.save(output)

                                    for images in os.listdir('./'):
                                        if fnmatch.fnmatch(images, '*.png'):
                                            shutil.move(images, settings.MEDIA_ROOT)

                                    image = ImgModel()
                                    image.file = docfile
                                    image.img = output
                                    image.save()
            
            #if the extension is psd
            elif extension == "psd":
                psd = PSDImage.open(docfile.file)
                psd.composite().save(name+'.png')

                for layer in psd:
                    print(layer)
                    layer_image = layer.composite()
                    layer_image.save('%s.png' % layer.name)


            images = ImgModel.objects.filter(file__id=docfile.id)
            serializer_class = ImageSerializer
            serializer = serializer_class(images, many=True)

        return Response(serializer.data)

