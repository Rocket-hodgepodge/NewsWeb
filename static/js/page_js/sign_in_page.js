$(function(){
	var sign_in_info = $('#sign_in_info');
	var sign_in_success = $('#sign_in_success');
	sign_in_info.hide();
	$('#sign_in_form').submit(function(e){
		e.preventDefault();
		var username = $('#username').val();
		var password = $('#password').val();
		var v_code = $('#v_code').val();
		if (username.length === 0 || password.length === 0 || v_code.length < 4){
			sign_in_info.show();
			sign_in_success.html('输入不能为空,或验证码长度不够!');
		}else {
			$('#sign_in_form').ajaxSubmit(function(data){
				if (data.code == 200){
					sign_up_info.show();
	                sign_up_success.html('登录成功,1秒后跳转到主页界面');
	                setTimeout(function (e) {
	                	role = data.role
	                	if (role){
	                		window.location.href = '/login/'; //这里的url需要修改,指向前台主页
	                	}else {
	                		window.location.href = '/login/'; //这里的url需要修改,指向后台主页
	                	}
	                },1000);
				}else {
					sign_in_success.html(data.msg);
					refresh_verify()
				}
			});
		}
	});
});
