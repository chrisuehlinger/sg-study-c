delay = 1000

$(document).ready ->
	wrongAnimation 0
	rightAnimation 0

wrongAnimation = (step) ->

	if step == 0
		$('#wrongInput').text ' '
		
	if step == 1
		$('#wrong1').addClass 'running'

	if step == 2
		$('#wrong1').removeClass 'running'
		$('#wrongInput').text 'd, I don\'t know...\\n'

	if step == 3
		$('#wrong2').addClass 'running'
		$('#wrongInput').text ', I don\'t know...\\n'

	if step == 4
		$('#wrong2').removeClass 'running'
		$('#wrong3').addClass 'running'

	if step == 5
		$('#wrong3').removeClass 'running'
		$('#wrong4').addClass 'running'
		$('#wrongInput').text ' I don\'t know...\\n'

	if step == 6
		$('#wrong4').removeClass 'running'
		window.setTimeout (-> wrongAnimation 0 ), 5*delay
	else
		window.setTimeout (-> wrongAnimation step+1 ), delay

rightAnimation = (step) ->

	if step == 0
		$('#rightInput').text ' '
		
	if step == 1
		$('#right1').addClass 'running'

	if step == 2
		$('#right1').removeClass 'running'
		$('#rightInput').text 'd, I don\'t know...\\n'

	if step == 3
		$('#right2').addClass 'running'
		$('#rightInput').text ', I don\'t know...\\n'

	if step == 4
		$('#right2').removeClass 'running'
		$('#right3').addClass 'running'

	if step == 5
		$('#right3').removeClass 'running'
		$('#right4').addClass 'running'

		if $('#rightInput').text().length > 2
			$('#rightInput').text $('#rightInput').text().substring 1
		else
			$('#rightInput').text ' '
		window.setTimeout (-> rightAnimation step+1 ), .1*delay

	if step == 6
		$('#right4').removeClass 'running'
		$('#right3').addClass 'running'
		if $('#rightInput').text() == ' '
			window.setTimeout (-> rightAnimation step+1 ), .1*delay
		else
			window.setTimeout (-> rightAnimation step-1 ), .1*delay
			


	if step == 7
		$('#right3').removeClass 'running'
		$('#right4').removeClass 'running'
		$('#right5').addClass 'running'

	if step == 8
		$('#right5').removeClass 'running'
		$('#rightInput').text 'a, I think...\\n'

	if step == 9
		$('#right6').addClass 'running'
		$('#rightInput').text ', I think...\\n'

	if step == 10
		$('#right6').removeClass 'running'
		window.setTimeout (-> rightAnimation 0 ), 5*delay
	else if step != 5 and step != 6
		window.setTimeout (-> rightAnimation step+1 ), delay
