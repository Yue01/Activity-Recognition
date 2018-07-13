import h5py
import numpy as np
from random import shuffle
from math import ceil
import matplotlib.pyplot as plt

batch_size = 100
hdf5_path = 'D:\Project\dataset.hdf5'

# open the hdf5 file
hdf5_file = h5py.File(hdf5_path, "r")

# Total number of samples
train_set_x_orig = np.array(hdf5_file["train_img"][:])
train_set_y_orig = np.array(hdf5_file["train_labels"][:])

test_set_x_orig = np.array(hdf5_file["test_img"][:])
test_set_y_orig = np.array(hdf5_file["test_img"][:])

print (train_set_x_orig.shape)
print (test_set_y_orig.shape)
# print (test_data)

data_num = hdf5_file["test_img"].shape[0]

batches_list = list(range(int(ceil(float(data_num) / batch_size))))
shuffle(batches_list)
# loop over batches
for n, i in enumerate(batches_list):
    i_s = i * batch_size  # index of the first image in this batch
    i_e = min([(i + 1) * batch_size, data_num])  # index of the last image in this batch
    # read batch images and remove training mean
    images = hdf5_file["test_img"][i_s:i_e, ...]
    # if subtract_mean:
    #     images = images - mm
    # read labels and convert to one hot encoding
    labels = hdf5_file["test_labels"][i_s:i_e]
    labels_one_hot = np.zeros((batch_size, 2))
    labels_one_hot[np.arange(batch_size), labels] = 1
    print (n+1, '/', len(batches_list))
    print (labels[0], labels_one_hot[0, :])
    plt.imshow(images[0])
    plt.show()
    if n == 10:  # break after 5 batches
        break
hdf5_file.close()