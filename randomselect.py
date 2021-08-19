import pandas as pd


def result(emotion,kind):
    df = pd.read_csv('./看圖說故事/poemlist.csv')
    if emotion == "sadness" :
        sadness = df[df["emotion"]=="sadness"]
        if kind == "歌":
            data = sadness[sadness['kind']== '歌']
        elif kind == "詩":
            data = sadness[sadness['kind']== '詩']
    elif (emotion == "happiness") or (emotion == "suprise"):
        happiness = df[df["emotion"]=="happiness"]
        if kind == "歌":
            data = happiness[happiness['kind']=='歌']
        elif kind == "詩":
            data = happiness[happiness['kind']=='詩']
    elif emotion == "neutral":
        neutral = df[df["emotion"]=="neutral"]
        if kind == "歌":
            data = neutral[neutral['kind']=='歌']
        elif kind == "詩":
            data = neutral[neutral['kind']=='詩']
    else :
        anger = df[df["emotion"]=="anger"]
        if kind == "歌":
            data = anger[anger['kind']=='歌']
        elif kind == "詩":
            data = anger[anger['kind']=='詩']
            
    result  = data.sample(n=1)
    name = result['name'].item()
    info = result['info'].item()
    return (name,info)

if __name__ == '__main__':
    emotion = "happiness"
    kind = '詩'
    print(result(emotion,kind))