//动画
function shake_box(id){
    var box = document.getElementById(id+'_box')
    box.className = 'shake animated'
}

//监听器清理动画
window.onload = function(){
    var list = ['username','email','password','password_confirm']
    var eventlist = ['webkitAnimationEnd','mozAnimationEnd','MSAnimationEnd','oanimationend','animationend']
    for(var i in list){
        var element = document.getElementById(list[i] + '_box')
        for(var e in eventlist){
            element.addEventListener(eventlist[e],function(){
                this.className = ''
            })
        }
    }
}

//检查表单
function check_form(){
    var formlist = ['username','email','password','password_confirm']
    //获取元素
    var elementmap = new Object()
    for(var i in formlist){
        elementmap[formlist[i]]=document.getElementById(formlist[i])
    }
    //检测用户名 邮箱 密码 是否合法
    var username = elementmap['username'].value
    var email = elementmap['email'].value
    var password = elementmap['password'].value
    var password_confirm = elementmap['password_confirm'].value
    var username_len = username.length
    var password_len = password.length
    var to_post = true
    //用户名
    if(username_len < 3 || username_len > 8){
        elementmap['username'].value = ''
        elementmap['username'].setAttribute('placeholder','用户名长度(3-8)个字符')
        shake_box('username')
        to_post = false
    }
    //邮箱
    /* 正则 */
    var email_reg = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    if(!email_reg.test(email)){
        elementmap['email'].value = ''
        elementmap['email'].setAttribute('placeholder','请输入合法邮箱')
        shake_box('email')
        to_post = false
    }
    //密码长度检测
    if(password_len < 6 || password_len > 18){
        elementmap['password'].value = ''
        elementmap['password'].setAttribute('placeholder','密码长度(6-18)个字符')
        shake_box('password')
        to_post = false
    }
    //重复密码检测
    if(password != password_confirm){
        elementmap['password_confirm'].value = ''
        elementmap['password_confirm'].setAttribute('placeholder','密码输入不相同')
        shake_box('password_confirm')
        to_post =false
    }

    //检测用户是否存在
    check_user(username)
    check_email(email)
    
    if(to_post){
        var params = 'username='+username+'&email='+email+'&password='+password
        post_form(params)
    }
}

//post 表单
function post_form(params){
    var request = new XMLHttpRequest()
    var url = '/register'
    request.open('POST',url,true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.send(params)
}

//调用接口检测用户和邮箱是否存在 TODO:需要接口
function check_user(username){
    var request = new XMLHttpRequest()
    var url = '/check/user/' + username
    request.open('GET',url,true)
    request.onreadystatechange = function(){
        if(request.readyState == 4 && request.status == 200){
            var jsonObj = JSON.parse(request.responseText)
            if(jsonObj['is_exist_user']){
                document.getElementById('username').value = ''
                document.getElementById('username').setAttribute('placeholder','用户已注册！')
                shake_box('username') 
            }
        }
    }
    request.send()
}

function check_email(email){
    var request = new XMLHttpRequest()
    var url = '/check/user/' + email
    request.open('GET',url,true)
    request.onreadystatechange = function(){
        if(request.readyState == 4 && request.status == 200){
            var jsonObj = JSON.parse(request.responseText)
            if(jsonObj['is_exist_email']){
                document.getElementById('email').value = ''
                document.getElementById('email').setAttribute('placeholder','邮箱已注册！')
                shake_box('email') 
            }
        }
    }
    request.send()
}