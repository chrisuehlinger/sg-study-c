var delay = 1000;

var start_prep = function(){
	var figure = $('#pre-processor');

	var title = figure.find('h3');
	title.text('Before Pre-Processor');

	var inc_local = figure.find("#inc_local").text('#include"hello_func.h"');
	var inc_lib = figure.find("#inc_lib").text('#include<stdio.h>');
	var comments = figure.find('#comment').show();
	var const_def = figure.find("#def_constant").show();
	var const_inst = figure.find("#constant_inst").text('THE_OUTPUT');

	window.setTimeout(function(){
		prep_include(figure);
	}, delay);
};

var prep_include = function(figure){
	var title = figure.find('h3');
	title.text('Copying #included files...');

	var inc_local = figure.find("#inc_local");
	inc_local.addClass('running');

	var inc_lib = figure.find("#inc_lib");
	inc_lib.addClass('running');

	window.setTimeout(function(){
		inc_local.removeClass('running');
		inc_local.text('void say_hello(int num_times);');

		inc_lib.removeClass('running');
		inc_lib.text('"stdio.h is huge. Just pretend it\'s here."')

		window.setTimeout(function(){
			prep_comments(figure);
		}, delay)
	}, delay);
};

var prep_comments = function(figure){
	var title = figure.find('h3');
	title.text('Removing Comments...');

	var comments = figure.find('#comment');
	comments.addClass('running');

	window.setTimeout(function(){
		comments.removeClass('running');
		comments.hide();
		window.setTimeout(function(){
			prep_constants(figure);
		}, delay);
	}, delay);
};

var prep_constants = function(figure){
	var title = figure.find('h3');
	title.text('Replacing #defined constants...');

	var const_def = figure.find("#def_constant");
	var const_inst = figure.find("#constant_inst");

	const_def.addClass('running');
	const_inst.addClass('running');

	window.setTimeout(function(){
		title.text('Pre-processor finished');
		const_def.removeClass('running');
		const_def.hide();

		const_inst.removeClass('running');
		const_inst.text('"Hello World!"')
		window.setTimeout(start_prep, 5000);
	}, delay);
};

var main_c = 'void say_hello(int num_times);\nint main(void)\n{\n\tsay_hello(2);\n\treturn;\n}'
var hello_func_c = 'void say_hello(int num_times)\n{\n\tint i;\n\tfor(i=1; i<= num_times; i++)\n\t\tprintf("Hello World!");\n}'
var main_asm = ".Ltext0:\n.globl	main\nmain:\n.LFB0:\n.cfi_startproc\npushq	%rbp\n.LCFI0:\n.cfi_def_cfa_offset 16\n.cfi_offset 6, -16\nmovq	%rsp, %rbp\n.LCFI1:\n.cfi_def_cfa_register 6\nmovl	$2, %edi\ncall	say_hello\npopq	%rbp\n.LCFI2:\n.cfi_def_cfa 7, 8\nret\n.cfi_endproc\n.LFE0:\n.Letext0:";
var hello_func_asm = '.Ltext0:\n.section	.rodata\n.LC0:\n.string	"Hello World!"\n.text\n.globl	say_hello\nsay_hello:\n.LFB0:\n.cfi_startproc\npushq	%rbp\n.LCFI0:\n.cfi_def_cfa_offset 16\n.cfi_offset 6, -16\nmovq	%rsp, %rbp\n.LCFI1:\n.cfi_def_cfa_register 6\nsubq	$32, %rsp\nmovl	%edi, -20(%rbp)\nmovl	$1, -4(%rbp)\njmp	.L2\n.L3:\naddl	$1, -4(%rbp)\nmovl	$.LC0, %eax\nmovq	%rax, %rdi\nmovl	$0, %eax\ncall	printf\n.L2:\nmovl	-4(%rbp), %eax\ncmpl	-20(%rbp), %eax\njle	.L3\nleave\n.LCFI2:\n.cfi_def_cfa 7, 8\nret\n.cfi_endproc\n.LFE0:\n.Letext0:';
var main_o = '2e 4c 74 65 78 74 30 3a 5c 6e 2e 67 6c 6f 62 6c 09 6d 61 69 6e 5c 6e 6d 61 69 6e 3a 5c 6e 2e 4c 46 42 30 3a 5c 6e 2e 63 66 69 5f 73 74 61 72 74 70 72 6f 63 5c 6e 70 75 73 68 71 09 25 72 62 70 5c 6e 2e 4c 43 46 49 30 3a 5c 6e 2e 63 66 69 5f 64 65 66 5f 63 66 61 5f 6f 66 66 73 65 74 20 31 36 5c 6e 2e 63 66 69 5f 6f 66 66 73 65 74 20 36 2c 20 2d 31 36 5c 6e 6d 6f 76 71 09 25 72 73 70 2c 20 25 72 62 70 5c 6e 2e 4c 43 46 49 31 3a 5c 6e 2e 63 66 69 5f 64 65 66 5f 63 66 61 5f 72 65 67 69 73 74 65 72 20 36 5c 6e 6d 6f 76 6c 09 24 32 2c 20 25 65 64 69 5c 6e 63 61 6c 6c 09 73 61 79 5f 68 65 6c 6c 6f 5c 6e 70 6f 70 71 09 25 72 62 70 5c 6e 2e 4c 43 46 49 32 3a 5c 6e 2e 63 66 69 5f 64 65 66 5f 63 66 61 20 37 2c 20 38 5c 6e 72 65 74 5c 6e 2e 63 66 69 5f 65 6e 64 70 72 6f 63 5c 6e 2e 4c 46 45 30 3a 5c 6e 2e 4c 65 74 65 78 74 30 3a'
var hello_func_o = '2e 4c 74 65 78 74 30 3a 5c 6e 2e 73 65 63 74 69 6f 6e 09 2e 72 6f 64 61 74 61 5c 6e 2e 4c 43 30 3a 5c 6e 2e 73 74 72 69 6e 67 09 22 48 65 6c 6c 6f 20 57 6f 72 6c 64 21 22 5c 6e 2e 74 65 78 74 5c 6e 2e 67 6c 6f 62 6c 09 73 61 79 5f 68 65 6c 6c 6f 5c 6e 73 61 79 5f 68 65 6c 6c 6f 3a 5c 6e 2e 4c 46 42 30 3a 5c 6e 2e 63 66 69 5f 73 74 61 72 74 70 72 6f 63 5c 6e 70 75 73 68 71 09 25 72 62 70 5c 6e 2e 4c 43 46 49 30 3a 5c 6e 2e 63 66 69 5f 64 65 66 5f 63 66 61 5f 6f 66 66 73 65 74 20 31 36 5c 6e 2e 63 66 69 5f 6f 66 66 73 65 74 20 36 2c 20 2d 31 36 5c 6e 6d 6f 76 71 09 25 72 73 70 2c 20 25 72 62 70 5c 6e 2e 4c 43 46 49 31 3a 5c 6e 2e 63 66 69 5f 64 65 66 5f 63 66 61 5f 72 65 67 69 73 74 65 72 20 36 5c 6e 73 75 62 71 09 24 33 32 2c 20 25 72 73 70 5c 6e 6d 6f 76 6c 09 25 65 64 69 2c 20 2d 32 30 28 25 72 62 70 29 5c 6e 6d 6f 76 6c 09 24 31 2c 20 2d 34 28 25 72 62 70 29 5c 6e 6a 6d 70 09 2e 4c 32 5c 6e 2e 4c 33 3a 5c 6e 61 64 64 6c 09 24 31 2c 20 2d 34 28 25 72 62 70 29 5c 6e 6d 6f 76 6c 09 24 2e 4c 43 30 2c 20 25 65 61 78 5c 6e 6d 6f 76 71 09 25 72 61 78 2c 20 25 72 64 69 5c 6e 6d 6f 76 6c 09 24 30 2c 20 25 65 61 78 5c 6e 63 61 6c 6c 09 70 72 69 6e 74 66 5c 6e 2e 4c 32 3a 5c 6e 6d 6f 76 6c 09 2d 34 28 25 72 62 70 29 2c 20 25 65 61 78 5c 6e 63 6d 70 6c 09 2d 32 30 28 25 72 62 70 29 2c 20 25 65 61 78 5c 6e 6a 6c 65 09 2e 4c 33 5c 6e 6c 65 61 76 65 5c 6e 2e 4c 43 46 49 32 3a 5c 6e 2e 63 66 69 5f 64 65 66 5f 63 66 61 20 37 2c 20 38 5c 6e 72 65 74 5c 6e 2e 63 66 69 5f 65 6e 64 70 72 6f 63 5c 6e 2e 4c 46 45 30 3a 5c 6e 2e 4c 65 74 65 78 74 30 3a';

var start_comp = function(){
	var figure = $('#compiler');

	var title = figure.find('h3');
	title.text('Before Compiler')

	var file_ext = figure.find('.file-ext');
	file_ext.text('c');

	var main_file = figure.find('#main');
	main_file.text(main_c);

	var hello_func_file = figure.find('#hello_func')	
	hello_func_file.text(hello_func_c);

	window.setTimeout(function(){
		comp_asm(figure);
	}, delay);
};

var comp_asm = function(figure){
	var title = figure.find('h3');
	title.text('Compiling to Assembly...')

	var main_file = figure.find('#main').addClass('running');
	var hello_func_file = figure.find('#hello_func').addClass('running');

	window.setTimeout(function(){
		var file_ext = figure.find('.file-ext');
		file_ext.text('asm');

		main_file.text(main_asm).removeClass('running');
		hello_func_file.text(hello_func_asm).removeClass('running');
		
		window.setTimeout(function(){
			comp_o(figure);
		}, delay)
	}, delay);
}

var comp_o = function(figure){
	var title = figure.find('h3');
	title.text('Compiling to Object Code...')

	var main_file = figure.find('#main').addClass('running');
	var hello_func_file = figure.find('#hello_func').addClass('running')	
	

	window.setTimeout(function(){
		var file_ext = figure.find('.file-ext');
		file_ext.text('o');

		main_file.text(main_o).removeClass('running');
		hello_func_file.text(hello_func_o).removeClass('running');

		title.text('Finished Compiling')
		window.setTimeout(start_comp, 5000);
	}, delay);
}


$(document).ready(function(){
	setTimeout(start_prep, 10);
	setTimeout(start_comp, 10);
});