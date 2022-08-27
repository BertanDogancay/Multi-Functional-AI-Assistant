from threading import Thread
import cv2
import time
import os
import tensorflow as tf
import numpy as np
from tensorflow.python.keras.utils.data_utils import get_file
from cv2 import threshold

def object_detection():

    modelURL = "http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_resnet50_v1_fpn_640x640_coco17_tpu-8.tar.gz"
    classFilePath = ""
    filePath = ""
    videoPath = 0
    threshold = 0.5

    np.random.seed(20)

    with open(classFilePath, 'r') as f:
        classesList = f.read().splitlines()
        
    colorList = np.random.uniform(low=0, high=255, size=(len(classesList), 3))
    print(len(classesList), len(colorList))

    fileName = os.path.basename(modelURL)
    modelName = fileName[:fileName.index('.')]

    cacheDir = ""
    os.makedirs(cacheDir, exist_ok=True)

    get_file(fname=fileName, origin=modelURL, cache_dir=cacheDir, cache_subdir="checkpoints", extract=True)
    
    print("Loading Model " +modelName)
    tf.keras.backend.clear_session()
    model = tf.saved_model.load(os.path.join(cacheDir, "checkpoints", modelName, "saved_model"))
    print("Model " +modelName +" loaded successfully...")

    cap = cv2.VideoCapture(videoPath)
        
    (success, image) = cap.read()
    startTime = 0

    while True:
        currentTime = time.time()
        fps = 1/(currentTime - startTime)
        startTime = currentTime

        inputTensor = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2RGB)
        inputTensor = tf.convert_to_tensor(inputTensor, dtype=tf.uint8)
        inputTensor = inputTensor[tf.newaxis,...]

        detections = model(inputTensor)

        bboxs = detections['detection_boxes'][0].numpy()
        classIndexes = detections['detection_classes'][0].numpy().astype(np.int32)
        classScores = detections['detection_scores'][0].numpy()

        imH, imW, imC = image.shape

        bboxIdx = tf.image.non_max_suppression(bboxs, classScores, max_output_size=50, iou_threshold=threshold, score_threshold=threshold)
        boxNameArray = []

        if len(bboxIdx) != 0:
            for i in bboxIdx:
                bbox = tuple(bboxs[i].tolist())
                classConfidance = round(100*classScores[i])
                classIndex = classIndexes[i]
                classLabelText = classesList[classIndex].upper()

                boxNameArray.append(classLabelText)

                # with open(filePath, 'r') as f:
                #     nameInList = f.read().splitlines

                with open(filePath, 'w') as f:
                    for i in boxNameArray:
                        f.writelines(f'{i}\n')

                classColor = colorList[classIndex]
                displayText = '{}: {}%'.format(classLabelText, classConfidance)

                ymin, xmin, ymax, xmax = bbox
                xmin, xmax, ymin, ymax = (xmin*imW, xmax*imW, ymin*imH, ymax*imH)
                xmin, xmax, ymin, ymax = int(xmin), int(xmax), int(ymin), int(ymax)

                cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color=classColor, thickness=1)
                cv2.putText(image, displayText, (xmin, ymin-10), cv2.FONT_HERSHEY_PLAIN, 1, classColor, 2)

                lineWidth = min(int((xmax-xmin) *0.2), int((ymax-ymin) *0.2))
                
                cv2.line(image, (xmin, ymin), (xmin+lineWidth, ymin), classColor, thickness=5)
                cv2.line(image, (xmin, ymin), (xmin, ymin+lineWidth), classColor, thickness=5)

                cv2.line(image, (xmax, ymin), (xmax-lineWidth, ymin), classColor, thickness=5)
                cv2.line(image, (xmax, ymin), (xmax, ymin+lineWidth), classColor, thickness=5)

                cv2.line(image, (xmin, ymax), (xmin+lineWidth, ymax), classColor, thickness=5)
                cv2.line(image, (xmin, ymax), (xmin, ymax-lineWidth), classColor, thickness=5)

                cv2.line(image, (xmax, ymax), (xmax-lineWidth, ymax), classColor, thickness=5)
                cv2.line(image, (xmax, ymax), (xmax, ymax-lineWidth), classColor, thickness=5)

        cv2.putText(image, "FPS: " +str(int(fps)), (20,70), cv2.FONT_HERSHEY_PLAIN, 2, (0.255,0), 2)
        cv2.imshow("Webcam", image)

        key = cv2.waitKey(1) 
        if key == 27:
            break

        (success,image) = cap.read()
    cv2.destroyAllWindows()

# if __name__ == "__main__":
#     object_detection()