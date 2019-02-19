import keys
import tweepy
import json
import langdetect as ld

consumer_key = keys.consumer_key
consumer_secret = keys.consumer_secret
access_token = keys.access_token
access_secret = keys.access_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth,
                 wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)
# здесь в качестве значения впишите количество твитов, которые вы хотите получить
TOTAL_NUMBER = 100

class MSL(tweepy.StreamListener):
    def __init__(self):
        super(MSL, self).__init__()
        self.counter = 0
        self.all_tweets = []

    #cледующая функция: начинаем с загрузки json'a, которому скармливается информация прошедшая фильтр.
    # (Фильтр мы увидим позже)
    def on_data(self, data):
        data_temp = json.loads(data, encoding='utf-8')
        try:
            if len(data_temp["text"]) > 50 and ld.detect(data_temp["text"]) == 'ru':
                self.all_tweets.append(data_temp)
                self.counter += 1
                print(data_temp["text"])
                print(self.counter)

                if self.counter == TOTAL_NUMBER:
                    #rus.json это название json файла, а "а" здесь значит "append", то есть файлы будут
                    #обновляться. Впрочем, зная капризный json формат, скорее всего вам придется немного
                    #подправлять файл мануально после каждого обновления
                    file = open('rus.json', 'a')
                    file.write(json.dumps(self.all_tweets, indent=4))
                    file.close()
                    return False
        except:
            pass
        return True

twitter_stream = tweepy.Stream(auth, MSL())
keywords = ['песик', 'футбол', 'собака', 'ты']
twitter_stream.filter(track=keywords, languages=['ru'])

