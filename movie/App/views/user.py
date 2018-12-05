from flask import Blueprint, render_template, flash, redirect, url_for, request
from App.models import User
from App.forms import Register,Login
from flask_login import login_user,logout_user,login_required
from datetime import datetime
from App.extensions import cache, file
import os
from PIL import Image
from App.settings import Config

user = Blueprint('user',__name__)

def random_filename(suffix):
    import string, random
    Str = string.ascii_letters+string.digits
    while True:
        newName = ''.join(random.choice(Str) for i in range(64)) + '.' + suffix
        newPath = os.path.join(Config.UPLOADED_PHOTOS_DEST, newName)
        if not os.path.exists(newName):
            break
    return newPath,newName


def img_zoom(path,prefix='s_',width=200,height=300):
    img = Image.open(path)  # 读取图片
    img.thumbnail((width, height))  # 重新设计尺寸
    pathInfo = os.path.split(path)
    newName = prefix + pathInfo[-1]
    img.save(os.path.join(pathInfo[0],newName))  # 保存图片
    return newName

@user.route('/register/',methods=['GET','POST'])
def register():
    form = Register()
    if form.validate_on_submit():
        photos = request.files.get('icon')
        suffix = photos.filename.split('.')[-1]
        imgInfo = random_filename(suffix)
        filename = file.save(photos, name=imgInfo[1])
        path = os.path.join(Config.UPLOADED_PHOTOS_DEST, filename)
        img_zoom(path)
        img_url = file.url(filename)
        u = User(username=form.username.data, password=form.userpass.data, email=form.email.data,icon=img_url)
        u.save()
        flash('恭喜注册成功')
        return redirect(url_for('user.login'))
    return render_template('user/register.html',form=form)


@user.route('/login/',methods=['GET','POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if not u.check_password(form.userpass.data):
            flash('请输入正确的密码')
        else:
            u.lastLogin = datetime.utcnow()
            u.save()
            flash('登陆成功!!!')
            cache.clear()
            login_user(u, remember=form.remember.data)
            return redirect(url_for('main.index'))
    return render_template('user/login.html',form=form)


@user.route('/userinfo_mod/',methods=['GET','POST'])
@login_required
def userinfo_mod():
    form = Register()
    if form.validate_on_submit():
        u = User(username=form.username.data,email=form.email.data, icon=form.icon.data)
        u.save()
        flash('修改成功')
        return redirect(url_for('main.home'))
    return render_template('user/userinfo_mod.html',form=form)


@user.route('/logout/')
def logout():
    flash('退出成功')
    logout_user()
    cache.clear()
    return redirect(url_for('main.index'))



