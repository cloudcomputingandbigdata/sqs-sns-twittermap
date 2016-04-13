# SQS-SNS TwitterMap

![shot](shot.png)

### AWS Demo
View the [twitter map](http://twittmap.q3f5vtg5g3.us-west-2.elasticbeanstalk.com/) on beanstalk.

### Overview
#### Streaming
- Reads a stream of tweets from the Twitter Streaming API. Note: you might follow a set of specific keywords that you find interesting
- After fetching a new tweet, check to see if it has geolocation info and is in English.
- Once the tweet validates these filters, send a message to SQS for asynchronous processing on the text of the tweet

#### Worker
- Define a worker pool that will pick up messages from the queue to process. These workers should each run on a separate pool thread.
- Make a call to the sentiment API off your preference (e.g. Alchemy (Links to an external site.)). This can return a positive, negative or neutral sentiment evaluation for the text of the submitted Tweet.
- As soon as the tweet is processed send a notification -using SNS- to an HTTP endpoint (Links to an external site.) that contains the information about the tweet.

#### Backend
- On receiving the notification, index this tweet in Elasticsearch. Make sure you preserve the sentiment of the tweet as well.
- The backend should provide the functionality to the user to search for tweets that match a particular keyword. To this end, you can either write a new webserver or simply reuse your first assignment.

#### Frontend
- When a new tweet is indexed, it will be added on the map.
- Give the user the ability to search your index via a free text input or a dropdown.
- Plot the tweets that match the query on a map. (use markers (Links to an external site.))
- Use a custom marker (Links to an external site.) to indicate the sentiment.

### Stack
- Elastic Search (tweet storage and search)
- Django (backend)
- React (frontend)
- NodeJS (streaming)

### Usage

##### Stream
```
// cd to twitterstream folder
$ npm run stream
```

#### Worker
```
// cd to worker folder
$ python worker.py
```

##### Build JS
```
$ npm install
$ npm run build
```

##### Install Dependencies
```
// install dependencies with:
$ pip install -r requirements.txt
```

##### Start server
```
$ python manage.py runserver
```
