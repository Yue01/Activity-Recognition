# A lambda function to interact with AWS RDS MySQL
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql
import sys
from time import gmtime, strftime
import time
import random

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


import paho.mqtt.client as mqtt #import the client1

import keras.backend as K

# RDS parameters
REGION = 'us-east-2'
rds_host  = "project.cjnbbwqwx2xa.us-east-2.rds.amazonaws.com"
name = "project"
password = "123456789"
db_name = "projectdata"
conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)


def fetch_result():
    # collect data from database about two lights
    # Time interval : 1 day +- 5 minutes
    result = []
    light1 = []
    light2 = []

    with conn.cursor() as cur1:
        #cur1.execute("""select * from projectdata.input_data WHERE time < NOW() - INTERVAL 5 MINUTE """)
        cur1.execute("""select * from projectdata.input_data WHERE category = '/test/light1' AND time < NOW() - INTERVAL 1 DAY """)
        conn.commit()
        cur1.close()
        for row in cur1:
            light1.append(list(row))
    result.append(light1)
    print (light1)

    with conn.cursor() as cur2:
        #cur1.execute("""select * from projectdata.input_data WHERE time < NOW() - INTERVAL 5 MINUTE """)
        cur2.execute("""select * from projectdata.input_data WHERE '/test/light2' AND time < NOW() - INTERVAL 1 DAY """)
        conn.commit()
        cur2.close()
        for row in cur2:
            light2.append(list(row))
    result.append(light2)
    print (light2)

    return result


def insert_result(acticity,category,distance,pattern,time_now):
    with conn.cursor() as cur:
        act = acticity
        cat = category
        dis = distance
        pat = pattern
        tim = time_now
        # cur.execute("insert into projectdata.actdata (act, cat, dis, pat, time) values (%s,%s,%s,%s,%s)")
        cur.execute("insert into projectdata.actdata (act, cat, dis, pat, time) values ( %s , %s , %s , %s , %s)",(act,cat,dis,pat,tim))
        conn.commit()
        cur.close()


def read_history():
    history_list=[]
    with conn.cursor() as cur3:
        #cur3.execute("""select * from  projectdata.actdata WHERE time < NOW() - INTERVAL 1 DAY + INTERVAL 5 MINUTE AND time > NOW() - INTERVAL 1 DAY - INTERVAL 5 MINUTE """)
        cur3.execute("""select * from projectdata.actdata""")
        conn.commit()
        cur3.close()
        for row in cur3:
            history_list.append(list(row))
    return history_list

def iot_program():
    while True:
        # record the start of the program
        # The time will be 30s. Eg : 0.00 starts, 0.15 stop, then wait until 0.30 for the next ex
        start_time = time.time()
        """  1. recognition part
        The machine learning recognition will be added here.
        Here randomly generate a 0/1 just for testing the process!
       """
        # predict = random.randint(0,1)
        img_path = "D:\Project\\test\\sit.jpg"
        # print (img_path)

        img = image.load_img(img_path, target_size=(64, 64))
        # plt.imshow(img)
        # pylab.show()

        x = image.img_to_array(img)
        print ("x shape: ", x.shape)

        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        print('Input image shape:', x.shape)
        # print ("X: ", x)
        # my_image = scipy.misc.imread(img_path)
        # imshow(my_image)

        label = model.predict(x)
        # print (label[0][0])
        # print (type(label[0][0]))

        if label[0][0] == 1.0:
            predict = 0
        elif label[0][1] == 1.0:
            predict = 1
        predict = 0
        # print("result: ", model.predict(x))


        """2. store the data
        This part is used for store the data
        """
        # fetch resout from the databases
        light_res= fetch_result()
        # add the image processing result to each light
        # esp information + image recognition information -> database
        for i in range(0,len(light_res)):
            light = light_res[i]
            for i in range(len(light)):
                acticity = predict
                category = light[i][0]
                distance = light[i][1]
                pattern  = light[i][2]
                tim      = light[i][3]
                # print " What user is doing: ", acticity,
                # print " Where does the message come from: ", category,
                # print " Its distance, ", distance,
                # print " pattern, " , pattern
                # print " time, ", time
                #insert_result(acticity,category,distance,pattern,tim)


        """ 3. predict with user history
        This is for making decision with user history
        """
        light_1 = [0,0,0,0]
        light_2   = [0,0,0,0]
        topic_1 = 0
        max_1 = 0
        topic_2 = 0
        max_2 = 0
        history_list = read_history()
        # print (history_list
        for i in range(len(history_list)):
            do = int(history_list[i][0])
            place = str(history_list[i][1])
            light_intensity = int(history_list[i][3])
            # 0 for sleeping and 1 for working/sitting
            # select from previous result which matches the activity at present
            if(do == predict):
                if(place == "/test/light1"):
                    light_1[light_intensity]+=1
                elif(place=="/test/light1"):
                    light_2[light_intensity]+=1
        print (light_1)
        print (light_2)
        # now we have: (just for eg)
        # light_1 : [88, 23, 4, 2 ]
        # light_2 : [234,5,6,7]
        for i in range(len(light_1)):
            if(light_1[i]>max_1):
                max_1= light_1[i]
                topic_1=i
        for i in range(len(light_2)):
            if(light_2[i]>max_2):
                max_2 = light_2[i]
                topic_2= i
        # now we have all of the things!  topic_1 and 2 are the light control signal in (0~3)
        # eg: topic_1 : 2           topic_2: 3
        # then the light 1 should have 2 lights up , and light 2 should have 3 lights up


        """4.Send the feedback to mqtt server!
        """

        broker_address="192.168.0.19" 
        client = mqtt.Client("P1") #create new instance
        client.connect(broker_address) #connect to broker

        print ("topic_1", topic_1)
        print ("topic_2", topic_2)

        client.publish("/test/light1_feedback",topic_1)#publish
        client.publish("/test/light2_feedback",topic_2)#publish

        """5. Keep waiting until next loop
        Considering the actual processing speed: 30 second is reasonable
        """
        while(time.time()-start_time)<30:
            # print ("wait for next start!")
            pass

    conn.close()



model = load_model('D:\Project\keras_model.h5')  

iot_program()



