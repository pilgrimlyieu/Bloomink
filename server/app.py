from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/api/data", methods=["GET"])
def get_data():
    data = {"message": "Hello, Vue.js!"}
    return jsonify(data)
from flask import Flask, render_template, request, redirect, url_for, session, flash
import uuid

app = Flask(__name__)

# 这里用一个简单的字典模拟用户数据库
users = {}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create_user", methods=["POST"])
def create_user():
    nickname = request.form["nickname"]
    password = request.form["password"]

    user_id = str(uuid.uuid4())

    users[user_id] = {"nickname": nickname, "password": password}

    return redirect(url_for("index"))


@app.route("/delete_user", methods=["DELETE"])
def delete_user():
    user_id = request.form["user_id"]

    if user_id in users:
        del users[user_id]

    return redirect(url_for("index"))


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    # 检查用户名和密码是否匹配
    if username in users and users[username] == password:
        session["username"] = username  # 将用户名存储在session中
        return redirect(url_for("index"))
    else:
        # 登录失败，显示错误消息
        flash("Invalid username or password", "error")
        return redirect(url_for("index"))


@app.route("/logout", methods=["DELETE"])
def logout():
    # 清除session
    session.pop("username", None)
    return redirect(url_for("index"))


@app.route("/info", methods=["GET"])
def info():
    # 如果用户已经登录，显示用户信息界面；否则重定向到登录页面
    if "username" in session:
        username = session["username"]
        user_info = users.get(username)
        return render_template("user_info.html", user_info=user_info)
    else:
        return redirect(url_for("login"))


@app.route("/update", methods=["PUT"])
def update_info():
    if "username" in session:
        username = session["username"]
        user_info = users.get(username)
        if request.method == "POST":
            # 更新用户信息
            user_info["email"] = request.form["email"]
            user_info["age"] = int(request.form["age"])
            return redirect(url_for("index"))
        return render_template("update_info.html", user_info=user_info)
    else:
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
