import cv2
import time
def updateSuspectLogs(name , location):
    fileObj = open("./modules/FriendRecognition/LocationLogs/"+name+".txt" , "a+")
    localtime = time.asctime( time.localtime(time.time()) )
    fileObj.write("Location: "+ location + "-----Timestamp: " + localtime + "\n")
    fileObj.close()

if __name__ == "__main__":
    updateSuspectLogs("Karthik" , "Chennai")


    