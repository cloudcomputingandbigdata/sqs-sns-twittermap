var React = require('react');
var Keywordfilter = require('./Keywordfilter');
var Timefilter = require('./Timefilter');
var DropPin = require('./DropPin');
var tweetLoader = require('./TweetLoader');
var Menu = require('./Menu');
var Accordion = require('./Accordion');
var UpdateSetting = require('./UpdateSetting');
var Counter = require('./Counter');

var TwitterMapController = React.createClass({
  propTypes: {
    mapbox: React.PropTypes.object.isRequired
  },

  getInitialState() {
    return {
      tweets: [],
      keyword: null,
      mode: "all",
      time: null,
      unit: "m",
      distance: 10,
      isPinned: false,
      lat: null,
      lon: null,
      isAuto: false,
      number: 0
    }
  },

  componentDidMount() {
    this.pointsLayer = null;
    this.pin = null;
  },

  showPin() {
    var self = this;
    var mapbox = this.props.mapbox;
    var bounds = mapbox.getBounds();
    var center = bounds.getCenter();
    this.pin = L.marker(center, {
      icon: L.mapbox.marker.icon({
        'marker-color': '#f86767'
      }),
      draggable: true
    }).addTo(mapbox);
    this.pin.on('dragend', ondragend);
    ondragend();

    function ondragend() {
        var m = self.pin.getLatLng();
        console.log('Latitude: ' + m.lat + ', Longitude: ' + m.lng);
        self.setState({
          lat: m.lat,
          lon: m.lng
        }, function() {
          if (self.state.keyword && self.state.distance > 0 && self.state.distance <= 200) {
            self.loadResults(self.state.keyword, self.state.isAuto);
          }
        });
    }
  },

  removePin() {
    var mapbox = this.props.mapbox;
    mapbox.removeLayer(this.pin);
    this.loadResults(this.state.keyword, this.state.isAuto);
  },

  

  buildParameters() {
    var parameters = {};
    if (this.state.mode == 'all') {

    } else {
      var time = this.state.time;
      var unit = this.state.unit;
      if (time && unit && time > 0) {
        parameters['from'] = "now-" + time + unit;
        parameters['to'] = "now";
      }
    }

    if (this.state.isPinned) {
      var distance = this.state.distance;
      var lat = this.state.lat;
      var lon = this.state.lon;
      if (distance && (lat && lon) && distance > 0) {
        parameters['distance'] = distance + 'km';
        parameters['lat'] = lat;
        parameters['lon'] = lon;
      }
    }
    return parameters;
  },

  loadResults(keyword, autoUpdate) {
    if(!keyword || keyword.length === 0){
      return;
    }
    window.clearInterval(this.autoUpdateInterval);
    //stop the polling of loading from scroll id?
    var parameters = this.buildParameters();
    if(autoUpdate){
      this.autoUpdateInterval = window.setInterval(this.__loadResult, 30000, keyword, parameters);
    }
    this.__loadResult(keyword, parameters);
  },

  __loadResult(keyword, parameters){
    var that = this;
    tweetLoader.loadByKeyword(keyword, parameters).done(function(data) {
      console.log(data);
      that.state.number = data.hits.total;
      var tweets = [];
      $('.menu').addClass("overlay");
      (function pollingLoad(scrollId){
        tweetLoader.scroll(scrollId).done(function(value){
          console.log(value);
          if (value.hits.length === 0) {
            $('.menu').removeClass('overlay');
            that.setState({
              tweets: tweets
            }, function(){
              that.showTweetsOnMap();
            });
          } else {
            tweets = tweets.concat(value.hits);
            pollingLoad(scrollId);
          }
        });
      })(data._scroll_id); 
    });
  },

  showTweetsOnMap() {
    var mapbox = this.props.mapbox;
    var tweets = this.state.tweets;
    if (this.pointsLayer != null) {
      mapbox.removeLayer(this.pointsLayer);
    }
    var clusterLayer = new L.MarkerClusterGroup({
      iconCreateFunction: function(cluster) {
        var html = '<div class="tweet-cluster-outer">' + 
        '<div class="tweet-cluster">' + cluster.getChildCount() + '</div>' + 
        '</div>';
        return L.divIcon({
          className: 'tweet-cluster-icon',
          html: html
        });
      }
    });

    tweets.forEach(function(tweet) {
      var coords = tweet.geometry.coordinates;
      var url = "http://twitter.com/" + tweet.properties.screen_name + "/status/" + tweet.properties.tweet_id;
      var text = "<div class='author'><strong>" + tweet.properties.title + "</strong></div>" +
      "<div class='date'>" + tweet.properties.datetime + "</div>" + 
      "<div class='contents'>" + tweet.properties.description + "</div>" +
      "<a href='" + url + "' target=_blank>View Tweet</a>" +
      "</div>"
      var marker = L.marker(new L.LatLng(coords[1], coords[0]), {
        icon: L.mapbox.marker.icon({
          'marker-color': '89C9FA',
          'marker-size': 'medium'
        }),
        description: text
      });
      marker.bindPopup(text);
      clusterLayer.addLayer(marker);
    });

    this.pointsLayer = clusterLayer;
    mapbox.addLayer(this.pointsLayer);

  },

  onFilterValueChanged(value) {
    console.log('value changed: ' + value);
    this.setState({keyword: value}, function(){
      this.loadResults(this.state.keyword, this.state.isAuto);
    });
  },

  onTimeUnitValueChanged(value) {
    console.log('time unit changed:' + value);
    this.setState({unit: value}, function(){
      if (this.state.time > 0)
        this.loadResults(this.state.keyword, this.state.isAuto);
    });
  },

  onTimeChanged(value) {
    console.log('time changed:' + value);
    this.setState({time: value}, function(){
      if(value > 0){
        this.loadResults(this.state.keyword, this.state.isAuto);
      }
    });
  },

  onModeChanged(value) {
    console.log('mode changed:' + value);
    this.setState({mode: value}, function(){
      if (value != 'all' && this.state.time <= 0) {
        return;
      }
      this.loadResults(this.state.keyword, this.state.isAuto);
    });
  },

  onDistanceChanged(value) {
    console.log('distance changed:' + value);
    this.setState({distance: value}, function(){
      if(value <= 200 && value > 0){
        this.loadResults(this.state.keyword, this.state.isAuto);
      }
    });
  },

  onPinStatusChanged(value) {
    console.log('show pin? ' + value);
    this.setState({isPinned: value}, function(){
      if(this.pin && !this.state.isPinned){
        this.removePin();
        this.pin = null;
      }else if(!this.pin && this.state.isPinned){
        this.showPin();
      }
    });
  },

  onCheckAutoUpdate(isAuto){
    console.log('auto update setting changed:' + isAuto);
    this.setState({isAuto: isAuto}, function(){
      this.loadResults(this.state.keyword, this.state.isAuto);
    });
  },

  render() {
    return (
      <div>
        <Menu ref="right" alignment="right" header={"TwittMap"} footer={"Developed by Yue Cen & Houliang Lu"}>
          <div className="keyword-container">
            <Keywordfilter onChange = {this.onFilterValueChanged}/>
          </div>
          <div className="time-container">
            <Accordion title={"Time range filter"}>
              <Timefilter onUnitChange = {this.onTimeUnitValueChanged} onModeChange = {this.onModeChanged} onTimeChange = {this.onTimeChanged} />
            </Accordion>
          </div>
          <div className="drop-pin-container">
            <Accordion title={"Distance range filter"}>
              <DropPin onPinStatusChange = {this.onPinStatusChanged} onDistanceChange = {this.onDistanceChanged} />
            </Accordion>
          </div>
          <div className="update-setting-container">
            <Accordion title={"Tweets update setting"} active={"active"}>
              <UpdateSetting onCheck={this.onCheckAutoUpdate} />
            </Accordion>
          </div>
          <div className="update-setting-container">
            <Accordion title={"Statistics"} active={"active"}>
              <Counter number={this.state.number} />
            </Accordion>
          </div>
        </Menu>
      </div>
    )
  }
});

module.exports = TwitterMapController;