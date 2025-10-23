<script setup lang="ts">
import { onLaunch, onShow, onHide } from '@dcloudio/uni-app'
import { useUserStore } from '@/stores'

const userStore = useUserStore()

onLaunch(() => {
  console.log('App Launch')
  // 尝试从本地存储恢复登录状态
  userStore.init()
})

onShow(() => {
  console.log('App Show')
})

onHide(() => {
  console.log('App Hide')
})
</script>

<style lang="scss">
@import '@/styles/variables.scss';
@import '@/styles/common.scss';

// ============================================
// 全局重置
// ============================================

page {
  font-family: $font-family;
  font-size: $font-base;
  color: $text-primary;
  background: $bg-page;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

// ============================================
// uni-app组件样式覆盖
// ============================================

// 按钮样式重置
button {
  padding: 0;
  margin: 0;
  line-height: inherit;
  font-size: inherit;
  
  &::after {
    border: none;
  }
}

// 输入框样式
input {
  font-family: inherit;
}

// 滚动视图
scroll-view {
  &::-webkit-scrollbar {
    display: none;
  }
}

// ============================================
// 自定义全局组件样式
// ============================================

// 加载提示
.uni-loading {
  .uni-loading__spinner {
    color: $primary;
  }
}

// Toast样式
.uni-toast {
  .uni-toast__content {
    border-radius: $radius-lg !important;
    box-shadow: $shadow-lg !important;
  }
}

// Modal样式
.uni-modal {
  .uni-modal__bd {
    padding: $space-xl $space-lg !important;
    line-height: 1.6 !important;
  }
  
  .uni-modal__ft {
    .uni-modal__btn {
      color: $primary !important;
      
      &.uni-modal__btn_primary {
        color: $primary !important;
        font-weight: $weight-semibold !important;
      }
    }
  }
}
</style>
