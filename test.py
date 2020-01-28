import cv2

if __name__ == "__main__":
    frame = cv2.imread("./Assets/botImage.png")
    while(True):
        cv2.imshow("HOpe it works !" , frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break 


    