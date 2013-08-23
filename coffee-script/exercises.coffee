myCodeMirror = {}

$(document).ready -> 
  myTextArea = document.getElementById 'editor' 
  codeMirrorConfig = 
    'theme':'night'
    'lineNumbers':true
    'mode':'clike'
    'value':$('#editor').text()
    'autofocus':true
  myCodeMirror = CodeMirror.fromTextArea myTextArea, codeMirrorConfig

  # highlightLine 2

  $('#output').hide()
  $('#cmpinfo').hide()

  $('input#submit-test').click (e) ->
    e.preventDefault()
    request = $.ajax 
      url: document.URL
      type: 'POST'
      data: {'action':'test', 'code': myCodeMirror.getValue()}
      dataType: 'application/json'
      beforeSend: beforeSubmit
      success: receiveResponse
      error: receiveError

  $('input#submit-check').click (e) ->
    e.preventDefault()
    request = $.ajax 
      url: document.URL
      type: 'POST'
      data: {'action':'check', 'code': myCodeMirror.getValue(), 'input':$('#input').text() }
      dataType: 'application/json'
      beforeSend: beforeSubmit
      success: receiveResponse
      error: receiveError

    false

#AJAX methods
beforeSubmit = ->
  document.getElementById('submit-test').disabled = true
  document.getElementById('submit-check').disabled = true
  document.getElementById('input').disabled = true
  $('#output').hide()
  $('#cmpinfo').hide()
  $('#message').text "Submitting..."

receiveResponse = (data) ->
  response = JSON.parse data
  if response.cmpinfo?
    $('#cmpinfo').show()
    $('#cmpinfo').find('div.code').html response.cmpinfo
    # pattern = /prog.c:([0-9]+):/
    # error_line = pattern.exec(response.cmpinfo)[1]
    # console.log(error_line)
    # highlightLine error_line
  if response.output?
    $('#output').show()
    $('#output').find('div.code').html response.output 
  document.getElementById('submit-test').disabled = false
  document.getElementById('submit-check').disabled = false
  document.getElementById('input').disabled = false
  $('#message').html response.message 

receiveError = (jqXHR, textStatus, errorThrown) ->
  document.getElementById('submit-test').disabled = false
  document.getElementById('submit-check').disabled = false
  document.getElementById('input').disabled = false
  $('#message').text "Site Error: #{textStatus} - #{errorThrown}"

highlightLine = (lineNumber) ->
        # Line number is zero based index
        actualLineNumber = lineNumber - 1

        # Select editor loaded in the DOM
        myEditor = $("#body_EditorSource .CodeMirror")
        console.log(myEditor)
        console.log(myEditor[0])
        console.log(myEditor.CodeMirror)

        codeMirrorEditor = myEditor[0].CodeMirror
            
        # Set line css class
        codeMirrorEditor.setLineClass actualLineNumber, 'background', 'codemirror-error'