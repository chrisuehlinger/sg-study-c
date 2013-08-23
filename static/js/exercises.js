// Generated by CoffeeScript 1.6.3
(function() {
  var beforeSubmit, highlightLine, myCodeMirror, receiveError, receiveResponse;

  myCodeMirror = {};

  $(document).ready(function() {
    var codeMirrorConfig, myTextArea;
    myTextArea = document.getElementById('editor');
    codeMirrorConfig = {
      'theme': 'night',
      'lineNumbers': true,
      'mode': 'clike',
      'value': $('#editor').text(),
      'autofocus': true
    };
    myCodeMirror = CodeMirror.fromTextArea(myTextArea, codeMirrorConfig);
    $('#output').hide();
    $('#cmpinfo').hide();
    $('input#submit-test').click(function(e) {
      var request;
      e.preventDefault();
      return request = $.ajax({
        url: document.URL,
        type: 'POST',
        data: {
          'action': 'test',
          'code': myCodeMirror.getValue()
        },
        dataType: 'application/json',
        beforeSend: beforeSubmit,
        success: receiveResponse,
        error: receiveError
      });
    });
    return $('input#submit-check').click(function(e) {
      var request;
      e.preventDefault();
      request = $.ajax({
        url: document.URL,
        type: 'POST',
        data: {
          'action': 'check',
          'code': myCodeMirror.getValue(),
          'input': $('#input').text()
        },
        dataType: 'application/json',
        beforeSend: beforeSubmit,
        success: receiveResponse,
        error: receiveError
      });
      return false;
    });
  });

  beforeSubmit = function() {
    document.getElementById('submit-test').disabled = true;
    document.getElementById('submit-check').disabled = true;
    document.getElementById('input').disabled = true;
    $('#output').hide();
    $('#cmpinfo').hide();
    return $('#message').text("Submitting...");
  };

  receiveResponse = function(data) {
    var response;
    response = JSON.parse(data);
    if (response.cmpinfo != null) {
      $('#cmpinfo').show();
      $('#cmpinfo').find('div.code').html(response.cmpinfo);
    }
    if (response.output != null) {
      $('#output').show();
      $('#output').find('div.code').html(response.output);
    }
    document.getElementById('submit-test').disabled = false;
    document.getElementById('submit-check').disabled = false;
    document.getElementById('input').disabled = false;
    return $('#message').html(response.message);
  };

  receiveError = function(jqXHR, textStatus, errorThrown) {
    document.getElementById('submit-test').disabled = false;
    document.getElementById('submit-check').disabled = false;
    document.getElementById('input').disabled = false;
    return $('#message').text("Site Error: " + textStatus + " - " + errorThrown);
  };

  highlightLine = function(lineNumber) {
    var actualLineNumber, codeMirrorEditor, myEditor;
    actualLineNumber = lineNumber - 1;
    myEditor = $("#body_EditorSource .CodeMirror");
    console.log(myEditor);
    console.log(myEditor[0]);
    console.log(myEditor.CodeMirror);
    codeMirrorEditor = myEditor[0].CodeMirror;
    return codeMirrorEditor.setLineClass(actualLineNumber, 'background', 'codemirror-error');
  };

}).call(this);
