$(function(){
    initAuthor();
    getDepart();
    getAuthor();
    $("#searchBtn").click(function(){ searchList(); })
});

function initAuthor(){
    //  邮箱失去焦点时  根剧相关规则获取用户登录账号
    $('[name="email"]').textbox({
        inputEvents: $.extend({}, $.fn.textbox.defaults.inputEvents, {
            blur: function (event) {
                $("#account").textbox("setValue",this.value.substr(0,this.value.indexOf("@")));
                $('#email').textbox('setValue',this.value)
            }
        })
    });
}

function formatOper(val,row,index){
    var html = '<a href="javascript:;" class="easyui-linkbutton" onclick="dlgShow('+index+')">修改</a>' +
        '<a href="javascript:;" class="easyui-linkbutton" onclick="del('+row.id+')">删除</a>' +
        '<a href="javascript:;" class="easyui-linkbutton" onclick="resetPsd('+row.id+')">重置密码</a>';
    return html
}

function add(){
    if(!$('#form').form('enableValidation').form('validate')) return;
    var formData = new FormData();
    formData.append("headimg", $("#headimg")[0].files[0]);
    formData.append('csrfmiddlewaretoken', $("#csrf_token").val());
    $("#form").serializeArray().forEach(function(item,i){
        formData.append(item.name , item.value)
    });
    $.ajax({
        type: 'post',
        url: '/addAuthor/',
        data: formData,
        processData: false,         // tell jquery not to process the data
        contentType: false,
        success: function(data){
            layer.msg(data.retMsg);
            if(data.success){
                $('#dlg').dialog('close');
                $('#dg').datagrid('reload');
            }
        }
    });
}

function dlgShow(index){
    if(index != undefined){
        $("#dg").datagrid('selectRow',index);
        var row = $("#dg").datagrid('getSelected');
        $("#modifyId").val(row.id);
        if(row){
            $("#dlg").dialog("open").dialog("setTitle","author modify");
            $("#form").form("load",row);
            $(".img_box img").attr("src",row.head_img)
        }
    }else {
        $("#dlg").dialog("open").dialog("setTitle","author add");
        $("#form").form('clear');
        $("#modifyId").val("")
    }

    //  密码输入框 默认赋值
    $("#defaultPsd").textbox("setValue","123456")

}
function edit(){
    if(!$('#form').form('enableValidation').form('validate')) return;
    var formData = new FormData();
    formData.append("headimg", $("#headimg")[0].files[0]);
    formData.append('csrfmiddlewaretoken', $("#csrf_token").val());
    $("#form").serializeArray().forEach(function(item,i){
        formData.append(item.name , item.value)
    });
    $.ajax({
        type: 'post',
        url: '/modifyAuthor/',
        data: formData,
        processData: false,         // tell jquery not to process the data
        contentType: false,
        success: function(data){
            layer.msg(data.retMsg);
            if(data.success){
                $('#dlg').dialog('close');
                $('#dg').datagrid('reload');
            }
        }
    });
}

function del(id){
    $.messager.confirm('Author删除', 'Are you confirm this?', function(r){
        if (r){
            $.ajax({
                type: 'post',
                url: '/delAuthor/',
                data: {
                    'id': id,
                },
                success: function(data){
                    layer.msg(data.retMsg);
                    if(data.success){
                        $('#dg').datagrid('reload');
                    }
                }
            });
        }
    });
}

function resetPsd(id){

}

function searchList(){
    var postData = formSerializeToObject($("#searchForm").serializeArray());
    if(postData.dateFrom) postData.dateFrom = moment(postData.dateFrom).format("YYYY-MM-DD HH:mm:ss");
    if(postData.dateTo) postData.dateTo = moment(postData.dateTo).format("YYYY-MM-DD HH:mm:ss");
    postData.page = $(".pagination-num").val();
    postData.rows = $(".pagination-page-list").val();
    postData.name = $('#author').combobox('getText');
    $.ajax({
        type: 'post',
        url: '/getAuthor/',
        data: postData,
        success: function(data){
            layer.msg(data.ret.retMsg);
            if(data.ret.success){
                $('#dg').datagrid('loadData',data);
            }
        }
    });
}

// 图书封面 上传
function uploadHeadPic(obj){
    var file_obj = $(obj)[0].files[0];
    // if (!file_obj.type.match('image.*')) {
    //     layer.msg("请选择符合格式的图片");
    //     return;
    // }
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
        console.log(3333)
    }
    $.ajaxFileUpload({
		url : "/uploadHeadimg/?id="+$("#modifyId").val(),
		secureuri : false,                 // 一般设置为false
		fileElementId : "headimg",       // 文件上传表单input的id
		// async : false,
		type:'post',
        processData: false,         // tell jquery not to process the data
        contentType: false,         // tell jquery not to set contentType
        dataType : 'json',              // 返回值类型 一般设置为json
		success : function(ret) {       // 服务器成功响应处理函数
		    if(ret.success){
		        layer.msg("头像上传成功！");
            }
		},
        error: function(data, status, e) {  //提交失败自动执行的处理函数。
            layer.msg(e);
        }
	});
}

function formatSex(val,row){
    return val=="1" ? "女" : "男";
}

function formatDepart(val,row){
    if(departList){
        for(var i=0;i<departList.length;i++){
            if(departList[i].id==val){
                return departList[i].name
            }
        }
        return '--'
    }
}

