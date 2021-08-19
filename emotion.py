from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import FaceAttributeType
from msrest.authentication import CognitiveServicesCredentials
import os

def emotion(url):
    KEY = 'c302e032923c41898312a5e880515493'
    ENDPOINT = 'https://serenafacerec.cognitiveservices.azure.com/'
    face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

    face_url = url
    
    face_name = os.path.basename(face_url)

    detected_faces = face_client.face.detect_with_url(url=face_url, return_face_attributes=['emotion'])
    if not detected_faces:
        raise Exception(
            'No face detected from image {}'.format(face_name))
    else: 
        # Creating emotionDictionary
        emotionDict = {}
        for face in detected_faces:
            emotionDict['anger'] = face.face_attributes.emotion.anger
            emotionDict['contempt'] = face.face_attributes.emotion.contempt
            emotionDict['disgust'] = face.face_attributes.emotion.disgust
            emotionDict['fear'] = face.face_attributes.emotion.fear
            emotionDict['happiness'] = face.face_attributes.emotion.happiness
            emotionDict['neutral'] = face.face_attributes.emotion.neutral
            emotionDict['sadness'] = face.face_attributes.emotion.sadness
            emotionDict['surprise'] = face.face_attributes.emotion.surprise
            max_key = max(emotionDict, key = emotionDict.get)


    return max_key

if __name__ == '__main__':
    url = "https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg"
    print(emotion(url))