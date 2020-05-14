;
let user_edit_ops = {
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
        $('.user_edit_wrap .save').click(function () {
            let btn_target = $(this);

            if(btn_target.hasClass("disabled")){
                common_ops.alert("正在处理！！ 请不要重复提交！");
            }

            let nickname_target = $('.user_edit_wrap input[name=nickname]'); //获取nickname参数
            let nickname = nickname_target.val();

            let email_target = $('.user_edit_wrap input[name=email]');
            let email = email_target.val();

            if(!nickname || nickname.length < 2){ //判断用户名，终止提交
                common_ops.tip('请输入符合规范的姓名', nickname_target);
                return false;
            }

            if(!email || email.length < 2){ //判断邮箱，终止提交
                common_ops.tip('请输入符合规范的邮箱', email_target);
                return false;
            }

            btn_target.addClass("disabled");

            let data = {
                nickname: nickname,
                email: email
            };

            $.ajax({
                url: common_ops.buildUrl('/user/edit'),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass("disabled");

                    let callback = null
                    if (res.code === 200){
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
    user_edit_ops.init();
});