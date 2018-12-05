$(function () {

   $(".addCart").click(function () {
        $this = $(this);
        //获得购物车的id,cardid
        cartid = $this.parents("li").attr("cartid");

        urlPath = '/axf/addCart';
        paramData = {'cartid':cartid};

        $.getJSON(urlPath,paramData,function (data) {
            if (data["code"] == 200){
                // alert(data["num"])
                $this.prev("span").html(data["num"]);
            }
        })
    });

   $(".subCart").click(function () {
        $this = $(this);
        //获得购物车的id,cardid
        cartid = $this.parents("li").attr("cartid");

        urlPath = '/axf/subCart';
        paramData = {'cartid':cartid};

        $.getJSON(urlPath,paramData,function (data) {
            if (data["code"] == 200){
                $this.next("span").html(data["num"])
            }else if (data['code'] == 201){
                $this.parents("li").remove()
            }
        })

   });


    // 给每个选中按钮设计点击事件
    $(".select_button").click(function () {
        $this = $(this);
        cartid = $this.parents("li").attr("cartid");
        urlPath = '/axf/changeSelectStatu';
        dataParam = {'cartid':cartid};

        $.getJSON(urlPath,dataParam,function (data) {
            if (data["code"] == 200){
                if (data["isselect"]){
                    $this.html("<span>√</span>");
                    $this.attr("isselect","True")
                }else{
                    $this.html("<span></span>");
                    $this.attr("isselect","False")
                }

                if (data["isAllSelect"]){
                    $("#all_select_button").html("<span>√</span>")
                }else{
                    $("#all_select_button").html("<span></span>")
                }

                $("#total_count").html("共计:" + data["totalCount"] + "件");
                $("#total_price").html("总价:" + data["totalPrice"] + "￥");
            }
        })
    });

//    全选按钮
    $("#all_select_button").click(function () {

        var allSelectArray = [];
        var noSelectArray = [];

    //    获取每一条cart记录的选中状态
         $('.select_button').each(function () {
             $this = $(this);
             isselect = $this.attr("isselect");
             cartid = $this.parents("li").attr("cartid");

             if (String(isselect) == "True"){
                 allSelectArray.push(cartid)
             }else{
                 noSelectArray.push(cartid)
             }

         });


        if (noSelectArray.length == 0 && allSelectArray.length >= 1){

             urlPath = '/axf/changeManySelectStatu';
             dataParam = {"selectArray":allSelectArray.join("#"),"flag":1}

             $.getJSON(urlPath,dataParam,function (data) {
                 if (data["code"] == 200){
                     $(".select_button").each(function () {
                         $(this).html("<span></span>");
                         $(this).attr("isselect","False");
                     });

                     $("#all_select_button").html("<span></span>")
                 }
             })

        }else{

             urlPath = '/axf/changeManySelectStatu';
             dataParam = {"selectArray":noSelectArray.join("#"),"flag":2}

             $.getJSON(urlPath,dataParam,function (data) {
                 if (data["code"] == 200){
                     $(".select_button").each(function () {
                         $(this).html("<span>√</span>");
                         $(this).attr("isselect","True");
                     })
                 }
             });

             $("#all_select_button").html("<span>√</span>")

        }

    })


    $("#create_order_button").click(function () {

        var allSelectArray = [];

        $(".select_button").each(function () {
            $this = $(this);
            isselect = $this.attr("isselect");
            cartid = $this.parents("li").attr("cartid");
            if (String(isselect) == "True"){
                allSelectArray.push(cartid)
            }
        });

        // 判断是否为空
        if (allSelectArray.length == 0){
            alert("没有选中任何商品")
            return
        }


        urlPath = '/axf/createOrder';
        dataParam = {"selectArray":allSelectArray.join("#")};

        $.getJSON(urlPath,dataParam,function (data) {

            if (data['code'] == 200){
                urlPath = '/axf/orderInfo/'+data["ordernum"]
                window.open(urlPath,target='_self')
            }

        })

    })



});