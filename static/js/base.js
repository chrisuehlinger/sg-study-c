// Generated by CoffeeScript 1.6.3
(function() {
  var Example, submitSuggestion,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  Example = (function() {
    function Example(figure) {
      var codeMirrorConfig,
        _this = this;
      this.figure = figure;
      this.receiveErrorExample = __bind(this.receiveErrorExample, this);
      this.receiveResponseExample = __bind(this.receiveResponseExample, this);
      this.beforeSubmitExample = __bind(this.beforeSubmitExample, this);
      this.textArea = this.figure.getElementsByTagName('textarea')[0];
      this.start_code = $(this.textArea).text();
      codeMirrorConfig = {
        'theme': $('meta[name="CodeMirrorTheme"]').attr('content'),
        'lineNumbers': true,
        'mode': {
          'name': 'text/x-csrc',
          'keywords': {
            'auto': 'auto',
            'break': 'break',
            'case': 'case',
            'char': 'char',
            'const': 'const',
            'continue': 'continue',
            'default': 'default',
            'do': 'do',
            'double': 'double',
            'else': 'else',
            'enum': 'enum',
            'extern': 'extern',
            'float': 'float',
            'for': 'for',
            'goto': 'goto',
            'if': 'if',
            'int': 'int',
            'long': 'long',
            'register': 'register',
            'return': 'return',
            'short': 'short',
            'signed': 'signed',
            'sizeof': 'sizeof',
            'static': 'static',
            'struct': 'struct',
            'switch': 'switch',
            'typedef': 'typedef',
            'union': 'union',
            'unsigned': 'unsigned',
            'void': 'void',
            'volatile': 'volatile',
            'while': 'while'
          },
          'useCPP': true
        },
        'indentUnit': 4,
        'value': this.start_code,
        'autoCloseBrackets': true,
        'matchBrackets': true
      };
      this.codeMirror = CodeMirror.fromTextArea(this.textArea, codeMirrorConfig);
      $(this.figure).find('#std-output').hide();
      $(this.figure).find('#cmpinfo').hide();
      $(this.figure).find('input#submit-test').click(function(e) {
        var request;
        e.preventDefault();
        request = $.ajax({
          url: document.URL,
          type: 'POST',
          data: {
            'action': 'test',
            'code': _this.codeMirror.getValue()
          },
          dataType: 'json'
        });
        _this.beforeSubmitExample();
        request.done(_this.receiveResponseExample);
        request.fail(_this.receiveErrorExample);
        return false;
      });
      $(this.figure).find('input#reset').click(function(e) {
        e.preventDefault();
        _this.codeMirror.setValue(_this.start_code);
        return false;
      });
    }

    Example.prototype.beforeSubmitExample = function() {
      $(this.figure).find('#message').text("Submitting...");
      $(this.figure).find('#std-output').hide();
      $(this.figure).find('#cmpinfo').hide();
      $(this.figure).find('input').attr('disabled', 'disabled');
      return $(this.figure).find('std-input').attr('disabled', 'disabled');
    };

    Example.prototype.receiveResponseExample = function(response) {
      $(this.figure).find('#message').html(response.message);
      if (response.cmpinfo != null) {
        $(this.figure).find('#cmpinfo').show();
        $(this.figure).find('#cmpinfo').find('div.code').html(response.cmpinfo);
      }
      if (response.output != null) {
        $(this.figure).find('#std-output').show();
        $(this.figure).find('#std-output').find('div.code').html(response.output);
      }
      $(this.figure).find('input').removeAttr('disabled');
      return $(this.figure).find('std-input').removeAttr('disabled');
    };

    Example.prototype.receiveErrorExample = function(jqXHR, textStatus, errorThrown) {
      $(this.figure).find('#message').text("Site Error: " + textStatus + " - " + errorThrown);
      $(this.figure).find('input').removeAttr('disabled');
      return $(this.figure).find('std-input').removeAttr('disabled');
    };

    return Example;

  })();

  submitSuggestion = function() {
    var request;
    return request = $.ajax({
      url: '/suggestion',
      type: 'POST',
      data: {
        'suggestion': $('#suggestion-input').val(),
        'page_url': window.location.pathname
      },
      dataType: 'json',
      beforeSend: function() {
        document.getElementById('suggestion-submit').disabled = true;
        document.getElementById('suggestion-input').disabled = true;
        return $('#suggestion-input').val("Submitting...");
      },
      success: function(data) {
        console.log("Received");
        document.getElementById('suggestion-submit').disabled = false;
        document.getElementById('suggestion-input').disabled = false;
        return $('#suggestion-input').val(data.message);
      },
      error: function(jqXHR, textStatus, errorThrown) {
        console.log("Error");
        document.getElementById('suggestion-submit').disabled = false;
        document.getElementById('suggestion-input').disabled = false;
        return $('#suggestion-input').val("Site Error: " + textStatus + " - " + errorThrown);
      }
    });
  };

  $(document).ready(function() {
    $('figure.example').each(function() {
      var this_example;
      return this_example = new Example(this);
    });
    return $('form#suggestion-box').submit(function(e) {
      e.preventDefault();
      submitSuggestion();
      return false;
    });
  });

}).call(this);
