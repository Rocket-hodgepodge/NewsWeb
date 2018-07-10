$(function () {
    getAllType();
    function getAllType() {
        $.get('/home/typeCount/', function (data) {
            var html_str = '';
            if (data.code === 200){
                var typlist = data.type_list;
                for (let i=0; i < typlist.length; i++){
                    let is_follow = typlist[i].isFollow;
                    let follow_str = '';
                    let class_str = '';
                    if (is_follow){
                        follow_str = '取消关注';
                        class_str = 'btn-default'
                    } else {
                        follow_str = '关注';
                        class_str = 'btn-success'
                    }
                    html_str += "<dl class=\"list-none navnow\">" +
                        "<dt id='part2_4'>" +
                        "<a href='/home/newsType/"+typlist[i].id+"/' title='"+typlist[i].name+"' class=\"zm\"><span>"+typlist[i].name+"("+typlist[i].total+")</span></a>" +
                        "<button t_id='"+typlist[i].id+"' class='btn is_follow_"+is_follow+" "+class_str+" btn-xs'>"+follow_str+"</button>"+
                        "</dt>" +
                        "</dl>"
                }
            } else {
                html_str = "<dl class=\"list-none navnow\">\n" +
                    "<dt id='part2_4'><a href='#' title='数据加载失败' class=\"zm\"><span>数据加载失败请检查网络!</span></a></dt>\n" +
                    "</dl>"
            }
            html_str += '<div class="clear"></div>';
            $('#sidebar').html(html_str);
            setEventListener()
        });
    }
    function setEventListener() {
        $('.is_follow_0').on('click', function (e) {
            let type_id = $(this).attr('t_id');
            let csrf = $("input[name='csrfmiddlewaretoken']").val();
            $.ajax('/news/addFollow/', {
                type: 'POST',
                headers: {"X-CSRFtoken": csrf},
                data: {type_id: type_id},
                success: function (data) {
                    if (data.code === 200){
                        // alert(data.msg);
                        let btn_obj = $("button[t_id='"+type_id+"']");
                        btn_obj.unbind('click');
                        btn_obj.attr('class', 'btn is_follow_1 btn-default btn-xs').html('取消关注');
                        setEventListener();
                    } else {
                        alert(data.msg);
                    }
                }
            })
        });
        $('.is_follow_1').on('click', function (e) {
            let type_id = $(this).attr('t_id');
            let csrf = $("input[name='csrfmiddlewaretoken']").val();
            $.ajax('/news/rmFollow/'+type_id+'/', {
                type: 'DELETE',
                headers: {"X-CSRFtoken": csrf},
                success: function (data) {
                    if (data.code === 200){
                        // alert(data.msg);
                        // console.log()
                        // e.attr('class', 'btn is_follow_0 btn-success btn-xs').html('关注');
                        let btn_obj = $("button[t_id='"+type_id+"']");
                        btn_obj.unbind('click');
                        btn_obj.attr('class', 'btn is_follow_0 btn-success btn-xs').html('关注');
                        setEventListener();
                    } else {
                        alert(data.msg)
                    }
                }
            })
        })

    }
});