// Generated by CoffeeScript 1.6.3
(function() {
  var submitEmail;

  $(document).ready(function() {
    return $('form#recovery-email').submit(function(e) {
      e.preventDefault();
      submitEmail();
      return false;
    });
  });

  submitEmail = function() {
    var request;
    return request = $.ajax({
      url: document.URL,
      type: 'POST',
      data: {
        'email': $('#recovery-email-input').val()
      },
      dataType: 'application/json',
      beforeSend: function() {
        console.log("Submitting");
        document.getElementById('recovery-submit').disabled = true;
        document.getElementById('recovery-email-input').disabled = true;
        return $('#recovery-message').text("Submitting...");
      },
      success: function(data) {
        var response;
        console.log("Received");
        response = JSON.parse(data);
        document.getElementById('recovery-submit').disabled = false;
        document.getElementById('recovery-email-input').disabled = false;
        return $('#recovery-message').text(response.message);
      },
      error: function() {
        console.log("Error");
        document.getElementById('recovery-submit').disabled = false;
        document.getElementById('recovery-email-input').disabled = false;
        return $('#recovery-message').text("Site Error: " + textStatus + " - " + errorThrown);
      }
    });
  };

}).call(this);
