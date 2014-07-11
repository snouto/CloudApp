$(document).ready(function(){
	


    returnRecommendation();




       function returnRecommendation(){

     var articleID = getParameterByName('articleID');

	 var apiURL = '/search/recommendation?articleID='+articleID;
	 $.getJSON(apiURL,function(r){

	        var results = r;

	        var recommendationDiv = $('<div>',{id:'recommendation'});

	        if(results.length){

	            for(var i=0;i<results.length;i++){
					// Creating a new result object and firing its toString method:
					recommendationDiv.append(new newResult(results[i]) + '');
				}


	        }else
	        {
	            //empty the recommendation div

	        }

	 });

	}

	function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

function newResult(r){

           var arr = [
					'<div class="webResult">',
					'<h2><a href="/search/?s=',r.id,'" target="_blank">',r.title,'</a></h2>',
					'<p>',r.abstract,'</p>',
					'<a href="/search/viewArticle?articleID=',r.id,'" target="_blank">Read More</a>',
					'</div>'
				];

				// The toString method.
            this.toString = function(){
                return arr.join('');
            }



	}

	
});


