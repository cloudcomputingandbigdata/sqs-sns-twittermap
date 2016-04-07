var React = require('react');

var Accordion = React.createClass({
  componentDidMount() {
    $('.ui.accordion')
      .accordion();
  },

  render: function() {
    var className = "content field " + (this.props.active ? this.props.active : '');
    return (
      <div className="ui accordion field">
        <div className="title">
          <i className="icon dropdown"></i>
          {this.props.title}
        </div>
        <div className={className}>
          {this.props.children}
        </div>
      </div>
    )
  }
});

module.exports = Accordion;