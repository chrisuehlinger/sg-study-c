delay = 500

randGen = ->
	no_bound = $("#rand-no-bound").find '.rand'
	no_bound.text Math.floor(Math.random()*32767)

	bound_100 = $("#rand-bound-100").find '.rand'
	bound_100.text Math.floor(Math.random()*100)

	bound_50_100 = $("#rand-50-100").find '.rand'
	bound_50_100.text Math.floor((Math.random()*51)+50)

	dice = $("#dice").find '.rand'
	dice.text Math.floor((Math.random()*6)+1)

	window.setTimeout randGen, delay

$(document).ready randGen