$(function () {
//    将0设置到未加入购物车的商品的数据上
    $(".subToCart").each(function () {
        $this = $(this);
        res = $this.next("span");
        if (res.length == 0){
            $this.after("<span>0</span>")
        }
    });



//    让全部分类隐藏
    $('#type_container').hide();
//    让排序的容器隐藏
    $("#sort_container").hide();

//    点击全部按钮
    $("#alltype_button").click(function () {
        $("#type_container").show();
        //更改箭头方向
        $("#alltype_arrow").removeClass().addClass("glyphicon glyphicon-chevron-up");

        $("#sort_container").hide();
        $("#sort_arrow").removeClass().addClass("glyphicon glyphicon-chevron-down");

    });

    $("#type_container").click(function () {
        $(this).hide();

        $("#alltype_arrow").removeClass().addClass("glyphicon glyphicon-chevron-down");
    });

    $("#sort_button").click(function () {
        $("#sort_container").show();
        $("#sort_arrow").removeClass().addClass("glyphicon glyphicon-chevron-up");
        $("#type_container").hide();
        //更改箭头方向
        $("#alltype_arrow").removeClass().addClass("glyphicon glyphicon-chevron-down");

    });

    $("#sort_container").click(function () {
        $(this).hide();
        $("#sort_arrow").removeClass().addClass("glyphicon glyphicon-chevron-down");
    });


    $(".addToCart").click(function () {
        goodsId = $(this).attr("goodsid");

        $this = $(this);

        urlPath = '/axf/addToCart';
        paramData = {'goodsid':goodsId};

        $.getJSON(urlPath,paramData,function (data) {
            if (data["code"] == 304){
                window.open('/axf/login',target="_self")
            }else if (data["code"] == 200){
                // alert(data["num"])
                $this.prev("span").html(data["num"])
            }
        })
    });

    $(".subToCart").click(function () {
        goodsId = $(this).attr("goodsid");

        $this = $(this);
        urlPath = '/axf/subToCart';
        paramData = {'goodsid':goodsId};
        $.getJSON(urlPath,paramData,function (data) {
            if (data["code"] == 304){
                window.open('/axf/login',target="_self")
            }else if (data["code"] == 200){
                // alert(data["num"])
                $this.next("span").html(data["num"])
            }
        })

    })
});