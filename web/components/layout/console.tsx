"use client";

import React, { useState, useEffect, useRef } from "react";
import { X, Terminal, ChevronDown, ChevronUp, Trash2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface LogEntry {
  timestamp: string;
  level: string;
  message: string;
}

export function Console({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isOpen) {
      // In a real app, we would subscribe to a log stream or fetch initial logs
      const mockLogs = [
        { timestamp: "17:20:01", level: "INFO", message: "Application initialized" },
        { timestamp: "17:20:05", level: "INFO", message: "WebSocket connected to /ws/scraper" },
        { timestamp: "17:20:10", level: "DEBUG", message: "Fetching news from repository..." },
      ];
      setLogs(mockLogs);
    }
  }, [isOpen]);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  if (!isOpen) return null;

  return (
    <div className="fixed bottom-0 left-20 right-0 h-64 bg-zinc-950 border-t border-zinc-800 z-50 flex flex-col animate-in slide-in-from-bottom-full duration-300">
      <div className="flex items-center justify-between px-4 py-2 border-b border-zinc-800 bg-zinc-900/50">
        <div className="flex items-center gap-2">
          <Terminal className="w-4 h-4 text-emerald-500" />
          <span className="text-xs font-bold text-zinc-400 uppercase tracking-widest">System Console</span>
        </div>
        <div className="flex items-center gap-2">
          <button 
            onClick={() => setLogs([])}
            className="p-1 hover:bg-zinc-800 rounded transition-colors text-zinc-500 hover:text-zinc-300"
            title="Clear logs"
          >
            <Trash2 className="w-3.5 h-3.5" />
          </button>
          <button 
            onClick={onClose}
            className="p-1 hover:bg-zinc-800 rounded transition-colors text-zinc-500 hover:text-zinc-300"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>
      
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-4 font-mono text-[11px] leading-relaxed"
      >
        {logs.length === 0 ? (
          <div className="h-full flex items-center justify-center text-zinc-700 italic">
            No active logs...
          </div>
        ) : (
          logs.map((log, i) => (
            <div key={i} className="flex gap-4 py-0.5 group">
              <span className="text-zinc-600 shrink-0">{log.timestamp}</span>
              <span className={cn(
                "shrink-0 font-bold",
                log.level === 'INFO' ? "text-blue-400" : 
                log.level === 'DEBUG' ? "text-zinc-500" : 
                log.level === 'WARN' ? "text-amber-400" : "text-rose-400"
              )}>
                {log.level.padEnd(5)}
              </span>
              <span className="text-zinc-300 break-all">{log.message}</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
