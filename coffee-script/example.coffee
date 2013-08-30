myCodeMirror = {}

$(document).ready -> 
  myTextArea = document.getElementById 'example'
  start_code = $('#example').text()
  codeMirrorTheme = $('meta[name="CodeMirrorTheme"]').attr 'content'
  codeMirrorConfig = 
    'theme':codeMirrorTheme
    'lineNumbers':true
    'mode':'clike'
    'indentUnit':4
    'value':start_code
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
      beforeSend: beforeSubmitExample
      success: receiveResponseExample
      error: receiveErrorExample

  $('input#reset').click (e) ->
    e.preventDefault()
    myCodeMirror.setValue start_code

    false

#AJAX methods
beforeSubmitExample = ->
  document.getElementById('submit-test').disabled = true
  document.getElementById('reset').disabled = true
  document.getElementById('input').disabled = true
  $('#output').hide()
  $('#cmpinfo').hide()
  $('#message').text "Submitting..."

receiveResponseExample = (data) ->
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
  document.getElementById('reset').disabled = false
  document.getElementById('input').disabled = false
  $('#message').html response.message 

receiveErrorExample = (jqXHR, textStatus, errorThrown) ->
  document.getElementById('submit-test').disabled = false
  document.getElementById('reset').disabled = false
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