var dataDepart = [];
var baseurl = "http://127.0.0.1:8088/";

$(function () {
    baseInit()
});

function baseInit(){
    tree();
    checklogin()
}

// 检查localStorage 确定登录状态
function checklogin(){
    if(localStorage.getItem("userName")){
        $(".username_box").menubutton({'text': localStorage.getItem("userName")})
    }else {
        location.href = "/login"
    }
}

// 获取连接导航树结构
function tree(){
    $("#tree").tree({
        // checkbox: true,
        url:'/treeJson/',
        method:'get',
        animate:true,
        formatter:function(node){
            var s = node.text;
            if (node.children){
                s += ' <span style=\'color:blue\'>('+ node.children.length +')</span>';
            }
            return s;
        },
        onClick : function (node) {
            if(node.attributes){
                console.log('自己添加的属性： 【URL】'+ node.attributes.url +',  【info】' + node.attributes.info);
                location.href = node.attributes.url
            }
        }
    });

}

// 修改密码
function modifyPsd(){
    if(!$('#psdform').form('enableValidation').form('validate')) return;
    $.ajax({
        type: 'post',
        url: '/modifyPsd/',
        data: {
            id: localStorage.getItem("userId"),
            password: sha256_digest($("#password").textbox("getValue"))
        },
        success: function(ret){
            layer.msg(ret.retMsg);
            if(ret.success){
                $("#modifyPsd").dialog("close").form('clear');
            }
        }
    });
}

// 退出登录
function loginOut(){
    $.messager.confirm('退出', 'Are you confirm this?', function(r){
        if (r){
            $.ajax({
                type: 'get',
                url: '/loginOut/',
                success: function(ret){
                    location.href = "/login";
                    localStorage.clear();
                }
            });
        }
    });
}



