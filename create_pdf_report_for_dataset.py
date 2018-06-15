# -*- coding: utf-8 -*

# получаем сюда файл name_pkl с датасетом и генерим для него репорт name_report

import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import utils
from reportlab.platypus.flowables import HRFlowable
import pickle as pkl
import cv2
import shutil

def create_report(dset_2d_pkl, name_report, labels_names):

    if os.path.exists(name_report):
        os.remove(name_report)

    story = [] # сюда будем складывать все сущности, которые должны быть в отчете
    # извлекаем датасет из файла
    print("loading dataset from file " + dset_2d_pkl)
    infile = open(dset_2d_pkl, 'rb')
    new_dict = pkl.load(infile)
    infile.close()
    print("data loaded, len = : " + str(len(new_dict['xs'])))

    # обходим все картинки и добавляем их в отчет (story)
    new_folder = "temp"
    if os.path.exists(new_folder):
        shutil.rmtree(new_folder)
    os.makedirs(new_folder)

    for entry_i in range(len(new_dict['xs'])):
        print (str(entry_i))
        pic = new_dict['xs'][entry_i]
        description =""
        for label_name in labels_names:
            description.append(label_name + " - " + str(new_dict[label_name][entry_i]))
        img_name = os.path.join(new_folder, str(entry_i)+".png" )
        cv2.imwrite(img_name, pic)
        img = _make_image_for_report(img_name, width=10 * cm)
        descr = _make_text_to_report(text=str(description) + ":")

        story.append(descr)
        story.append(img)
        story.append(_make_line())

    # собственно строим сам отчет из
    doc = SimpleDocTemplate(name_report, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    doc.build(story)
    print("generated:    "+ name_report)



def _make_text_to_report(text):
    ptext = '<font size=12>%s</font>' % text
    styles = getSampleStyleSheet()
    return Paragraph(ptext, styles["Normal"])

def _make_image_for_report(path, width=8*cm):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))

def _make_line():
    return HRFlowable(width="80%", thickness=1, lineCap='round',  spaceBefore=1, spaceAfter=2, hAlign='CENTER',
               vAlign='BOTTOM', dash=None)

if __name__ == "__main__":
    name_report = "report.pdf"          # название отчетика
    dset_name_2d = "2d_healthy.pkl"     # файл с датасетом - 2d

    labels_names = ['ys']
    # labels_names = ['y1', 'y2','y3'] # какие лейблы есть для каждой картинки

    create_report(dset_name_2d, name_report, labels_names)

    shutil.rmtree('temp')  # удаляем папку с промежуточным слжебым мусором


