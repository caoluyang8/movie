from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from flask_wtf.file import FileAllowed,FileRequired,FileField
from wtforms.validators import DataRequired,Length,EqualTo,Email,ValidationError
from App.models import User
from App.extensions import file


class Register(FlaskForm):
    username = StringField('用户名',validators=[DataRequired('用户名不能为空'),Length(min=6,max=12,message='用户名在6~12位之间')],render_kw={'placeholder':'请输入用户名','minlength':6,'maxlength':12})
    userpass = PasswordField('密码',validators=[DataRequired('密码不能为空'),Length(min=6,max=12,message='密码在6~12位之间')],render_kw={'placeholder':'请输入密码','minlength':6,'maxlength':12})
    confirm = PasswordField('确认密码',validators=[DataRequired('确认密码不能为空'),Length(min=6,max=12,message='密码在6~12位之间'),EqualTo('userpass',message='确认密码和密码不一致')],render_kw={'placeholder':'请输入确认密码','minlength':6,'maxlength':12})
    email = StringField('邮箱',validators=[DataRequired('邮箱不能为空'),Email('请输入正确的邮箱地址')],render_kw={'placeholder':'请输入有效的邮箱地址'})
    icon = FileField('选择头像',validators=[FileAllowed(file,message='该文件类型不允许上传！'),FileRequired('您还没有选择文件')])
    submit = SubmitField('注册')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已存在,请重新输入')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已存在,请重新输入')

class Login(FlaskForm):
    username = StringField('用户名',validators=[DataRequired('用户名不能为空'),Length(min=6,max=12,message='用户名在6~12位之间')],render_kw={'placeholder':'请输入用户名','minlength':6,'maxlength':12})
    userpass = PasswordField('密码',validators=[DataRequired('密码不能为空'),Length(min=6,max=12,message='密码在6~12位之间')],render_kw={'placeholder':'请输入密码','minlength':6,'maxlength':12})
    remember = BooleanField('记住我')
    submit = SubmitField('登录')

    def validate_username(self,field):
        if not User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名不存在,请重新输入')


class Changeinfo(FlaskForm):
    username = StringField('用户名',validators=[DataRequired('用户名不能为空'),Length(min=6,max=12,message='用户名在6~12位之间')],render_kw={'placeholder':'请输入用户名','minlength':6,'maxlength':12})
    email = StringField('邮箱',validators=[DataRequired('邮箱不能为空'),Email('请输入正确的邮箱地址')],render_kw={'placeholder':'请输入有效的邮箱地址'})
    icon = FileField('选择头像', validators=[FileAllowed(file, message='该文件类型不允许上传！'), FileRequired('您还没有选择文件')])
    submit = SubmitField('修改')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已存在,请重新输入')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已存在,请重新输入')