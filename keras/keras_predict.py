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


model = load_model('D:\Project\keras_model.h5')  

# hdf5_path = 'D:\Project\dataset.hdf5'
# hdf5_file = h5py.File(hdf5_path, "r")

# X_train_orig = np.array(hdf5_file["train_img"][:])
# Y_train_orig = np.array(hdf5_file["train_labels"][:])
# Y_train_orig = Y_train_orig[:, np.newaxis]
# print (Y_train_orig[0 : 9])

# X_test_orig = np.array(hdf5_file["test_img"][:])
# Y_test_orig = np.array(hdf5_file["test_labels"][:])
# Y_test_orig = Y_test_orig[:, np.newaxis]
# # print (Y_test_orig.shape)

# print (X_train_orig.shape)
# print (Y_train_orig.shape)
# print (X_test_orig.shape)
# print (Y_test_orig.shape)
# # X_train_orig, Y_train_orig, X_test_orig, Y_test_orig, classes = load_dataset()


# X_train = X_train_orig/255.
# X_test = X_test_orig/255.
# Y_train = convert_to_one_hot(Y_train_orig, 2).T
# Y_test = convert_to_one_hot(Y_test_orig, 2).T

# preds = model.evaluate(X_test, Y_test)
# print ("Loss = " + str(preds[0]))
# print ("Test Accuracy = " + str(preds[1]))

img_path = "D:\Project\\test\\sit.jpg"
print (img_path)

img = image.load_img(img_path, target_size=(64, 64))
plt.imshow(img)
pylab.show()



x = image.img_to_array(img)
print ("x shape: ", x.shape)

x = np.expand_dims(x, axis=0)
x = preprocess_input(x)
print('Input image shape:', x.shape)
# print ("X: ", x)
my_image = scipy.misc.imread(img_path)
imshow(my_image)

label = model.predict(x)
# print("result: ", model.predict(x))
print ("[0. 1.]")