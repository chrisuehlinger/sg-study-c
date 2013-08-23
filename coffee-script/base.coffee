$(document).ready ->

  # scrolling nav
  top = $('#sidebar').offset().top - parseFloat $('#sidebar').css('marginTop').replace /auto/, 0
  $(window).scroll (event) ->
    # what the y position of the scroll is
    y = $(@).scrollTop()

    # whether that's below the form
    if y >= top-10
      # if so, ad the fixed class
      $('#sidebar').addClass 'fixed'
    else
      # otherwise remove it
      $('#sidebar').removeClass 'fixed'

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





