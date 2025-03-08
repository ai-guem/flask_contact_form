from flask import Flask, render_template, redirect, url_for, flash, request
from flask_mail import Mail, Message
from forms import ContactForm  # 前回作成したフォームを利用
import os
import csv
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"

# Flask-Mail 設定（環境変数を利用）
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

mail = Mail(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # ユーザーからの入力データを取得
        name = form.name.data
        email = form.email.data
        inquiry = form.inquiry.data

        # メール送信
        msg = Message(
            subject="【お問い合わせ】",
            sender=app.config["MAIL_DEFAULT_SENDER"],
            recipients=[app.config["MAIL_USERNAME"]],  # 自分のメールアドレス
            body=f"名前: {name}\nメールアドレス: {email}\n\nお問い合わせ内容:\n{inquiry}",
        )

        mail.send(msg)

        # 通知メール（HTMLテンプレート使用）
        send_email(
            email,
            "お問い合わせありがとうございました",
            "contact_mail",
            username=name,
            email=email,
            description=inquiry,
        )

        # CSVに問い合わせ内容を保存する
        save_to_csv(name, email, inquiry)  # contactでCSV保存

        flash("お問い合わせ内容を送信しました。ありがとうございます！", "success")
        return redirect(url_for("contact_complete"))  # 送信完了ページにリダイレクト

    return render_template("contact.html", form=form)

def send_email(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)  # テキスト版メール
    msg.html = render_template(template + ".html", **kwargs)  # HTML版メール
    mail.send(msg)


def save_to_csv(username, email, description):
    # 保存するCSVファイルのパス
    file_path = "contact.csv"
    
    # ファイルが存在しない場合はヘッダーを追加して新規作成
    file_exists = os.path.isfile(file_path)
    print(f"File exists: {file_exists}")  # デバッグ用
    
    try:
        with open(file_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            
            # ヘッダーが存在しない場合は追加
            if not file_exists:
                writer.writerow(["Username", "Email", "Description", "Date"])
            
            # 問い合わせ内容をCSVに追加
            writer.writerow([username, email, description, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        print("Data saved to CSV.")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        # フォーム属性を使ってフォームの値を取得する
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]
        is_valid = True
        
        # ユーザー名が空かどうかをチェックする
        if not username:
            flash("ユーザー名を入力してください")
            is_valid = False
        
        if not email:
            flash("メールアドレスを入力してください")
            is_valid = False
        
        # メールアドレスが正しいかどうかをチェックする
        try:
            validate_email(email)
        except EmailNotValidError as e:
            flash(str(e))
            is_valid = False
        
        if not description:
            flash("お問い合わせ内容を入力してください")
            is_valid = False
        
        if not is_valid:
            return redirect(url_for("contact"))
        
        # メールを送信する
        send_email(
            email,
            "問い合わせありがとうございました",
            "contact_mail",
            username=username,
            description=description,
        )

        # 通知メールを送信する
        notify_email = os.environ.get("NOTIFY_EMAIL")
        if notify_email:
            app.logger.debug(f"Sending notification email to {notify_email}")
            send_email(
                notify_email,
                "新しい問い合わせがありました",
                "contact_mail",
                username=username,
                description=description,
            )
        else:
            app.logger.error("NOTIFY_EMAIL is not set")

        flash("問い合わせ内容はメールにて送信しました。問い合わせありがとうございました。")
        return redirect(url_for("contact_complete")) 
    return render_template("contact_complete.html")

if __name__ == "__main__":
    app.run(debug=True)
