;
let food_cat_ops = {
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
        let that = this;
        $('.wrap_search select[name=status]').change(function () {
            $('.wrap_search').submit();
        });
        // 删除事件
        $('.remove').click(function () {
            that.ops('remove', $(this).attr('data'));
        });
        // 恢复事件
        $('.recover').click(function () {
            that.ops('recover', $(this).attr('data'));
        });
    },
    ops:function (act, id) {
        let callback = {
            'ok':function () {
                       $.ajax({
                            url: common_ops.buildUrl('/food/cat-ops'),
                            type: 'POST',
                            data: {
                                act: act,
                                id: id
                            },
                            dataType: 'json',
                            success: function (res) {
                                let callback = null;
                                if(res.code == 200){
                                    callback = function () {
                                        window.location.reload();
                                    }
                                }
                                common_ops.alert(res.msg, callback);
                            }
                        });
            },
            'cancel': null
        };
        common_ops.confirm((act === 'remove' ? '确定删除吗？': '确定恢复嘛？'), callback)

    }
};

$(document).ready(function () {
    food_cat_ops.init();
});