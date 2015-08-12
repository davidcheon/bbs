$(function(){
	var B=setInterval(function(){
	var aj=$.ajax({type:'Get',
		dataType:'json',
			url:'/getonlineusers/',
			cache:false,
			success:function(data){
				$('#onlineusers').empty();
					for(var i=0;i<data.length;i++){
						var h='<li><a href="/chatwith/'+data[i]+'/">'+data[i]+'</a></li>';
						$('#onlineusers').append(h);
					}
				
			}});
	},10000);
//	alert(decodeURIComponent(document.cookie.split(';')[0].substring(10)));
//	alert(document.cookie);
//	alert(getcookie('csrftoken'));
	
});
function sendmessage(obj){
//	datas=obj.content.value;
	
	var aj=$.ajax({
		url:'/sendmessage/',
		type:'POST',
		data:$("#sendmessageform").serialize(),
		dataType:'json',
		success:function(data){
			var fromuser="<div><p class='sendfromuser'>"+data.fromuser+"</p></div>";
			var content="<div><p class='onemessage'>"+data.content+"</p></div>";
			var senddate="<div class='to_right_show'><p class='senddate'>"+data.senddate+"</p></div><hr/>";
			$("#message").append(fromuser);
			$("#message").append(content);
			$("#message").append(senddate);
			$("#id_content").val("");
		},
		error:function(error){
			alert('send error occured!');
		},
	});
	return false;
}
function bbs_delete(id){
	var result=confirm('are you sure to delete?');
	if (result){
	$.ajax({
		url:'/bbs_remove/'+id+'/',
		type:'GET',
		success:function(data){
			if(data=='success'){
				var divid="#bbs_"+id;
				$(divid).remove();
			}else if (data=='error'){
				alert('error:'+data);
			}
		},
		error:function(data){
		},
	});
	}
}
function getcookie(name){
	var cookies=document.cookie.split(";");
	var cookvalue=null;
	for(var i=0;i<cookies.length;i++){
		var cookie=jQuery.trim(cookies[i]);
		if (cookie.substring(0,name.length+1)==name+'='){
			cookvalue=cookie.substring(name.length+1);
			break;
		}
	}
	return cookvalue;
}