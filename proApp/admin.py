from django.contrib import admin
from .models import Article,BioDrug,Entry,Author,Blog,Person,Catinfo,Department, Book, Publisher


admin.site.site_header = '修改后'
admin.site.site_title = '哈哈'

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',"content", 'publish_date', 'update_time',)
admin.site.register(Article,ArticleAdmin)

admin.site.register(BioDrug)
admin.site.register(Entry)

class AuthorAdmin(admin.ModelAdmin):
    list_max_show_all = 10
    list_per_page = 10         # 分页
    list_display_links = ('id', 'account')                          # 哪些字段 点击链接进入编辑界面
    search_fields = ('name', 'depart',)                            # 搜索字段
    list_filter = ('name', 'account', 'depart', 'publish_date' )   # 过滤器
    list_editable = ( 'name', )                                  # 可编辑那几个字段
    date_hierarchy = 'publish_date'                             # 头部添加  详细时间分层筛选　
    ordering = ('-publish_date',)                               # 排序
    fk_fields = ('id',)                                          # 设置显示外键字段
    empty_value_display = ' -空白- '
    # fields = (('name', 'account'), 'password', 'email', 'sex', 'depart', 'phone',)  # 修改页  多字段一行展示
    # fieldsets = (                                                # 修该页  分组显示
    #     ("base info", {'fields': ['name', 'account', 'sex']}),
    #     ("Content", {'fields': ['password', 'email','depart','phone']})
    # )
    readonly_fields = ('account',)         #  只读字段
    list_display = ('id','name', "account", 'password', 'email', 'sex', 'depart', 'head_img', 'image_show', 'phone', 'publish_date')  # 展示字段

    # def get_readonly_fields(self, request, obj=None):
    #     """  重新定义此函数，限制普通用户所能修改的字段  """
    #     if request.user.is_superuser:
    #         self.readonly_fields = []
    #     return self.readonly_fields

    def save_model(self, request, obj, form, change):
        """  重新定义此函数，提交时自动添加申请人和备案号  """
        def make_paper_num():
            """ 生成随机备案号 """
            import datetime
            import random
            CurrentTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
            RandomNum = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
            UniqueNum = str(CurrentTime) + str(RandomNum)   # 2018122815425634
            return UniqueNum

        obj.proposer = request.user
        obj.paper_num = make_paper_num()
        super(AuthorAdmin, self).save_model(request, obj, form, change)

admin.site.register(Author,AuthorAdmin)

admin.site.register(Blog)
admin.site.register(Person)
admin.site.register(Catinfo)
admin.site.register(Department)

class BookAdmin(admin.ModelAdmin):
    list_display = ( 'name',"price", 'saleNum', 'publisher','author_list','publish_date')
admin.site.register(Book,BookAdmin)

admin.site.register(Publisher)