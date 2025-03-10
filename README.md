# Flask お問い合わせフォーム

このプロジェクトは、Flask を使用したお問い合わせフォームの Web アプリケーションです。  
ユーザーがフォームに入力した内容をメールで送信し、CSV に保存する機能があります。

---

## 🔹 主な機能

✅ お問い合わせフォームの表示  
✅ 入力内容のバリデーション（入力チェック）  
✅ 問い合わせ内容のメール送信（Flask-Mail）  
✅ 問い合わせ内容の CSV への保存  
✅ `.env` を使用した環境変数の管理  

---

## 👉 セットアップ手順

### 1. リポジトリのクローン

```sh
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

### 2. 仮想環境の作成と依存関係のインストール

```sh
# 仮想環境の作成
python -m venv venv

# 仮想環境のアクティベート
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

# 必要なパッケージのインストール
pip install -r requirements.txt
```

### 3. `.env` ファイルの作成

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
SECRET_KEY=your-secret-key
NOTIFY_EMAIL=your-notification-email@gmail.com
```

### 4. アプリの実行

```sh
python app.py
```

### 5. アクセス

```sh
http://127.0.0.1:5000
```

---

##  `.gitignore` の設定

```txt
# 環境変数ファイル（必須）
.env

# Python 仮想環境
venv/
__pycache__/

# 不要なログファイル
*.log

# CSV ファイル（データの保護）
contact.csv
```

---

## 📄 ファイル構成

```
your-repository/
│── app.py                 # Flask アプリケーション（メインファイル）
│── forms.py               # Flask-WTF を使用したフォームの定義
│── templates/             # HTML テンプレート（フロントエンド）
│   ├── index.html         # トップページ
│   ├── contact.html       # お問い合わせフォーム
│   ├── contact_complete.html  # 送信完了ページ
│   ├── contact_mail.txt   # メール通知用テキスト版
│   ├── contact_mail.html  # メール通知用 HTML 版
│── static/                # CSS / JS / 画像
│── contact.csv            # お問い合わせ履歴（CSV形式で自動作成）
│── .env                   # 環境変数（Git に追加しない）
│── .gitignore             # Git 無視リスト（contact.csv や .env を除外）
│── requirements.txt       # 必要な Python ライブラリ
│── README.md              # このファイル

```

## ⚙️ 使用技術

- **Flask**: Python のマイクロ Web フレームワーク
- **Flask-WTF**: フォームバリデーション
- **Flask-Mail**: メール送信
- **dotenv**: 環境変数の管理
- **CSV**: 問い合わせ内容の保存

## 📧 メール送信について

アプリは Flask-Mail を使用してメールを送信します。Gmail を使用する場合は、アプリパスワードを設定してください。


