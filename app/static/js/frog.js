/* post json */
var post_data = function(url,data,callback){
    var request = new XMLHttpRequest()
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8')
    request.onreadystatechange = function(){
        if(request.readyState == XMLHttpRequest.DONE && request.status == 200){
            callback(request.responseText)
        }
    }
    request.open('POST',url,true)
    request.send(data)
}
/* get json */
var get_data = function(url,callback){
    var request = new XMLHttpRequest()
    /* callback */
    request.onreadystatechange = function(){
        if(request.readyState == XMLHttpRequest.DONE && request.status == 200){
            callback(request.responseText)
        }
    }
    request.open('GET',url,true)
    request.send()
}
 /*获取参数*/
var getUrlParam = function(name){
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); 
    var r = window.location.search.substr(1).match(reg);  
    if (r != null) return unescape(r[2]); return null; 
}