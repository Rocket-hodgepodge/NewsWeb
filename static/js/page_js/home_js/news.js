$(function () {
    getNewsList(1);
    $('#page_box').page({
       leng: 10,//分页总数
       activeClass: 'activP' , //active 类样式定义
       clickBack:function(page){
           getNewsList(page)

       }
    });
    // $('#page_box').simplePaging();
    function getNewsList(page) {
        $.get('/news/getNewsOrder/?page='+page+'&order=-publish_time', function (data) {
            let news_list = data.news_list;
            let htmlstr = "";
            for (let i=0; i < news_list.length; i++){
                htmlstr += "<li class='list'>" +
                    "<span>["+news_list[i].publish_time+"]</span>" +
                    "<a href='/home/showNews/"+news_list[i].id+"/' title='"+news_list[i].title+"' target='_self'>"+news_list[i].title+"</a>" +
                    "<img class='listhot' src='/static/img/home_img/new_ico.png' alt='图片关键词'/>\n" +
                    "</li>";
            }
            $('#news_list').html(htmlstr);
        })
    }
    $('#logout_a').on('click', function (e) {
        $.get('/user_operation/logout/', function (data) {
            if (data.code === 200){
                window.location.href = '/';
            }else {
                alert('注销错误！');
            }
        });
    });
});
