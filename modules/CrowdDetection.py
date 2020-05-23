import cv2

def scene_detect(frame):
    import json
    from collections import OrderedDict
    from ibm_watson import VisualRecognitionV3
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

    authenticator = IAMAuthenticator('mto9k-KHFPcM1jKbmvsy0-qDK7qYX4CJnKOtSDFSPxo0')
    visual_recognition = VisualRecognitionV3(
        version='2018-03-19',
        authenticator=authenticator
    )

    visual_recognition.set_service_url('https://api.us-south.visual-recognition.watson.cloud.ibm.com/instances/185b8d2d-f8cd-4e52-89bf-7d444dc56161')

    url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQmCVpuaSeV9lrhKKN7YxZBbydUHNVo1IM7b5-yM00xbFxz5q8E&usqp=CAU'
    url2 = 'https://thumbs.dreamstime.com/z/empty-street-india-empty-street-india-day-effects-109146697.jpg'

    #classes_result = visual_recognition.classify(url=url2).get_result()
    classes_result = visual_recognition.classify(images_file = frame , images_filename = 'sample').get_result()
    store = dict()
    flag = 0
    for i in range(len(classes_result["images"][0]["classifiers"][0]["classes"])):
        store[json.dumps(classes_result["images"][0]["classifiers"][0]["classes"][i]["score"])] = json.dumps(classes_result["images"][0]["classifiers"][0]["classes"][i]["class"]) 
        if(str((classes_result["images"][0]["classifiers"][0]["classes"][i]["class"])) == "crowd" or str(json.dumps(classes_result["images"][0]["classifiers"][0]["classes"][i]["class"])) == "people"):
                      flag = 1
    #print(len(classes_result["images"][0]["classifiers"][0]["classes"]))
    store = OrderedDict(sorted(store.items(),reverse = True))
    #print(store)
#     flag = 0
#     for k,v in store.items():
#         if(v == )
#             break
#     print(store)
    return flag
#print(scene_detect())

if __name__ == "__main__":
    cam1_addr = "192.168.1.3"
    cap1 = cv2.VideoCapture("http://"+ cam1_addr +":4747/mjpegfeed")
    counter = 0
    """
    ret1 , frame1 = cap1.read()
    frame1 = frame1[50: , 50:]

    ###     Frame to Image Conversion...
    image = frame1
    success, encoded_image = cv2.imencode('.jpg', image)
    content  = encoded_image.tobytes()
    
    print(scene_detect(content))
    """
    
    while(True):
        ret1 , frame1 = cap1.read()
        frame1 = frame1[50: , 50:]
        cv2.imshow('Location :  ', frame1)

        if(counter == 30):
            image = frame1
            success, encoded_image = cv2.imencode('.jpg', image)
            content  = encoded_image.tobytes()
            
            print(scene_detect(content))
            counter = 0
        counter += 1

    
