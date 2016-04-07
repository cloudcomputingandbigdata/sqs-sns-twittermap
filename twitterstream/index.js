var Twit = require('twit');
var SQS = require('./sqs');
var config = require('./config');

// AWS SQS
var sqs = new SQS();

// fetch tweets by streaming API
var T = new Twit(config.auth);

var containKeyword = function(text) {
  var keywords = config.track;
  var contained = false;
  for (var i=0; i<keywords.length; i++) {
    if (text.indexOf(keywords[i]) > -1) {
      contained = true;
      break;
    }
  }
  return contained;
}

sqs.createQueue().then(function(url) {
  var cnt = 0;
  var tweetsList = [];
  var stream = T.stream('statuses/filter', {
    // track: config.track,
    language: 'en',
    locations: ['-180.0', '-90.0', '180.0', '90.0']
  });
  stream.on('tweet', function(tweet) {
    if (tweet.place && containKeyword(tweet.text)) {
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