// Generated by CoffeeScript 1.6.3
(function() {
  $(document).delegate('#submission', 'keydown', function(e) {
    var end, keyCode, start;
    keyCode = e.keyCode || e.which;
    if (keyCode === 9) {
      e.preventDefault();
      start = $(this).get(0).selectionStart;
      end = $(this).get(0).selectionEnd;
    }
    $(this).val($(this).val().substring(0, start) + "\t" + $(this).val().substring(end));
    $(this).get(0).selectionStart = start + 1;
    $(this).get(0).selectionEnd = start + 1;
    return true;
  });

}).call(this);
