from elastic.services import *

class SearchServices:

    def __init__(self):
        self.es = ElasticsearchServices()
        self.index = "tweetmap"
        self.doc_type = "tweets"
        self.keywords = ["soccer", "football", "messi", "beach", "food", "travel", "photo", "basketball", "nba", "gym"]

    # This method is only for testing
    def get_results_by_keyword(self, keyword, from_time=None, to_time=None):
        body = {
            "query": {
                "filtered": {
                    "query": {
                        "query_string": {
                            "query": "*" + keyword + "*",
                            "fields": ["contents"]
                        }
                    },
                    "filter": {
                        "range": {
                            "timestamp": {
                                "from": ("0" if from_time is None or from_time == '' else from_time),
                                "to": ("now" if to_time is None or to_time == '' else to_time)
                            }
                        }
                    }
                }
            }
        }
        res = self.es.search(self.index, self.doc_type, body)

        return res

    def search_scroll(self, keyword, from_time=None, to_time=None, lat=None, lon=None, distance=None):
        body = {
            # "query": {
            #     "filtered": {
            #         "query": {
            #             "query_string": {
            #                 "query": "*" + keyword + "*",
            #                 "fields": ["contents"]
            #             }
            #         },
            #         "filter": {
            #             "range": {
            #                 "timestamp": {
            #                     "from": ("0" if from_time is None or from_time == '' else from_time),
            #                     "to": ("now" if to_time is None or to_time == '' else to_time)
            #                 }
            #             }
            #         }
            #     }
            # }
        }
        body['query'] = {
            "filtered" : {
                "query": {
                    "query_string": {}
                },
                "filter": {
                    "bool": {
                        "must": [

                        ]
                    }
                }
            }
        }
        body['query']['filtered']['query']['query_string']['query'] = "*" + keyword + "*"
        body['query']['filtered']['query']['query_string']['fields'] = ['contents']
        body['query']['filtered']['filter']['bool']['must'].append({
            "range": {
                "timestamp": {
                    "from": ("0" if from_time is None or from_time == '' else from_time),
                    "to": ("now" if to_time is None or to_time == '' else to_time)
                }
            }
        })

        if lat is not None and lon is not None and distance is not None:
            body['query']['filtered']['filter']['bool']['must'].append({
                "geo_distance": {
                    "distance": distance,
                    "distance_type": "plane",
                    "location": {
                        "lat": lat,
                        "lon": lon
                    }
                }
            })

        print body

        page = self.es.search_scroll(self.index, self.doc_type, body)
        # sid = page['_scroll_id']
        # scroll_size = page['hits']['total']
        # print scroll_size
        # print page

        return page

        # # Start scrolling
        # while (scroll_size > 0):
        #     print "Scrolling..."
        #     page = self.es.scroll(scroll_id = sid, scroll = '2m')
        #     # Update the scroll ID
        #     sid = page['_scroll_id']
        #     # Get the number of results that we returned in the last scroll
        #     scroll_size = len(page['hits']['hits'])
        #     print "scroll size: " + str(scroll_size)
        #     # Do something with the obtained page
        #     print page

    def scroll_results(self, scroll_id):
        print "Scrolling..."
        res = self.es.scroll(scroll_id = scroll_id)
        # Update the scroll ID
        #sid = page['_scroll_id']
        # Get the number of results that we returned in the last scroll
        #scroll_size = len(page['hits']['hits'])
        #print "scroll size: " + str(scroll_size)
        # Do something with the obtained page
        hits = []
        for h in res['hits']['hits']:
            h = h['_source']

            icon = {
                "iconSize": [50, 50],
                "iconAnchor": [25, 25],
                "popupAnchor": [0, -25],
            }
            icon['iconUrl'] = '/static/twittermap/img/' + h['sentiment'] + '.png'

            hit = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": h['location']
                },
                "properties": {
                    "title": h['author'],
                    "description": h['contents'],
                    "datetime": h['datetime'],
                    "tweet_id": h['tweet_id'],
                    "screen_name": h['screen_name'],
                    "sentiment": h['sentiment'],
                    "icon": icon
                }
            }
            hits.append(hit)

        output = {"hits": hits}

        return output

    def insert_tweet(self, id, contents, author, screen_name, timestamp, datetime, location_name, coordinates, country_code, country, sentiment):
        body = {
            "tweet_id": id,
            "contents": contents,
            "author": author,
            "screen_name": screen_name,
            "timestamp": timestamp,
            "datetime": datetime,
            "location_name": location_name,
            "location": coordinates,
            "country_code": country_code,
            "country": country,
            "sentiment": sentiment
        }
        res = self.es.feed_data(self.index, self.doc_type, body)

        return res