from django.shortcuts import render
from django.conf import settings
from .forms import UploadFileForm
from PIL import Image, ImageOps
import numpy as np
import tensorflow as tf

CLASSES = ['Blusa', 'Calça', 'Colete', 'Vestido', 'Casaco', 'Sandália', 'Camisa', 'Tênis', 'Bolsa', 'Bota de Cano Longo']

def index(request):
    contexto = {}
    contexto['modo'] = request.method
    if request.method == "GET":
        contexto["form"] = UploadFileForm()
        contexto['msg'] = "Tire uma foto para que o sistema a classifique em uma das 10 classes"
    elif request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            model = tf.keras.models.load_model(settings.BASE_DIR / 'modelo.h5')
            img = Image.open(request.FILES['file'])
            img.save("original.jpg")
            largura, altura = img.size
            if largura > altura:
                img = img.rotate(-90, Image.NEAREST, expand = 1)
                img.save("original_roted.jpg")
            if largura != altura:
                largura, altura = img.size
                left, top = ( 0, int((altura / 2) - (largura / 2)))
                right, bottom = ( largura, int(altura / 2 + largura / 2))
                img = img.crop((left, top, right, bottom))
                img.save("teste_cortada.jpg")
            img = ImageOps.grayscale(img)
            img.thumbnail((28,28))
            img.save(settings.BASE_DIR / 'editada.jpg')
            matrizImg = np.array(img)
            matrizImg = (np.expand_dims(matrizImg, 0))
            predicaoSimples = model.predict(matrizImg)
            predicao = CLASSES[np.argmax(predicaoSimples[0])]
            contexto['msg'] = "Sua Foto é um "+str(predicao)+" | Precisão de "+str(int(max(predicaoSimples[0]*100)))+"%"
        else:
            contexto['msg'] = "Houve um problema com o upload!"
    return render(request, 'index.html', contexto)

