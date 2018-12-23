
/* Ready Function */

$(document).ready(function(){

	/* Definitions */
	var inputText = "";
	var outputText = "";
	var langSel = "langA" ;

	/* Clear the input/output fields */
	$("#inputText").val("");
	$("#outputLbl").val("");
	$("#langSel").val("");


	$("#submitBtn").click(function(){
		inputText=$("#inputText").val();
		langSel=$("#langSel").val();
		$.ajax({url: "/transfer", data: {o:inputText, j:langSel}, type: "GET", dataType: "json",})
			.done(function(json) {
				$("#outputLbl").html(function() {
					content = "";
					for (item in json) {
						if (! item.tag) content += "<li>" + item.text + "</li>";
						else content += "<li>" + item.text + "</li>";
					}
					return content;
				});
			})

	});


});



