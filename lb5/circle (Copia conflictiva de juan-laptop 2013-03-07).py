#!/usr/bin/python
from PIL import Image, ImageDraw, ImageFont
import sys, time, random, math


def gradient(image, mask_type='sobel'):
    indice_mascara = {
        "sobelx":[[-1.0, 0.0, 1.0], [-2.0, 0.0, 2.0], [-1.0, 0.0, 1.0]],
        "sobely":[[1.0, 2.0, 1.0], [0.0, 0.0, 0.0], [-1.0, -2.0, -1.0]],
        "prewittx":[[-1.0, 0.0, 1.0], [-1.0, 0.0, 1.0], [-1.0, 0.0, 1.0]],
        "prewitty":[[1.0, 1.0, 1.0], [0.0, 0.0, 0.0], [-1.0, -1.0, -1.0]]
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
                        pixel = max(pixel)/len(pixel)
                        gx += pixel*kernelx[int(kernel_pos/3)][kernel_pos%3]
                        gy += pixel*kernely[int(kernel_pos/3)][kernel_pos%3]
                        kernel_pos += 1

            gradiente = int(math.sqrt(math.pow(gx, 2) + math.pow(gy, 2)))
            pic[i, j] = tuple([gradiente]*3)
            if gradiente > max_value:
                max_value = gradiente
    return max_value

def normalizar(image, max_value):
    pic = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            (R, G, B) = pic[i,j]
            if max_value > 0:
                R = G = B = int( (float(R)/max_value)*255 )
            else:
                R = G = B = 0
            pic[i,j] = (R, G, B)

def filtro_umbral(image, umbral=128):
    pic = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):

            colors = list(pic[i,j])
            for h in range(len(colors)):
                if colors[h] < umbral:
                    colors[h] = 0
                else:
                    colors[h] = 255
            pic[i,j] = tuple(colors)
    return pic

def border_detection(picture, output="output.png", umbral=125):
    max_values = gradient(picture)
    pseudo_promedio = normalizar(picture, max_values)
    filtro_umbral(picture, umbral=umbral)

class DrawCircle:
    def __init__(self, image):
        self.image = image
        self.pic = image.load()

    def draw(self, center, radio, intensity = 2):
#        for x in range( -radio, +radio+1):
        i = float(-radio-0.2) 
        while i < radio+0.2:
            x = int(i)
            y = int(math.sqrt(math.fabs(radio*radio - i*i)) + 0.5)
            try:
#            if True:
                pixel = max(self.pic[center[0]+x, center[1]+y])
                self.pic[center[0]+x, center[1]+y] = tuple([pixel + intensity]*3)

                pixel = max(self.pic[center[0]+x, center[1]-y])
                self.pic[center[0]+x, center[1]-y] = tuple([pixel + intensity]*3)
            except:
                pass
            if i < -radio+1 or i > radio-1:
                i += 0.1
            else:
                i += 1

def draw_circles(image, imageCircles, radio, intensity = 2):
    pic = image.load()
    dc = DrawCircle(imageCircles)
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            if pic[x, y] == (255, 255, 255):
                dc.draw((x, y), radio, intensity = intensity)

    """
    pic = imageCircles.load()
    values = list()
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            values.append(pic[x, y][0])
    values.sort()
    print values[-5:]
    """
def random_yellow():
    return (255, random.randint(100,255), random.randint(0, 50))

def remover_duplicados(l):
    res = list()
    for i in l:
        cmd = True
        for j in res:
            if math.fabs(i[0]-j[0]) < 5 and math.fabs(i[1]-j[1]) < 5:
                cmd = False
        if cmd:
            res.append(i)
    return res

def find_circle(image):
    pic = image.load()
    circles = list()
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            if pic[x, y] == (255, 255, 255):
                circles.append([x,y])
    return circles

def circle_detection(image_name, output="output.png", size=(128, 128)):
    image = Image.open(image_name)
    image.thumbnail(size, Image.ANTIALIAS)
    border_detection(image, output="output.png", umbral=60)

    diagonal_mini = int(math.sqrt(math.pow(image.size[0], 2) + math.pow(image.size[1], 2)))
    circulos = list()

    for r in range(10, 20):
        imageCircles = Image.new('RGB', image.size, (0,0,0))
        draw_circles(image, imageCircles, r)
        imageCircles.save('circle_'+("%02d"%r)+'_'+output)

        filtro_umbral(imageCircles, umbral=int(r*8.5))
        for i in find_circle(imageCircles):
            circulos.append(tuple(i+[r]))

    circulos = remover_duplicados(circulos)

    size = image.size
    image = Image.open(image_name)
    diagonal = int(math.sqrt(math.pow(image.size[0], 2) + math.pow(image.size[1], 2)))
    razon = (image.size[0]/size[0], image.size[0]/size[0], diagonal/diagonal_mini)
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", 18)
    draw = ImageDraw.Draw(image)

    counter = 1
    for x, y, r in circulos:
        x = int(x*razon[0])
        y = int(y*razon[1])
        r = int(r*razon[2])

        draw.setink(random_yellow())
        for i in range(3):
            r += 1
            draw.ellipse((x-r, y-r, x+r, y+r))
        draw.ellipse((x-2, y-2, x+2, y+2), fill=(0, 255, 0))
        draw.text((x+5, y), ('C'+str(counter)), fill=(0, 255, 0), font=font)
        print ('C'+str(counter))+',', 'Radio(pixeles):', str(r)+',', 'porcentaje de diagonal:', str((r*2*100)/diagonal)+'%'
        counter += 1

    image.save(output)


def main():
    before = time.time()
    circle_detection(sys.argv[1])
    print "Tiempo de corrida:", (time.time() - before)

main()
