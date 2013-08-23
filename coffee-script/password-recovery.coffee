$(document).ready ->
	$('form#recovery-email').submit (e) ->
    e.preventDefault()
    submitEmail()
    false

submitEmail = ->
  request = $.ajax 
      url: document.URL
      type: 'POST'
      data: {'email': $('#recovery-email-input').val()}
      dataType: 'application/json'
      beforeSend: ->
        console.log("Submitting")
        $('#recovery-message').text "Submitting..."
      success: (data) ->
        console.log("Received")
        response = JSON.parse data
        $('#recovery-message').text response.message
      error: ->
        console.log("Error")
        $('#recovery-message').text "Site Error: #{textStatus} - #{errorThrown}"