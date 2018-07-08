$(function(){

	$('#news_table').bootstrapTable({
		url:'/news/query/',
		method: 'GET',
        dataType: "json",
        striped: true, //隔行变色
        pagination: true, //分页
        paginationLoop: false,
		sidePagination: 'server',
        sortable: false,           //是否启用排序
        pageNumber: 1,
        pageSize: 10,
        pageList: [10, 25, 50, 100],
        uniqueId: "id", //每一行的唯一标识，一般为主键列
        queryParams: queryParams,
		columns: [{
	        field: 'id',
	        title: '新闻ID'
	    }, {
		    field: 'title',
            title: '标题'
        },{
	        field: 'type',
	        title: '类型'
	    }, {
	        field: 'host',
	        title: '站点'
	    },{
	    	field: 'publish_time',
	    	title: '发布时间'
	    },{
	    	field: 'read_total',
	    	title: '点击量'
	    },{
		    field: 'option',
            title: '操作',
            formatter: function (value, row, index) {
                var edit_bt = '<button n_id="'+row.id+'" data-toggle="modal" data-target=".bs-example-modal-lg" class="edit_btn btn btn-warning btn-xs">编辑</button>';
                var del_btn = '<button n_id="'+row.id+'" class="del_btn btn btn-danger btn-xs">删除</button>';
                return edit_bt+del_btn
		    }

        }],
        onLoadSuccess: function (data) {
            setEventListener()
        },
        onLoadError: function (status) {

        }
	});
    function queryParams (params) {
        let option = $('#type_select  option:selected');
        let t_id = option.attr('t_id');
        if (!t_id) {t_id=''}
        let title = $('#news_title').val();
        console.log(t_id);
        return {  //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            rows: params.limit,  //页面大小
            page: (params.offset / params.limit) + 1,   //页码
            type: t_id,
            title: title
        };
    }
    function refresh_table() {
        console.log('正在刷新');
        $("#news_table").bootstrapTable('refresh', {
            url: '/news/query/',
            silent: true,
            query: queryParams,
        });
    }
    $.get('/news/all_type/', function (data) {
        console.log(data);
        if (data.code === 200){
            let datas = data.data;
            for (let i=0; i < data.data.length; i++){
                let op = $('<option></option>').attr('t_id', datas[i].id).html(datas[i].name);
                $('#type_select').append(op);
            }
        }else {
            console.log('新闻类型加载失败');
        }
    });
    $('#search_bt').on('click', function () {
        refresh_table();
    });
    $('#search_form').submit(function () {
        $(this).preventDefault();
    });
    function setEventListener() {
        $('.edit_btn').on('click', function () {
            var n_id = $(this).attr('n_id');
            $('#test').html(n_id)
        });
        $('.del_btn').on('click', function () {
            if (confirm('确认删除该条数据吗')){
                let n_id = $(this).attr('n_id');
                let csrf = $("input[name='csrfmiddlewaretoken']").val();
                console.log(csrf);
                $.ajax('/news/delNews/'+n_id+'/',{
                    method: 'DELETE',
                    headers: {"X-CSRFtoken": csrf},
                    success:function (data) {
                        if (data.code===200){
                            alert('删除成功');
                            refresh_table();
                        }else {
                            alert('删除失败')
                        }
                    }
                });
            }
        })
    }

});
