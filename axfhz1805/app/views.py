import uuid

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from app.models import Wheel, Nav, Mustbuy, shop, Mainshow, FoodTypes, Goods, UserModel, CartModel, OrderModel, \
    OrderGoods


def home(request):

    wheels = Wheel.objects.all()
    navs = Nav.objects.all()
    mustbuys = Mustbuy.objects.all()
    shops = shop.objects.all()
    shops1 = shops[0]
    shops2_3 = shops[1:3]
    shops4_7 = shops[3:7]
    shops8_ = shops[7:]
    mainshows = Mainshow.objects.all()
    data = {
        "title": "主页",
        "wheels": wheels,
        "navs": navs,
        "mustbuys": mustbuys,
        "shops1": shops1,
        "shops2_3": shops2_3,
        "shops4_7": shops4_7,
        "shops8_": shops8_,
        'mainshows': mainshows,
    }

    return render(request, 'home/home.html', context=data)


def market(request):
    # 查询所有的商品类型信息
    # foodtypes = FoodTypes.objects.all().order_by('typesort')
    # goods = Goods.objects.all()
    # data = {
    #     "title": "闪购",
    #     'foodtypes': foodtypes,
    #     'goods': goods,
    # }
    #
    # return render(request, 'market/market.html', context=data)
    # 默认104749表示显示热销榜
    return redirect(reverse('axf:marketWithParam',args=(104749,0,0)))



# typeid 商品分类id
# childid 子分类id
def marketWithParam(request,typeid,childid,sorttype):

    foodtypes = FoodTypes.objects.all().order_by('typesort')

    goods = Goods.objects.filter(categoryid=typeid)

    if not str(childid) == '0':
        # 再次根据子分类id进行筛选
        goods = goods.filter(childcid=childid)

    if int(sorttype) == 0:
        pass
    elif int(sorttype) == 1:
        goods = goods.order_by("-productnum")
    elif int(sorttype) == 2:
        goods = goods.order_by("price")
    elif int(sorttype) == 3:
        goods = goods.order_by("-price")

    foodtype = FoodTypes.objects.filter(typeid=typeid).first()

    childtypenames = foodtype.childtypenames.split("#")

    allChild = []

    for child in childtypenames:
        allChild.append(child.split(":"))

    data = {
        "title": "闪购",
        'foodtypes': foodtypes,
        'goods': goods,
        'typeid': str(typeid),
        'allChild': allChild,
        'childid': int(childid),
    }

    # 获得当前用户的购物车的数据
    user_id = request.session.get("user_id")
    if user_id:
        user = UserModel.objects.filter(pk=user_id).first()
        carts = CartModel.objects.filter(c_user=user)
        data["carts"] = carts

    return render(request, 'market/market.html', context=data)


def cart(request):
    userid = request.session.get("user_id")
    if userid:
        user = UserModel.objects.filter(pk=userid).first()
    else:
        return redirect(reverse('axf:login'))

    carts = CartModel.objects.filter(c_user=user)
    isAllselect = True
    for cart in carts:
        if not cart.c_isselect:
            isAllselect = False
            break
    countAndPrice = totalCountAndPrice(user)


    data = {
        "title": "购物车",
        "carts": carts,
        'isAllselect': isAllselect,
        'totalCount': countAndPrice['totalCount'],
        'totalPrice': countAndPrice['totalPrice'],
    }

    return render(request, 'cart/cart.html', context=data)


def mine(request):
    userid = request.session.get("user_id")
    data = {}
    data['title'] = "我的"
    if userid:
        user = UserModel.objects.filter(pk=userid).first()
        # user = UserModel()
        data["user"] = user
        data["imgPath"] = '/static/upload/'+user.u_img.url

        objects = OrderModel.objects.filter(o_user=user)
        nopay = objects.filter(o_status=1).count()
        noCollect = objects.filter(o_status=2).count()
        noEvaluate = objects.filter(o_status=3).count()
        returnGoods = objects.filter(o_status=4).count()

        data["nopay"] = nopay
        data["noCollect"] = noCollect
        data["noEvaluate"] = noEvaluate
        data["returnGoods"] = returnGoods
    else:
        data["user"] = None


    return render(request, 'mine/mine.html', context=data)


def register(request):
    if request.method == "GET":
        # 展示注册界面
        return render(request, 'user/register.html')
    elif request.method == "POST":
        # 获得表单提交的数据
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        img = request.FILES.get("img")
        # print(username)
        # print(password)
        # print(email)
        # print(img)
        user = UserModel()
        user.u_name = username
        user.u_password = password
        user.u_email = email
        user.u_img = img

        user.save()

        return HttpResponseRedirect(reverse('axf:login'))


# 定义一个函数,用来验证用户名的唯一性
def checkUserUnique(request):
    username = request.GET.get("username")
    # print(username)
    # 根据用户名去查询数据库
    res = UserModel.objects.filter(u_name=username)
    data = {}
    if res.exists():
        data["code"] = 800
        data["msg"] = '用户名已存在'
    else:
        data["code"] = 801
        data["msg"] = '用户名可用'

    return JsonResponse(data)

def login(request):
    if request.method == "GET":
        return render(request,'user/user_login.html')
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        # print(username)
        # print(password)
        res = UserModel.objects.filter(u_name=username)
        data = {}
        if res.exists():
            user = res.first()
            # user = user()
            mypassword = user.u_password
            if password == mypassword:
                # 保留登录成功的状态
                request.session["user_id"] = user.id
                # 进入 我的 页面
                return HttpResponseRedirect(reverse('axf:mine'))

            return HttpResponse("用户名或密码错误")

        return HttpResponse("用户名不存在")


def logout(request):
    # 清除session
    request.session.flush()

    return redirect(reverse('axf:login'))


def addToCart(request):
    userid = request.session.get("user_id")
    data = {}
    if userid:
        user = UserModel.objects.filter(pk=userid).first()
    else:
        # 在ajax请求中,不能进行重定向
        # return redirect(reverse('axf:login'))
        data["code"] = 304 #需要重定向到登录页面
        data["msg"] = "登录后可继续操作"
        return JsonResponse(data)

    goodsid = request.GET.get("goodsid")
    goods = Goods.objects.filter(pk=goodsid).first()

    # 查询cart记录
    res = CartModel.objects.filter(c_user=user).filter(c_goods=goods)
    if res.exists():
        cart = res.first()
        # cart = CartModel()
        cart.c_num += 1
        cart.save()
        data["code"] = 200
        data["msg"] = '添加到购物车成功'
        data["num"] = cart.c_num
    else:
        cart = CartModel()
        cart.c_user = user
        cart.c_goods = goods
        cart.save()
        data["code"] = 200
        data["msg"] = '添加到购物车成功'
        data["num"] = 1

    return JsonResponse(data)


# 将购物车中的商品数量-1
def subToCart(request):
    userid = request.session.get("user_id")
    data = {}
    if userid:
        user = UserModel.objects.filter(pk=userid).first()
    else:
        # 在ajax请求中,不能进行重定向
        # return redirect(reverse('axf:login'))
        data["code"] = 304  # 需要重定向到登录页面
        data["msg"] = "登录后可继续操作"
        return JsonResponse(data)

    goodsid = request.GET.get("goodsid")
    goods = Goods.objects.filter(pk=goodsid).first()

    # 查询cart记录
    res = CartModel.objects.filter(c_user=user).filter(c_goods=goods)
    if res.exists():
        cart = res.first()
        num = cart.c_num
        if cart.c_num == 1:#删除该记录
            cart.delete()
            data["code"]  = 200
            data["msg"] = "操作成功"
            data["num"] = 0
        else:#大于1
            cart.c_num -=1
            cart.save()
            data["code"] = 200
            data["msg"] = "操作成功"
            data["num"] = cart.c_num
    else:
        data['code'] = 200
        data['msg'] = '购物车没有该记录'
        data['num'] = 0

    return JsonResponse(data)


# 修改购物车商品数量,加操作
def addCart(request):
    # 获取商品id
    cartid = request.GET.get('cartid')
    cart = CartModel.objects.filter(pk=cartid).first()
    cart.c_num +=1
    cart.save()
    data = {}
    data["code"] = 200
    data["msg"] = '数量加操作成功'
    data["num"] = cart.c_num
    return JsonResponse(data)


# 修改购物车商品数量,减操作
def subCart(request):
    # 获取商品id
    cartid = request.GET.get('cartid')
    cart = CartModel.objects.filter(pk=cartid).first()
    num = cart.c_num
    data = {}
    if num == 1:
        cart.delete()
        data["code"] = 201
        data["msg"] = '数量减操作成功'
        data["num"] = 0
    elif num > 1:
        cart.c_num -= 1
        cart.save()
        data["code"] = 200
        data["msg"] = '数量减操作成功'
        data["num"] = cart.c_num
    return JsonResponse(data)



def changeSelectStatu(request):
    # 获取购物车id
    cartid = request.GET.get("cartid")
    # 根据订单号查询出cart订单记录
    cart = CartModel.objects.filter(pk=cartid).first()
    # 修改订单的状态
    # cart = CartModel()
    cart.c_isselect = not cart.c_isselect
    cart.save()

    # 是否全选
    user_id = request.session.get("user_id")
    user = UserModel.objects.filter(pk=user_id).first()
    # 获得该用户下的所有的购物车数据
    carts = CartModel.objects.filter(c_user=user)

    isAllSelect = True
    for cart1 in carts:
        # cart = CartModel()
        if not cart1.c_isselect:
            isAllSelect = False
    data = {}
    data["code"] = 200 #状态码,表示修改成功
    data["msg"] = '状态修改成功'
    data["isselect"] = cart.c_isselect
    data["isAllSelect"] = isAllSelect

    countAndPrice = totalCountAndPrice(user)
    data['totalCount'] = countAndPrice['totalCount']
    data['totalPrice'] = countAndPrice['totalPrice']

    return JsonResponse(data)


def changeManySelectStatu(request):
    selectList = request.GET.get("selectArray").split("#")
    flag = request.GET.get("flag")
    carts = CartModel.objects.filter(id__in=selectList)
    data={}
    for cart in carts:
        if flag == "1":
            cart.c_isselect = False
        elif flag == "2":
            cart.c_isselect = True
        cart.save()
    data["code"] = 200

    return JsonResponse(data)


# 定义一个函数,用来计算选中的商品的数量和总价格
def totalCountAndPrice(user):
    # 查询出所有选中的cart记录
    carts = CartModel.objects.filter(c_user=user).filter(c_isselect=True)
    # 选中的商品数量
    totalCount = 0
    # 选中商品的总价格
    totalPrice = 0
    for cart in carts:
        totalCount += cart.c_num
        totalPrice += cart.c_num * cart.c_goods.price

    # return (totalCount,totalPrice)
    return {'totalCount': totalCount, 'totalPrice': totalPrice}


# 目的：生成一个订单
#     1.先创建一个订单
#         1.订单号--uuid
#         2.用户--
#             获得user_id,查询出对应的user
#         3.设置时间*(自动)
#         4.设置状态(待付款 1)
#         5.保存
#     2.再创建多个订单商品关系表
#         0.创建一个订单商品关系
#         1.订单号--关联上方的订单
#         2.商品对象--cart中
#         3.商品数量--cart中
#         4.保存
#         5.删除对应的cart记录
#     3.返回结果给前端
def createOrder(request):
    userid = request.session.get("user_id")
    user = UserModel.objects.filter(pk=userid).first()
    order = OrderModel()
    order.o_num = str(uuid.uuid4())
    order.o_user = user
    order.o_status = 1
    order.save()
    cartidList = request.GET.get("selectArray").split("#")
    carts = CartModel.objects.filter(id__in=cartidList)
    for cart in carts:
        orderGoods = OrderGoods()
        orderGoods.og_order = order
        orderGoods.og_goods = cart.c_goods
        orderGoods.og_num = cart.c_num

        orderGoods.save()
        cart.delete()
    data = {
        "code": 200,
        "ordernum": order.o_num,
    }
    return JsonResponse(data)


# 展示订单详细信息
def orderInfo(request,ordernum):
    # print(ordernum)
    # 查询该订单下的所有商品信息
    order = OrderModel.objects.filter(o_num=ordernum).first()
    orderGoods = OrderGoods.objects.filter(og_order=order)
    statu = order.o_status
    if statu == 0:
        orderStatu = "无效"
    elif statu == 1:
        orderStatu = "代付款"
    elif statu == 2:
        orderStatu = "待收货"
    elif statu == 3:
        orderStatu = "待评价"
    elif statu == 4:
        orderStatu = "售后/退款"
    data={
        'title': "订单详情",
        "orderGoods":orderGoods,
        "ordernum":ordernum,
        "orderstatu": orderStatu,
    }

    return render(request,'cart/orderinfo.html',context=data)


# 修改订单的状态
def changeOrderStatus(request):
    # 获取订单号和要改的状态
    status = request.GET.get("status")
    ordernum = request.GET.get("ordernum")
    order = OrderModel.objects.filter(o_num=ordernum).first()
    # order = OrderModel()
    order.o_status = status
    order.save()
    data = {
        "code": 200,
    }
    return JsonResponse(data)