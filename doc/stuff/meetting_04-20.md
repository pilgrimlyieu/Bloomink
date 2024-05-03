# 4 月 20 日组会

- 记录人：[@PilgrimLyieu](https://github.com/pilgrimlyieu)
- 记录时间：2024 年 4 月 20 日

## 会前

### Copilot

鉴于组长与组员均没有 Web 开发的经验，向 Copilot 进行咨询就成为了必不可少的一步。如下图是向 Copilot 了解 API Reference 的构成，与 API 的编写等。

![](img/04-20_api-reference.png)

![](img/04-20_create-an-api.png)

以及后端编写拆分为多个模块的思路，也由 Copilot 提供帮助。

![](img/04-20_copilot-backend-1.png)

![](img/04-20_copilot-backend-2.png)

![](img/04-20_copilot-backend-3.png)

后端外，还有就是组长本人觉得格外棘手的前端了。

![](img/04-20_copilot-frontend-1.png)

![](img/04-20_copilot-frontend-2.png)

![](img/04-20_copilot-frontend-3.png)

![](img/04-20_copilot-frontend-4.png)

虽然一行代码都还没开始写，但是还是提前了解了一下发布的流程。

![](img/04-20_copilot-publish-1.png)

![](img/04-20_copilot-publish-2.png)

以及一些数据存储的信息。

![](img/04-20_copilot-storage-1.png)

![](img/04-20_copilot-storage-2.png)

### 代码规范

为了统一代码格式，全组在组长的要求下安装了 Black Formatter 等插件，并开启了保存自动格式化的功能。

除此以外，约定后端 Python 代码采用 Snake 命名法（`get_data_reference`），而前端 Vue.js 代码采用 Camel 命名法（`getDataReference`）。

### 代码框架

#### 搭建

毫无 Web 开发经验的组长，在网上翻阅了很多资料，堪堪摸索出一条搭建项目框架的路线。

为了与组员保持一致，组长也最终放弃了在 WSL 进行开发的决定。

安装 Node.js, Python 等基本内容不再赘述。

首先是安装 Vue.js 命令行，这样就能直接使用 `vue` 命令。使用下面的命令进行安装（可能需要配置 NPM 镜像）：

```
npm install -g @vue/cli
```

随后创建前端项目

```
vue create client
```

然后创建 Python 虚拟环境

```
python -m venv .venv
```

启动虚拟环境

```
source .venv/Scripts/activate
```

然后安装 Flask

```
pip3 install flask
```

紧接着创建后端文件夹 `server`

```
mkdir server
```

在其中创建一个 `app.py` 作为应用的入口文件，并根据 Copilot 的指导，输入以下内容：

```py
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/api/data", methods=["GET"])
def get_data():
    data = {"message": "Hello, Vue.js!"}
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
```

同时修改 `client/src/components/HelloWorld.vue` 组件中 `script` 标签为

```js

export default {
  name: 'HelloWorld',
  data() {
    return {
      message: 'Loading...'
    };
  },
  async mounted() {
    const response = await fetch('/api/data');
    const data = await response.json();
    this.message = data.message;
  }
}
```

并修改 `client/vue.config.js` 为

```js
const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      }
    }
  }
})
```

以将 Vue.js 的 API 请求转发到 5000 端口，供后端进行处理。

最后使用两个 Bash 终端分别在后端 `server` 和前端 `flask` 执行 `flask run`（或 `flask run --reload`）和 `vue serve` 启动前后端进行检查。

成功启动后，按指示打开 `https://localhost:8080`，并使用 <kbd>F12</kbd> 打开开发者工具，在网络选项卡使用 <kbd>Ctrl</kbd> + <kbd>R</kbd> 刷新后，成功发现 data 名称的 GET 请求，同时状态码返回 200，并能看到预期的 JSON 数据，验证成功。

#### 复刻

下一个难题便是如何让组员本地获得与组长相同的环境。经过摸索，组长也发现了下面的路径。

首先组长导出需要安装的 Python 依赖

```
pip3 freeze > server/requirements.txt
```

随后组员按下面的步骤进行重复操作，即可复刻组长的本地环境。

1. Git
    1. 同步 main 分支（先切换到 main 再切回来）
    2. 合并 main 分支更改（分支 > 合并 > main）
2. Python 虚拟环境
    1. `python -m venv .venv`
    2. `source .venv/Scripts/activate`
    3. `pip3 install -r server/requirements.txt`
3. Node.js 包
    1. `npm install -g @vue/cli`
    2. `cd client`
    3. `npm install`
4. 运行并测试
    1. `flask run`
    2. `vue serve`

至此便完成了框架的搭建。

组长也将 VSCode 设置一并传入库中，免去了组员的设置之苦（当然格式化工具还是手动帮助组员完成了设置）

```json
{
    "editor.formatOnSave": true,
    "editor.formatOnPaste": true
}
```

完成上面的工作后发布了 Pull Request [#3 初始化项目框架](https://github.com/pilgrimlyieu/ELProject/pull/3)。

然而因为组长设置了 main branch 保护机制，必须要一个 Review Approve 才能合并到主分支，而组长不能审阅自己的代码，组员也并不了解其中的机制，无奈之下组长给 Repo Admin 开了 bypass，并强行合并了 PR。

![](img/04-20_bypass.png)

### 资料

组长也搜罗了很多资料供组员进行参考。

- 3W(HTML, JavaScript, CSS)
    - [HTML 简介](https://developer.mozilla.org/zh-CN/docs/Learn/HTML/Introduction_to_HTML)
    - [重新介绍 JavaScript（简短 JS 教程）](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Language_overview)
    - [JavaScript 教程](https://zh.javascript.info)
    - [CSS 入门概述](https://developer.mozilla.org/zh-CN/docs/Learn/CSS/First_steps)
    - [W3School](https://www.w3school.com.cn)
        - [HTML 请求方法](https://www.w3school.com.cn/tags/html_ref_httpmethods.asp)
- 前端
    - [Vue.js 文档](https://cn.vuejs.org/guide/quick-start.html)
- 后端
    - [Flask 中文文档](https://dormousehole.readthedocs.io/en/latest)
    - [Flask 英文文档](https://flask.palletsprojects.com/en/3.0.x)

目前组长本人看完了 3W 的概述，快速翻阅了 JavaScript 的基本语法、面向对象语法、回调与模块等，以及 Vue.js 和 Flask 的快速上手部分。

并为了节约时间，向组员提出了一些阅读建议：

![](img/04-20_reading-advice.png)

未来也许会对这些资料继续进行补充。

## 会议内容

- 组长协助组员完成合并主分支操作，及环境复刻等
- 前后端分别讨论并制定开发路线图，进一步确定部分细节、分工与 DDL 等内容，~~组长划水~~
- 组长进一步介绍 Pull Request 发布流程，并正式开始开发

### 开发线路图

#### 前端

![](img/04-20_frontend-first-version.png)

前端开发路线图初稿

<!-- {{{原稿 -->
<details>
<summary>原稿</summary>

```md
## step_one

**1**.**主页面**，包含搜索界面（中部偏上），用户登录，注册，头像按钮（右上角），主体功能（右上角），AI助手（按钮），创作空间（按钮），（个性化）推荐总览（主体），文化库（按钮）

## step_two
**2**.**用户界面**（主页），显示头像（左上），用户名（头像右），模块：我的创作，草稿，浏览历史，我的点赞，我的收藏，我的黑名单，我的关注，我的粉丝，我的转发

（1）“**我的草稿**“：搜索页面，新建草稿，已创作草稿（草稿模块），回收站，
- 【1】新建草稿页面，标签分类：小说，散文，诗歌...，输入投稿人姓名，投稿人想对读者说的话，新建（按钮）
- 【2】已创作草稿页面（草稿编辑页面），字数（左下角），投稿（右上角按钮）（确认or取消），标题名称编辑，目录名称编辑，
- 【3】回收站，草稿已有的标签，删除（永久），恢复，
  
（2）“**我的创作**“：搜索页面，创作的过往文章，有获赞数，收藏数，转发数（文章模块）
- 【1】文章模块浏览页面（预览）：标题，文章，投稿人，发布时间，点赞数，文章所含标签
- 【2】点进某一个模块之后：文章浏览页面：投稿人想对读者说的话，标题，目录，文章，投稿人，（右上，以头像形式显示，点击可进入该作者主页），发布时间，读者点评，文章所含标签

（3）”**浏览历史**“：（左边竖线）浏览时间，（右侧）文章模块
- 【1】文章模块浏览页面（预览）：标题，文章，投稿人，发布时间，点赞数，文章所含标签
- 【2】点进某一个模块之后：文章浏览页面：投稿人想对读者说的话，标题，目录，文章，投稿人，（右上，以头像形式显示，点击可进入该作者主页），发布时间，读者点评，文章所含标签
  
（4）”**我的点赞**“：（左边竖线）浏览时间，（右侧）文章模块
- 【1】文章模块浏览页面（预览）：标题，文章，投稿人，发布时间，点赞数，文章所含标签
- 【2】点进某一个模块之后：文章浏览页面：投稿人想对读者说的话，标题，目录，文章，投稿人，（右上，以头像形式显示，点击可进入该作者主页），发布时间，读者点评，文章所含标签
- 
（5）”**我的收藏**“：（左边竖线）浏览时间，（右侧）文章模块
- 【1】文章模块浏览页面（预览）：标题，文章，投稿人，发布时间，点赞数，文章所含标签
- 【2】点进某一个模块之后：文章浏览页面：投稿人想对读者说的话，标题，目录，文章，投稿人，（右上，以头像形式显示，点击可进入该作者主页），发布时间，读者点评，文章所含标签

（6）”**我的关注**“：用户列表

（7）”**我的粉丝**“：用户列表

（8）”**我的转发**“：文章模块

（9）”**我的黑名单**“：文章模块

## step_three
**3**.**分类页面**，搜索，分类。（个性化）推荐，

## step_three
**3**.**创作空间**：搜索，文章分类，排行榜，（个性化）推荐总览，
（1）**（个性化）推荐总览**：文章模块预览

（2）**文章分类**：小说，散文，诗歌...，点进某一个分类后：
  - 【1】文章模块预览
  - 【2】点进某一个模块之后：文章浏览页面：投稿人想对读者说的话，标题，目录，文章，投稿人，（右上，以头像形式显示，点击可进入该作者主页），发布时间，读者点评，文章所含标签

（3）**排行榜**：文章模块预览
- 【1】点进某一个模块之后：文章浏览页面：投稿人想对读者说的话，标题，目录，文章，投稿人，（右上，以头像形式显示，点击可进入该作者主页），发布时间，读者点评，文章所含标签

## step_four
**4**.**AI助手**，参考chatgpt页面
```

</details>
<!-- }}} -->

- 前端组成员
    - [@EnndWang](https://github.com/EnndWang)
- 撰写人：[@EnndWang](https://github.com/EnndWang)

#### 后端

![](img/04-20_backend-first-version.png)

后端开发路线图初稿

<!-- {{{原稿 -->
<details>
<summary>原稿</summary>

```md
# Steps

## 1.Users DDL-4.30

**Li**  

1. 创建用户
   - API: `POST /api/users/register`
   - req: name, password.
   - res: 
2. 注销用户
   - API: `DELETE /api/users/delete/{id}`
   - req: ;
   - res: ;
3. 用户登录
   - API: `POST /api/users/login`
   - req: name, password.
   - res: 
4. 用户登出
   - API: `DELETE /api/users/logout/{id}`
   - req: ;
   - res:;
5. 用户信息界面
   - API: `GET /api/users/info/{id}`
   - req: ;
   - res: 性别,生日,...
6. 更新用户信息
   - API: `PUT /api/users/info/{id}`
   - req: 性别,生日,...
   - res: ;

**Mao**

7. 显示收藏列表
   - API: `GET /api/users/{id}/collect`
   - req: (进入收藏文章,我的想法是使用查看文章功能)
   - res:
8. 显示作品列表
   - API: `GET /api/users/{id}/works`
   - req:;
   - res:;
9. 显示关注列表
    - API: `GET /api/users/{id}/following`
    - req:;
    - res:;

## 2.Article DDL-5.12

**Li**

1. 新建文章
    - API: `POST /api/article/new`
    - req: (content),作者info,header...
    - res: ;
2. 更新文章
   - API: `PUT /api/article/update/{id}`
   - req: content
   - res: ;
3. 查看文章
   - API: `GET /api/article/get/{id}`
   - req: ;
   - res: 内容,作者info,
4. 下载文章
   - API: `GET /api/article/get/download/{id}`
   - req: ;
   - res: 内容
5. 删除文章
    - API: `DELETE /api/article/delete/{id}`
    - req: ;
    - res: ;
6. 为文章添加分类
   - API: `PUT /api/article/{id}/categories`
   - req: 类型(网页给定)
   - res: ;
7. 从指定文章删除分类
   - API: `DELETE /api/article/{id}/categories/{categoryld}`
   - req: ;
   - res:;
8. OCR导入旧文档
   - API: `POST /api/ocr`
   - ...?

## 2.Assistant DDL-5.12

**Mao**

1. 获取文化库到本地
   - API: `GET /api/library/`
   - req: 文化库id
   - res: ;
2. 新增文化库中内容
   - API: `POST /api/library`
3. 更新个人文化库中的内容
   - API: `PUT /api/library/{id}`
   - req: 内容;
   - res: ;
4. 删除文化库中内容
   - API: `DELETE /api/library/{id}`
   - req: ;
   - res: ;
5. 分享文化库到公用
   - API: `POST /api/library/share`
   - req: ;
   - res: ;
6. 将文化库设置为本地独有
    - API: `DELETE /api/library/share/{id}`
    - req: ;
    - res: ;
7. AI生成文字
   - API: `GET /api/ai/words`
   - req: 需求;
   - res: ;
8. AI生成图片
   - API: `GET /api/ai/images`
   - req: ;
   - res: ;
9. AI引用文化库
   - API: `GET /api/ai/refer`
   - req: 要求;
   - res: ;
10. 翻译功能
    - API: `GET /api/translate`
    - req: 内容;
    - res: ;

## 3.Interaction DDL-5.23

1. 为指定文章点赞
   - API: `POST /api/article/{id}/likes`
   - req: ;(谁给你赞不重要)
   - res: ;
2. 取消点赞
   - API: `DELETE /api/article/{id}/likes`
   - req: ;
   - res: ;
3. 为指定文章添加评论
   - API: `POST /api/article/{id}/comments`
   - req: 评论用户info,评论内容
   - res: ;
4. 更新指定评论
   - API: `PUT /api/article/{id}/comments/{comid}`
   - req: 内容
   - res: ;
5. 删除评论
    - API: `DELETE /api/article/{id}/comments/{comid}`
    - req: ;
    - res: ;
6. 回复评论
   - API: `POST /api/article/{id}/comments/{comid}/reply`
   - req: 评论用户info,评论内容
   - res: ;
7. 更新回复
   - API: `PUT /api/article/{id}/comments/{comid}/reply/{replyid}`
   - req: 内容;
   - res: ;
8. 删除回复
   - API: `DELETE /api/article/{id}/comments/{comid}/reply/{replyid}`
   - req: ;
   - res: ;
9. 收藏文章
    - API: `POST /api/article/{id}/users/{id}/collect`
    - req: ;
    - res: ;
10. 进入某一类
   - API: `GET /api/categories`
   - req: 类名;
   - res: ;
11. 关注
   - API: `POST /api/users/{id}/follow`
   - req: ;
   - res: ;
12. 搜索header中的关键词
   - API: `POST /api/search`
   - req: 关键词
   - res: 返回搜索结果界面
```

</details>
<!-- }}} -->

- 后端组成员
    - [@t0mo0n](https://github.com/t0mo0n)
    - [@KashingLiking](https://github.com/KashingLiking)
- 撰写人：[@t0mo0n](https://github.com/t0mo0n)

### 前端开发流程

#### 主页面

内容：
1. 用户信息
2. 创作空间
3. 分类
4. 收藏
5. 搜索框
6. 文化库
7. 个性化推荐

#### 用户信息界面

1. 未登录
    1. 注册
    2. 登录
2. 登录后
    1. 用户信息：头像、昵称、性别、生日、简介等
    2. 信息编辑
    3. 作品列表
    4. 草稿列表
    5. 关注列表
    6. 粉丝列表
    7. 收藏列表
    8. 关注列表
3. 草稿
    1. 新建草稿：标题、内容、标签
    2. 编辑草稿：字数统计、保存、发布
    3. 删除草稿：回收站、彻底删除
4. 作品
    1. 新建作品：标题、内容、标签
    2. 作品信息：作者、字数、点赞量、评论量
    3. 编辑作品：字数统计、保存、发布
    4. 删除作品：回收站、彻底删除
5. 历史记录
    1. 浏览记录
    2. 搜索记录
    3. 点赞记录
    4. 评论记录

#### 分类

1. 分类列表

#### 创作空间

1. 编辑器
2. 文化库
3. AI 助手

### API Reference

> 二版 API Reference，随后可能在实际开发中进一步确定参数、返回值等细节，以及调整现有 API 或增加新的 API。

- Users `users.py`

| HTML 方法 | URL | 参数 | 返回值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/users/register` | `name`, `password` | - | 创建用户 |
| `DELETE` | `/api/users/delete/{uid}` | - | - | 注销用户 |
| `POST` | `/api/users/login` | `name`, `password` | - | 用户登录 |
| `DELETE` | `/api/users/logout/{uid}` | - | - | 用户登出 |
| `GET` | `/api/users/info/{uid}` | - | `gender`, `birthday`, ... | 用户信息 |
| `PUT` | `/api/users/info/{uid}` | `gender`, `birthday`, ... | - | 更新用户信息 |
| `GET` | `/api/users/{uid}/collect` | - | - | 收藏列表 |
| `GET` | `/api/users/{uid}/works` | - | - | 作品列表 |
| `GET` | `/api/users/{uid}/following` | - | - | 关注列表 |

- Article `article.py`

| HTML 方法 | URL | 参数 | 返回值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/article/new` | `content`, `author_info`, `header`, ... | - | 新建文章 |
| `PUT` | `/api/article/update/{aid}` | `content` | - | 更新文章 |
| `GET` | `/api/article/get/{aid}` | - | `content`, `author_info`, ... | 查看文章 |
| `GET` | `/api/article/download/{aid}` | - | `content` | 下载文章 |
| `DELETE` | `/api/article/delete/{aid}` | - | - | 删除文章 |
| `PUT` | `/api/article/{aid}/categories` | `type` | - | 添加分类 |
| `DELETE` | `/api/article/{aid}/categories/{category}` | - | - | 删除分类 |
| `POST` | `/api/ocr` | ... | ... | OCR 导入旧文档 |

- Assistant `assistant.py`

| HTML 方法 | URL | 参数 | 返回值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/api/library` | `lid` | - | 获取文化库到本地 |
| `POST` | `/api/library` | - | - | 新增文化库中内容 |
| `PUT` | `/api/library/{lid}` | `content` | - | 更新文化库中内容 |
| `DELETE` | `/api/library/{lid}` | - | - | 删除文化库中内容 |
| `POST` | `/api/library/share` | - | - | 分享文化库到公用 |
| `DELETE` | `/api/library/share/{lid}` | - | - | 将文化库设置为本地独有 |
| `GET` | `/api/ai/words` | `demand` | - | AI 生成文字 |
| `GET` | `/api/ai/images` | - | - | AI 生成图片 |
| `GET` | `/api/ai/library` | `requirement` | - | AI 引用文化库 |
| `GET` | `/api/translate` | `content` | - | 翻译功能 |

- Interaction `interaction.py`

| HTML 方法 | URL | 参数 | 返回值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/article/{aid}/likes` | - | - | 为指定文章点赞 |
| `DELETE` | `/api/article/{aid}/likes` | - | - | 取消点赞 |
| `POST` | `/api/article/{aid}/comments` | `comment_user_info`, `content` | - | 为指定文章添加评论 |
| `PUT` | `/api/article/{aid}/comments/{cid}` | `content` | - | 更新指定评论 |
| `DELETE` | `/api/article/{aid}/comments/{cid}` | - | - | 删除评论 |
| `POST` | `/api/article/{aid}/comments/{cid}/reply` | `reply_user_info`, `content` | - | 回复评论 |
| `PUT` | `/api/article/{aid}/comments/{cid}/reply/{rid}` | `content` | - | 更新回复 |
| `DELETE` | `/api/article/{aid}/comments/{cid}/reply/{rid}` | - | - | 删除回复 |
| `POST` | `/api/article/{aid}/users/{uid}/favorite` | - | - | 收藏文章 |
| `GET` | `/api/categories` | `category` | - | 进入某一类 |
| `POST` | `/api/users/{uid}/follow` | - | - | 关注 |
| `POST` | `/api/search` | `keyword` | - | 搜索 header 中的关键词 |

### 流程

写代码与合并更改流程：
1. 写代码前，切换到 main 分支，同步 GitHub 的更改，再切回来
2. 如果 main 上有更新，将 main 上的更新合并到自己的分支上
3. 写代码……
4. 每完成一个部分（一个部分的界定可以有自己的理解），提交一个 Pull Request，写好标题，同时内容详细说明这个 Pull Request 实现了什么，我会尽快审查合并或提出建议
5. 或者完成了一天的代码工作，今天不会更新了，即使一个函数或某个部分还没写完，也先用注释标记未完成部分，提交一个 Pull Request，跟上面一样，而且需要另外说明未完成的部分

- 打开后端：先启动 Python 虚拟环境，再在 server 文件夹打开 Bash，运行 `flask run`（或 `flask run --reload`）
- 打开前端：在 client 文件夹打开 Bash，运行 `vue serve`
- 关闭前/后端：<kbd>Ctrl</kbd> + <kbd>C</kbd>
