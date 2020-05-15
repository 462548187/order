;
let member_set_ops = {
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
        $('.wrap_member_set .save').click(function () {
            let btn_target = $(this);

            if(btn_target.hasClass("disabled")){
                common_ops.alert("正在处理！！ 请不要重复提交！");
            }

            let nickname_target = $('.wrap_member_set input[name=nickname]'); //获取nickname参数
            let nickname = nickname_target.val();

            let mobile_target = $('.wrap_member_set input[name=mobile]'); //获取mobile参数
            let mobile = mobile_target.val();

            if(!nickname || nickname.length < 2){ //判断用户名，终止提交
                common_ops.tip('请输入符合规范的姓名', nickname_target);
                return false;
            }

            if(!mobile || mobile.length < 11){ //判断邮箱，终止提交
                common_ops.tip('请输入符合规范的手机号码', mobile_target);
                return false;
            }

            btn_target.addClass("disabled");

            let data = {
                nickname: nickname,
                mobile: mobile,
                member_id:$('.wrap_member_set input[name=id]').val()
            };

            $.ajax({
                url: common_ops.buildUrl('/member/set'),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass("disabled");

                    let callback = null
                    if (res.code == 200){
                        callback = function () {
                            window.location.href=common_ops.buildUrl('/member/index');
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            });

        });
    }
};

$(document).ready(function () {
    member_set_ops.init();
});