## 博客系统xblog              作者：肖新勇            一位帅气的码农

```
说明     

​  文章采用了blog-v1:一个uuid

​  社区采用discussion-v1:一个序号 
```



#### model设计

```
继承django user表 的一个用户表（权限和角色的定义)
	多表处理逻辑
	评论用mongo试试
	文件系统表
	日志表
	系统一些链接配置表
	系统配置表
	站点一些信息记录表
	系统一些页面模板表
	标签表
	标检关联表
    文章表
    收藏表

    好友表

    关注表

    文章推荐表

    下载记录表	
```

​	

#### 站点系统配置模块 （core)

```
    可热配置系统一些参数和数据
```



#### 博客文章模块(core)

```
	markdown编辑器的支持
    审核功能
    发布状态（公开，私密，粉丝可见，vip）
	发布或草稿
    文章类型
	文章标签
	article
	文章表：
	     标题
	     markdown内容
	     unido富文本内容
	     选择哪种文本
	     标签
	     分类
	     类型（原创，转载，翻译）
	     资源信息（图片，文件等）
	     发布形式（公开，密码，粉丝, vip)可见
	     阅读人数
	     评论人数
	     创建时间
	     更新时间
	标签表
        名称
        
    分类表
       名称
       描述
       图片路径
```



#### 文件系统模块(core)

```
    可配本地，云存储服务
	记录文件路径对象和关联对象
```



#### 推荐模块(web)

```
    推荐博客人
    推荐博客文章
    推荐帖子  
	
```



#### 通知模块(core)

```
    系统公告
	系统消息
    页面通知
    邮件通知
    手机通知
	私信功能
```

​	

#### 支付模块(core)

```
    支付宝支付
	微信支付
	卡支付    
	会员资格权限
	订单查询和充值，余额显示
```



#### 用户模块(core)

```
    收藏
    粉丝
    关注   	
    
    pbkdf2_sha256
    pbkdf2_sha1
    bcrypt_sha256
    bcrypt
    sha1
    unsalted_md5
    crypt   make_passwrd方法加密方式
    
    # settings of session cache
    SESSION_CACHE_ALIAS = ENV_TOKENS.get('SESSION_CACHE_ALIAS', 'default')
    SESSION_ENGINE = 'django.contrib.sessions.backends.db'   # 引擎（默认）
    SESSION_COOKIE_NAME ＝ "sessionid"                       # Session的cookie保存在浏览器上时的key，即：sessionid＝随机字符串（默认）
    SESSION_COOKIE_PATH ＝ "/"                               # Session的cookie保存的路径（默认）
    SESSION_COOKIE_DOMAIN = None                             # Session的cookie保存的域名（默认）
    SESSION_COOKIE_SECURE = False                            # 是否Https传输cookie（默认）
    SESSION_COOKIE_HTTPONLY = True                           # 是否Session的cookie只支持http传输（默认）
    SESSION_COOKIE_AGE = 1209600                             # Session的cookie失效日期（2周）（默认）
    SESSION_EXPIRE_AT_BROWSER_CLOSE = False                  # 是否关闭浏览器使得Session过期（默认）
    SESSION_SAVE_EVERY_REQUEST = False                       # 是否每次请求都保存Session，默认修改之后才保存（默认）


	reverse('blog:article_detail', args=[str(article.pk), article.slug])
```

​	

#### 权限管理模块(core)

  

```
  权限（二叉树模型）
      内容操作权限列表清单
      文件下载权限列表清单
      评论操作权限列表清单
      支付操作权限列表清单
  角色可设定
      超级管理可自己配置
  角色-用户
      取最大权限就可
```



#### 登陆模块(core)

```
     本地登陆和注册
     第三方登陆  
     QQ登陆
     微信登陆
     csdn登陆
     微博登陆
     gitee登陆
     github登陆	
     等等，最好可配置
```



#### 搜索模块(web admin)

```
    配置eleasticsearch到django即可使用
```



#### 数据分析模块(admin)

```
    看看django有没有自带	
```



#### 下载模块(core)

```
    普通和会员下载资格权限控制
	任务记录
```



#### 讨论模块 (core)

```
    问答模块，既求助模块
	社区
    利用mongo模块
    增加角色权限管理
```



#### 活动模块(core)

```
	签到模块
	活动模块
	广告模块
```



#### 客户模块，帮助中心说明模块(core)

```
    系统配置就可
```

#### 爬取博客数据

​    