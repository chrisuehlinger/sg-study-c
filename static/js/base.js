// Generated by CoffeeScript 1.6.3
(function() {
  var submitSuggestion;

  $(document).ready(function() {
    return $('form#suggestion-box').submit(function(e) {
      e.preventDefault();
      submitSuggestion();
      return false;
    });
  });

  submitSuggestion = function() {
    var request;
    return request = $.ajax({
      url: '/suggestion',
      type: 'POST',
      data: {
        'suggestion': $('#suggestion-input').val(),
        'page_url': window.location.pathname
      },
      dataType: 'application/json',
      beforeSend: function() {
        document.getElementById('suggestion-submit').disabled = true;
        document.getElementById('suggestion-input').disabled = true;
        return $('#suggestion-input').val("Submitting...");
      },
      success: function(data) {
        var response;
        console.log("Received");
        document.getElementById('suggestion-submit').disabled = false;
        document.getElementById('suggestion-input').disabled = false;
        response = JSON.parse(data);
        return $('#suggestion-input').val(response.message);
      },
      error: function() {
        console.log("Error");
        document.getElementById('suggestion-submit').disabled = false;
        document.getElementById('suggestion-input').disabled = false;
        return $('#suggestion-input').val("Site Error: " + textStatus + " - " + errorThrown);
      }
    });
  };

}).call(this);
