import { useState } from 'react';
import { LoginPage } from './components/LoginPage';
import { ChatPage } from './components/ChatPage';
import { ProfilePage } from './components/ProfilePage';
import { MessageSquare, User } from 'lucide-react';

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [activeTab, setActiveTab] = useState<'chats' | 'profile'>('chats');

  if (!isLoggedIn) {
    return <LoginPage onLogin={() => setIsLoggedIn(true)} />;
  }

  return (
    <div className="flex flex-col h-screen bg-[#ededed] max-w-md mx-auto">
      {/* 主内容区 */}
      <div className="flex-1 overflow-hidden">
        {activeTab === 'chats' && <ChatPage />}
        {activeTab === 'profile' && <ProfilePage onLogout={() => setIsLoggedIn(false)} />}
      </div>

      {/* 底部导航栏 */}
      <div className="bg-white border-t border-gray-200 flex items-center justify-around py-2 px-4">
        <button
          onClick={() => setActiveTab('chats')}
          className={`flex flex-col items-center gap-1 py-1 px-8 ${
            activeTab === 'chats' ? 'text-[#07c160]' : 'text-gray-500'
          }`}
        >
          <MessageSquare className="w-6 h-6" />
          <span className="text-xs">对话</span>
        </button>
        <button
          onClick={() => setActiveTab('profile')}
          className={`flex flex-col items-center gap-1 py-1 px-8 ${
            activeTab === 'profile' ? 'text-[#07c160]' : 'text-gray-500'
          }`}
        >
          <User className="w-6 h-6" />
          <span className="text-xs">我的</span>
        </button>
      </div>
    </div>
  );
}