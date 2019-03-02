$(function(){
    initCommon()
});

function initCommon(){
    // dialog 弹框初始化设置
    dialogFunc();
    // 表单验证
    validate();
}

// 表单序列化转化 键值对 对象
function formSerializeToObject(data){
    var dict = {};
    data.forEach(function(item,i){
        dict[item.name] = item.value
    });
    return dict;
}

// dialog 弹框初始化设置
function dialogFunc(){
    $.extend($.fn.dialog.methods, {
        bindButtonEvents: function (jq, param) {
            return jq.each(function () {
                var dialog = $(this);
                dialog.parent().on('click', '.dialog-button a', function (e) {
                    var name = $(this).linkbutton('options').name;
                    var method = param[name];
                    if (method) { method(dialog); }
                });
            });
        }
    });
    $('.easyui-dialog').dialog('bindButtonEvents', {
        Cancel: function (dialog) {
            $(dialog).dialog('close')
        }
    });

    // style
    $('.easyui-dialog').dialog({
        // title: '',            // 弹框标题
		// width : 600,
		// height : 400,
		// closed : true,       // 是否关闭
		// cache : false,       // 缓存
		// draggable : false,   // 拖动
		href : '',             // 嵌入页面
		//modal : false,         // 是否将窗体显示为模式化窗口
		onClose : function() {
			console.log("关闭")
		}
	}).window('center');

    $('.easyui-dialog.easyui-dialog-big').dialog({
		width : 600,
		height : 400
	}).window('center');
}

// 表单验证
function validate(){
    $.extend($.fn.validatebox.defaults.rules, {
        equals: {
            validator: function(value,param){
                return value == $(param[0]).val();
            },
            message: 'Field do not match.'
        },
        pwdLength: {
            validator: function(value, param){
            //正则表达式需要动态传递参数，必须采用正则对象即构造器方式，传入拼接了动态参数的字符串的方式
                var re =new RegExp("^[a-zA-Z0-9]{" + param[0]+ "," + param[1] + "}$","g");
                return re.test(value);
            },
        //提示信息中也需要动态添加参数，此时获取param中的参数方式为{0}、{1}，分别代表param[0]，param[1]
            message: "密码长度要求为{0}-{1}位字母或数字!"
        },
        equalTo: {
            validator:function(value,param){
                return $(param[0]).val() == value;
            },
            message:'字段不匹配'
        }
    });
}

// 图片预览
function imagePreview(obj){
    var file_obj = $(obj)[0].files[0];
    // 浏览器兼容处理 实现图片预览功能
    if(window.URL.createObjectURL){
        var v = window.URL.createObjectURL(file_obj);     // 传obj这个文件对象，相当于把这个文件上传到了浏览器，这个时候就可以预览了
        $('.img_box img').attr('src',v);              // 找到img标签，把src修改后就可以访问了，但是对于浏览器有兼容性
       //  window.URL.revokeObjectURL(v);                  // 手动清除内存中，要想手动，需要加载完毕再去释放#}
        $('.img_box img').load(function () {
            window.URL.revokeObjectURL(v);
        })
    }else if(window.FileReader){
        var file_Read = new FileReader();
        file_Read.onload = function (){
            $(".img_box img").attr('src',this.result);
        };
        file_Read.readAsDataURL(file_obj);
    }else{
        console.log("图片预览失败")
    }
}



