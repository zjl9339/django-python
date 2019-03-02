$(function(){
    init();
    getDepart();
});

function init(){
    // 表格初始化  get the pager of datagrid
    var pager = $('#dg').datagrid().datagrid('getPager');
    pager.pagination({
        buttons:[{
            iconCls:'icon-search',
            handler:function(){
                alert('search');
            }
        },{
            iconCls:'icon-add',
            handler:function(){
                alert('add');
            }
        },{
            iconCls:'icon-edit',
            handler:function(){
                alert('edit');
            }
        }]
    });
    // 获取部门列表
    $('#depart').combobox('reload', '/getDepart/')
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
        data: formSerializeToObject($("form").serializeArray()),
        success: function(ret){
            $('#dlg').dialog('close');
            location.href = ""
        }
    });
}

function dlgShow(index){
    if(index){
        $("#dg").datagrid('selectRow',index);
        var row = $("#dg").datagrid('getSelected');
        if(row){
            $("#dlg").dialog("open").dialog("setTitle","author modify");
            $("#form").form("load",row);
            // url = ""
        }
    }else {
        $("#dlg").dialog("open").dialog("setTitle","author add");
        $("#form").form("load","");
    }

}
function edit(){
    if(!$('#form').form('enableValidation').form('validate')) return;
    $.ajax({
        type: 'post',
        url: '{% url "modifyAuthor" %}',
        data: formSerializeToObject($("form").serializeArray()),
        success: function(ret){
            $('#dlg').dialog('close');
            location.href = "/author/"
        }
    });
}

function del(id){
    $.messager.confirm('删除', 'Are you confirm this?', function(r){
        if (r){
            $.ajax({
                type: 'post',
                url: '/delAuthor/',
                data: {
                    'id': id,
                },
                success: function(ret){
                    location.href = "/author/";
                }
            });
        }
    });
}