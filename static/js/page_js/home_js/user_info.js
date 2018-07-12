$(function () {
    var info_success = $('#info_success');
    info_success.hide();
    $.get('/user_operation/info_modify/', function (data) {
        console.log(data);
        if(data.code == 200){
            $('#head_icon').attr('src', data.head_icon);
            $('#name').text(data.name);
            $('#nick_name').text(data.nick_name);
            $('#last_login_time').text(data.last_login_time)
        }else{
            $('#newslist').html('您尚未登陆')
        }
    });
    $('#file_but').click(function () {
        $('#file_input').trigger('click')
    });
    $('#info_modify').submit(function (e) {
        e.preventDefault();
        var img = $('#file_input').val();
        if(img){
            $(this).ajaxSubmit(function (data) {
                if(data.code == 200){
                    info_success.show()
                }else{
                    info_success.html('发生错误,请重试');
                    info_success.show()
                }
            })
        }
    })
});


 $("#file_input").change(function(){
      // getObjectURL是自定义的函数，见下面
      // this.files[0]代表的是选择的文件资源的第一个，因为上面写了 multiple="multiple" 就表示上传文件可能不止一个
      // ，但是这里只读取第一个
      var objUrl = getObjectURL(this.files[0]) ;
      // 这句代码没什么作用，删掉也可以
      // console.log("objUrl = "+objUrl) ;
      if (objUrl) {
        // 在这里修改图片的地址属性
        $("#head_icon").attr("src", objUrl) ;
      }
    }) ;
    //建立一個可存取到該file的url
    function getObjectURL(file) {
      var url = null ;
      // 下面函数执行的效果是一样的，只是需要针对不同的浏览器执行不同的 js 函数而已
      if (window.createObjectURL!=undefined) { // basic
        url = window.createObjectURL(file) ;
      } else if (window.URL!=undefined) { // mozilla(firefox)
        url = window.URL.createObjectURL(file) ;
      } else if (window.webkitURL!=undefined) { // webkit or chrome
        url = window.webkitURL.createObjectURL(file) ;
      }
      return url ;
    }


function p_change_input() {
    var m_this=$('p[id="nick_name"]');
    var value = m_this.html();
    var par = m_this.parent();
    par.html('<input id="nick_name" value="' + value + '" type="text" onblur="blur_input()" onkeydown="if(event.keyCode==13){blur_input();}">');
    $('input[id="nick_name"]').focus();
}


function blur_input() {
    var m_this = $('input[id="nick_name"]');
    var info_success = $('#info_success');
    var sPartten = /^[\s]/;
    var nPartten = /^[\u4E00-\u9FA5a-zA-Z0-9_-]{1,32}$/;
    console.log(m_this.val());
    console.log(m_this.html());
    if (!m_this.val()){
        info_success.html('昵称不能为空');
        info_success.show()
    }else if (sPartten.test(m_this.val())) {
        info_success.html('昵称中不能有空格');
        info_success.show()
    } else if (!nPartten.test(m_this.val())){
        info_success.html('昵称长度为1-32字符')
    } else {
        m_this.parent().html('<p id="nick_name" onclick="p_change_input()" >' + m_this.val() + '</p>');
        info_success.hide();
        var nick_name = $('p[id="nick_name"]').html();
        var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            url: '/user_operation/info_modify/',
            type: 'POST',
            dataType: 'json',
            data: {'nick_name': nick_name},
            headers: {'X-CSRFToken':csrf_token},
            success: function (data) {
                if(data.code == 200){
                    info_success.show()
                }else{
                    info_success.html('服务器忙,数据操作失败');
                    info_success.show()
                }
            },
            error: function () {
                info_success.html('服务器忙,数据操作失败');
                info_success.show()
            }
        })
    }
}