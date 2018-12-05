//标记密码是否设置合法
var flag1 = false
var flag2 = false

$(function () {
//    验证用户名是否已经存在
//    当用户名输入框失去焦点，且内容改变的时候去请求服务器验证用户名的唯一性
    $("#username").change(function () {

        // 获得用户输入的用户名
        usernameval = $(this).val();
        // 异步请求服务器
        // 参数1:url地址,请求地址
        // 参数2:data 请求参数 类字典的形式的数据
        // 参数3:回调函数,当请求成功时调用,携带服务器返回的数据data(json格式的数据)
        $.getJSON('/axf/checkUserUnique',{'username':usernameval},function (data) {
            if (data["code"] == 800){
                $("#error_user").html(data["msg"]).css("color","rgb(255,0,0)");
                flag2 = false
            } else if (data["code"] == 801){
                $("#error_user").html("用户名可用").css("color","rgb(0,255,0)");
                flag2 = true
            }
        })





    });


//    验证设置的密码是否合法
//    当确认密码框失去焦点,且内容发生变化的时候校验 change
//    password1 是设置密码框,password2 是确认密码框
    $("#password1").change(function () {
        //    1.密码的长度至少6位
        //    2.输入的密码必须符合规范

        //  获得用户输入的内容
        password1val = $("#password1").val();
        password2val = $("#password2").val();
        if(password1val.length < 6){
            // 密码小于6位
            $("#error_info1").html("密码至少6位").css("color","rgb(255,0,0)");
            flag1 = false;
            return
        }else {
            $("#error_info1").html("密码可用").css("color","rgb(0,255,0)");
            flag1 = true;
        }
    });

    $("#password2").change(function () {
        //   两次输入的密码必须一致

        //  获得用户输入的内容
        password1val = $("#password1").val();
        password2val = $("#password2").val();

        if (password2val != password1val){
            $("#error_info2").html("两次输入的密码不一致").css("color","rgb(255,0,0)");
            flag1 = false;
            return
        }else{
            $("#error_info2").html("密码一致").css("color","rgb(0,255,0)");
            flag1 = true;
        }
    })

});


//    form中onsubmit属性调用的方法
//    当用户提交form的时候，会自动调用onsubmit，onsubmit不是是否可以提交
//    onsubmit的值如果是True，表示可以提交；onsubmit的值如果是False，表示不可以提交；
    function submitCheck(){
        // 用户是否合法
        if (!flag2){
            alert("输入的用户名不合法");
            return false
        }
        // 密码是否合法
        if (!flag1){
            alert("输入的密码不合法");
            return false
        }

        password1val = $("#password1").val();

        // 密码做md5处理,会生产一个md5处理后的16进制的结果
        res = md5(password1val);
        // alert(res)
        $("#password1").val(res);

        return true

    }

