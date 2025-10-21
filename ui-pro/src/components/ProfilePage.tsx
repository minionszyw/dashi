import {
  Avatar,
  AvatarFallback,
  AvatarImage,
} from "./ui/avatar";
import {
  ChevronRight,
  Settings,
  Wallet,
  Heart,
  Camera,
  Edit,
  LogOut,
} from "lucide-react";
import { Button } from "./ui/button";

interface ProfilePageProps {
  onLogout: () => void;
}

export function ProfilePage({ onLogout }: ProfilePageProps) {
  return (
    <div className="flex flex-col h-full bg-[#ededed] overflow-y-auto">
      {/* 个人信息卡片 */}
      <div className="bg-white px-6 py-6 mb-3">
        <div className="flex items-center">
          <Avatar className="w-16 h-16 mr-4">
            <AvatarImage src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop" />
            <AvatarFallback>Me</AvatarFallback>
          </Avatar>
          <div className="flex-1">
            <h2 className="text-gray-800 mb-1">用户昵称</h2>
            <p className="text-sm text-gray-500">
              ID: user123456
            </p>
          </div>
          <button className="px-4 py-1.5 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-md text-sm flex items-center gap-1">
            <Edit className="w-4 h-4" />
            编辑
          </button>
        </div>
      </div>

      {/* 余额卡片 */}
      <div className="bg-white px-6 py-4 mb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-orange-400 to-orange-500 rounded-full flex items-center justify-center">
              <Wallet className="w-5 h-5 text-white" />
            </div>
            <div>
              <p className="text-sm text-gray-500 mb-0.5">
                账户余额
              </p>
              <p className="text-gray-800">¥ 100</p>
            </div>
          </div>
          <Button className="bg-[#07c160] hover:bg-[#06ad56] text-white px-6 py-2 rounded-lg">
            充值
          </Button>
        </div>
      </div>

      {/* 功能列表 */}
      <div className="bg-white mb-3">
        <MenuItem
          icon={<Wallet className="w-5 h-5" />}
          label="八字排盘"
        />
        <div className="border-t border-gray-100 mx-4" />
        <MenuItem
          icon={<Heart className="w-5 h-5" />}
          label="系统设置"
        />
        <div className="border-t border-gray-100 mx-4" />
        <MenuItem
          icon={<Camera className="w-5 h-5" />}
          label="使用帮助"
        />
        <div className="border-t border-gray-100 mx-4" />
        <MenuItem
          icon={<Settings className="w-5 h-5" />}
          label="关于我们"
        />
      </div>

      {/* 退出登录按钮 */}
      <div className="px-4 py-4">
        <Button
          onClick={onLogout}
          variant="outline"
          className="w-full h-12 bg-white hover:bg-gray-50 text-gray-800 border border-gray-300 rounded-lg flex items-center justify-center gap-2"
        >
          <LogOut className="w-5 h-5" />
          退出登录
        </Button>
      </div>
    </div>
  );
}

interface MenuItemProps {
  icon: React.ReactNode;
  label: string;
}

function MenuItem({ icon, label }: MenuItemProps) {
  return (
    <button className="w-full flex items-center justify-between px-6 py-4 hover:bg-gray-50 active:bg-gray-100">
      <div className="flex items-center gap-3">
        <div className="text-gray-700">{icon}</div>
        <span className="text-gray-800">{label}</span>
      </div>
      <ChevronRight className="w-5 h-5 text-gray-400" />
    </button>
  );
}