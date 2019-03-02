$(function(){
    initAuthor();
    getPublisher();
    $("#searchBtn").click(function(){ searchList(); })
});

function initAuthor(){
    var pager = $('#dg').datagrid().datagrid('getPager');	// get the pager of datagrid
    pager.pagination({
        loadMsg:'数据加载中....',
    });

    //  邮箱失去焦点时  根绝相关规则获取用户登录账号
    $('[name="email"]').textbox({
        inputEvents: $.extend({}, $.fn.textbox.defaults.inputEvents, {
            blur: function (event) {
                $("#account").textbox("setValue",this.value.substr(0,this.value.indexOf("@")))
            }
        })
    });
}

function formatOper(val,row,index){
    var html = '<a href="javascript:;" class="easyui-linkbutton" onclick="dlgShow('+index+')">修改</a>' +
        '<a href="javascript:;" class="easyui-linkbutton" onclick="del('+row.id+')">删除</a>';
    return html
}

function add(){
    if(!$('#form').form('enableValidation').form('validate')) return;
    $.ajax({
        type: 'post',
        url: '/addAuthor/',
        data: formSerializeToObject($("#form").serializeArray()),
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
    $.ajax({
        type: 'post',
        url: '/modifyAuthor/',
        data: formSerializeToObject($("#form").serializeArray()),
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

