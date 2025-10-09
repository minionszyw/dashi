# 国学大师 - 前端小程序

基于uni-app开发的AI命理分析微信小程序。

## 技术栈

- **框架**: uni-app 3.0
- **语言**: TypeScript + Vue 3
- **UI**: 自定义UI组件
- **构建**: Vite

## 快速开始

### 1. 环境准备

```bash
# Node.js 16+
node --version

# 安装依赖
npm install
```

### 2. 配置环境变量

修改 `.env.development` 配置开发环境API地址：

```env
VITE_API_BASE_URL=http://localhost:8000
```

### 3. 开发运行

```bash
# 微信小程序
npm run dev:mp-weixin

# H5
npm run dev:h5
```

### 4. 微信开发者工具

1. 打开微信开发者工具
2. 导入项目，选择 `dist/dev/mp-weixin` 目录
3. 配置AppID（测试可使用测试号）

## 构建发布

```bash
# 构建微信小程序
npm run build:mp-weixin

# 构建H5
npm run build:h5
```

## 项目结构

```
web/
├── src/
│   ├── api/              # API接口
│   │   ├── auth.ts
│   │   ├── chat.ts
│   │   └── billing.ts
│   ├── pages/            # 页面
│   │   ├── index/        # 主页（对话）
│   │   ├── login/        # 登录
│   │   ├── chat/         # 会话详情
│   │   ├── sessions/     # 会话列表
│   │   └── profile/      # 个人中心
│   ├── utils/            # 工具函数
│   │   └── request.ts    # 网络请求
│   ├── static/           # 静态资源
│   ├── App.vue           # 应用入口
│   ├── main.ts           # 主文件
│   └── pages.json        # 页面配置
├── .env.development      # 开发环境配置
├── .env.production       # 生产环境配置
├── vite.config.ts        # Vite配置
└── package.json
```

## 功能说明

### 页面列表

1. **登录页** (`/pages/login/login`)
   - 微信授权登录
   - 用户信息存储

2. **对话页** (`/pages/index/index`)
   - 创建新会话
   - 发送消息
   - AI流式回复
   - 余额显示

3. **会话列表** (`/pages/sessions/sessions`)
   - 历史会话查看
   - 会话删除

4. **会话详情** (`/pages/chat/chat`)
   - 查看历史消息
   - 继续对话

5. **个人中心** (`/pages/profile/profile`)
   - 用户信息展示
   - 余额查询
   - 交易记录
   - 充值功能
   - 退出登录

### API接口

所有API请求通过 `utils/request.ts` 统一处理：

- 自动添加Authorization头
- 统一错误处理
- Token过期自动跳转登录

## 开发指南

### 添加新页面

1. 在 `src/pages/` 创建页面目录
2. 在 `pages.json` 注册页面
3. 开发页面组件

### 调用API

```typescript
import { get, post } from '@/utils/request'

// GET请求
const data = await get('/api/v1/xxx')

// POST请求
const data = await post('/api/v1/xxx', { param: 'value' })
```

### 环境变量

在 `.env.development` 或 `.env.production` 中定义：

```env
VITE_XXX=value
```

在代码中使用：

```typescript
const apiUrl = import.meta.env.VITE_API_BASE_URL
```

## 注意事项

1. **微信登录**
   - 需要配置微信小程序AppID
   - 需要后端配置相同的AppID和Secret

2. **网络请求**
   - 微信小程序需要配置合法域名
   - 开发时可在开发者工具中关闭域名校验

3. **图片资源**
   - tabBar图标需要放在 `static/tabbar/` 目录
   - 用户头像、logo等放在 `static/` 目录

## 常见问题

### 1. 登录失败

检查：
- 后端是否正常运行
- AppID和Secret是否正确配置
- 网络请求域名是否配置

### 2. API请求失败

检查：
- API地址配置是否正确
- 后端CORS是否配置
- Token是否有效

### 3. 页面样式问题

- 确保使用rpx单位
- 检查不同平台的样式兼容性

## License

待定

