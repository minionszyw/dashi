<template>
  <view class="legal-page">
    <view class="content">
      <view class="header">
        <text class="title">隐私政策</text>
        <text class="update-date">更新日期：2025年10月24日</text>
      </view>

      <view class="section">
        <text class="section-title">一、信息收集</text>
        <text class="section-text">
          我们可能会收集以下信息：
        </text>
        <text class="section-text">• 微信授权信息（昵称、头像等基本信息）</text>
        <text class="section-text">• 您主动提供的出生信息（用于八字排盘）</text>
        <text class="section-text">• 对话记录（用于AI服务优化）</text>
        <text class="section-text">• 设备信息和日志信息</text>
      </view>

      <view class="section">
        <text class="section-title">二、信息使用</text>
        <text class="section-text">
          我们使用收集的信息用于：
        </text>
        <text class="section-text">• 提供八字排盘和AI命理分析服务</text>
        <text class="section-text">• 改进和优化用户体验</text>
        <text class="section-text">• 保障服务安全和防止欺诈</text>
        <text class="section-text">• 处理账户和支付事务</text>
      </view>

      <view class="section">
        <text class="section-title">三、信息保护</text>
        <text class="section-text">
          我们采取以下措施保护您的信息：
        </text>
        <text class="section-text">• 使用加密技术传输和存储数据</text>
        <text class="section-text">• 严格限制员工访问权限</text>
        <text class="section-text">• 定期进行安全审计</text>
        <text class="section-text">• 不会向第三方出售您的个人信息</text>
      </view>

      <view class="section">
        <text class="section-title">四、信息共享</text>
        <text class="section-text">
          除以下情况外，我们不会与第三方共享您的信息：
        </text>
        <text class="section-text">• 获得您的明确同意</text>
        <text class="section-text">• 法律法规要求或司法程序需要</text>
        <text class="section-text">• 保护用户或公众的权益、财产或安全</text>
        <text class="section-text">• 与服务提供商（如AI服务、支付服务）必要共享</text>
      </view>

      <view class="section">
        <text class="section-title">五、您的权利</text>
        <text class="section-text">您对自己的个人信息享有以下权利：</text>
        <text class="section-text">• 访问和更正您的个人信息</text>
        <text class="section-text">• 删除您的账户和相关数据</text>
        <text class="section-text">• 撤回已授权的同意</text>
        <text class="section-text">• 拒绝特定的信息处理活动</text>
      </view>

      <view class="section">
        <text class="section-title">六、未成年人保护</text>
        <text class="section-text">
          我们非常重视未成年人的隐私保护。如果您是未成年人，请在监护人的指导下使用我们的服务。
        </text>
      </view>

      <view class="section">
        <text class="section-title">七、政策变更</text>
        <text class="section-text">
          我们可能会不时更新本隐私政策。重大变更时，我们会在应用内通知您。继续使用服务即表示您接受更新后的政策。
        </text>
      </view>

      <view class="section">
        <text class="section-title">八、联系我们</text>
        <text class="section-text">
          如果您对本隐私政策有任何疑问或建议，请通过以下方式联系我们：
        </text>
        <text class="section-text">• 邮箱：privacy@guoxuedashi.com</text>
        <text class="section-text">• 应用内反馈功能</text>
      </view>

      <view class="divider"></view>

      <view class="footer-note">
        <text class="note-text">
          本隐私政策是《国学大师用户协议》的重要组成部分。使用本应用即表示您已仔细阅读并同意本隐私政策的全部内容。
        </text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { onLoad } from '@dcloudio/uni-app'

onLoad(() => {
  uni.setNavigationBarTitle({
    title: '隐私政策'
  })
})
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';
@import '@/styles/mixins.scss';

.legal-page {
  min-height: 100vh;
  background: $bg-page;
}

.content {
  padding: $space-lg;
}

.header {
  margin-bottom: $space-xl;
  text-align: center;
}

.title {
  display: block;
  font-size: $font-xl;
  font-weight: 600;
  color: $primary;
  margin-bottom: $space-sm;
}

.update-date {
  display: block;
  font-size: $font-sm;
  color: $text-secondary;
}

.section {
  margin-bottom: $space-lg;
}

.section-title {
  display: block;
  font-size: $font-base;
  font-weight: 600;
  color: $text-primary;
  margin-bottom: $space-base;
  margin-top: $space-lg;
}

.section-text {
  display: block;
  font-size: $font-sm;
  color: $text-secondary;
  line-height: 2;
  margin-bottom: $space-xs;
}

.divider {
  height: 1rpx;
  background: $border-color;
  margin: $space-lg 0;
}

.footer-note {
  padding: $space-base 0;
}

.note-text {
  display: block;
  font-size: $font-sm;
  color: $text-tertiary;
  line-height: 2;
}
</style>

