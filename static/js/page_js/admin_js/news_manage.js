$(function () {
    $(".form_datetime").datetimepicker({
        language: 'zh-CN',
        format: "yyyy-mm-dd hh:ii:ss",
        todayBtn: true
    });
    // noinspection JSJQueryEfficiency
    $('#news_modal').modal({
        show: false,
        keyboard: false,
        backdrop: 'static'
    });
    $('#edit_news_content').summernote({
        lang: 'zh-CN'
    });

    // noinspection JSJQueryEfficiency
    $('#news_modal').on('hidden.bs.modal', function () {
        $('#edit_news_id').attr('placeholder', '');
        $('#edit_news_title').val('');
        $('#edit_news_type').val('');
        $('#edit_news_host').val('');
        $('#edit_news_time').attr('value', getCurrentTime());
        $('#edit_news_rTotal').val('');
        $('#edit_news_content').summernote('code', '');
    });

    $('#news_table').bootstrapTable({
        url: '/news/query/',  // 请求地址
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
            title: '新闻ID'
        }, {
            field: 'title',
            title: '标题'
        }, {
            field: 'type',
            title: '类型'
        }, {
            field: 'host',
            title: '站点'
        }, {
            field: 'publish_time',
            title: '发布时间',
            sortable: true
        }, {
            field: 'read_total',
            title: '点击量'
        }, {
            field: 'option',
            title: '操作',
            formatter: function (value, row, index) {
                var edit_bt = '<button n_id="' + row.id + '" data-toggle="modal" data-target=".bs-example-modal-lg" class="edit_btn btn btn-warning btn-xs">编辑</button>';
                var del_btn = '<button n_id="' + row.id + '" class="del_btn btn btn-danger btn-xs">删除</button>';
                return edit_bt + del_btn
            }

        }],
        // 加载成功回调事件
        onLoadSuccess: function (data) {
            setEventListener()
        },
        // 加载失败回调事件
        onLoadError: function (status) {

        }
    });

    /**
     * 表格查询的参数
     * @param params 表格的页面limit,和offset
     * @returns {{rows: *, page: number, type: *, title: (*|jQuery)}}
     */
    function queryParams(params) {
        let option = $('#type_select  option:selected');
        let t_id = option.attr('t_id');
        if (!t_id) {
            t_id = ''
        }
        let title = $('#news_title').val();
        let sort = params.sort;
        if (!sort) {
            sort = ''
        }
        console.log(params);
        return {  //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            rows: params.limit,  //页面大小
            page: (params.offset / params.limit) + 1,   //页码
            type: t_id,
            title: title,
            order: params.order,
            sort: sort
        };
    }

    /**
     * 刷新表格的方法
     */
    function refresh_table() {
        console.log('正在刷新');
        $("#news_table").bootstrapTable('refresh', {
            url: '/news/query/',
            silent: true,
            query: queryParams,
        });
    }

    // 获取所有新闻类型
    $.get('/news/all_type/', function (data) {
        console.log(data);
        if (data.code === 200) {
            let datas = data.data;
            for (let i = 0; i < data.data.length; i++) {
                let op1 = $('<option></option>').attr('t_id', datas[i].id).html(datas[i].name);
                let op2 = $('<option></option>').attr('t_id', datas[i].id).html(datas[i].name);
                $('#type_select').append(op1);
                $('#edit_news_type').append(op2);
            }
        } else {
            console.log('新闻类型加载失败');
        }
    });
    // 搜索按钮,刷新表格
    $('#search_bt').on('click', function () {
        refresh_table();
    });

    // 取消表单的默认提交
    $('#search_form').submit(function () {
        $(this).preventDefault();
    });

    /**
     * 为表格中的按钮设置监听事件
     */
    function setEventListener() {
        $('.edit_btn').on('click', function () {
            var n_id = $(this).attr('n_id');
            $('#edit_news_id').attr('placeholder', n_id);
            $.get('/news/getOneNews/' + n_id + '/', function (data) {
                if (data.code === 200) {
                    var newsobj = data.data;
                    $('#edit_news_id').attr('placeholder', newsobj.id);
                    $('#edit_news_title').val(newsobj.title);
                    $('#edit_news_type').val(newsobj.type);
                    $('#edit_news_host').val(newsobj.host);
                    $('#edit_news_time').attr('value', newsobj.publish_time);
                    $('#edit_news_rTotal').val(newsobj.read_total);
                    $('#edit_news_content').summernote('code', newsobj.content);
                } else {
                    $('#news_modal').modal('hide');
                    alert('数据获取失败!');
                }

            })
        });
        $('.del_btn').on('click', function () {
            if (confirm('确认删除该条数据吗')) {
                let n_id = $(this).attr('n_id');
                let csrf = $("input[name='csrfmiddlewaretoken']").val();
                console.log(csrf);
                $.ajax('/news/delNews/' + n_id + '/', {
                    method: 'DELETE',
                    headers: {"X-CSRFtoken": csrf},
                    success: function (data) {
                        if (data.code === 200) {
                            $('#delete_info').show();
                            setTimeout(function () {
                                $('#delete_info').hide();
                            }, 3000);
                            refresh_table();
                        } else {
                            alert('删除失败');
                        }
                    }
                });
            }
        })
    }

    $('#model_ok').on('click', function (e) {
        let csrf = $("input[name='csrfmiddlewaretoken']").val();
        let new_id = $('#edit_news_id').attr('placeholder');
        let title = $('#edit_news_title').val();
        let type_id = $('#edit_news_type option:selected').attr('t_id');
        let host = $('#edit_news_host').val();
        let publish_time = $('#edit_news_time').val();
        let read_total = $('#edit_news_rTotal').val();
        let content = $('#edit_news_content').summernote('code');
        $.ajax('/news/alterNews/', {
            method: 'POST',
            data: {
                'news_id': new_id,
                'title': title,
                'type_id': type_id,
                'from_host': host,
                'publish_time': publish_time,
                'content': content,
                'read_total': read_total
            },
            headers: {"X-CSRFtoken": csrf},
            success: function (data,status) {
                if (data.code === 200){
                    $('#news_modal').modal('hide');
                    $('#alter_info').show();
                    setTimeout(function () {
                        $('#alter_info').hide();
                    }, 3000);
                }else {
                    alert('修改失败');
                }
            }
        });
    });

    function getCurrentTime() {
        var date = new Date();
        var year = date.getFullYear(); //获取当前年份
        var mon = date.getMonth() + 1; //获取当前月份
        var day = date.getDate(); //获取当前日期
        var h = date.getHours(); //获取小时
        var m = date.getMinutes(); //获取分钟
        var s = date.getSeconds(); //获取秒
        return year + '-' + mon + '-' + day + ' ' + h + ':' + m + ':' + s
    }
});
