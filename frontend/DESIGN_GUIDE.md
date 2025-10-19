# 大师AI命理 - 前端设计规范

> 基于苹果设计原则和微信小程序设计语言重新设计

## 🎨 设计理念

### 核心原则
1. **简洁优雅** - 减少视觉噪音，突出核心功能
2. **层次分明** - 清晰的信息架构和视觉层级
3. **一致性** - 统一的设计语言和交互模式
4. **细节精致** - 注重每一个像素的完美呈现

### 设计参考
- **苹果 Human Interface Guidelines**
  - 大量留白
  - 优雅的动画过渡
  - 清晰的视觉层次
  - 细腻的阴影和圆角

- **微信设计规范**
  - 卡片式布局
  - 简洁的配色
  - 底部导航栏
  - 清晰的分隔

## 🎯 设计系统

### 颜色系统

#### 主题色
```scss
$primary: #667eea;              // 主色调（优雅紫）
$primary-light: #818cf8;        // 浅色
$primary-dark: #5568d3;         // 深色
$primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

#### 功能色
```scss
$success: #07c160;              // 成功（微信绿）
$warning: #ff976a;              // 警告
$error: #ee0a24;                // 错误
$info: #1989fa;                 // 信息
```

#### 中性色
```scss
$text-primary: #000000;         // 主要文字
$text-secondary: #666666;       // 次要文字
$text-tertiary: #999999;        // 辅助文字
$text-disabled: #c8c9cc;        // 禁用文字

$bg-page: #f7f8fa;              // 页面背景
$bg-card: #ffffff;              // 卡片背景
$bg-hover: #f2f3f5;             // 悬停背景
$border-color: #ebedf0;         // 边框
$divider: #e5e5e5;              // 分割线
```

### 字体系统

#### 字体家族
```scss
$font-family: -apple-system, BlinkMacSystemFont, 
              'Helvetica Neue', 'PingFang SC', 
              'Hiragino Sans GB', 'Microsoft YaHei', 
              sans-serif;
```

#### 字号（rpx）
```scss
$font-size-xs: 20rpx;           // 10px - 辅助信息
$font-size-sm: 24rpx;           // 12px - 次要文字
$font-size-base: 28rpx;         // 14px - 正文
$font-size-md: 32rpx;           // 16px - 小标题
$font-size-lg: 36rpx;           // 18px - 标题
$font-size-xl: 40rpx;           // 20px - 大标题
$font-size-xxl: 48rpx;          // 24px - 特大标题
$font-size-xxxl: 64rpx;         // 32px - 品牌标题
```

#### 字重
```scss
$font-weight-light: 300;        // 轻
$font-weight-normal: 400;       // 常规
$font-weight-medium: 500;       // 中等
$font-weight-semibold: 600;     // 半粗
$font-weight-bold: 700;         // 粗体
```

### 间距系统（8的倍数）

```scss
$spacing-xs: 8rpx;              // 4px
$spacing-sm: 16rpx;             // 8px
$spacing-md: 24rpx;             // 12px
$spacing-base: 32rpx;           // 16px（基准间距）
$spacing-lg: 40rpx;             // 20px
$spacing-xl: 48rpx;             // 24px
$spacing-xxl: 64rpx;            // 32px
$spacing-xxxl: 96rpx;           // 48px
```

### 圆角系统

```scss
$radius-xs: 4rpx;               // 2px
$radius-sm: 8rpx;               // 4px
$radius-md: 12rpx;              // 6px
$radius-base: 16rpx;            // 8px（基准圆角）
$radius-lg: 24rpx;              // 12px
$radius-xl: 32rpx;              // 16px
$radius-round: 999rpx;          // 圆形
```

### 阴影系统

```scss
$shadow-xs: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
$shadow-sm: 0 4rpx 16rpx rgba(0, 0, 0, 0.06);
$shadow-md: 0 8rpx 24rpx rgba(0, 0, 0, 0.08);
$shadow-lg: 0 12rpx 32rpx rgba(0, 0, 0, 0.10);
$shadow-xl: 0 16rpx 48rpx rgba(0, 0, 0, 0.12);
```

### 动画系统

```scss
// 时长
$duration-fast: 0.2s;
$duration-base: 0.3s;
$duration-slow: 0.5s;

// 缓动函数
$ease-in: cubic-bezier(0.4, 0, 1, 1);
$ease-out: cubic-bezier(0, 0, 0.2, 1);
$ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
$ease-apple: cubic-bezier(0.25, 0.1, 0.25, 1);  // 苹果标准
```

## 📱 页面设计

### 1. 登录页（login/index.vue）

**设计要点：**
- 渐变背景装饰
- 大Logo + 品牌名
- 特性展示卡片
- 固定底部登录按钮
- 协议提示

**视觉特点：**
- 微妙的渐变装饰
- 卡片悬浮效果
- 微信绿色登录按钮
- 淡入动画

### 2. 对话页（chat/index.vue）

**设计要点：**
- 自定义导航栏（显示Token余额）
- 空状态引导（快速问题）
- 气泡式消息列表
- AI输入指示器
- 圆角输入框 + 发送按钮
- 功能菜单（网格布局）

**交互特点：**
- 消息淡入上移动画
- 输入框聚焦效果
- 发送按钮状态变化
- 底部抽屉菜单

### 3. 会话列表页（session/index.vue）

**设计要点：**
- 页面标题 + 管理按钮
- 会话卡片（标题、预览、时间）
- 编辑模式（多选、删除）
- 空状态引导

**交互特点：**
- 卡片点击缩放
- 复选框动画
- 渐进加载动画
- 底部工具栏

### 4. 个人中心页（profile/index.vue）

**设计要点：**
- 渐变用户卡片
- Token余额展示（大数字）
- 功能菜单分组
- 彩色图标背景
- 退出登录按钮

**视觉特点：**
- 毛玻璃效果
- 渐变背景
- 图标颜色分类
- 卡片阴影

## 🎭 组件设计

### 通用组件

#### 1. 卡片（Card）
```scss
.card {
  background: $bg-card;
  border-radius: $radius-lg;
  box-shadow: $shadow-sm;
  padding: $spacing-base;
}
```

#### 2. 按钮（Button）
```scss
// 主按钮
.btn-primary {
  background: $primary-gradient;
  color: #ffffff;
  border-radius: $radius-round;
  box-shadow: $shadow-sm;
  
  &:active {
    transform: scale(0.96);
  }
}

// 次要按钮
.btn-secondary {
  background: $bg-card;
  border: 2rpx solid $border-color;
  border-radius: $radius-round;
  
  &:active {
    background: $bg-hover;
  }
}
```

#### 3. 输入框（Input）
```scss
.input {
  background: $bg-card;
  border: 2rpx solid $border-color;
  border-radius: $radius-lg;
  padding: $spacing-base;
  
  &:focus {
    border-color: $primary;
    box-shadow: 0 0 0 6rpx rgba($primary, 0.1);
  }
}
```

## ✨ 动画效果

### 1. 淡入（Fade In）
```scss
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

### 2. 淡入上移（Fade In Up）
```scss
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(40rpx);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### 3. 缩放（Scale）
```scss
@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
```

## 📐 布局规范

### 1. 页面边距
- 标准页面边距：`32rpx`（16px）
- 卡片间距：`32rpx`（16px）

### 2. 安全区域
```scss
// 底部安全区域
.safe-area-bottom {
  padding-bottom: calc(32rpx + env(safe-area-inset-bottom));
}
```

### 3. 导航栏
- 标准高度：`88rpx`（44px）
- 加上状态栏高度：`88rpx + env(safe-area-inset-top)`

### 4. 底部标签栏
- 高度：`100rpx`（50px）
- 加上安全区域：`100rpx + env(safe-area-inset-bottom)`

## 🎨 设计资源

### 图标系统
- 使用 Emoji 表情图标
- 简洁、通用、跨平台
- 无需额外图标库

### 插画资源
- `/static/empty-chat.svg` - 空状态图标
- `/static/default-avatar.svg` - 默认头像
- `/static/wechat-icon.svg` - 微信图标

## 🔧 开发工具

### Sass Mixins
```scss
@mixin flex-center { ... }       // Flex居中
@mixin ellipsis { ... }          // 文本省略
@mixin card { ... }              // 卡片样式
@mixin btn-primary { ... }       // 主按钮
@mixin frosted-glass { ... }     // 毛玻璃效果
```

### 工具类
```scss
.text-center                     // 文本居中
.ellipsis                        // 单行省略
.ellipsis-2                      // 两行省略
.flex-center                     // Flex居中
.mt-base                         // 上边距
.safe-area-bottom                // 底部安全区域
```

## 📱 响应式设计

### 屏幕适配
- 设计稿基准：`750px`
- 使用 `rpx` 单位自动适配
- 关键元素使用固定像素（1px线条）

### 多端兼容
```scss
// 微信小程序特定样式
/* #ifdef MP-WEIXIN */
.weixin-only { ... }
/* #endif */

// H5特定样式
/* #ifdef H5 */
.h5-only { ... }
/* #endif */
```

## 🎯 设计检查清单

- [ ] 颜色使用设计系统变量
- [ ] 间距使用8的倍数
- [ ] 圆角统一使用系统规范
- [ ] 阴影使用系统定义
- [ ] 动画使用苹果标准缓动
- [ ] 按钮添加活动状态
- [ ] 卡片添加悬停效果
- [ ] 文本考虑省略处理
- [ ] 底部考虑安全区域
- [ ] 加载状态友好提示

## 📚 参考资源

- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [微信小程序设计指南](https://developers.weixin.qq.com/miniprogram/design/)
- [uni-app 官方文档](https://uniapp.dcloud.net.cn/)

---

**版本**: v1.0.0  
**更新日期**: 2025-10-19  
**设计师**: AI Assistant (基于苹果设计原则)

