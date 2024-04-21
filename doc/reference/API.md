## Users

- `server/users.py`

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

## Article

- `server/article.py`

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

## Assistant

- `server/assistant.py`

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

## Interaction

- `server/interaction.py`

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
