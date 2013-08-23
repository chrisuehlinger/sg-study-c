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
        document.getElementById('recovery-submit').disabled = true
        document.getElementById('recovery-email-input').disabled = true
        $('#recovery-message').text "Submitting..."
      success: (data) ->
        console.log("Received")
        response = JSON.parse data
        document.getElementById('recovery-submit').disabled = false
        document.getElementById('recovery-email-input').disabled = false
        $('#recovery-message').text response.message
      error: ->
        console.log("Error")
        document.getElementById('recovery-submit').disabled = false
        document.getElementById('recovery-email-input').disabled = false
        $('#recovery-message').text "Site Error: #{textStatus} - #{errorThrown}"