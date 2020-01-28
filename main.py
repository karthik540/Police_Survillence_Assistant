from flask import Flask, render_template, request , jsonify
from modules.DialogFlowConnect import botResponseReciever
from modules.FriendRecognition.face_recog import FaceRecog
import threading , cv2 , requests , time

face = FaceRecog()
app = Flask(__name__)

###     Buffer Variables...

location_buffer = "Nothing"
stop_threads = False
module_buffer = "Nothing"
ip_addr = "192.168.1.4"
victimFound = False
data_buffer = ""
location_buffer = ""

cam1_addr = "192.168.1.5"
cam2_addr = "192.168.1.3"


def webcamCap(stop):
    global location_buffer
    global data_buffer
    global victimFound
    global module_buffer
    global stop_threads
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
        try:
            cap2 = cv2.VideoCapture("http://"+ cam2_addr +":4747/mjpegfeed")
        except:
            pass

        while(True):

            try:
                ret1 , frame1 = cap1.read()
                frame1 = frame1[50: , 50:]
                cv2.imshow('Location :  Chennai' , frame1)
            except:
                pass
            
            try:
                ret2 , frame2 = cap2.read()
                frame2 = frame2[50: , 50:]
                cv2.imshow('Location :  Delhi' , frame2)
            except:
                pass
            



            #   Face Condition...
            if counter >= 60:
                counter = 0
                name = face.render_frame(frame1)
                if(name != "No faces"):
                    name = name.split(" ")[0]
                    data_buffer = name
                    location_buffer = "Chennai"
                    if name != "":
                        victimFound = True
                        print("[ALERT] suspect found at Chennai: " + name)
            if counter == 30:
                name = face.render_frame(frame2)
                if(name != "No faces"):
                    name = name.split(" ")[0]
                    data_buffer = name
                    location_buffer = "Delhi"
                    if name != "":
                        victimFound = True
                        print("[ALERT] suspect found at Delhi: " + name)
            
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

def bot_Event_Handler(message , intent):
    global location_buffer
    global module_buffer
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
    global location_buffer

    requests.post('http://'+ip_addr + ':5000/stop')
    time.sleep(0.3)
    victimFound = False
    module_buffer = "Surveillance"
    if not stop_threads:
        print('[STATUS] Thread Initiating.')
        webcam_thread = threading.Thread(target = webcamCap, args =(lambda : stop_threads, )) 
        webcam_thread.start()
        while(not victimFound):
            continue
        print("comes out of face !{}".format(data_buffer))
        return jsonify({ 'flag' : False, 'message': "Suspect "+data_buffer +" at " + location_buffer })
    print('[STATUS] Thread running...')
    return jsonify({'flag': True})

@app.route('/location' , methods = ['POST' , 'GET'])
def locationChange():
    global stop_threads
    global location_buffer
    stop_threads = True
    time.sleep(0.3)
    stop_threads = False
    print('[STATUS] Location changed to ' + location_buffer)
    return jsonify({'flag' : True})


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/botResponse' , methods = ['POST' , 'GET'])
def botResponse():
    userInput = request.form['utext']
    botMessage = botResponseReciever(userInput)
    
    handler_data = bot_Event_Handler(botMessage[0] , botMessage[1])
    handler_data = handler_data.json()

    if not handler_data['flag']:
        print("comes handler")
        return jsonify({'response': handler_data['message'] , 'class' : botMessage[1]})

    

    #errorMessage = json.loads(request.data.decode("utf-8"))["utext"]
    #errorMessage = errorMessage.replace("'", "")
    #print(errorMessage)
    #return solution_finder(errorMessage)



    return  jsonify({'response': botMessage[0] , 'class' : botMessage[1]})

if __name__ == "__main__":
    app.run(debug = True , host= "0.0.0.0" , port= 5000)