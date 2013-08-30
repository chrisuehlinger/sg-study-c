delay = 1500

start_animation = ->
	figure = $('figure.run')

	table = figure.find 'table'
	code = figure.find 'div.code'

	default_values = new Array 34, 1, 180, 92, 17, 17, 0, 12
	for i in [1..8]
		arr_item = table.find('tr:nth-child(2)').find ':nth-child(' + i + ')'
		arr_item.text default_values[i-1]
		arr_item.addClass 'changed'

	running_code = code.find '#create-array'
	running_code.addClass 'running'


	window.setTimeout ->
		for i in [1..8]
			arr_item = table.find('tr:nth-child(2)').find ':nth-child(' + i + ')'
			arr_item.removeClass 'changed'
		
		running_code.removeClass 'running'
		init_i figure
	, delay


init_i = (figure) ->
	code = figure.find 'div.code'

	running_code = code.find '#init'
	running_code.addClass 'running'

	window.setTimeout ->
		running_code.removeClass 'running'
		cond figure, 1
	, delay

cond = (figure, index) ->
	code = figure.find 'div.code'
	running_code = code.find '#cond'
	running_code.addClass 'running'

	if index <= 8
		window.setTimeout ->
			running_code.removeClass 'running'
			change_item figure, index
		, delay
	else
		window.setTimeout ->
			running_code.removeClass 'running'
			start_animation figure
		, delay


change_item = (figure, index) ->
	table = figure.find 'table'

	arr_item = table.find('tr:nth-child(2)').find ':nth-child(' + index + ')'
	console.log index + ": " + arr_item.text()
	arr_item.text parseInt(arr_item.text()) + 1
	arr_item.addClass 'changed'

	index_item = table.find('tr:nth-child(1)').find ':nth-child(' + index + ')'
	index_item.addClass 'selected-index'

	code = figure.find 'div.code'
	running_code = code.find '#inc-array'
	running_code.addClass 'running'

	window.setTimeout ->
		arr_item.removeClass 'changed'
		index_item.removeClass 'selected-index'
		running_code.removeClass 'running'
		inc figure,index
	, delay

inc = (figure, index) ->
	code = figure.find 'div.code'
	running_code = code.find '#inc'
	running_code.addClass 'running'

	window.setTimeout ->
		running_code.removeClass 'running'
		cond figure, index+1
	, delay

$(document).ready start_animation