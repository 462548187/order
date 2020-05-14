;
let mod_pwd_ops = {
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
        $('.user_reset_pwd_wrap .save').click(function () {
            let btn_target = $(this);

            if(btn_target.hasClass("disabled")){
                common_ops.alert("正在处理！！ 请不要重复提交！");
            }

            let old_password_target = $('.user_reset_pwd_wrap input[name=old_password]'); //获取nickname参数
            let old_password = old_password_target.val();

            let new_password_target = $('.user_reset_pwd_wrap input[name=new_password]');
            let new_password = new_password_target.val();

            if(!old_password || old_password.length < 6){ //判断old_password，终止提交
                common_ops.tip('请输入不少于6位的原密码', old_password_target);
                return false;
            }

            if(!new_password || new_password.length < 6){ //判断邮箱new_password，终止提交
                common_ops.tip('请输入不少于6位的新密码', new_password_target);
                return false;
            }

            btn_target.addClass("disabled");

            let data = {
                old_password: old_password,
                new_password: new_password
            };

            $.ajax({
                url: common_ops.buildUrl('/user/reset-pwd'),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass("disabled");

                    let callback = null
                    if (res.code == 200){
                        callback = function () {
                            window.location.reload();
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            });

        });
    }
};

$(document).ready(function () {
    mod_pwd_ops.init();
});