window.onload = function(){
    get_articles()
}
function get_articles(){
    var request = new XMLHttpRequest()
    var url = "http://127.0.0.1:5000/api/article.list"
    request.onreadystatechange = function(){
        if(request.readyState == 4 && request.status == 200){
            var jsonObj = JSON.parse(request.responseText)
            if(jsonObj['status'] == 'OK'){
                var num=jsonObj['num_of_articles']
                var blog=document.getElementById('blog')
                for(var i=1; i<=num ; i++){
                    var article=jsonObj[i]
                    var article_class=document.createElement('div')
                    article_class.className='articles'
                    article_class.innerHTML=
                    '<h3>'+article.title+'</h3><hr><span><i class="fa fa-folder-o" aria-hidden="true"></i> '+
                    article.category+'</span><span><i class="fa fa-tags" aria-hidden="true"></i> '+
                    article.tags+'</span>'+'<span><i class="fa fa-eye" aria-hidden="true"></i> '+
                    article.num_of_view+'</span>' + '<span><i class="fa fa-clock-o" aria-hidden="true"></i> '+
                    article.public_time + '/' + article.update_time +
                    '<a href="'+ article.url+'">> Read More</a>'
                    blog.appendChild(article_class)
                }
            }
        }
    }
    request.open('GET',url,true)
    request.send()
}
