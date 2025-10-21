import { useState } from 'react';
import { Search, Plus } from 'lucide-react';
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';
import { ChatDetailPage } from './ChatDetailPage';

interface Chat {
  id: string;
  name: string;
  avatar: string;
  lastMessage: string;
  time: string;
  unread?: number;
}

const mockChats: Chat[] = [
  {
    id: '1',
    name: '张三',
    avatar: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=100&h=100&fit=crop',
    lastMessage: '好的，明天见！',
    time: '15:30',
    unread: 2,
  },
  {
    id: '2',
    name: '李四',
    avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&h=100&fit=crop',
    lastMessage: '文件已发送',
    time: '14:20',
  },
  {
    id: '3',
    name: '工作群',
    avatar: 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=100&h=100&fit=crop',
    lastMessage: '王五: 收到',
    time: '昨天',
    unread: 5,
  },
  {
    id: '4',
    name: '家人',
    avatar: 'https://images.unsplash.com/photo-1511632765486-a01980e01a18?w=100&h=100&fit=crop',
    lastMessage: '晚上回来吃饭吗？',
    time: '昨天',
  },
  {
    id: '5',
    name: '赵六',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&h=100&fit=crop',
    lastMessage: '周末一起吃饭',
    time: '星期五',
  },
];

export function ChatPage() {
  const [selectedChat, setSelectedChat] = useState<Chat | null>(null);

  if (selectedChat) {
    return (
      <ChatDetailPage
        chat={selectedChat}
        onBack={() => setSelectedChat(null)}
      />
    );
  }

  return (
    <div className="flex flex-col h-full bg-white">
      {/* 顶部导航 */}
      <div className="bg-[#ededed] px-4 py-3">
        <div className="flex items-center justify-between mb-3">
          <h1 className="text-gray-800">微信</h1>
          <button className="p-1">
            <Plus className="w-6 h-6 text-gray-800" />
          </button>
        </div>
        {/* 搜索栏 */}
        <div className="flex items-center bg-white rounded-md px-3 py-2">
          <Search className="w-4 h-4 text-gray-400 mr-2" />
          <input
            type="text"
            placeholder="搜索"
            className="flex-1 bg-transparent outline-none text-sm"
          />
        </div>
      </div>

      {/* 聊天列表 */}
      <div className="flex-1 overflow-y-auto">
        {mockChats.map((chat) => (
          <div
            key={chat.id}
            onClick={() => setSelectedChat(chat)}
            className="flex items-center px-4 py-3 border-b border-gray-100 hover:bg-gray-50 active:bg-gray-100 cursor-pointer"
          >
            <Avatar className="w-12 h-12 mr-3">
              <AvatarImage src={chat.avatar} />
              <AvatarFallback>{chat.name[0]}</AvatarFallback>
            </Avatar>
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between mb-1">
                <span className="text-gray-800">{chat.name}</span>
                <span className="text-xs text-gray-400">{chat.time}</span>
              </div>
              <div className="flex items-center justify-between">
                <p className="text-sm text-gray-500 truncate flex-1">
                  {chat.lastMessage}
                </p>
                {chat.unread && (
                  <span className="ml-2 bg-red-500 text-white text-xs rounded-full px-1.5 py-0.5 min-w-[18px] text-center">
                    {chat.unread}
                  </span>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
