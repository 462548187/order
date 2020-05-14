;
let user_login_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $(".login_warp .do-login").click(function () {

            let btn_target = $(this)

            if(btn_target.hasClass("disabled")){
                common_ops.alert("正在处理！！ 请不要重复提交！")
            }

            let login_name = $(".login_warp input[name=login_name]").val();
            let login_pwd = $(".login_warp input[name=login_pwd]").val();

            if (login_name === undefined || login_name.length < 1){
                common_ops.alert("请输入正确的用户名");
            }

            if (login_pwd === undefined || login_pwd.length < 1){
                common_ops.alert("请输入正确的密码");
            }

            btn_target.addClass("disabled")

            $.ajax({
                url: common_ops.buildUrl('/user/login'),
                type: "POST",
                data:{'login_name':login_name, 'login_pwd':login_pwd},
                dataType:'json',
                success:function (res) {
                    btn_target.removeClass("disabled");

                    let callback = null
                    if (res.code === 200){
                        callback = function () {
                            // common_ops.alert(common_ops.buildUrl("/"))
                            window.location.href = common_ops.buildUrl("/");
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            });

        });
    }
};

$(document).ready(function () {
    user_login_ops.init();
});