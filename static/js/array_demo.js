var delay=1500;

var start_animation = function(){
	var figure = $('figure.run');

	var table = figure.find('table');
	var code = figure.find('div.code');

	var default_values = new Array(34, 1, 180, 92, 17, 17, 0, 12);
	for (var i = 1; i <=8; i++) {
		var arr_item = table.find('tr:nth-child(2)').find(':nth-child(' + i + ')');
		arr_item.text(default_values[i-1]);
		arr_item.addClass('.changed');
	}

	var running_code = code.find('#create-array');
	running_code.addClass('running');


	window.setTimeout(function(){
		for (var i = 1; i <=8; i++) {
			var arr_item = table.find('tr:nth-child(2)').find(':nth-child(' + i + ')');
			arr_item.removeClass('.changed');
		}
		running_code.removeClass('running');
		init_i(figure);
	}, delay);
}

var init_i = function(figure){
	var code = figure.find('div.code');

	var running_code = code.find('#init');
	running_code.addClass('running');

	window.setTimeout(function(){
			running_code.removeClass('running');
			cond(figure, 1);
		}, delay);

};

var cond = function(figure, index) {
	var code = figure.find('div.code');
	var running_code = code.find('#cond');
	running_code.addClass('running');

	if(index <= 8)
		window.setTimeout(function(){
			running_code.removeClass('running');
			change_item(figure, index);
		}, delay);
	else
		window.setTimeout(function(){
			running_code.removeClass('running');
			start_animation(figure);
		}, delay);
};

var change_item = function(figure, index){
	var table = figure.find('table');

	var arr_item = table.find('tr:nth-child(2)').find(':nth-child(' + index + ')');
	arr_item.text(parseInt(arr_item.text()) + 1);
	arr_item.addClass('changed');

	var index_item = table.find('tr:nth-child(1)').find(':nth-child(' + index + ')');
	index_item.addClass('selected-index');

	var code = figure.find('div.code');
	var running_code = code.find('#inc-array');
		running_code.addClass('running');

	window.setTimeout(function(){
		arr_item.removeClass('changed');
		index_item.removeClass('selected-index');
		running_code.removeClass('running');
		inc(figure,index);
	}, delay);
}

var inc = function(figure, index){
	var code = figure.find('div.code');
	var running_code = code.find('#inc');
	running_code.addClass('running');

	window.setTimeout(function(){
		running_code.removeClass('running');
		cond(figure, index+1);
	}, delay);
};



$(document).ready(start_animation);