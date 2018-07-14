$(function () {
    var news_id = $('#news_id').val();  //初始化当前新闻的ID
    var review_index = 2;  // 初始化新闻评论显示的条数
    getNewsLiked();  // 获取点赞数量
    getData(review_index); //获取评论数据

    /**
     * 获取服务器评论数据的事件
     * @param rows 获取多少行
     */
    function getData(rows) {
        if (rows) {
            var url = '/review/reviews/?news_id=' + news_id + '&page=1&rows=' + rows
        } else {
            var url = '/review/reviews/?news_id=' + news_id
        }
        $.get(url, function (data) {
            if (data.code === 200) {
                let review_list = data.rows;
                let review_total = data.total;
                let html_str = '';
                for (let i = 0; i < review_list.length; i++) {
                    html_str += "<li class=\"review_item bg-info\"><div>" +
                        "<span>" + review_list[i].user_name + ":</span>" + review_list[i].rev_content +
                        "</div>" +
                        "<div id=\"review_islike\">" +
                        "<div class=\"islike_item\"><button r_id='" + review_list[i].id + "' class='btn btn-default liked_btn'>" +
                        "<img src=\"/static/img/home_img/review_liked.png\"/>" +
                        "</button><span class='span_num' id='like_num_" + review_list[i].id + "'>" + review_list[i].liked_num + "</span>" +
                        "</div>" +
                        "<div class=\"islike_item\"><button r_id='" + review_list[i].id + "' class='btn btn-default unliked_btn'>" +
                        "<img src=\"/static/img/home_img/review_unlike.png\"/>" +
                        "</button><span class='span_num' id='unlike_num_" + review_list[i].id + "'>" + review_list[i].unliked_num + "</span>" +
                        "</div><div class='btn_info bg-success'><p id='info_" + review_list[i].id + "'></p></div>" +
                        "<div class='review_time'>" + review_list[i].time + "</div><div class=\"clear\"></div></div></li>"
                }
                $('#review_ul').html(html_str);
                if (review_total <= review_index) {
                    $('#get_more_review').hide();
                } else {
                    $('#get_more_review').show();
                }
                setEvent();
            } else {
                alert(data.msg);
            }
        });
    }

    /**
     * 设置事件监听
     */
    function setEvent() {
        $('.liked_btn').on('click', function () {
            let r_id = $(this).attr('r_id');
            // 点赞的方法
            is_liked(r_id, 1);
        });
        $('.unliked_btn').on('click', function () {
            let r_id = $(this).attr('r_id');
            // 踩的方法
            is_liked(r_id, 0);
        });

        /**
         * 显示消息的方法
         * @param r_id  评论ID
         * @param msg 消息
         */
        function showInfo(r_id, msg) {
            $('#info_' + r_id).html(msg);
            setTimeout(function () {
                $('#info_' + r_id).html('');
            }, 3000)
        }

        /**
         * 点赞和踩的方法
         * @param r_id 评论的ID
         * @param action 1为赞，0为猜
         */
        function is_liked(r_id, action) {
            if (action) {
                var msg = '赞成功';
                var num_span = $('#like_num_' + r_id)
            } else {
                var msg = '踩成功'
                var num_span = $('#unlike_num_' + r_id)
            }
            let csrf = $("input[name='csrfmiddlewaretoken']").val();
            $.ajax('/review/addLiked/', {
                type: 'POST',
                headers: {"X-CSRFtoken": csrf},
                data: {
                    r_id: r_id,
                    is_liked: action
                },
                success: function (data) {
                    if (data.code === 200) {
                        showInfo(r_id, msg);
                        let num = num_span.html();
                        num_span.html(parseInt(num) + 1);
                    } else {
                        showInfo(r_id, data.msg)
                    }
                }
            });
        }
    }

    /**
     * 添加评论的事件
     */
    $('#add_review_btn').on('click', function (e) {
        let review = $('#add_review_text').val();
        if (review.length <= 0) {
            setInfo('输入不能为空');
            return
        }
        let csrf = $("input[name='csrfmiddlewaretoken']").val();
        $.ajax('/review/addReview/', {
            type: 'POST',
            headers: {"X-CSRFtoken": csrf},
            data: {
                news_id: news_id,
                review: review
            },
            success: function (data) {
                if (data.code === 200) {
                    // alert('添加成功')
                    // 刷新评论列表
                    getData(review_index);
                    setInfo('添加评论成功')
                } else if (data.code === 300) {
                    if (confirm('暂未登录是否跳转到登录页面？')) {
                        window.location.href = '/user_operation/login/'
                    }
                } else {
                    alert(data.msg)
                }
            }
        });

        /**
         * 输出消息的方法
         * @param msg 需要输出的消息
         */
        function setInfo(msg) {
            $('#add_info').html(msg);
            $('#add_info').show();
            $('#add_review_text').val('');
            setTimeout(function () {
                $('#add_info').hide();
            }, 3000);
        }
    });
    /**
     * 获取更多评论事件，每次多5条
     */
    $('#get_more_review').on('click', function (e) {
        review_index += 5;
        getData(review_index);
    });

    /**
     * 获取新闻的点赞数量
     */
    function getNewsLiked() {
        $.get('/news/newsLikedNum/?news_id=' + news_id, function (data) {
            if (data.code === 200) {
                $('#news_like_num').html(data.num)
            }
        });
    }

    /**
     * 点赞按钮点击事件
     */
    $('#btn_liked_news').on('click', function (e) {
        let csrf = $("input[name='csrfmiddlewaretoken']").val();
        $.ajax('/news/addLiked/', {
            type: 'POST',
            headers: {"X-CSRFtoken": csrf},
            data: {
                news_id: news_id
            },
            success: function (data) {
                let num = $('#news_like_num').html();
                if (data.code === 200) {
                    setInfo('点赞成功');
                    $('#news_like_num').html(parseInt(num) + 1);
                } else if (data.code === 4301) {
                    setInfo('请勿重复点赞！')
                }
            }
        });

        /**
         * 消息提示方法
         * @param msg 提示的消息
         */
        function setInfo(msg) {
            $('#news_liked_info').html(msg);
            setTimeout(function () {
                $('#news_liked_info').html('');
            }, 3000);
        }
    });

});