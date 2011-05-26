var rand;
function refresh(){
	$.getJSON('/api/getstate', function(data, status){
		if(data.state == "won") $("#state").html("Gewonnen!")
		if(data.state == "lost") $("#state").html("Verloren!")
		if(data.state == "noword") $("#state").html("Hallo!")
		if(data.state == "won" || data.state == "lost" || data.state == "noword"){			
			$(".overlay").fadeIn();		
		}else{
			$(".overlay").fadeOut();		
		}
		for(i=0;i<data.tried.length;i++){
			c = data.tried[i]
			$("#key"+c).css("opacity", 0.2);
		}
		if(rand != data.rand){
			$(".key").css("opacity", 1);
			rand = data.rand;
		}
		window.setTimeout(refresh, 300)
	});
}
function setword(){
	$.getJSON('/api/setword/'+$("#newword").val(), function(data, status){
			if(data.warning){
				alert("Das Wort ist entweder unlösbar (unmögliche Zeichen verwendet) oder 100% lösbar (mehr als 21 verschiedene Zeichen). Probiere ein anderes.");
			}else{
				refresh();
				$(".overlay").fadeOut();
			}
		});
}
function adjustsize(){
	if((
			$("#keyboard").width() <= window.innerWidth
		&&
			$("#keyboard").height() < window.innerHeight-20
	)){
		while(true){
			$(".key").css("font-size", parseInt($(".key").css("font-size").replace(/px/, ''))+1)
			if(!(
						$("#keyboard").width() <= window.innerWidth
					&&
						$("#keyboard").height() < window.innerHeight-20
				))
				break;
		}
	}else{
		while(true){
			$(".key").css("font-size", parseInt($(".key").css("font-size").replace(/px/, ''))-1)
			if(
						$("#keyboard").width() <= window.innerWidth
					&&
						$("#keyboard").height() < window.innerHeight-20
				)
				break;
		}
	}
}
$(document).ready(function(){
		adjustsize();
		$(".key").click(function(){
				c = $(this).html()
				if(c == "Ä") c = "a";
				if(c == "Ö") c = "o";
				if(c == "Ü") c = "u";
				if(c == "ß") c = "s";
				var ob = $(this);
				$.get('/api/char/'+c, function(){
						ob.css("opacity", 0.2);
					});
			});
		refresh();
	});

