#!/usr/bin/python
from PIL import Image
import sys, time

def filtros(picture):
    
    image = Image.open(picture)
    total_pixel = image.size[0]*image.size[1]
    pic = image.load()
    image_name = ".png"#(time.ctime().replace(" ", "_"))+".png"

    # Obtener escala de grises 8bits de RGB 32 bits
    for i in range(image.size[0]):
        for j in range(image.size[1]):

            (R, G, B) = pic[i,j]
            # Grayscale
            intensity = int((R+G+B)/3)
            R = G = B = intensity
            pic[i,j] = (R, G, B)

    image.save("grayscale_"+image_name,"PNG")

    # Umbral filtro
    for i in range(image.size[0]):
        for j in range(image.size[1]):

            (R, G, B) = pic[i,j]
            # Grayscale
            intensity = R
            if intensity < 128:
                intensity = 0
            else:
                intensity = 255
            R = G = B = intensity
            pic[i,j] = (R, G, B)

    image.save("umbral_"+image_name,"PNG")

    # Median Filter
    for i in range(image.size[0]):
        for j in range(image.size[1]):

            temp = []
            for h in range(i-1, i+2):
                for l in range(j-1, j+2):
                    if h >= 0 and l >= 0 and h < image.size[0] and l < image.size[1]:
                        temp.append(pic[i, j][0])

            temp.sort()
            R = G = B = int(temp[int(len(temp)/2)])
            pic[i,j] = (R, G, B)

    image.save("median_filter_"+image_name,"PNG")


def main():
    filtros(sys.argv[1])

main()
