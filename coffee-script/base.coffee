class Example
  constructor: (@figure) ->
    @textArea = @figure.getElementsByTagName('textarea')[0]
    @start_code = $(@textArea).text()
    codeMirrorConfig = 
      'theme': $('meta[name="CodeMirrorTheme"]').attr 'content'
      'lineNumbers':true
      'mode':
        'name':'text/x-csrc'
        'keywords': {'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if', 'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while'}
        'useCPP':true
      'indentUnit':4
      'value': @start_code
      'autoCloseBrackets': true
      'matchBrackets':true

    @codeMirror = CodeMirror.fromTextArea @textArea, codeMirrorConfig

    $(@figure).find('#std-output').hide()
    $(@figure).find('#cmpinfo').hide()

    $(@figure).find('input#submit-test').click (e) =>
      e.preventDefault()
  
      request = $.ajax 
        url: document.URL
        type: 'POST'
        data: {'action':'test', 'code': @codeMirror.getValue()}
        dataType: 'json'
      
      @beforeSubmitExample()
      request.done @receiveResponseExample
      request.fail @receiveErrorExample

      false

    $(@figure).find('input#reset').click (e) =>
      e.preventDefault()
      @codeMirror.setValue @start_code

      false

  beforeSubmitExample: =>
    $(@figure).find('#message').text "Submitting..."

    $(@figure).find('#std-output').hide()
    $(@figure).find('#cmpinfo').hide()

    $(@figure).find('input').attr 'disabled','disabled'
    $(@figure).find('std-input').attr 'disabled','disabled'

  receiveResponseExample: (response) =>
    $(@figure).find('#message').html response.message 

    if response.cmpinfo?
      $(@figure).find('#cmpinfo').show()
      $(@figure).find('#cmpinfo').find('div.code').html response.cmpinfo
      # pattern = /prog.c:([0-9]+):/
      # error_line = pattern.exec(response.cmpinfo)[1]
      # console.log(error_line)
      # highlightLine error_line

    if response.output?
      $(@figure).find('#std-output').show()
      $(@figure).find('#std-output').find('div.code').html response.output

    $(@figure).find('input').removeAttr 'disabled'
    $(@figure).find('std-input').removeAttr 'disabled'

  receiveErrorExample: (jqXHR, textStatus, errorThrown) =>
    $(@figure).find('#message').text "Site Error: #{textStatus} - #{errorThrown}"

    $(@figure).find('input').removeAttr 'disabled'
    $(@figure).find('std-input').removeAttr 'disabled'

submitSuggestion = ->
  request = $.ajax 
      url: '/suggestion'
      type: 'POST'
      data: {'suggestion': $('#suggestion-input').val(), 'page_url':window.location.pathname}
      dataType: 'json'
      beforeSend: ->
        document.getElementById('suggestion-submit').disabled = true
        document.getElementById('suggestion-input').disabled = true
        $('#suggestion-input').val "Submitting..."
      success: (data) ->
        console.log "Received"
        document.getElementById('suggestion-submit').disabled = false
        document.getElementById('suggestion-input').disabled = false
        $('#suggestion-input').val data.message
      error: (jqXHR, textStatus, errorThrown) ->
        console.log "Error"
        document.getElementById('suggestion-submit').disabled = false
        document.getElementById('suggestion-input').disabled = false
        $('#suggestion-input').val "Site Error: #{textStatus} - #{errorThrown}"

sample = (el) ->
  $(el).addClass 'cm-s-neat'
  the_code = $(el).find('code').text()
  the_mode = 
    'name':'text/x-csrc'
    'keywords': {'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if', 'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while'}
    'useCPP':true
  CodeMirror.runMode(the_code, 'text/x-csrc', el)

$(document).ready -> 
  $('figure.example').each ->
    this_example = new Example @

  $('pre').each ->
    sample @

  # suggestion box
  $('form#suggestion-box').submit (e) ->
    e.preventDefault()
    submitSuggestion()
    false






