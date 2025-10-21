import { useState } from 'react';
import { ChevronLeft, Plus, Send } from 'lucide-react';
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';
import { Button } from './ui/button';

interface Chat {
  id: string;
  name: string;
  avatar: string;
  lastMessage: string;
  time: string;
  unread?: number;
}

interface ChatDetailPageProps {
  chat: Chat;
  onBack: () => void;
}

interface Message {
  id: string;
  content: string;
  isSelf: boolean;
  time: string;
}

const mockMessages: Message[] = [
  {
    id: '1',
    content: '你好！',
    isSelf: false,
    time: '14:20',
  },
  {
    id: '2',
    content: '你好，有什么事吗？',
    isSelf: true,
    time: '14:21',
  },
  {
    id: '3',
    content: '明天下午有空吗？一起吃个饭',
    isSelf: false,
    time: '14:22',
  },
  {
    id: '4',
    content: '好的，明天见！',
    isSelf: true,
    time: '15:30',
  },
];

export function ChatDetailPage({ chat, onBack }: ChatDetailPageProps) {
  const [messages, setMessages] = useState<Message[]>(mockMessages);
  const [inputValue, setInputValue] = useState('');

  const handleSend = () => {
    if (!inputValue.trim()) return;

    const newMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      isSelf: true,
      time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages([...messages, newMessage]);
    setInputValue('');
  };

  return (
    <div className="flex flex-col h-full bg-[#ededed]">
      {/* 顶部导航 */}
      <div className="bg-white border-b border-gray-200 px-4 py-3 flex items-center">
        <button onClick={onBack} className="mr-3">
          <ChevronLeft className="w-6 h-6 text-gray-800" />
        </button>
        <h2 className="text-gray-800">{chat.name}</h2>
      </div>

      {/* 消息列表 */}
      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.isSelf ? 'justify-end' : 'justify-start'}`}
          >
            <div className={`flex gap-2 max-w-[70%] ${message.isSelf ? 'flex-row-reverse' : 'flex-row'}`}>
              <Avatar className="w-10 h-10 flex-shrink-0">
                <AvatarImage src={message.isSelf ? 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop' : chat.avatar} />
                <AvatarFallback>{message.isSelf ? 'Me' : chat.name[0]}</AvatarFallback>
              </Avatar>
              <div className={`flex flex-col ${message.isSelf ? 'items-end' : 'items-start'}`}>
                <div
                  className={`rounded-lg px-4 py-2 ${
                    message.isSelf
                      ? 'bg-[#95ec69] text-gray-800'
                      : 'bg-white text-gray-800'
                  }`}
                >
                  {message.content}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* 输入框 */}
      <div className="bg-[#f7f7f7] border-t border-gray-200 px-4 py-3">
        <div className="flex items-end gap-2">
          <button className="p-2 hover:bg-gray-200 rounded mb-0.5">
            <Plus className="w-6 h-6 text-gray-600" />
          </button>
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            placeholder="输入消息..."
            className="flex-1 bg-white border border-gray-300 rounded-lg px-3 py-2 resize-none outline-none focus:border-[#07c160]"
            rows={1}
          />
          <Button
            onClick={handleSend}
            className="bg-[#07c160] hover:bg-[#06ad56] text-white px-4 py-2 rounded-lg"
          >
            <Send className="w-5 h-5" />
          </Button>
        </div>
      </div>
    </div>
  );
}