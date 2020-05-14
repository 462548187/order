;
let account_set_ops = {
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
        $('.wrap_account_set .save').click(function () {
            let btn_target = $(this);

            if(btn_target.hasClass("disabled")){
                common_ops.alert("正在处理！！ 请不要重复提交！");
            }

            let nickname_target = $('.wrap_account_set input[name=nickname]'); //获取nickname参数
            let nickname = nickname_target.val();

            let mobile_target = $('.wrap_account_set input[name=mobile]'); //获取mobile参数
            let mobile = mobile_target.val();

            let email_target = $('.wrap_account_set input[name=email]'); //获取email参数
            let email = email_target.val();

            let login_name_target = $('.wrap_account_set input[name=login_name]'); //获取login_name参数
            let login_name = login_name_target.val();

            let login_pwd_target = $('.wrap_account_set input[name=login_pwd]'); //获取login_pwd参数
            let login_pwd = login_pwd_target.val();


            if(!nickname || nickname.length < 2){ //判断用户名，终止提交
                common_ops.tip('请输入符合规范的姓名', nickname_target);
                return false;
            }

            if(!mobile || mobile.length < 11){ //判断邮箱，终止提交
                common_ops.tip('请输入符合规范的手机号码', mobile_target);
                return false;
            }

            if(!email || email.length < 2){ //判断用户名，终止提交
                common_ops.tip('请输入符合规范的邮箱', email_target);
                return false;
            }

            if(!login_name || login_name.length < 1){ //判断邮箱，终止提交
                common_ops.tip('请输入符合规范的登录名', login_name_target);
                return false;
            }

            if(!login_pwd || login_pwd.length < 6){ //判断邮箱，终止提交
                common_ops.tip('请输入符合规范的密码', login_pwd_target);
                return false;
            }

            btn_target.addClass("disabled");

            let data = {
                nickname: nickname,
                mobile: mobile,
                email: email,
                login_name: login_name,
                login_pwd: login_pwd,
                user_id:$('.wrap_account_set input[name=id]').val()
            };

            $.ajax({
                url: common_ops.buildUrl('/account/set'),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass("disabled");

                    let callback = null
                    if (res.code === 200){
                        callback = function () {
                            window.location.href=common_ops.buildUrl('/account/index');
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            });

        });
    }
};

$(document).ready(function () {
    account_set_ops.init();
});