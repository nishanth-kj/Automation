"use client";

import React from "react";
import { Newspaper, Bot, RefreshCw, Layers } from "lucide-react";

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  isScraping: boolean;
  onRefresh: () => void;
}

export function Sidebar({ activeTab, setActiveTab, isScraping, onRefresh }: SidebarProps) {
  return (
    <div className="w-20 border-r border-zinc-100 dark:border-zinc-900 flex flex-col items-center py-8 gap-8 bg-white/50 dark:bg-black/50">
      <div className="w-10 h-10 bg-zinc-900 dark:bg-zinc-100 rounded-xl flex items-center justify-center shadow-lg mb-4">
        <Layers className="w-6 h-6 text-zinc-100 dark:text-zinc-900" />
      </div>
      
      <NavButton 
        icon={<Newspaper />} 
        active={activeTab === 'news'} 
        onClick={() => setActiveTab('news')} 
      />
      
      <NavButton 
        icon={<Bot />} 
        active={activeTab === 'chat'} 
        onClick={() => setActiveTab('chat')} 
      />
      
      <div className="mt-auto">
        <NavButton 
          icon={<RefreshCw className={isScraping ? "animate-spin" : ""} />} 
          onClick={onRefresh} 
        />
      </div>
    </div>
  );
}

function NavButton({ icon, active, onClick }: { icon: React.ReactNode, active?: boolean, onClick?: () => void }) {
  return (
    <button 
      onClick={onClick}
      className={`p-3 rounded-2xl transition-all duration-300 ${
        active 
        ? 'bg-zinc-900 text-white shadow-xl scale-110' 
        : 'text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-900 hover:text-zinc-600'
      }`}
    >
      {React.cloneElement(icon as React.ReactElement<any>, { className: "w-6 h-6" })}
    </button>
  );
}
