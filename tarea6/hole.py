#! /usr/bin/python
from time import time
from random import randint
from sys import argv, exit
from math import fabs, pow, sqrt
from PIL import Image, ImageOps, ImageDraw, ImageFont
from subprocess import call



def gradient(image, mask_type='prewitt', const = 2.0):
    
    indice_mascara = {
        "sobelx":[[-1.0*const, 0.0, 1.0*const], [-2.0*const, 0.0, 2.0*const], [-1.0*const, 0.0, 1.0*const]],
        "sobely":[[1.0*const, 2.0*const, 1.0*const], [0.0, 0.0, 0.0], [-1.0*const, -2.0*const, -1.0*const]],
        "prewittx":[[-1.0*const, 0.0, 1.0*const], [-1.0*const, 0.0, 1.0*const], [-1.0*const, 0.0, 1.0*const]],
        "prewitty":[[1.0*const, 1.0*const, 1.0*const], [0.0, 0.0, 0.0], [-1.0*const, -1.0*const, -1.0*const]]
        }

    pic_copy = (image.copy()).load()
    pic = image.load()
    kernelx = indice_mascara[mask_type+'x']
    kernely = indice_mascara[mask_type+'y']
    max_value = 0
    for i in range(image.size[0]):
        for j in range(image.size[1]):

            gx, gy = (0.0, 0.0)
            kernel_len = len(kernelx[0])
            kernel_pos = 0
            for h in range(i-1, i+2):
                for l in range(j-1, j+2):
                    if h >= 0 and l >= 0 and h < image.size[0] and l < image.size[1]:
                        pixel = pic_copy[h, l]

                        gx += pixel*kernelx[int(kernel_pos/3)][kernel_pos%3]
                        gy += pixel*kernely[int(kernel_pos/3)][kernel_pos%3]
                        kernel_pos += 1

            gradiente = int(sqrt(pow(gx, 2) + pow(gy, 2)))
            pic[i, j] = gradiente
            if pic[i, j] > max_value:
                max_value = pic[i, j]
    return max_value

def normalizar(image, max_value):
    pic = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            if max_value > 0:
                pic[i,j] = int( (float(pic[i,j])/max_value)*255 )
            else:
                pic[i,j] = 0

def filtro_umbral(image, umbral=128):
    pic = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            if pic[i, j] < umbral:
                pic[i, j] = 0
            else:
                pic[i, j] = 255

def border_detection(picture, umbral=128):
    max_values = gradient(picture)
    pseudo_promedio = normalizar(picture, max_values)
    filtro_umbral(picture, umbral=umbral)
    median_filter(picture)
    filtro_umbral(picture, umbral=umbral)

def horizontal_histogram(image, output = 'horizontal.dat'):
    hist = list()
    pic = image.load()
    fl = open(output, 'w')

    for x in range(image.size[0]):
        suma = 0
        for y in range(image.size[1]):
            suma += pic[x, y]
        fl.write(str(x)+' '+str(suma)+'\n')
        hist.append(suma)

    fl.close()
    return hist

def vertical_histogram(image, output = 'vertical.dat'):
    hist = list()
    pic = image.load()
    fl = open(output, 'w')

    for y in range(image.size[1]):
        suma = 0
        for x in range(image.size[0]):
            suma += pic[x, y]
        fl.write(str(y)+' '+str(suma)+'\n')
        hist.append(suma)

    fl.close()
    return hist

def median_filter(image):
    pic = image.load()
    pic_copy = (image.copy()).load()

    for i in range(image.size[0]):
        for j in range(image.size[1]):

            temp = []
            for h in range(i-1, i+2):
                for l in range(j-1, j+2):
                    if h >= 0 and l >= 0 and h < image.size[0] and l < image.size[1]:
                        temp.append(pic_copy[h, l])
            temp.sort()
            pic[i,j] = int(temp[int(len(temp)/2)])
    return pic

def find_local_minimums(histogram):
    cosa = list()
    for i in range(1, len(histogram)-1):
        if histogram[i-1] > histogram[i] and histogram[i+1] > histogram[i]:
            yield i

pat = [[1.6756756756756757, 1.6756756756756757, 1.6756756756756757, 1.6621621621621621, 1.6621621621621621, 1.6486486486486487, 1.6621621621621621, 1.6486486486486487, 1.6486486486486487, 1.6621621621621621, 1.6486486486486487], [1.6756756756756757, 1.6621621621621621, 1.6081081081081081, 1.5, 1.4324324324324325, 1.4324324324324325, 1.5, 1.6081081081081081, 1.6486486486486487, 1.6621621621621621, 1.6486486486486487], [1.6621621621621621, 1.6081081081081081, 1.3918918918918919, 1.0810810810810811, 1.0675675675675675, 1.0945945945945945, 1.4189189189189189, 1.5, 1.6081081081081081, 1.6621621621621621, 1.6486486486486487], [1.6486486486486487, 1.3918918918918919, 1.0810810810810811, 1.027027027027027, 1.0, 1.0405405405405406, 1.0945945945945945, 1.4459459459459461, 1.6486486486486487, 1.6621621621621621, 1.6486486486486487], [1.6486486486486487, 1.2837837837837838, 1.027027027027027, 1.0, 1.0, 1.0, 1.0675675675675675, 1.4459459459459461, 1.6486486486486487, 1.6621621621621621, 1.6486486486486487], [1.6756756756756757, 1.2837837837837838, 1.027027027027027, 1.0135135135135136, 1.0135135135135136, 1.0135135135135136, 1.0675675675675675, 1.5135135135135136, 1.6621621621621621, 1.6621621621621621, 1.6486486486486487], [1.6756756756756757, 1.5945945945945945, 1.2837837837837838, 1.027027027027027, 1.027027027027027, 1.0675675675675675, 1.4594594594594594, 1.6486486486486487, 1.6621621621621621, 1.6621621621621621, 1.6486486486486487], [1.7027027027027026, 1.7027027027027026, 1.5945945945945945, 1.3378378378378379, 1.3378378378378379, 1.4594594594594594, 1.6621621621621621, 1.6621621621621621, 1.6621621621621621, 1.6621621621621621, 1.6486486486486487], [1.7027027027027026, 1.6891891891891893, 1.6891891891891893, 1.6756756756756757, 1.6756756756756757, 1.6756756756756757, 1.6621621621621621, 1.6621621621621621, 1.6621621621621621, 1.6486486486486487, 1.6486486486486487], [1.6891891891891893, 1.6891891891891893, 1.6891891891891893, 1.6891891891891893, 1.6891891891891893, 1.6756756756756757, 1.6756756756756757, 1.6621621621621621, 1.6621621621621621, 1.6621621621621621, 1.6486486486486487], [1.6891891891891893, 1.6891891891891893, 1.6891891891891893, 1.6891891891891893, 1.6891891891891893, 1.6756756756756757, 1.6756756756756757, 1.6621621621621621, 1.6621621621621621, 1.6621621621621621, 1.6486486486486487]]

def nuevo_visitados(size):
    visitados = dict()
    for i in range(size[0]):
        for j in range(size[1]):
            visitados[i,j] = False
    return visitados

def mean(values):
    suma = 0.0
    for i in values:
        suma += i
    return suma / len(values)

def dfs(image, inicio, color, border_color):
    visitados = nuevo_visitados(image.size)
    pic = image.load()
    siguientes = list()
    size = 0
    siguientes.append(inicio)
    reference_color = (mean(pic[tuple(inicio)]) / pat[len(pat)/2][len(pat[0])/2])*1.2

    while len(siguientes) > 0:
        actual = siguientes.pop(0)
        pic[tuple(actual)] = tuple(color)
        visitados[tuple(actual)] = True
        size += 1

        for h in range(int(actual[0])-1, int(actual[0])+2):
            for l in range(int(actual[1])-1, int(actual[1])+2):
                if h >= 0 and l >= 0 and h < image.size[0] and l < image.size[1]:
                    if not visitados[h, l]:
                        if reference_color > mean(pic[h,l]):
                            if not [h, l] in siguientes:
                                siguientes.append([h, l])
                        else:
                            visitados[h, l] = True
                            pic[tuple(actual)] = tuple(border_color)
    return size
                            
def compare(pat, finded):
    diff = 0.0
    unit = finded[0][0]/pat[0][0]
    for y in range(len(pat)):
        for x in range(len(pat[0])):
            diff += fabs( (finded[x][y]/unit) - pat[x][y])
    return diff

def random_purple():
    return (randint(200,250), randint(100, 200), randint(100, 200))

def hole_detection(image_name, output="output.png", size=(128, 128)):
    image = Image.open(image_name)
    original_image = image.copy()
    image.thumbnail(size, Image.ANTIALIAS)
    
    image = ImageOps.grayscale(image)
    median_filter(image)

    horizontal_hist = horizontal_histogram(image)
    vertical_hist = vertical_histogram(image)
    
    horizontal = [ y for y in find_local_minimums(horizontal_hist)]
    vertical = [ x for x in find_local_minimums(vertical_hist)] 

    call(['gnuplot', 'hole.plot'])
 
    holes_centers = list()
    threshold = 17.0
    d = 5
    pic = image.load()
    for y in vertical:
        for x in horizontal:
            finded = list()
            for y1 in range(y-d, y+d+1):
                temp = list()
                for x1 in range(x-d, x+d+1):
                    try:
                        temp.append(pic[x1, y1])
                    except:
                        temp.append(float('inf'))
                finded.append(temp)
            if compare(pat, finded) < threshold:
                holes_centers.append((x, y))

    # Detectar bordes
    border_detection(image, umbral = 20)
    # empieza lo de lab
    
    razon = image.size
    image = original_image
    razon = (float(image.size[0])/razon[0], float(image.size[1])/razon[1])
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", 18)
    
    print 'Porcentaje del agujero con respecto a la imagen'
    image_size = image.size[0]*image.size[1]

    r = 2
    for i in range(len(holes_centers)):
        nombre = 'H'+str(i+1)
        x = holes_centers[i][0]*razon[0]
        y = holes_centers[i][1]*razon[1]
        purple = random_purple()
        size = dfs(image, (x, y), purple, (purple[0], purple[1]-70, purple[2]))
        draw.ellipse((x-r, y-r, x+r, y+r), fill=(200, 255, 50))
        draw.text((x, y+(15)), nombre, fill=(0, 255, 0), font=font)
        print '    Agujero: ', nombre, str((float(size)*100)/image_size)+'%' 
    image.save(output)

def main():
    before = time()
    hole_detection(argv[1])
    print "Tiempo de corrida:", (time() - before)

main()
