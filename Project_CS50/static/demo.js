
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
					let content = "";
					var n = json.length;
					for (var i=0; i < n; i++) {
						if (json[i].tag) content += "<p>" + json[i].text + "</p>";
						else content += '<p style="color:red">' + json[i].tag + "</p>";
					}
					return content;
				});
			})

	});


});



