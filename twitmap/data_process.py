from services import *
import json


class DataProcess:
    def __init__(self):
        self.ss = SearchServices()

    def process(self, data):
        # keywords = self.ss.keywords
        data_json = json.loads(data)
        contents = data_json['text']
        sentiment = data_json['sentiment']

        # if the tweet contains one of the keywords, it will be stored in the index
        # if any(x in contents.lower() for x in keywords):
        if data_json['place'] is not None:
            location_name = data_json['place']['full_name']
            #location_type = 'Point'
            coordinates = data_json['place']['bounding_box']['coordinates']
            country_code = data_json['place']['country_code']
            country = data_json['place']['country']

            if coordinates[0] is not None and len(coordinates[0]) > 0:
                avg_x = 0
                avg_y = 0
                for c in coordinates[0]:
                    avg_x = (avg_x + c[0])
                    avg_y = (avg_y + c[1])
                avg_x /= len(coordinates[0])
                avg_y /= len(coordinates[0])
                coordinates = [avg_x, avg_y]

            print coordinates

            timestamp = data_json['timestamp_ms']
            datetime = data_json['created_at']
            author = data_json['user']['name']
            screen_name = data_json['user']['screen_name']
            id = data_json['id_str']
            #print(coordinates)
            #print("timestamp=%s, contents=%s, author=%s, location=%s" % (timestamp, contents, author, location))
            self.ss.insert_tweet(id, contents, author, screen_name, timestamp, datetime, location_name, coordinates, country_code, country, sentiment)

            # print(data)