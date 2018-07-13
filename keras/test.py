import math
import numpy as np
import h5py
import matplotlib.pyplot as plt
import scipy
from PIL import Image
from scipy import ndimage
import tensorflow as tf
from tensorflow.python.framework import ops
from cnn_utils import *
from model import *
import cv2
from scipy.misc import imread
from keras.preprocessing import image

import numpy as np
from keras import layers
from keras.layers import Input, Add, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D, AveragePooling2D, MaxPooling2D, GlobalMaxPooling2D
from keras.models import Model, load_model
from keras.preprocessing import image
from keras.utils import layer_utils
from keras.utils.data_utils import get_file
from keras.applications.imagenet_utils import preprocess_input
import pydot
from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot
from keras.utils import plot_model
from resnets_utils import *
from keras.initializers import glorot_uniform
import scipy.misc
from matplotlib.pyplot import imshow
import matplotlib.pyplot as plt
import pylab


import keras.backend as K


imagePath = 'D:\Project\\test\\msleep.jpg'

# img = imread("123.jpg")
# img = img[:, :,:,np.newaxis]
# print('Input image shape:', img.shape)
# newimg = img.flatten()
# newimg = newimg[:, np.newaxis]
# newimg = newimg[:, np.newaxis]
# newimg.reshape((64,64,3,1))

img = image.load_img(imagePath, target_size=(64, 64))
plt.imshow(img)
pylab.show()

x = image.img_to_array(img)
print ("x shape: ", x.shape)

x = np.expand_dims(x, axis=0)
x = preprocess_input(x)
print('Input image shape:', x.shape)
# print ("X: ", x)
# my_image = scipy.misc.imread(img_path)
# imshow(my_image)


_, _, parameters = model(X_train, Y_train, X_test, Y_test)

res = forward_propagation(img, parameters)

print (res)



# my_image = scipy.misc.imread(img_path)
# imshow(my_image)
# print("class prediction vector [p(0), p(1), p(2), p(3), p(4), p(5)] = ")
# print(model.predict(x))