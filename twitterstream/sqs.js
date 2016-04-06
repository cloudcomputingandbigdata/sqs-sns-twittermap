var AWS = require('aws-sdk');
AWS.config.update({
  region: 'us-east-1'
});

var sqs = function() {
  this.sqsClient = new AWS.SQS();
};

sqs.prototype.createQueue = function(params) {
  var that = this;
  var createQueueParams = {
    QueueName: "twitterMap"
  };

  if (params) {
    for (key in params) {
      createQueueParams[key] = params[key];
    }
  } else {
    callback = params;
  }

  return new Promise(function(resolve, reject) {
    that.sqsClient.createQueue(createQueueParams, function(err, data) {
      if (err) {
        reject(err);
      } else {
        resolve(data.QueueUrl);
      }
      /*
      data = {
       QueueUrl: "https://queue.amazonaws.com/012345678910/MyQueue"
      }
      */
    });
  });
};

var buildBatchMessageParams = function(datas, url) {
  var params = {};
  params.QueueUrl = url;
  params.Entries = [];
  for (i = 0; i < datas.length; i++) {
    var item = datas[i];
    var entry = {
      Id: "" + i,
      MessageBody: JSON.stringify(item),
      DelaySeconds: 0
    }
    params.Entries.push(entry);
  }
  return params;
};

sqs.prototype.sendBatchMessages = function(datas, url) {
  var params = buildBatchMessageParams(datas, url);
  var that = this;
  return new Promise(function(resolve, reject) {
    that.sqsClient.sendMessageBatch(params, function(err, data) {
      if (err) {
        reject(err);
      } else {
        console.log('send to SQS successful')
        resolve(data);
      }
    });
  });
};


module.exports = sqs;