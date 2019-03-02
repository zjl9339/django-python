var departList = [];
var authorList = [];
var publisherList = [];
var bookList = [];

$(function(){

});


// 获取部门字典数据  combobox初始化
function getDepart(){
    $.ajax({
		url : "/showTreeDepart/",
		type: 'get',
		async: false,
		success: function(data){
		    var searchName  = [{"name":"全部","id":"-1"}].concat(data);
            $('#searchForm [name="depart"]').combobox({
                data: searchName,
                valueField :"id",
                textField : "name",
                panelHeight:'200',
                onSelect:function(obj){
                },
                onLoadSuccess: function (data){
                    $(this).combobox("setValue","-1")
                }
            });
            $('[name="depart"]').combobox({
                data: data,
                valueField :"id",
                textField : "name",
                // multiple:true,
                panelHeight:'200',
                onSelect:function(obj){
                },
                onLoadSuccess: function (data){
                    departList = data;
                }
            });
		}
	});
}


// 获取出版社字典数据  combobox初始化
function getPublisher(){
    $.ajax({
		url : "/getPublisher/",
		type: 'get',
		async: false,
		success: function(data){
		    var searchName  = [{"name":"全部","id":"-1"}].concat(data);
            $('#searchForm [name="publisher"]').combobox({
                data: searchName,
                valueField :"id",
                textField : "name",
                panelHeight:'200',
                onSelect:function(obj){
                },
                onLoadSuccess: function (data){
                    $(this).combobox("setValue","-1")
                }
            });
            $('[name="publisher"]').combobox({
                data: data,
                valueField :"id",
                textField : "name",
                panelHeight:'200',
                onSelect:function(obj){
                },
                onLoadSuccess: function (data){
                    publisherList = data;
                }
            });
		}
	});
}

// 获取作者字典数据  combobox初始化
function getAuthor(){
    $.ajax({
		url : "/getAuthor/",
		type: 'get',
		async: false,
		success: function(data){
		    var searchName  = [{"name":"全部","id":"-1"}].concat(data);
            $('#searchForm [name="author"]').combobox({
                editable: false, // 不能直接输入到列表框
                data: searchName,
                valueField :"id",
                textField : "name",
                panelHeight:'200',
                missingMesage: '请选择',
                onSelect:function(obj){
                },
                onLoadSuccess: function (data){
                    $(this).combobox("setValue","-1")
                }
            });
            $('[name="author"]').combobox({
                data: data,
                valueField :"id",
                textField : "name",
                panelHeight:'200',
                multiple:true,
                onSelect:function(obj){
                },
                onLoadSuccess: function (data){
                    authorList = data;
                }
            });
		}
	});
}

// 获取书籍字典数据  combobox初始化
function getBook(){
    $.ajax({
		url : "/getBook/",
		type: 'get',
		async: false,
		success: function(data){
		    var searchName  = [{"name":"全部","id":"-1"}].concat(data);
            $('#searchForm [name="bookname"]').combobox({
                data: searchName,
                valueField :"id",
                textField : "name",
                panelHeight:'200',
                onSelect:function(obj){
                },
                onLoadSuccess: function (data){
                    $(this).combobox("setValue","-1")
                }
            });
            $('[name="bookname"]').combobox({
                data: data,
                valueField :"id",
                textField : "name",
                panelHeight:'200',
                onSelect:function(obj){
                },
                onLoadSuccess: function (data){
                    bookList = data;
                }
            });
		}
	});
}


