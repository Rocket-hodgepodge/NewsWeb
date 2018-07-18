$(function () {
    $.get('/home_page/followNews/', function (data) {
        let follow_list = $('#follow_list');
        if (data.code === 200) {
            //<li class='list top'><span class='time'>2012-07-16</span><a href='#' >PHP技术支持</a></li>
            for (let i = 0; i < data.data.length; i++){
                let my_span = $('<span>').attr('class', 'time').html(data.data[i].publish_time);
                let my_a = $('<a>').attr('href', '/home/showNews/'+data.data[i].id+'/').html(data.data[i].title);
                let my_li = $('<li>').attr('class', 'list').append(my_span).append(my_a);
                follow_list.append(my_li);
            }
        }  else {
            let my_a = $('<a>').attr('href', '/user_operation/login/').html('您还没有登录哦,点我登录哦');
            let my_li = $('<li>').attr('class', 'list').append(my_a);
            follow_list.append(my_li);
        }
    });

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
