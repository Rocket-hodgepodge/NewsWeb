$(function () {
    $('#search_form').submit(function (e) {
        $(this).preventDefault();
    });
    getNewsTitleList(1);
    $('#page_box').page({
       leng: 10,//分页总数
       activeClass: 'activP' , //active 类样式定义
       clickBack:function(page){
           getNewsTitleList(page)
       }
    });
    $('#search_btn').on('click', function (e) {
        getNewsTitleList(1);
    });
    function getNewsTitleList(page) {
        var title = $('#search_input').val();
        $.get('/news/newsSearch/?page='+page+'&title='+title+'&order=-publish_time', function (data) {
            var news_title_list = data.content;
            var htmlstr = "";
            for (var i=0; i < news_title_list.length; i++){
                htmlstr += "<li class='list'>" +
                    "<span>["+news_title_list[i].publish_time+"]</span>" +
                    "<a href='/home/showNews/"+news_title_list[i].id+"/' title='"+news_title_list[i].title+"' target='_self'>"+news_title_list[i].title+"</a>" +
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

