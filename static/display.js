var fs = "3px";
var rand;
function refresh(){
	$.getJSON('/api/getstate', function(data, status){
		if(data.state == 'playing'){
			if('img/0'+data.fails+'.png' != $("#top img").attr("src"))
				$("#top img").attr("src", 'img/0'+data.fails+'.png')
		}else if(data.state == 'won'){
			if('img/won.png' != $("#top img").attr("src"))
				$("#top img").attr("src", 'img/won.png')
		}else if(data.state == 'lost'){
			if('img/lost.png' != $("#top img").attr("src"))
				$("#top img").attr("src", 'img/lost.png')
		}
		newl = ""
		for(i=0;i<data.progress.length;i++){
			c = data.progress[i]
			if(c == "a") c = "Ä";
			if(c == "o") c = "Ö";
			if(c == "u") c = "Ü";
			if(c == "s") c = "ß";
			newl += '<span class="letter" style="font-size: '+fs+'">'+c+'</span> '
		}
		if(newl != $("#letters").html())
			$("#letters").html(newl)
		if(rand != data.rand){
			adjustsize();
			rand = data.rand;
		}
		window.setTimeout(refresh, 300)
	});
}
function adjustsize(){
	if($(".letter").length == 0) return;
	if(
						$("#letters").width() < window.innerWidth
					&&
						$("#letters").height() < window.innerHeight/2
		){
			while(true){
					$(".letter").css("font-size", parseInt($(".letter").css("font-size").replace(/px/, ''))+1)
					if(!(
								$("#letters").width() < window.innerWidth
							&&
								$("#letters").height() < window.innerHeight/2
						))
						break;
				}
					
		}else{
			while(true){
					$(".letter").css("font-size", parseInt($(".letter").css("font-size").replace(/px/, ''))-1)
					if(
								$("#letters").width() < window.innerWidth
							&&
								$("#letters").height() < window.innerHeight/2
						)
						break;
				}
		}
	fs = $(".letter").css("font-size");
}
$(document).ready(function(){
		$("#top").height(window.innerHeight/2);
		$("#top img").height(window.innerHeight/2);
		$("#bottom").height(window.innerHeight/2);
		refresh();
	});
