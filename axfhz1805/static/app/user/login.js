$(function () {



});


function submitCheck(){
    $pass = $("#password");
    password = $pass.val();
    res = md5(password);
    $pass.val(res);
    return true
}