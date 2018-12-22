
/* Ready Function */

$(document).ready(function(){

	/* Definitions */
	var inputText = "";
	var outputText = "";
	var langSel = "langA" ;

	/* Clear the input/output fields */
	$("#inputText").val("");
	$("#outputLbl").val("");
	$("#langSel").val("langA");


	$("#submitBtn").click(function(){
		inputText=$("#inputText").val();
		langSel=$("#langSel").val();
		outputText=transfer(inputText);
		$("#outputLbl").html(langSel + " : " + inputText + outputText);


	});


});

function transfer(query, syncResults, asyncResults)
{
    // Get places matching query (asynchronously)
    let parameters = {
        original: query
    };
    $.getText("/transfer", parameters, function(data, textStatus, jqXHR) {

        // Call typeahead's callback with search results (i.e., places)
        asyncResults(data);
    });
}
