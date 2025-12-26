import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Users, 
  MessageSquare, 
  Bell, 
  TrendingUp, 
  Settings,
  Menu,
  X,
  LogOut,
  User,
  Shield
} from 'lucide-react';
import { useAuthStore } from '../../store/authStore';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Entities', href: '/entities', icon: Users },
  { name: 'Mentions', href: '/mentions', icon: MessageSquare },
  { name: 'Alerts', href: '/alerts', icon: Bell },
  { name: 'Analytics', href: '/analytics', icon: TrendingUp },
  { name: 'Settings', href: '/settings', icon: Settings },
];

const adminNavigation = [
  { name: 'Admin Panel', href: '/admin', icon: Shield, adminOnly: true },
];

function Layout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();
  const { user, logout } = useAuthStore();

  return (
    <div className="min-h-screen bg-slate-950">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside 
        className={`
          fixed inset-y-0 left-0 z-50 w-64 bg-slate-900 border-r border-slate-800
          transform transition-transform duration-200 ease-in-out
          lg:translate-x-0
          ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
        `}
      >
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center justify-between h-16 px-6 border-b border-slate-800">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
                <span className="text-white font-bold text-sm">AI</span>
              </div>
              <span className="text-white font-semibold text-lg">AI Guardian</span>
            </div>
            <button 
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden text-slate-400 hover:text-white"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href;
              const Icon = item.icon;
              
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`
                    flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium
                    transition-all duration-200
                    ${isActive 
                      ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/50' 
                      : 'text-slate-400 hover:text-white hover:bg-slate-800'
                    }
                  `}
                  onClick={() => setSidebarOpen(false)}
                >
                  <Icon className="w-5 h-5" />
                  {item.name}
                </Link>
              );
            })}
            
            {/* Admin navigation - only for admin users */}
            {user?.role === 'admin' && (
              <div className="pt-4 mt-4 border-t border-slate-800">
                <div className="px-3 py-1 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  Administration
                </div>
                {adminNavigation.map((item) => {
                  const isActive = location.pathname === item.href;
                  const Icon = item.icon;
                  
                  return (
                    <Link
                      key={item.name}
                      to={item.href}
                      className={`
                        flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium
                        transition-all duration-200
                        ${isActive 
                          ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/50' 
                          : 'text-slate-400 hover:text-white hover:bg-slate-800'
                        }
                      `}
                      onClick={() => setSidebarOpen(false)}
                    >
                      <Icon className="w-5 h-5" />
                      {item.name}
                    </Link>
                  );
                })}
              </div>
            )}
          </nav>

          {/* User section */}
          <div className="p-4 border-t border-slate-800">
            <div className="flex items-center gap-3 px-3 py-2 rounded-lg bg-slate-800">
              <div className="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center">
                <User className="w-4 h-4 text-white" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-white truncate">
                  {user?.full_name || user?.username || 'User'}
                </p>
                <p className="text-xs text-slate-400 truncate">
                  {user?.email}
                </p>
                {user?.role === 'admin' && (
                  <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-indigo-100 text-indigo-800 mt-1">
                    Admin
                  </span>
                )}
              </div>
              <button
                onClick={logout}
                className="text-slate-400 hover:text-white transition-colors"
                title="Logout"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <div className="lg:pl-64">
        {/* Top bar */}
        <header className="sticky top-0 z-30 bg-slate-900/95 backdrop-blur border-b border-slate-800">
          <div className="flex items-center justify-between h-16 px-4 sm:px-6">
            <button
              onClick={() => setSidebarOpen(true)}
              className="lg:hidden text-slate-400 hover:text-white"
            >
              <Menu className="w-6 h-6" />
            </button>
            
            <div className="flex-1 lg:flex-none" />
            
            <div className="flex items-center gap-4">
              <button className="relative text-slate-400 hover:text-white transition-colors">
                <Bell className="w-5 h-5" />
                <span className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full text-xs text-white flex items-center justify-center">
                  3
                </span>
              </button>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="p-4 sm:p-6 lg:p-8">
          {children}
        </main>
      </div>
    </div>
  );
}

export default Layout;
