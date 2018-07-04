$(function(){
	$('#sign_up_form').submit(function(e){
		var sign_up_info = $('#sign_up_info');
		var sign_up_success = $('#sign_up_success');
		sign_up_info.hide();
		e.preventDefault()
		var username = $('#name').val();
		var password = $('#password').val();
		var repassword = $('#re-password').val();
		var v_code = $('#v_code').val();
		var uPattern = /^[a-zA-Z0-9_-]{4,20}$/;
		var pPattern = /^[a-zA-Z0-9_-]{6,20}$/;
		if (!uPattern.test(username)){
			sign_up_info.show();
			sign_up_success.html('用户名为4到20位（字母，数字，下划线，减号）');
		}else if(!pPattern.test(password)){
			sign_up_info.show();
			sign_up_success.html('密码为6到20位（字母，数字，下划线，减号）');
		}else if(password.length === 0 || repassword === 0){
			sign_up_info.show();
			sign_up_success.html('密码不能为空');
		}else if(password !== repassword){
			sign_up_info.show();
			sign_up_success.html('两次密码不一致');
		}else if(v_code.length < 4){
			sign_up_info.show();
			sign_up_success.html('验证码不能为空,或长度为4!');
		}else {
			$('#sign_up_form').ajaxSubmit(function(data){
				if (data.code === 200){
	                sign_up_info.show();
	                sign_up_info.html('注册成功,1秒后跳转到登录界面');
	                setTimeout(function (e) {
	                   window.location.href = '/login/'; //这里的url需要修改
	                },1000);
	            }else {
	                sign_up_info.show();
					sign_up_success.html(data.msg);
	            }
			});
		}
		
	});
});