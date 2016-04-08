var React = require('react');

var Counter = React.createClass({
  render: function() {
    return (
      <div>
        <div className="counter-container settings">
          <div>Total tweets on the map: <span className="stat-number">{this.props.number}</span></div>
          <p> </p>
          <div>New tweets since last request: <span className="stat-number">{this.props.new_tweets}</span></div>
          <div>New tweets put on map since last request: <span className="stat-number red">{this.props.new_tweets_on_map}</span></div>
        </div>
      </div>
    )
  }
});

module.exports = Counter;