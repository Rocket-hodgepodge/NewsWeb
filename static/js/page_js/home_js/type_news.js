$(function () {
   $.get('/news/getFollowNews/', function (data) {
       if (data.code === 200){
          let html_str = '';
          let newslist = $('#news_list');
          for (let i = 0; i < data.news_list.length; i++) {
             let news_obj = data.news_list[i];
             html_str += "<li class='list'>" +
                 "<span>["+news_obj.publish_time+"]</span>" +
                 "<a href='/home/showNews/"+news_obj.id+"/' title='"+news_obj.title+"' target='_self'>"+news_obj.title+"</a>" +
                 "<img class='listhot' src='/static/img/home_img/fire.png' alt='hot'/>\n" +
                 "</li>"
          }
          newslist.html(html_str);
       }else {
          alert(data.msg)
       }
   })
});