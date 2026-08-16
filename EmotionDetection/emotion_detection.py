import requests
import json

def emotion_detector(text_to_analyze):
    """
    Function to analyze emotion using IBM Watson NLP Emotion Detection
    """
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    myobj = {"raw_document": {"text": text_to_analyze}}
    
    response = requests.post(url, json=myobj, headers=headers)
    response_dict = json.loads(response.text)
    
    # Extract emotions from the response
    emotions = response_dict.get('emotionPredictions', [{}])[0].get('emotion', {})
    
    output = {
        'anger': emotions.get('anger', 0.0) or 0.0,
        'disgust': emotions.get('disgust', 0.0) or 0.0,
        'fear': emotions.get('fear', 0.0) or 0.0,
        'joy': emotions.get('joy', 0.0) or 0.0,
        'sadness': emotions.get('sadness', 0.0) or 0.0
    }
    
    # Dominant emotion
    if all(value == 0.0 for value in output.values()):
        output['dominant_emotion'] = 'No emotion detected'
    else:
        output['dominant_emotion'] = max(output, key=output.get)
    
    return output

if __name__ == '__main__':
    # Testing of the emotion_detector function
    result = emotion_detector("I love this new technology")
    print(json.dumps(result, indent=2))
    