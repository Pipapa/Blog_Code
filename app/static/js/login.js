//显示密码 
var show_password = function(){
    document.getElementById('password').setAttribute('type','text')
    document.getElementById('icon_password').setAttribute('src','statics/images/icon_password_cansee.png')
}
var hidden_password = function(){
    document.getElementById('password').setAttribute('type','password')
    document.getElementById('icon_password').setAttribute('src','statics/images/icon_password.png')
}

//动画
function shake_box(id){
    document.getElementById(id+'_box').className = 'shake animated'
}
//清理动画
function clear_box(list){
    for(var i in list){
        document.getElementById(list[i]+'_box').className = ''
    }
}

//登录检测
function check_form(){
    var username = document.getElementById('username').value
    var password = document.getElementById('password').value

    if(username && password){
        var form = 'username='+username+'&password='+password
        //检测
        post_form(form)
        get_status()
    }else{
        if(!password){shake_box('password')}
        if(!username){shake_box('username')}
    }
}

//POST登录表单
function post_form(post_params){
    //采用ajax异步处理
    var request = new XMLHttpRequest()
    var url = "/login"
    request.open("POST",url,true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.send(post_params)
}

//GET获取登录状态
function get_status(){
    var request = new XMLHttpRequest()
    var url = "/check/user/me.json"
    request.onreadystatechange = function(){
        if(request.readyState == 4 && request.status == 200){
            var jsonObj = JSON.parse(request.responseText)
            if(jsonObj['is_login']){
                /* 登录成功 */
            }else{
                document.getElementById('password').value = ''
                document.getElementById('password').setAttribute('placeholder','密码错误!')
                shake_box('password')
            }
        }
    }
    request.open("GET",url,true)
    request.send()
}