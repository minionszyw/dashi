<template>
  <view class="legal-page">
    <view class="content">
      <view class="header">
        <text class="title">用户协议</text>
        <text class="update-date">更新日期：2025年10月24日</text>
      </view>

      <view class="section">
        <text class="section-title">一、服务说明</text>
        <text class="section-text">
          欢迎使用国学大师！我们提供基于中国传统命理学的八字排盘和AI智能分析服务。使用本服务即表示您同意本协议的全部条款。
        </text>
        <text class="section-text">
          本服务仅供娱乐和参考，不构成任何决策建议。
        </text>
      </view>

      <view class="section">
        <text class="section-title">二、账户注册</text>
        <text class="section-text">
          您需要使用微信账号登录本应用。注册时，您同意：
        </text>
        <text class="section-text">• 提供真实、准确的个人信息</text>
        <text class="section-text">• 妥善保管账户安全</text>
        <text class="section-text">• 对账户下的所有行为负责</text>
        <text class="section-text">• 不将账户转让或出借给他人</text>
      </view>

      <view class="section">
        <text class="section-title">三、服务内容</text>
        <text class="section-text">本应用提供的主要服务包括：</text>
        <text class="section-text">• 八字排盘：根据出生信息计算个人命盘</text>
        <text class="section-text">• AI对话：基于命理知识的智能问答</text>
        <text class="section-text">• 命理分析：五行、十神、大运等解读</text>
        <text class="section-text">• 个人档案：保存和管理命理信息</text>
      </view>

      <view class="section">
        <text class="section-title">四、使用规范</text>
        <text class="section-text">使用本服务时，您不得：</text>
        <text class="section-text">• 发布违法、违规、虚假或有害信息</text>
        <text class="section-text">• 侵犯他人知识产权或隐私权</text>
        <text class="section-text">• 利用服务从事商业活动或牟利</text>
        <text class="section-text">• 破坏或干扰服务的正常运行</text>
        <text class="section-text">• 使用自动化工具或恶意软件</text>
        <text class="section-text">• 传播迷信、封建或不健康内容</text>
      </view>

      <view class="section">
        <text class="section-title">五、收费服务</text>
        <text class="section-text">
          本应用采用余额付费模式：
        </text>
        <text class="section-text">• 新用户注册赠送初始余额</text>
        <text class="section-text">• AI对话服务按Token消耗计费</text>
        <text class="section-text">• 充值余额不可退款</text>
        <text class="section-text">• 我们保留调整价格的权利，但会提前通知</text>
      </view>

      <view class="section">
        <text class="section-title">六、知识产权</text>
        <text class="section-text">
          本应用的所有内容（包括但不限于文字、图片、算法、代码）的知识产权归我们或相关权利人所有。未经许可，您不得复制、修改、传播或商业使用。
        </text>
      </view>

      <view class="section">
        <text class="section-title">七、免责声明</text>
        <text class="section-text">
          重要提示：
        </text>
        <text class="section-text">
          • 命理分析结果仅供娱乐和参考，不代表科学论断
        </text>
        <text class="section-text">
          • 我们不对分析结果的准确性、完整性承担责任
        </text>
        <text class="section-text">
          • 您不应基于分析结果做出重大人生决策
        </text>
        <text class="section-text">
          • 因使用本服务产生的任何损失，我们不承担责任
        </text>
        <text class="section-text">
          • 我们不保证服务的持续性和稳定性
        </text>
      </view>

      <view class="section">
        <text class="section-title">八、服务变更与终止</text>
        <text class="section-text">我们有权：</text>
        <text class="section-text">• 随时修改、暂停或终止服务</text>
        <text class="section-text">• 对违规用户进行警告、限制或封禁</text>
        <text class="section-text">• 在服务终止时删除用户数据</text>
        <text class="section-text">• 修改本协议并通过应用内通知</text>
      </view>

      <view class="section">
        <text class="section-title">九、争议解决</text>
        <text class="section-text">
          本协议的解释、执行和争议解决适用中华人民共和国法律。发生争议时，双方应友好协商；协商不成的，提交我方所在地人民法院诉讼解决。
        </text>
      </view>

      <view class="section">
        <text class="section-title">十、联系我们</text>
        <text class="section-text">
          如有任何问题或建议，请联系我们：
        </text>
        <text class="section-text">• 邮箱：support@guoxuedashi.com</text>
        <text class="section-text">• 应用内反馈功能</text>
      </view>

      <view class="divider"></view>

      <view class="footer-note">
        <text class="note-text">
          再次感谢您选择国学大师！我们致力于传承和弘扬中国传统文化，为您提供优质的命理分析服务。请您理性看待命理分析，科学把握人生方向。
        </text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { onLoad } from '@dcloudio/uni-app'

onLoad(() => {
  uni.setNavigationBarTitle({
    title: '用户协议'
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

