var Twit = require('twit');
var SQS = require('./sqs');
var config = require('./config');

// AWS SQS
var sqs = new SQS();

// fetch tweets by streaming API
var T = new Twit(config);

sqs.createQueue().then(function(url) {
  var cnt = 0;
  var tweetsList = [];
  var stream = T.stream('statuses/filter', {
    track: 'food',
    language: 'en',
    locations: ['-180.0', '-90.0', '180.0', '90.0']
  });
  stream.on('tweet', function(tweet) {
    if (tweet.place) {
      console.log(tweet);
      tweetsList.push(tweet);
      ++cnt;
      if (cnt === 10) {
        cnt = 0;
        //send message to SQS
        var datas = tweetsList;
        tweetsList = [];
        sqs.sendBatchMessages(datas, url).then(function(data) {
          console.log("send successful");
          console.log(data);
        });
      }
    }
  });
});


console.log('start streaming');