import boto3
import datetime
import time

def parseText(textDetections):
    detectedText = ""
    for text in textDetections:
        if not 'ParentId' in text:
            detectedText += text['DetectedText'] + " "

    return detectedText


if __name__ == "__main__":

    bucket='rene-tarea7'
    photo='tarea-{}.jpg'
    control='control.png'
    session = boto3.Session(profile_name="renemujica-usm")
    client=session.client('rekognition')

  
    controlDetection=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':control}})
    controlText = parseText(controlDetection['TextDetections'])
    logs = []

    for i in range(1, 11):
        print("Test ID:", i)
        logs.append("Test ID: "+ str(i))
        print("Hora de la prueba:",datetime.datetime.now())
        logs.append("Hora de la prueba: "+str(datetime.datetime.now()))
        testDetection = client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo.format(i)}})
        detectedText = parseText(testDetection['TextDetections'])
        print("Texto detectado: ", detectedText.lower())
        logs.append("Texto detectado: "+ detectedText.lower())
        print("iguales?", controlText.lower().strip() == detectedText.lower().strip())
        logs.append("iguales? "+ str(controlText.lower().strip() == detectedText.lower().strip()))
        print("====")
        logs.append("====")

    with open("logs-"+str(time.time())+".txt", "w") as f:
        for log in logs:
            f.write("%s\n" % log)
    