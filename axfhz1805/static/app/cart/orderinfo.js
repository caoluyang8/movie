$(function () {
    $("#pay_button").click(function () {
        // 支付方式 -- 支付宝 微信 银联 ......

        // 1.修改当前订单的状态
        // 2.回到主页
        urlPath = '/axf/changeOrderStatus';
        dataParam = {"ordernum":$(this).attr("ordernum"), 'status':2};
        $.getJSON(urlPath,dataParam,function (data) {
            if (data["code"] == 200){
                window.open('/axf/mine',target='_self')
            }
        })



    })

});