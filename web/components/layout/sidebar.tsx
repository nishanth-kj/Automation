"use client";

import React from "react";
import { Newspaper, Bot, RefreshCw, Home, History, Settings, Database, Terminal } from "lucide-react";
import { cn } from "@/lib/utils";

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
  const items = [
    { id: 'home', icon: Home, label: 'Home' },
    { id: 'news', icon: Newspaper, label: 'News' },
    { id: 'chat', icon: Bot, label: 'Studio' },
    { id: 'rag', icon: Database, label: 'Docs' },
    { id: 'history', icon: History, label: 'History' },
    { id: 'settings', icon: Settings, label: 'Settings' },
  ];

  return (
    <div className="w-16 md:w-56 border-r border-zinc-100 dark:border-zinc-900 bg-white dark:bg-black flex flex-col transition-all">
      <div className="flex-1 py-4 space-y-1">
        {items.map((item) => (
          <button
            key={item.id}
            onClick={() => setActiveTab(item.id)}
            className={cn(
              "w-full flex items-center gap-3 px-4 py-2 text-sm font-medium transition-colors group",
              activeTab === item.id 
                ? "text-zinc-950 dark:text-white bg-zinc-50 dark:bg-zinc-900" 
                : "text-zinc-500 hover:text-zinc-950 dark:hover:text-white hover:bg-zinc-50/50 dark:hover:bg-zinc-900/50"
            )}
          >
            <item.icon className={cn(
              "w-4 h-4 shrink-0",
              activeTab === item.id ? "text-zinc-950 dark:text-white" : "text-zinc-400 group-hover:text-zinc-600"
            )} />
            <span className="hidden md:block">{item.label}</span>
          </button>
        ))}
      </div>

      <div className="p-4 border-t border-zinc-100 dark:border-zinc-900 space-y-2">
        <button
          onClick={() => setShowConsole(!showConsole)}
          className={cn(
            "w-full flex items-center gap-3 px-3 py-2 rounded-md text-xs font-medium transition-all",
            showConsole ? "bg-zinc-900 text-white" : "text-zinc-500 hover:bg-zinc-100"
          )}
        >
          <Terminal className="w-3.5 h-3.5" />
          <span className="hidden md:block">Console</span>
        </button>
        
        <button
          disabled={isScraping}
          onClick={onRefresh}
          className={cn(
            "w-full flex items-center gap-3 px-3 py-2 rounded-md text-xs font-medium bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 hover:opacity-90 disabled:opacity-50 transition-all",
            isScraping && "animate-pulse"
          )}
        >
          <RefreshCw className={cn("w-3.5 h-3.5", isScraping && "animate-spin")} />
          <span className="hidden md:block">{isScraping ? "Scraping..." : "Refresh"}</span>
        </button>
      </div>
    </div>
  );
}
