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
                /* article nums */
                var num=jsonObj['num_of_articles']
                var blog=document.getElementById('article')

                for(var i=1; i<=num ; i++){
                    var article=jsonObj[i]
                    /* append list append_article<-module<-footer */
                    var append_article=document.createElement('article')
                    var module=document.createElement('div')
                    var footer=document.createElement('footer')

                    /* TODO IF NONE */
                    var category=''
                    var tags=''
                    /* title */
                    var title = '<a class="title" href="'+article.url+'">' + article.title+
                                     '</a><p></p><p>'+'内容概要'+'</p><p></p>' 
                    /* category */
                    for(var c=0;c<article.category.length;c++){
                        category='<a class="word-keep" href="#"><span class="octicon octicon-book"></span>&nbsp;'+
                                    article.category
                    }
                    /* tags */
                    for(var t=0;t<article.tags.length;t++){
                        tags+='</a><a class="word-keep" href="'+ 'api/article.list?tag='+ article.tags[t] +'"><span class="octicon octicon-tag"></span>&nbsp;'+article.tags[t]+'</a>'
                    }
                    
                    /* date */
                    var date='<a><span class="octicon octicon-clock"></span>&nbsp;'+article.update_time+'</a>'
                    
                    /* num_of_view */
                    var num_of_view='<a><span class="octicon octicon-star"></span>&nbsp;'+article.num_of_view+'</a>'

                    /* module */
                    module.className='module'
                    module.innerHTML=title

                    /* footer */
                    footer.innerHTML=category+tags+
                    '<span class="word-keep pull-right">' +  
                    date+num_of_view+
                    '<a class="readmore" href="#">Read More</a></span>'

                    /* append */
                    module.appendChild(footer)
                    append_article.appendChild(module)                    
                    blog.appendChild(append_article)
                }
            }
        }
    }
    request.open('GET',url,true)
    request.send()
}
