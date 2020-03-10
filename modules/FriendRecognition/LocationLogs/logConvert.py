from datetime import datetime

def suspectSerialize(name):
    fileObj = open('./modules/FriendRecognition/LocationLogs/'+ name + '.txt' , 'r')
    #fileObj = open(name + '.txt' , 'r')
    prev = None

    logList = {}
    
    for line in fileObj:
        pair = line.split('-')
        location = pair[0].split('=')[1].strip()
        time = pair[1].split('=')[1].strip()
        
        #tempTime = datetime.strptime(time , "%a %b %d %H:%M:%S %Y")
        
        if prev == None:
            prev = location
            logList[location] = time
            continue
        else:
            logList[location] = time

    result = []

    for key in logList:
        log = {}
        log["location"] = key
        log["time"] = logList[key]
        result.append(log)
    result = str(result).replace("'" , '"')
    return result

if __name__ == "__main__":
    print(suspectSerialize("Shyam"))
    

