from django.db import models

# Create your models here.
class Home(models.Model):
    img = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    trackid = models.CharField(max_length=50)

    class Meta:
        abstract = True

class Wheel(Home):
    class Meta:
        db_table = 'axf_wheel'


class Nav(Home):
    class Meta:
        db_table = 'axf_nav'


class Mustbuy(Home):
    class Meta:
        db_table = 'axf_mustbuy'


class shop(Home):
    class Meta:
        db_table = 'axf_shop'


class Mainshow(models.Model):
    trackid = models.CharField(max_length=16)
    name = models.CharField(max_length=50)
    img = models.CharField(max_length=200)
    categoryid = models.CharField(max_length=16)
    brandname = models.CharField(max_length=50)

    img1= models.CharField(max_length=200)
    childcid1= models.CharField(max_length=16)
    productid1= models.CharField(max_length=16)
    longname1= models.CharField(max_length=100)
    price1= models.FloatField(default=0)
    marketprice1= models.FloatField(default=0)

    img2 = models.CharField(max_length=200)
    childcid2 = models.CharField(max_length=16)
    productid2 = models.CharField(max_length=16)
    longname2 = models.CharField(max_length=100)
    price2 = models.FloatField(default=0)
    marketprice2 = models.FloatField(default=0)

    img3 = models.CharField(max_length=200)
    childcid3 = models.CharField(max_length=16)
    productid3 = models.CharField(max_length=16)
    longname3 = models.CharField(max_length=100)
    price3 = models.FloatField(default=0)
    marketprice3 = models.FloatField(default=0)

    class Meta:
        db_table = "axf_mainshow"


class FoodTypes(models.Model):
    typeid = models.CharField(max_length=16)
    typename = models.CharField(max_length=50)
    childtypenames = models.CharField(max_length=200)
    typesort = models.IntegerField(default=-1)

    class Meta:
        db_table = 'axf_foodtypes'


class Goods(models.Model):
    productid = models.CharField(max_length=16)
    productimg = models.CharField(max_length=200)
    productname = models.CharField(max_length=50)
    productlongname = models.CharField(max_length=100)
    isxf = models.BooleanField(default=0)
    pmdesc = models.IntegerField(default=0)
    specifics = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    marketprice = models.FloatField(default=0)
    categoryid = models.CharField(max_length=16)
    childcid = models.CharField(max_length=16)
    childcidname = models.CharField(max_length=50)
    dealerid = models.CharField(max_length=16)
    storenums = models.IntegerField(default=0)
    productnum = models.IntegerField(default=0)

    class Meta:
        db_table = 'axf_goods'


# 用户模型 --- 用来存储用户信息
# 设计：
# 用户名-唯一,密码-MD5加密处理,邮箱-唯一,头像,...,性别,手机号,年龄,...,逻辑删除
class UserModel(models.Model):
    u_name = models.CharField(max_length=32,unique=True)
    u_password = models.CharField(max_length=32)
    u_email = models.CharField(max_length=50,unique=True)
    u_sex = models.BooleanField(default=1)
    u_isdelete = models.BooleanField(default=False)
    u_img = models.ImageField(upload_to="icon")

    class Meta:
        db_table = 'axf_user'


class CartModel(models.Model):
    c_user = models.ForeignKey(UserModel)
    c_goods = models.ForeignKey(Goods)
    c_num = models.IntegerField(default=1)
    c_isselect = models.BooleanField(default=True)

    class Meta:
        db_table = 'axf_cart'


class OrderModel(models.Model):
    o_num = models.CharField(max_length=64)
    o_user = models.ForeignKey(UserModel)
    o_time = models.DateTimeField(auto_now_add=True)
    o_status = models.IntegerField(default=0)

    class Meta:
        db_table = 'axf_order'


class OrderGoods(models.Model):
    og_order = models.ForeignKey(OrderModel)
    og_goods = models.ForeignKey(Goods)
    og_num = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_order_goods'