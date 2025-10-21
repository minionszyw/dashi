import { Button } from './ui/button';
import { Input } from './ui/input';
import { MessageSquare } from 'lucide-react';

interface LoginPageProps {
  onLogin: () => void;
}

export function LoginPage({ onLogin }: LoginPageProps) {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-white px-8 max-w-md mx-auto">
      {/* Logo */}
      <div className="mb-16">
        <div className="w-24 h-24 bg-[#07c160] rounded-2xl flex items-center justify-center mb-6 mx-auto">
          <MessageSquare className="w-14 h-14 text-white" />
        </div>
        <h1 className="text-center text-gray-800 mb-2">聊天小程序</h1>
        <p className="text-center text-sm text-gray-500">欢迎使用</p>
      </div>

      {/* 微信登录按钮 */}
      <Button
        onClick={onLogin}
        className="w-full h-12 bg-[#07c160] hover:bg-[#06ad56] text-white rounded-lg flex items-center justify-center gap-2"
      >
        <MessageSquare className="w-5 h-5" />
        微信登录
      </Button>

      {/* 底部提示 */}
      <p className="text-xs text-gray-400 text-center mt-8">
        登录即表示同意用户协议和隐私政策
      </p>
    </div>
  );
}