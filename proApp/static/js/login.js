
function login(){
    if(!$('#form').form('enableValidation').form('validate')) return;
    data = formSerializeToObject($("form").serializeArray());
    data.password = sha256_digest(data.password);
    $.ajax({
        type: 'post',
        url: '/loginIn/',
        data: data,
        success: function(data){
            if(data.ret.success){
                location.href = "/index";
                localStorage.setItem("userId",data.userInfo.id);
                localStorage.setItem("userName",data.userInfo.name)
            }else {
                layer.msg(data.ret.retMsg);
                changeCaptcha()
            }
        }
    });
}

function changeCaptcha(){
    $(".identifyCode").attr("src", "/getCaptcha/?" + Math.random());
}