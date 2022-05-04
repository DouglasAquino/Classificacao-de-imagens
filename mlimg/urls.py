from django.conf import settings
from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from PIL import Image, ImageOps
import numpy as np
import tensorflow as tf
from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

def index(request):
    contexto = {}
    classes = ['Camiseta/topo', 'Camiseta', 'Pullover', 'Vestido', 'Casaco', 'Sandália', 'Camisa', 'Sneaker', 'Tênis', 'Bota de Cano Longo']
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
            img = img.rotate(-90, Image.NEAREST, expand = 1)
            img.save("original_roted.jpg")
            print(30*"-",'\n',5*"-","PROCESSANDO",5*"-")
            largura, altura = img.size
            print("TAMANHO roted: ",img.size)
            if largura != altura:
                x, y = (0,int((altura / 4)))
                print("imensões:",(x,y,2 * y,3 * y))
                img = img.crop((x,y,2 * y,3 * y))
                print("pos crop? ",img.size)
                img.save("teste_cortada.jpg")
            img = ImageOps.grayscale(img)
            img.thumbnail((28,28))
            print(5*"-",img.size,5*"-")
            img.save(settings.BASE_DIR / 'editada.jpg')
            matrizImg = np.array(img)
            matrizImg = (np.expand_dims(matrizImg, 0))
            predicaoSimples = model.predict(matrizImg)
            print("PREDIÇÂO: \n",predicaoSimples)
            print(30*"-")
            predicao = classes[np.argmax(predicaoSimples[0])]
            contexto['msg'] = "Sua Foto é um "+str(predicao)+" | Precisão de "+str(int(max(predicaoSimples[0]*100)))+"%"
        else:
            contexto['msg'] = "Houve um problema com o upload!"
    return render(request, 'index.html', contexto)

urlpatterns = [
    path('', index, name="home"),
    path('admin/', admin.site.urls),
]
