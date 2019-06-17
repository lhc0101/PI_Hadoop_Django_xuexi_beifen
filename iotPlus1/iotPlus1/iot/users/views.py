from .forms import RegisterForm
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import requests as rts
from users.models import HistoryValue
from django.conf import settings

from django.db import connection
from django.http import HttpResponse
from django.template import loader
from pyecharts import Line

from django.shortcuts import render, redirect

from email.mime.text import MIMEText
import smtplib
from users import models



REMOTE_HOST = "https://pyecharts.github.io/assets/js"


def list_shebei(request):
    ret = models.HistoryValue.objects.all().order_by("shebieid")
    context = {'list_shebei':ret}
    return render(request, 'list_shebei.html', context)

def delete_shebei(request):
    del_id = request.GET.get("id", None)  # 字典取值,娶不到默认为None
    # 如果能取到id值
    if del_id:
        # 去数据库删除当前id值的数据
        # 根据id值查找到数据
        del_obj = models.HistoryValue.objects.filter(shebieid=del_id)
        # 删除
        del_obj.delete()
        # 返回删除后的页面,跳转到出版社的列表页,查看删除是否成功
        return redirect("/list_shebei/")
    else:
        return HttpResponse("要删除的数据不存在!")

def edit_shebei(request):
    # 用户修改完出版社的名字,点击提交按钮,给我发来新的出版社名字
    if request.method == "POST":
        print(request.POST)
        # 取新出版社名字
        edit_id = request.POST.get("id")
        # 更新出版社
        # 根据id取到编辑的是哪个出版社
        edit_obj = models.HistoryValue.objects.get(shebieid=edit_id)
        edit_obj.shebieid = edit_id
        edit_obj.save()  # 把修改提交到数据库
        # 跳转出版社列表页,查看是否修改成功
        return redirect("/list_shebei/")
    # 从GET请求的URL中取到id参数
    edit_id = request.GET.get("id")
    if edit_id:
        # 获取到当前编辑的出版社对象
        obj = models.HistoryValue.objects.filter(shebieid=edit_id)
        return render(request, "edit_shebei.html", {"obj": obj})
    else:
        return HttpResponse("编辑的出版社不存在!")


def exc_sql(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def pyecharts(request):
    template = loader.get_template('pyecharts.html')
    b = bar()
    context = dict(
        myechart=b.render_embed(),
        host=REMOTE_HOST,
        script_list=b.get_js_dependencies()
    )
    return HttpResponse(template.render(context, request))

def charts1(request):
    template = loader.get_template('pyecharts1.html')
    b = bar1()
    context = dict(
        myechart=b.render_embed(),
        host=REMOTE_HOST,
        script_list=b.get_js_dependencies()
    )
    return HttpResponse(template.render(context, request))

def charts2(request):
    template = loader.get_template('pyecharts2.html')
    b = bar2()
    context = dict(
        myechart=b.render_embed(),
        host=REMOTE_HOST,
        script_list=b.get_js_dependencies()
    )
    return HttpResponse(template.render(context, request))

def charts3(request):
    template = loader.get_template('pyecharts3.html')
    b = bar3()
    context = dict(
        myechart=b.render_embed(),
        host=REMOTE_HOST,
        script_list=b.get_js_dependencies()
    )
    return HttpResponse(template.render(context, request))

def charts4(request):
    template = loader.get_template('pyecharts4.html')
    b = bar4()
    context = dict(
        myechart=b.render_embed(),
        host=REMOTE_HOST,
        script_list=b.get_js_dependencies()
    )
    return HttpResponse(template.render(context, request))


def bar():
    query_sql = "select  temperature,humidity,turanghanshuliang,guangzhao from historyvalue"
    data_list = exc_sql(query_sql)
    temperature = [i[0] for i in data_list]
    humidity = [i[1] for i in data_list]
    turanghanshuliang = [i[2] for i in data_list]
    guangzhao = [i[3] for i in data_list]
    attr = ["{}时".format(i) for i in range(1, 24)]
    bar = Line("植物24小时状态")
    bar.add(
        "大气24h温度",
        attr,
        temperature,
        mark_point=["max", "min"],
        mark_line=["average"],
        yaxis_formatter="°C",
    )
    bar.add(
        "大气24h湿度",
        attr,
        humidity,
        mark_point=["max", "min"],
        mark_line=["average"],
        yaxis_formatter="%RH",
    )
    bar.add(
        "土壤24h含水量",
        attr,
        turanghanshuliang,
        mark_point=["max", "min"],
        mark_line=["average"],
        yaxis_formatter="%",
    )
    bar.add(
        "生长24h光照强度",
        attr,
        guangzhao,
        mark_point=["max", "min"],
        mark_line=["average"],
        yaxis_formatter="Lux",
    )
    bar.render()
    return bar

def bar1():
    # query_sql = "select  temperature from tem"
    query_sql = "select  temperature from my_iot_historyvalue"
    data_list = exc_sql(query_sql)
    lens = len(data_list)
    print(data_list)
    x = data_list[:lens-24:-1][::-1]
    print(x)
    # temperature = [i[0] for i in data_list]
    attr = ["{}时".format(i) for i in range(1, 24)]
    bar1 = Line("植物24小时状态")
    bar1.add(
        "大气24h温度",
        attr,
        x,
        mark_point=["max", "min"],
        mark_line=["average"],
        yaxis_formatter="°C",
    )
    bar1.render()
    return bar1


def bar2():
    query_sql = "select humidity from historyvalue"
    data_list = exc_sql(query_sql)
    humidity = [i[0] for i in data_list]
    attr = ["{}时".format(i) for i in range(1, 24)]
    bar2 = Line("植物24小时状态")

    bar2.add(
        "大气24h湿度",
        attr,
        humidity,
        mark_point=["max", "min"],
        mark_line=["average"],
        yaxis_formatter="%RH",
    )

    bar2.render()
    return bar2


def bar3():
    query_sql = "select  turanghanshuliang from historyvalue"
    data_list = exc_sql(query_sql)
    turanghanshuliang = [i[0] for i in data_list]
    attr = ["{}时".format(i) for i in range(1, 24)]
    bar3 = Line("植物24小时状态")
    bar3.add(
        "土壤24h含水量",
        attr,
        turanghanshuliang,
        mark_point=["max", "min"],
        mark_line=["average"],
        yaxis_formatter="%",
    )

    bar3.render()
    return bar3
def bar4():
    query_sql = "select guangzhao from historyvalue"
    data_list = exc_sql(query_sql)
    guangzhao = [i[0] for i in data_list]
    attr = ["{}时".format(i) for i in range(1, 24)]
    bar4 = Line("植物24小时状态")
    bar4.add(
        "生长24h光照强度",
        attr,
        guangzhao,
        mark_point=["max", "min"],
        mark_line=["average"],
        yaxis_formatter="Lux",
    )
    bar4.render()
    return bar4





def getValue():
    t = ''
    h = ''
    s = ''
    g = ''
    id = ''
    if settings.CURRENT_TEMPERATURE == None:
        t = "无读数"
    else:
        t = str(settings.CURRENT_TEMPERATURE)
    if settings.CURRENT_HUMIDITY == None:
        h = "无读数"
    else:
        h = str(settings.CURRENT_HUMIDITY)
    if settings.CURRENT_SHIDU == None:
        s = "无读数"
    else:
        s = str(settings.CURRENT_SHIDU)
    if settings.CURRENT_GUANGZHAO == None:
        g = "无读数"
    else:
        g = str(settings.CURRENT_GUANGZHAO)
    if settings.CURRENT_SHEBEIID == None:
        id = "无读数"
    else:
        id = str(settings.CURRENT_SHEBEIID)
    return t, h, s, g , id

def send_mail(message):
    # message = "尊敬的I植物保姆用户，您账号下的{id}的"
    msg = MIMEText(message,"plain ","utf - 8")
    msg['FROM']="I植物保姆"
    msg['Subject'] = "【I植物保姆状态提醒】"
    receivers = ['321782792@qq.com']
    server = smtplib.SMTP(settings.EMAIL_HOST,settings.EMAIL_PORT)
    server.set_debuglevel(1)
    server.login(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)
    server.sendmail(settings.EMAIL_FROM,receivers,msg.as_string())
    server.close()

# @login_required
def index(request):
    t, h, s, g ,id= getValue()
    return render(request, 'index.html', {'t':t, 'h':h, 's':s, 'g':g ,'id':id})

@csrf_exempt
def data(request):
    if 'data' in request.GET:
        d = json.loads(request.GET['data'].replace("'", '"'))
        print("get data {0}, {1}, {2}, {3},{4}".format(d['t'], d['h'], d['s'], d['g'], d['id']))
        # value = HistoryValue(temperature=d['t'], humidity=d['h'],shidu=d['s'],guangzhao=d['g'])
        # value.save()
        settings.CURRENT_TEMPERATURE = d['t']
        settings.CURRENT_HUMIDITY = d['h']
        settings.CURRENT_SHIDU = d['s']
        settings.CURRENT_GUANGZHAO = d['g']
        settings.CURRENT_SHEBEIID = d['id']
        if settings.CURRENT_GUANGZHAO != None:
            message = "尊敬的‘I’植物保姆用户Test1，您好，您账号下的id为的植物需要照顾了,快登录网站或微信小程序看看吧。"
            send_mail(message)
    if 'get' in request.GET:
        rts.get("http://iot1.xchcloud.cn:5000" + "?op=" + request.GET['get'])
    if 'recv' in request.GET:
        t, h, s, g , id = getValue()
        return HttpResponse(json.dumps({'t': t, 'h': h, 's': s, 'g':g , 'id':id}))
    return HttpResponse("ok")

def detail(request):
    return render(request,'detail.html')



def register(request):
    # 从 get 或者 post 请求中获取 next 参数值
    # get 请求中，next 通过 url 传递，即 /?next=value
    # post 请求中，next 通过表单传递，即 <input type="hidden" name="next" value="{{ next }}"/>
    redirect_to = request.POST.get('next', request.GET.get('next', ''))

    # 只有当请求为 POST 时，才表示用户提交了注册信息
    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、确认密码、邮箱（email）
        # 用这些数据实例化一个用户注册表单
        form = RegisterForm(request.POST)

        # 验证数据的合法性
        if form.is_valid():
            # 如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库
            form.save()

            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm()

    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    # 将记录用户注册前页面的 redirect_to 传给模板，以维持 next 参数在整个注册流程中的传递
    return render(request, 'users/register.html', context={'form': form, 'next': redirect_to})


def user(request):
    return render(request, 'user.html')

def design(request):
    return render(request, 'design.html')

def water(request):
    return render(request, 'water.html')

def add(request):
    return render(request, 'add.html')

def jiankong(request):
    return render(request, 'jiankong.html')
from users.models import User
# def shebei(request):
#     # print("0")
#     if request.method == 'POST':
#         id = request.POST.get("id", None)
#         # 添加到数据库
#         shebeiid = HistoryValue(shebieid=id)
#         shebeiid.save()
#         print("1")
#     return HttpResponseRedirect('/add/')