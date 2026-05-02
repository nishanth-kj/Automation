"use client";

import React from "react";
import { Newspaper, Bot, RefreshCw, Layers, Home, History, Settings, Database, Terminal } from "lucide-react";

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  isScraping: boolean;
  onRefresh: () => void;
  showConsole: boolean;
  setShowConsole: (val: boolean) => void;
}

export function Sidebar({ 
  activeTab, 
  setActiveTab, 
  isScraping, 
  onRefresh,
  showConsole,
  setShowConsole
}: SidebarProps) {
  return (
    <div className="w-20 border-r border-zinc-100 dark:border-zinc-900 flex flex-col items-center py-8 gap-6 bg-white/50 dark:bg-black/50">
      <div className="w-10 h-10 bg-zinc-900 dark:bg-zinc-100 rounded-xl flex items-center justify-center shadow-lg mb-4">
        <Layers className="w-6 h-6 text-zinc-100 dark:text-zinc-900" />
      </div>
      
      <NavButton 
        icon={<Home />} 
        active={activeTab === 'home'} 
        onClick={() => setActiveTab('home')} 
        label="Home"
      />

      <NavButton 
        icon={<Newspaper />} 
        active={activeTab === 'news'} 
        onClick={() => setActiveTab('news')} 
        label="News"
      />
      
      <NavButton 
        icon={<Bot />} 
        active={activeTab === 'chat'} 
        onClick={() => setActiveTab('chat')} 
        label="AI Chat"
      />

      <NavButton 
        icon={<Database />} 
        active={activeTab === 'rag'} 
        onClick={() => setActiveTab('rag')} 
        label="Knowledge"
      />

      <NavButton 
        icon={<History />} 
        active={activeTab === 'history'} 
        onClick={() => setActiveTab('history')} 
        label="History"
      />
      
      <div className="mt-auto flex flex-col gap-6">
        <NavButton 
          icon={<Terminal />} 
          active={showConsole} 
          onClick={() => setShowConsole(!showConsole)} 
          label="Console"
        />
        <NavButton 
          icon={<Settings />} 
          active={activeTab === 'settings'} 
          onClick={() => setActiveTab('settings')} 
          label="Settings"
        />
        <NavButton 
          icon={<RefreshCw className={isScraping ? "animate-spin" : ""} />} 
          onClick={onRefresh} 
          label="Refresh"
        />
      </div>
    </div>
  );
}

function NavButton({ icon, active, onClick, label }: { icon: React.ReactNode, active?: boolean, onClick?: () => void, label?: string }) {
  return (
    <button 
      onClick={onClick}
      title={label}
      className={`p-3 rounded-2xl transition-all duration-300 relative group ${
        active 
        ? 'bg-zinc-900 text-white shadow-xl scale-110' 
        : 'text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-900 hover:text-zinc-600'
      }`}
    >
      {React.cloneElement(icon as React.ReactElement<any>, { className: "w-6 h-6" })}
      <span className="absolute left-16 bg-zinc-900 text-white text-[10px] px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-50">
        {label}
      </span>
    </button>
  );
}

