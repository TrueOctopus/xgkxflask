# xgkxflask
### 数据表结构

**User**

|     User      |         definition          |      description       |
| :-----------: | :-------------------------: | :--------------------: |
|      id       | Integer, primary_key, index |          主键          |
|   username    |     String(12), unique      |         用户名         |
|     name      |         String(64)          |          姓名          |
|     email     |  String(64), unique, index  |        邮箱地址        |
|      sex      |           Integer           |  性别（1为男 0为女）   |
|     grade     |         String(64)          |          年级          |
|    college    |         String(64)          |          学院          |
|     major     |         String(64)          |          专业          |
|  student_num  |  String(12), unique, index  |          学号          |
|   phone_num   |     String(11), unique      |          电话          |
| profile_photo | Text(), default=default_img | 用户头像（base64存储） |
| password_hash |         String(128)         |          密码          |
|   about_me    |           Text()            |        个人介绍        |
|   confirmed   |   Boolean, default=False    |        邮箱验证        |



|        @staticmethod        |       parameter       |     description      |
| :-------------------------: | :-------------------: | :------------------: |
|          password           |    self, password     |       创建密码       |
|       verify_password       |    self, password     |       核对密码       |
| generate_confirmation_token | self, expiration=3600 |  生成邮件验证token   |
|           confirm           |      self, token      |    验证邮件token     |
|           to_json           |         self          | 将信息封装为json格式 |



**Article**

|  Article  |                          definition                          |         description          |
| :-------: | :----------------------------------------------------------: | :--------------------------: |
|    id     |                     Integer, primary_key                     |             主键             |
| art_type  |                      String(64), index                       | 文章类型（activity或notice） |
|   title   |                  String(64), unique, index                   |             标题             |
|   body    |                             Text                             |             正文             |
| timestamp | String(64),default=datetime.now().strftime('%Y-%m-%d %H:%M:%S') |            时间戳            |
|   image   |                        db.String(64)                         |       图片（以\|分割）       |

| @staticmethod | parameter |     description      |
| :-----------: | :-------: | :------------------: |
|    to_json    |   self    | 将信息封装为json格式 |



### API定义

#### api v1

{{baseUrl}} = http://81.70.11.36/api/v1

**users**

|                api                 |                 request                 |                           response                           |                         description                          |
| :--------------------------------: | :-------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
|            /users/login            |          {'email', 'password'}          | {'code', 'message', 'id', 'username', 'name', 'profile_photo', 'sex', 'college', 'major', 'grade', 'student_num', 'phone_num', 'email', 'about_me', 'confirmed'} |       用户登录; 0:用户不存在; 1:登录成功; -1:密码错误        |
|          /users/register           |    {'email', 'password', 'username'}    |                     {'code', 'message'}                      |      用户注册; 0:用户已存在; 1:注册成功,验证邮件已发送       |
|           /users/confirm           |                {'email'}                |                     {'code', 'message'}                      | 发送验证邮件; 0:用户不存在; 1:验证邮件已发送; 2:用户已完成验证 |
| /users/confirm/{{email}}/{{token}} |                  None                   |                     {'code', 'message'}                      | 邮箱验证; 0:链接是无效的或已经超时; 1:验证完成; 2:用户已完成验证; -1:用户不存在 |
|       /users/changePassword        | {'email', 'oldPassword', 'newPassword'} |                     {'code', 'message'}                      | 修改密码; 0:用户不存在 1: 密码修改成功; -1: 修改失败; -2: 原密码错误 |
|       /users/forgetPassword        |                {'email'}                |                     {'code', 'message'}                      |           发送修改邮件; 0:用户不存在; 1:邮件已发送           |
|    /users/deleteUserById/{{id}}    |              Authorization              |                     {'code', 'message'}                      | 通过id删除用户; 0:删除失败; -2:权限不足; -3:-token失效请重新登录; -4:你不能删除你自己; -1:用户不存在; 1:删除成功 |
| /users/deleteUserByEmail/{{email}} |              Authorization              |                     {'code', 'message'}                      | 通过邮箱删除用户; 0:删除失败; -1:用户不存在; -2:权限不足; -3:token失效请重新登录; -4:你不能删除你自己; 1:删除成功 |
|      /users/changePermission       |     Authorization {'email', 'perm'}     |                     {'code', 'message'}                      | 修改用户权限; 1:修改成功; 0:权限不足; -1:用户不存在; -2:添加至数据库失败; -3:你不能修改管理员的权限; -4:token失效请重新登录 |
|        /users/confirmToken         |              Authorization              |                     {'code', 'message'}                      |   验证token是否有效; 0:token失效请重新登录; 1:token未失效    |

**article**

|         api          |  request  |      response       |                         description                          |
| :------------------: | :-------: | :-----------------: | :----------------------------------------------------------: |
|  /article/uploadArt  |   file    | {'code', 'message'} | 上传文章; 0:上传失败; 1:上传成功; -1:类型错误，应为md文档; -2:上传失败,信息缺失; -3:录入数据库失败; -4:文档已存在 |
| /article/upgradeArt  |   file    | {'code', 'message'} | 更新文档; 0:更新失败; 1:更新成功; -1:类型错误，应为md文档; -2:更新失败,信息缺失; -3:更新数据库失败; -4:文档不存在 |
|  /article/deleteArt  | {'title'} | {'code', 'message'} |    删除文档; 0:文档不存在; -1:更新数据库失败; 1:删除成功     |
| /article/downloadArt |  'name'   |        file         |              根据文件名下载文档; 0: 文档不存在               |

**gets**

|              api               |    request    |                           response                           |       description       |
| :----------------------------: | :-----------: | :----------------------------------------------------------: | :---------------------: |
|      /gets/getById/{{id}}      | Authorization | {'id', 'username', 'name', 'profile_photo', 'sex', 'college', 'major', 'grade', 'student_num', 'phone_num', 'email', 'about_me', 'confirmed'} |   通过id查看用户信息    |
|         /gets/getList          | Authorization | {'id', 'username', 'name', 'profile_photo', 'sex', 'college', 'major', 'grade', 'student_num', 'phone_num', 'email', 'about_me', 'confirmed'} |    查看所用用户信息     |
|   /gets/getImgs/{{imgName}}    |     None      |                             file                             |   通过图片名获取图片    |
|      /gets/getAllArtList       |     None      | {'id', 'art_type', 'title', ’image‘, 'body', 'timestamp', 'filename'} |    获取所有文章信息     |
|     /gets/getNoticeArtList     |     None      | {'id', 'art_type', 'title', ’image‘, 'body', 'timestamp', 'filename'} |    获取所用公告信息     |
|    /gets/getActivityArtList    |     None      | {'id', 'art_type', 'title', ’image‘, 'body', 'timestamp', 'filename'} |    获取所用活动信息     |
|    /gets/getArtById/{{id}}     |     None      | {'id', 'art_type', 'title', ’image‘, 'body', 'timestamp', 'filename'} |     通过id获取信息      |
|     /gets/getNoBodyArtList     |     None      | {'id', 'art_type', 'title', ’image‘, 'timestamp', 'filename'} | 获取所有文章信息 无正文 |
|  /gets/getNoBodyNoticeArtList  |     None      | {'id', 'art_type', 'title', ’image‘, 'timestamp', 'filename'} | 获取所用公告信息 无正文 |
| /gets/getNoBodyActivityArtList |     None      | {'id', 'art_type', 'title', ’image‘, 'timestamp', 'filename'} | 获取所用活动信息 无正文 |
| /gets/getNoBodyArtById/{{id}}  |     None      | {'id', 'art_type', 'title', ’image‘, 'timestamp', 'filename'} |  通过id获取信息 无正文  |
|  /gets/getArtImgs/{{imgName}}  |     None      |                             file                             | 通过图片名获取文章图片  |

**posts**

|         api          |                           request                            |                           response                           |                         description                          |
| :------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
| /posts/uploadProfile | {'email', 'username', 'name', 'sex', 'college', 'major', 'grade', 'student_num', 'phone_num', 'about_me', 'profile_photo'} |                     {'code', 'message'}                      |     更新用户资料; 0:用户不存在; 1:更新成功; -1:添加失败;     |
|    /posts/addUser    |              {'email', 'username', 'password'}               | {'code', 'message', 'id', 'username', 'name', 'profile_photo', 'sex', 'college', 'major', 'grade', 'student_num', 'phone_num', 'email', 'about_me', 'confirmed'} | 添加用户,默认邮箱验证完成; 0:添加失败; 1:添加成功,返回信息; -1:添加失败，信息不全 |
|   /posts/uploadImg   |                             None                             |                     {'code', 'message'}                      |       上传图片；0:图片已存在; 1:上传成功; -1:类型错误        |

**Applicant**

|               api               |                           request                            |                           response                           |                         description                          |
| :-----------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
|        /uploadApplicant         | {"about_me", "birthday", "class_name",  "cognition", "email", "id", "intention", "major", "message", "name", "office", "phone_num", "qq", "sex", "software", "specialty"} |                     {'code', 'message'}                      |                报名; 1:上传成功; -1:上传失败                 |
|    /getApplicantById/{{id}}     |                             None                             | {"id", "about_me", "birthday", "class_name", "code": , "cognition", "email", "id", "intention", "major", "message", "name", "office", "phone_num", "qq", "sex", "software", "specialty", 'code', 'message'} |          通过id获得信息; 0:用户不存在; 1:查询成功;           |
|  /getApplicantByName/{{name}}   |                             None                             | {"id", "about_me", "birthday", "class_name", "code": , "cognition", "email", "id", "intention", "major", "message", "name", "office", "phone_num", "qq", "sex", "software", "specialty", 'code', 'message'} |         通过姓名获取信息; 0:用户不存在; 1:查询成功;          |
|        /getApplicantList        |                             None                             | [{"id", "about_me", "birthday", "class_name", "code": , "cognition", "email", "id", "intention", "major", "message", "name", "office", "phone_num", "qq", "sex", "software", "specialty"}] |                         获取报名列表                         |
|   /deleteApplicantById/{{id}}   |                             None                             |                     {'code', 'message'}                      |                        根据id删除信息                        |
| /deleteApplicantByName/{{name}} |                             None                             |                     {'code', 'message'}                      |                       根据姓名删除信息                       |
|       /confirmApplication       |             Authorization, {'email', 'message'}              |                     {'code', 'message'}                      | 确认通过; 1: 已通过，邮件发送成功; 0:token失效请重新登录; -1:权限不足; -2:用户不存在; -3:已通过; -4:添加至数据库失败 |

**permissions**

|               用户               |             权限              |                        说明                        |
| :------------------------------: | :---------------------------: | :------------------------------------------------: |
|          1 游客 Tourist          |              无               |                  相关内容不可访问                  |
| 2 未验证用户 UnauthenticatedUser |            ACCESS             | 只可访问相关内容,不可发言,发表文章与论坛, 默认用户 |
|      3 普通用户 NormalUser       |         ACCESS, SPEAK         |            可访问, 可留言, 不可发表文章            |
|       4 科协成员 KXMember        |    ACCESS, SPEAK, PUBLISH     |   可访问, 可留言, 可发表文章, 删除相关文章与留言   |
|      5 管理员 Administrator      | ACCESS, SPEAK, PUBLISH, ADMIN |                      超级用户                      |

