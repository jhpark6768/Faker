import tensorflow as tf
from PIL import Image
import numpy as np
from project import settings
import os

#pip install tensorflow
#pip install pillow
#pip install numpy



def predmain(imagefile):
    ## 고정값
    ## path 어케 해야대지...?
    # root 값 찾아와야대나?
    
    ## yolo5vs.pt 
    ## best.pt
    modelpath = 'C:\\Users\\82107\\Desktop\\python\\python_workspace2\\project\\predict\\model\\cats_and_dogs_small_1.h5'

    model = tf.keras.models.load_model(modelpath)

    imgpath = 'C:\\Users\\82107\\Desktop\\python\\python_workspace2\\project\\media\\' + imagefile
    print(imgpath)
    
    img = Image.open(imgpath)
    img = img.convert("RGB")
    img = img.resize((150, 150))

    data = np.asarray(img)
    data_reshape = data.reshape((1,) + data.shape)

    result = model.predict(data_reshape)

    if result == 1:
        return 1
    else :
        return 0

  

