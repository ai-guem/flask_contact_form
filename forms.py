from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

class ContactForm(FlaskForm):
    name = StringField('名前', validators=[DataRequired(message="名前を入力してください")])
    email = StringField('メールアドレス', validators=[
        DataRequired(message="メールアドレスを入力してください"),
        Email(message="正しいメールアドレスを入力してください")
    ])
    inquiry = TextAreaField('お問い合わせ内容', validators=[DataRequired(message="お問い合わせ内容を入力してください")])
    submit = SubmitField('送信')
