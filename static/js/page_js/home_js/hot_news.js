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
        $.get('/news/getNewsOrder/?page='+page+'&order=-read_total', function (data) {
            let news_list = data.news_list;
            let htmlstr = "";
            for (let i=0; i < news_list.length; i++){
                htmlstr += "<li class='list'>" +
                    "<span>["+news_list[i].publish_time+"]</span>" +
                    "<a href='/news/showNews/"+news_list[i].id+"/' title='"+news_list[i].title+"' target='_self'>"+news_list[i].title+"</a>" +
                    "<img class='listhot' src='/static/img/home_img/new_ico.png' alt='图片关键词'/>" +
                    "</li>";
            }
            $('#news_list').html(htmlstr);
        })
    }
});