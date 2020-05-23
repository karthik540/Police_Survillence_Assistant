from flask import Flask, render_template, request , jsonify
#from modules.DialogFlowConnect import botResponseReciever
from modules.watsonConnect import botResponseReciever
from modules.FriendRecognition.face_recog import FaceRecog
from modules.CrowdDetection import scene_detect
from modules.FriendRecognition.LocationLogs.logConvert import suspectSerialize
from google.cloud import vision

import threading , cv2 , requests , time , os
import cv2, time, pandas 
from datetime import datetime 
from time import sleep,time
import time
import math
from datetime import datetime

from googletrans import Translator

translator = Translator()


face = FaceRecog()
app = Flask(__name__)

###     Buffer Variables...

location_buffer = "Nothing"
stop_threads = False
module_buffer = "Nothing"

ip_addr = "192.168.1.13"

victimFound = False
data_buffer = ""
location_buffer = ""
isCrowd = False
special_buffer = False
wait_flag = False

cam1_addr = "192.168.1.11"
cam2_addr = "192.168.1.3"

location1 = "Egmore"
location2 = "Tambaram"

def updateSuspectLogs(name , location):
    fileObj = open("./modules/FriendRecognition/LocationLogs/"+name+".txt" , "a+")
    localtime = time.asctime( time.localtime(time.time()) )
    fileObj.write("Location= "+ location + "-Timestamp= " + localtime + "\n")
    fileObj.close()

def webcamCap(stop):
    global location_buffer
    global data_buffer
    global victimFound , isCrowd
    global module_buffer
    global stop_threads
    global wait_flag
    global location1
    global location2

    counter = 0

    frame = cv2.imread("./Assets/botImage.png")

    if module_buffer == "Nothing":
        print("[STATUS] Welcome to PSA !")
        
        
        while(True):
            #print('[STATUS] stop_var = ' + str(stop_threads))
            cv2.imshow("Welcome to Police Survillance Assistant - (PSA)" , frame)
            if stop_threads:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    elif module_buffer == "Surveillance":
        print("[STATUS] Survillence Mode Activated !")
        victimFound = False
        try:
            cap1 = cv2.VideoCapture("http://"+ cam1_addr +":4747/mjpegfeed")
        except:
            pass
        """
        try:
            cap2 = cv2.VideoCapture("http://"+ cam2_addr +":4747/mjpegfeed")
        except:
            pass
        """
        counter = 0
        while(True):

            try:
                ret1 , frame1 = cap1.read()
                frame1 = frame1[50: , 50:]
                cv2.imshow('Location :  ' + location1 , frame1)
            except:
                pass
            
            """
            try:
                ret2 , frame2 = cap2.read()
                frame2 = frame2[50: , 50:]
                cv2.imshow('Location :  ' + location2 , frame2)
            except:
                pass
            """



            #   Face Condition...
            if counter == 60:
                counter = 0
                name = face.render_frame(frame1)
                if(name != "No faces"):
                    name = name.split(" ")[0]
                    data_buffer = name
                    location_buffer = location1
                    if name != "":
                        updateSuspectLogs(name , location_buffer)
                        victimFound = True
                        print("[ALERT] suspect found at "+location1+": " + name)
                    


            """
            if counter == 30:
                name = face.render_frame(frame2)
                if(name != "No faces"):
                    name = name.split(" ")[0]
                    data_buffer = name
                    location_buffer = location2
                    if name != "":
                        updateSuspectLogs(name , location_buffer)
                        victimFound = True
                        print("[ALERT] suspect found at "+location2+": " + name)
            """
            counter = counter + 1
            

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if stop():
                break
        try:
            cap1.release()
        except:
            pass
        """
        try:
            cap2.release()
        except:
            pass
        """
        cv2.destroyAllWindows()
    
    elif module_buffer == "Lockdown":
        print("[STATUS] Lockdown Mode Activated !")
        victimFound = False
        try:
            cap1 = cv2.VideoCapture("http://"+ cam1_addr +":4747/mjpegfeed")
        except:
            pass
        
        try:
            cap2 = cv2.VideoCapture("http://"+ cam2_addr +":4747/mjpegfeed")
        except:
            pass
        
        counter = 0
        while(True):

            try:
                ret3 , frame3 = cap1.read()
                frame3 = frame3[50: , 50:]
                cv2.imshow('Location :  ' + location1 , frame3)
            except:
                pass
        
            
            try:
                ret4 , frame4 = cap2.read()
                frame4 = frame4[50: , 50:]
                cv2.imshow('Location :  ' + location2 , frame4)
            except:
                pass
            


            #   Face Condition...
            if counter == 100:
                counter = 0
                    
                image = frame3
                success, encoded_image = cv2.imencode('.jpg', image)
                content  = encoded_image.tobytes()
                
                isCrowd = scene_detect(content)

                if(isCrowd == 1):
                    location_buffer = location1
                    victimFound = True
                    print("[ALERT] Crowd detected at "+location1)


            
            if counter == 30:
                image = frame4
                success, encoded_image = cv2.imencode('.jpg', image)
                content  = encoded_image.tobytes()
                
                isCrowd = scene_detect(content)

                if(isCrowd == 1):
                    location_buffer = location1
                    victimFound = True
                    print("[ALERT] Crowd detected at "+location1)
            
            counter = counter + 1
            

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if stop():
                break
        try:
            cap1.release()
        except:
            pass
        
        try:
            cap2.release()
        except:
            pass
        
        cv2.destroyAllWindows()

    elif module_buffer == "Scene":
        print("[STATUS] DATA BUFFER = " + data_buffer)
        if data_buffer == location1:
            cap1 = cv2.VideoCapture("http://"+ cam1_addr +":4747/mjpegfeed")
        
        elif data_buffer  == location2:
            cap1 = cv2.VideoCapture("http://"+ cam2_addr +":4747/mjpegfeed")
        
        ret , frame = cap1.read()
        frame = frame[50: , 50:]


        credential_path = "./modules/FriendRecognition/collagepro-e87be00445b2.json"
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
        client = vision.ImageAnnotatorClient()

        image = frame
        success, encoded_image = cv2.imencode('.jpg', image)
        content  = encoded_image.tobytes()

        image = vision.types.Image(content=content)

        response = client.web_detection(image=image)
        annotations = response.web_detection

        if annotations.best_guess_labels:
            for label in annotations.best_guess_labels:
                #print('\nBest guess label: {}'.format(label.label))
                b_guess = label.label

        if annotations.pages_with_matching_images:
            print('\n{} Pages with matching images found:'.format(
                len(annotations.pages_with_matching_images)))

            for page in annotations.pages_with_matching_images:
                print('\n\tPage url   : {}'.format(page.url))

                if page.full_matching_images:
                    print('\t{} Full Matches found: '.format(
                        len(page.full_matching_images)))

                    for image in page.full_matching_images:
                        print('\t\tImage url  : {}'.format(image.url))

                if page.partial_matching_images:
                    print('\t{} Partial Matches found: '.format(
                        len(page.partial_matching_images)))

                    for image in page.partial_matching_images:
                        print('\t\tImage url  : {}'.format(image.url))

        if annotations.web_entities:
            # print('\n{} Web entities found: '.format(
            #     len(annotations.web_entities)))

            for entity in annotations.web_entities:
                #print('\n\tScore      : {}'.format(entity.score))
                data_buffer = "I think this is either a " + entity.description + " or " + b_guess
                break
        wait_flag = False
        print(data_buffer)
    
    elif module_buffer == "Track":
        temp = suspectSerialize(data_buffer)
        data_buffer = str(temp)
        print(data_buffer)
        
        wait_flag = False
    

    try:
        cap1.release()
    except:
        pass
    try:
        cap2.release()
    except:
        pass
    cv2.destroyAllWindows()

def bot_Event_Handler(message , intent):
    global location_buffer
    global module_buffer
    global data_buffer

    if intent == "Launch":
        return requests.post('http://'+ip_addr + ':5000/start')
    elif intent == "Sleep":
        return requests.post('http://'+ip_addr + ':5000/stop')
    elif intent == "Surveillance":
        """
        requests.post('http://'+ip_addr + ':5000/stop')
        module_buffer = "Surveillance"
        print('[STATUS] stop_var = ' + str(stop_threads))
        requests.post('http://'+ip_addr + ':5000/start')
        """
        return requests.post('http://'+ip_addr + ':5000/survey')
    elif intent == "Lockdown":
        return requests.post('http://'+ip_addr + ':5000/lockdown')
    elif intent == "Scene":
        data_buffer = message.replace("Okay analyzing " , "")
        return requests.post('http://'+ip_addr + ':5000/scene')
    elif intent == "Track":
        data_buffer = message.replace("Tracking " , "")
        return requests.post('http://'+ip_addr + ':5000/track')
    return jsonify({'flag': True})  

@app.route('/start' , methods = ['POST' , 'GET'])
def startRender():
    global stop_threads
    if not stop_threads:
        print('[STATUS] Thread Initiating.')
        webcam_thread = threading.Thread(target = webcamCap, args =(lambda : stop_threads, )) 
        webcam_thread.start()
    print('[STATUS] Thread running...')
    return jsonify({'flag' : True})

@app.route('/stop' , methods = ['POST' , 'GET'])
def stopRender():
    global stop_threads
    global module_buffer

    stop_threads = True
    time.sleep(0.3)
    #module_buffer = "Nothing"
    cv2.destroyAllWindows()
    stop_threads = False
    print('[STATUS] stop_var = ' + str(stop_threads))
    print('[STATUS] Thread stops...')
    return jsonify({'flag' : True})

@app.route('/survey' , methods = ['POST' , 'GET'])
def surveyMode():
    global stop_threads
    global module_buffer
    global victimFound
    global data_buffer
    global isCrowd
    global location_buffer

    requests.post('http://'+ip_addr + ':5000/stop')
    time.sleep(0.3)
    victimFound = False
    isCrowd = False
    module_buffer = "Surveillance"
    if not stop_threads:
        print('[STATUS] Thread Initiating.')
        webcam_thread = threading.Thread(target = webcamCap, args =(lambda : stop_threads, )) 
        webcam_thread.start()
        while(not victimFound):
            continue
        print("comes out of lockdown !{}".format(data_buffer)) 
        return jsonify({ 'flag' : False, 'message': "Corona Suspect " + data_buffer +" found at "+ location_buffer }) 
    print('[STATUS] Thread running...')
    return jsonify({'flag': True})

@app.route('/lockdown' , methods = ['POST' , 'GET'])
def lockdownMode():
    global stop_threads
    global module_buffer
    global victimFound
    global data_buffer
    global isCrowd
    global location_buffer

    requests.post('http://'+ip_addr + ':5000/stop')
    time.sleep(0.3)
    victimFound = False
    isCrowd = False
    module_buffer = "Lockdown"
    if not stop_threads:
        print('[STATUS] Thread Initiating.')
        webcam_thread = threading.Thread(target = webcamCap, args =(lambda : stop_threads, )) 
        webcam_thread.start()
        while(not victimFound):
            continue
        print("comes out of face !{}".format(data_buffer))

        return jsonify({ 'flag' : False, 'message': "Crowd Detected at "+ location_buffer })
    print('[STATUS] Thread running...')
    return jsonify({'flag': True})

@app.route('/scene' , methods = ['POST' , 'GET'])
def sceneDetection():
    global module_buffer
    global special_buffer
    global wait_flag

    requests.post('http://'+ip_addr + ':5000/stop')
    time.sleep(0.3)
    special_buffer = True
    wait_flag = True
    module_buffer = "Scene"
    requests.post('http://'+ip_addr + ':5000/start')
    
    return jsonify({'flag': True})

@app.route('/track' , methods = ['POST' , 'GET'])
def trackSuspect():
    global module_buffer
    global special_buffer
    global wait_flag

    requests.post('http://'+ip_addr + ':5000/stop')
    time.sleep(0.3)
    special_buffer = True
    wait_flag = True
    module_buffer = "Track"
    requests.post('http://'+ip_addr + ':5000/start')
    
    return jsonify({'flag': True})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/botResponse' , methods = ['POST' , 'GET'])
def botResponse():
    global special_buffer
    global wait_flag
    userInput = request.form['utext']
    print(userInput)

    #newText = translator.translate(userInput ,dest='en' , src = 'auto')

    #print(newText.text)
    #userInput = request.form.get('utext')
    #print(userInput)
    
    #botMessage = botResponseReciever(newText.text)
    botMessage = botResponseReciever(userInput)

    handler_data = bot_Event_Handler(botMessage[0] , botMessage[1])
    #print(handler_data)
    try:
        if special_buffer == True:
            while(wait_flag == True and special_buffer == True):
                continue
            print("Comes this way too !" + data_buffer)
            #   print("buffer : " + special_buffer)
            special_buffer = False
            return jsonify({'response': data_buffer , 'class' : botMessage[1]})
        handler_data = handler_data.json()
        if not handler_data['flag']:
            print("comes handler")
            return jsonify({'response': handler_data['message'] , 'class' : botMessage[1]})
    except:
        pass

    

    

    #errorMessage = json.loads(request.data.decode("utf-8"))["utext"]
    #errorMessage = errorMessage.replace("'", "")
    #print(errorMessage)
    #return solution_finder(errorMessage)


    #newText = translator.translate(userInput ,dest='en' , src = 'auto')
    return  jsonify({'response': botMessage[0] , 'class' : botMessage[1]})
    
    
if __name__ == "__main__":
    app.run(debug = True , host= "0.0.0.0" , port= 5000)