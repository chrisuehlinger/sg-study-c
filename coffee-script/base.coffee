$(document).ready ->

  # suggestion box
  $('form#suggestion-box').submit (e) ->
    e.preventDefault()
    submitSuggestion()
    false

submitSuggestion = ->
  request = $.ajax 
      url: '/suggestion'
      type: 'POST'
      data: {'suggestion': $('#suggestion-input').val(), 'page_url':window.location.pathname}
      dataType: 'application/json'
      beforeSend: ->
        document.getElementById('suggestion-submit').disabled = true
        document.getElementById('suggestion-input').disabled = true
        $('#suggestion-input').val "Submitting..."
      success: (data) ->
        console.log "Received"
        document.getElementById('suggestion-submit').disabled = false
        document.getElementById('suggestion-input').disabled = false
        response = JSON.parse data
        $('#suggestion-input').val response.message
      error: ->
        console.log "Error"
        document.getElementById('suggestion-submit').disabled = false
        document.getElementById('suggestion-input').disabled = false
        $('#suggestion-input').val "Site Error: #{textStatus} - #{errorThrown}"





