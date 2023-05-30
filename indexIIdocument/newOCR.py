    
from re import L
import pdf2image as pp
from .Ath_table_ocr import Athextract_tables
from .Ath_table_ocr import Athextract_cells
from .Ath_table_ocr import Athocr_image
from .Ath_table_ocr import Athocr_to_csv
from django.conf import settings

from PIL import Image

fileCore = settings.CONTENT_DIR+"/"
# fileCore ="./tmp/"
def pdfToImg(pdfpath):
    # Store Pdf with convert_from_path function
    images = pp.convert_from_path(pdfpath)

    imageList=[]

    for i in range(len(images)):
        nameOfFile=fileCore+'page'+ str(i) +'.jpg'
        # Save pages as images in the pdf
        imageList.append(str(nameOfFile))
        images[i].save(nameOfFile, 'JPEG')

    return imageList

def makeinputImage(input):
    print("input is",input)
    listOfFiles=[]
    # name,ext=os.path.splittext(input)
    ext=input.endswith('.pdf')
    if ext:
        print("this is pdf")
        listOfFiles= pdfToImg(input)
    else:
        img=Image.open(input)
        nameOfFile=fileCore+str(input)+'.jpg'
        # Save pages as images in the pdf
        img.save(nameOfFile, 'JPEG')
        img.close()
        listOfFiles=[nameOfFile]
        pass
    return listOfFiles


def main(inputFile):
    # image_filepath = download_image_to_tempdir(url)
    image_filepath=inputFile
    image_tables = Athextract_tables.main([image_filepath])

    print("Running `{}`".format(f"extract_tables.main([{image_filepath}])."))
    print("Extracted the following tables from the image:")
    print(image_tables)
    for image, tables in image_tables:
        print(f"Processing tables for {image}.")
        for table in tables:
            print(f"Processing table {table}.")
            cells = Athextract_cells.main(table)
            ocr = [
                Athocr_image.main(cell, 'config= --psm 14')   #None language is set bydefault mar+eng 
                for cell in cells
            ]
            
            print("Extracted {} cells from {}".format(len(ocr), table))
            print("Cells:")
            for c, o in zip(cells[:3], ocr[:3]):
                print("%"*20)
                print("c,o: "+c+","+o)
                print("%"*20)
                with open(o,encoding="utf-8") as ocr_file:
                    # Tesseract puts line feeds at end of text.
                    # Stript it out.
                    text = ocr_file.read()
                    print("{}: {}".format(c, text))
                    print("%"*20)
            # If we have more than 3 cells (likely), print an ellipses
            # to show that we are truncating output for the demo.
            if len(cells) > 3:
                print("...")
            return Athocr_to_csv.text_files_to_csv(ocr)


def write_list(fname, lines):
    with open(fname, "w",encoding='utf-8') as fhandle:
      for line in lines:
        fhandle.write(f'{line}\n')
    fhandle.close()

def getFullOCR(filename):
    listOfImages=(list(makeinputImage(filename)))
    csv_output=(list(map(main,listOfImages)))
    
    write_list(str(filename)+'output.csv',csv_output)
    return str(filename)+'output.csv'