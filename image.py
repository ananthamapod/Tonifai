########## IMPORTS ###########
from PIL import Image
from io import BytesIO
import base64

########### MAIN #############

def image(phone_num, uristring):
    savefile = phone_num[1:]
    with open('static/images/A'+savefile+'.png', 'w') as img:
        print len(uristring)
        # uristring = "====" + uristring + "==="
        #print uristring
        img.write(uristring.decode(encoding='base64',errors='strict'))

    image = Image.open('static/images/A' + savefile + '.png', 'r')

    data = image.tobytes()

    R = data[::4]

    print R

def scale():
    pass
