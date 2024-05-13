import time
import cv2
from flask import sessions
import numpy as np
from database import *
from admin import*
import keras.backend as K
import os
import winsound
import time




# Load Yolo 
# Load Yolo
def detect():
        
   
    net = cv2.dnn.readNet("yolov3_training_2000 (1).weights", "yolov3_testing.cfg")
    # net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")


    

    classes = ["weapon"]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[int(i[0]) - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))



   
    def value():
        val = input("Enter file name or press enter to start webcam : ")
        if val == "":
            val = 0
        return val



   
    cap = cv2.VideoCapture(0)

    frame_counter = 0  # Counter for naming each frame uniquely
    save_interval = 30  # Save one frame every 5 minutes (300 seconds)
    last_save_time = time.time()
    
    # val = cv2.VideoCapture()
    while True:    
        _, img = cap.read()
        height, width, channels = img.shape
        # width = 512
        # height = 512

        # Detecting objects
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)
        outs = net.forward(output_layers)

        # Showing information on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        print(indexes)
        if indexes == 0: print("weapon detected in frame")
        font = cv2.FONT_HERSHEY_PLAIN
        # for i in range(len(boxes)):
        #     if i in indexes:
        #         x, y, w, h = boxes[i]
        #         label = str(classes[class_ids[i]])
        #         color = colors[class_ids[i]]
        #         cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        #         cv2.putText(img, label, (x, y + 30), font, 3, color, 3)
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = f"{classes[class_ids[i]]}: {confidences[i]:.2f}"  # Add confidence score to the label
                color = colors[class_ids[i]]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y + 30), font, 3, color, 3)
            
            print(time.time(),"tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt")
            print(last_save_time,"last____________________________________________________")
            print(save_interval,"intervelllllllllllllllllllllllllllllllll")
            print("time.time() - last_save_time : ",time.time() - last_save_time)
            # if time.time() - last_save_time >= save_interval:
            
            # Define the frequency and duration for the beep
            
            frequency = 1000  # Hz
            duration = 1000  # milliseconds

            # Play the beep
            winsound.Beep(frequency, duration)

            # Wait for a while
            time.sleep(1)
            print("helooo world")
            static_folder = 'static/detect'
            frame_name = f'{int(time.time())}.jpg'
            frame_path = os.path.join(static_folder, frame_name)
            path="static/detect/"+frame_name
            cv2.imwrite(frame_path, img)

            print("Frame Path: ", frame_path)

            q = "insert into detect values(null,'%s','weapon detected',NOW(),'0','0','pending')"%(path) 
            # q = "INSERT INTO detect VALUES (NULL, '%s', 'weapon detected', NOW(), 'pending')" % (path)

            # q = "insert into detect values(null,'%s','weapon detected',curdate(), curtime(),'0','0','pending')" % (path)

            inserts(q)

            frame_counter += 1
            last_save_time = time.time()
                

        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    
    K.clear_session()

    
