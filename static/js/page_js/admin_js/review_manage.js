$(function () {
    $('#success_info').hide();
    $('#warning_info').hide();
    var csrf = $("input[name='csrfmiddlewaretoken']").val();
    $('#review_table').bootstrapTable({
        url: '/review/reviews/',  // 请求地址
        method: 'GET',  // 请求方法
        dataType: "json",  // 请求数据
        striped: true, // 隔行变色
        pagination: true, // 分页
        paginationLoop: false,  // 是否无限循环
        sidePagination: 'server',  // 服务器实现分页
        sortable: true,           //是否启用排序
        pageNumber: 1,  // 初始页号
        pageSize: 10,  // 初始页面行数
        pageList: [10, 25, 50, 100],  // 科学选择的每页多少行
        uniqueId: "id", //每一行的唯一标识，一般为主键列
        queryParams: queryParams, // q请求参数
        // 表头和数据过滤值
        columns: [{
            field: 'id',
            title: '评论ID'
        }, {
            field: 'news_id',
            title: '新闻ID'
        }, {
            field: 'user_id',
            title: '用户ID'
        }, {
            field: 'user_name',
            title: '昵称'
        }, {
            field: 'rev_content',
            title: '评论内容',
        }, {
            field: 'liked_num',
            title: '赞数量',
        }, {
            field: 'unliked_num',
            title: '踩数量',
        }, {
            field: 'time',
            title: '评论时间',
        }, {
            field: 'option',
            title: '操作',
            formatter: function (value, row, index) {
                var del_btn = '<button r_id="' + row.id + '" class="del_btn btn btn-danger btn-xs">删除</button>';
                return del_btn
            }
        }],
        onLoadSuccess: function () {
            //设置按钮的监听事件
            setEventListener()
        },
        onLoadError: function (status) {

        }
    });

    function queryParams(params) {
        let news_id = $('#news_id_input').val();
        if (!news_id) {
            news_id = ''
        }
        let user_id = $('#user_id_input').val();
        if (!user_id) {
            user_id = ''
        }
        console.log(params);
        return {  //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            rows: params.limit,  //页面大小
            page: (params.offset / params.limit) + 1,   //页码
            news_id: news_id,
            user_id: user_id
        };
    }

    function refresh_table() {
        console.log('正在刷新');
        $("#review_table").bootstrapTable('refresh', {
            url: '/review/reviews/',
            silent: true,
            query: queryParams,
        });
    }

    $('#search_btn').on('click', function (e) {
        refresh_table();
    });
    $('#search_form').submit(function () {
        $(this).preventDefault();
    });

    function setEventListener(e) {
        $('.del_btn').on('click', function (e) {

            var r_id = $(this).attr('r_id');
            if (confirm('确定删除id='+r_id+'该条评论吗?')) {
                $.ajax('/review/deleteReview/' + r_id + '/', {
                    type: 'DELETE',
                    headers: {"X-CSRFtoken": csrf},
                    success: function (data) {
                        if (data.code === 200){
                            setInfo(1, '删除成功，正在刷新列表，请稍后...');
                            refresh_table()
                        } else {
                            setInfo(0, '删除失败，'+ data.msg);
                        }
                    }
                })
            }

        });
    }

    /**
     *输出消息
     * @param status 0为错误， 1为成功
     * @param msg
     */
    function setInfo(status, msg) {
        let info_id = '';
        if (status){
            info_id = '#success_info'
        } else {
            info_id = '#warning_info'
        }
        $(info_id).html(msg).show();
        setTimeout(function () {
            $(info_id).html('').hide();
        }, 3000);
    }
});