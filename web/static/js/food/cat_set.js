;
let food_cat_set_ops = {
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
        $('.wrap_cat_set .save').click(function () {
            let btn_target = $(this);

            if(btn_target.hasClass("disabled")){
                common_ops.alert("正在处理！！ 请不要重复提交！");
            }

            let name_target = $('.wrap_cat_set input[name=name]'); //获取name参数
            let name = name_target.val();

            let weight_target = $('.wrap_cat_set input[name=weight]'); //获取weight参数
            let weight = weight_target.val();



            if(!name || name.length < 1){ //判断name，终止提交
                common_ops.tip('请输入符合规范的分类名称', name_target);
                return false;
            }

            if(!weight || parseInt(weight) < 1){ //判断weight，终止提交
                common_ops.tip('请输入符合规范的权重，并且至少要大于1', weight_target);
                return false;
            }

            let data = {
                name: name,
                weight: weight,
                set_id:$('.wrap_cat_set input[name=id]').val()
            };

            $.ajax({
                url: common_ops.buildUrl('/food/cat-set'),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass("disabled");

                    let callback = null
                    if (res.code == 200){
                        callback = function () {
                            window.location.href=common_ops.buildUrl('/food/cat');
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            });

        });
    }
};

$(document).ready(function () {
    food_cat_set_ops.init();
});