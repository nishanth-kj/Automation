"use client";

import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { 
  Sparkles, 
  TrendingUp, 
  Zap, 
  Clock, 
  ShieldCheck, 
  ArrowRight,
  Newspaper,
  Image as ImageIcon,
  Bot
} from "lucide-react";
import { NewsItem } from "@/types/api";

interface HomeDashboardProps {
  news: NewsItem[];
  onNavigate: (tab: string) => void;
}

export function HomeDashboard({ news, onNavigate }: HomeDashboardProps) {
  return (
    <div className="space-y-8 animate-in fade-in duration-1000">
      {/* Hero Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="col-span-2 bg-zinc-950 text-white border-none shadow-2xl overflow-hidden relative group">
          <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/20 via-purple-500/10 to-transparent opacity-50" />
          <div className="absolute top-0 right-0 p-12 opacity-5 group-hover:opacity-10 transition-opacity">
            <Sparkles className="w-64 h-64 rotate-12" />
          </div>
          <CardHeader className="p-10 pb-2 relative z-10">
            <Badge className="w-fit mb-4 bg-white/10 text-white border-white/20 backdrop-blur-md uppercase tracking-widest text-[10px] font-black">
              AI Powered Studio
            </Badge>
            <CardTitle className="text-5xl font-black leading-tight tracking-tighter">
              Create Viral Memes <br /> <span className="text-zinc-500">From Today's News.</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="p-10 pt-0 relative z-10">
            <p className="text-zinc-400 text-lg mb-8 max-w-md font-medium leading-relaxed">
              Transform trending headlines into engaging social content using native AI and ComfyUI.
            </p>
            <div className="flex gap-4">
              <Button 
                className="bg-white text-zinc-900 hover:bg-zinc-200 rounded-2xl px-8 h-14 font-bold text-base gap-3 shadow-xl shadow-white/10 transition-all hover:scale-105 active:scale-95"
                onClick={() => onNavigate('news')}
              >
                Launch Studio <ArrowRight className="w-5 h-5" />
              </Button>
              <Button 
                variant="outline" 
                className="rounded-2xl px-8 h-14 font-bold text-base border-zinc-800 hover:bg-zinc-900 text-white gap-3"
                onClick={() => onNavigate('chat')}
              >
                Talk to AI
              </Button>
            </div>
          </CardContent>
        </Card>

        <div className="space-y-6">
          <Card className="bg-white dark:bg-zinc-950 border-zinc-100 dark:border-zinc-900 shadow-sm overflow-hidden">
            <CardHeader className="pb-2">
              <div className="flex items-center justify-between">
                <CardTitle className="text-xs font-black text-zinc-400 uppercase tracking-widest">Live Stats</CardTitle>
                <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <StatItem label="Active News" value={news.length.toString()} icon={<Newspaper className="w-3.5 h-3.5" />} />
              <StatItem label="Generations" value="1,284" icon={<Zap className="w-3.5 h-3.5 text-amber-500" />} />
              <StatItem label="Models" value="4 Active" icon={<Bot className="w-3.5 h-3.5 text-purple-500" />} />
              <div className="pt-2 border-t border-zinc-50 dark:border-zinc-900 flex justify-between items-center">
                <span className="text-[10px] font-bold text-zinc-400 uppercase">System Integrity</span>
                <Badge className="bg-emerald-500/10 text-emerald-500 border-none text-[10px] font-black">99.9% SECURE</Badge>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-indigo-600 text-white border-none shadow-lg shadow-indigo-500/20">
            <CardContent className="p-6">
              <div className="flex items-center gap-4 mb-4">
                <div className="w-10 h-10 rounded-xl bg-white/20 flex items-center justify-center">
                  <TrendingUp className="w-5 h-5" />
                </div>
                <div>
                  <p className="text-xs font-bold text-indigo-200 uppercase tracking-widest">Current Trend</p>
                  <p className="font-bold text-lg">AI Regulation</p>
                </div>
              </div>
              <Button size="sm" className="w-full bg-white text-indigo-600 hover:bg-indigo-50 rounded-lg font-bold">
                View Coverage
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Quick Access Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <QuickAction 
          title="Recent History" 
          desc="View your last generated memes" 
          icon={<Clock className="text-blue-500" />} 
          onClick={() => onNavigate('history')}
        />
        <QuickAction 
          title="Knowledge" 
          desc="Manage RAG documents" 
          icon={<ShieldCheck className="text-emerald-500" />} 
          onClick={() => onNavigate('rag')}
        />
        <QuickAction 
          title="Media Library" 
          desc="Access ComfyUI assets" 
          icon={<ImageIcon className="text-purple-500" />} 
          onClick={() => {}}
        />
        <QuickAction 
          title="Studio Config" 
          desc="Tweak AI parameters" 
          icon={<Zap className="text-amber-500" />} 
          onClick={() => onNavigate('settings')}
        />
      </div>

      {/* Recent News Snippet */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-bold tracking-tight">Recent Updates</h3>
          <Button variant="link" className="text-zinc-500 font-bold" onClick={() => onNavigate('news')}>View all news <ArrowRight className="ml-2 w-4 h-4" /></Button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {news.slice(0, 2).map((item, i) => (
            <div key={i} className="flex items-center gap-4 p-4 bg-white dark:bg-zinc-950 rounded-2xl border border-zinc-100 dark:border-zinc-900 group cursor-pointer hover:border-zinc-300 dark:hover:border-zinc-700 transition-all shadow-sm">
              <div className="w-16 h-16 rounded-xl bg-zinc-100 dark:bg-zinc-900 overflow-hidden shrink-0">
                {item.image_url ? (
                  <img src={item.image_url} className="w-full h-full object-cover" alt="" />
                ) : (
                  <div className="w-full h-full flex items-center justify-center text-zinc-300">
                    <Newspaper className="w-6 h-6" />
                  </div>
                )}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-[10px] font-black text-zinc-400 uppercase tracking-widest mb-1">{item.source}</p>
                <p className="font-bold text-sm line-clamp-1 group-hover:text-indigo-500 transition-colors">{item.title}</p>
              </div>
              <ArrowRight className="w-5 h-5 text-zinc-200 group-hover:text-zinc-900 transition-colors" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function StatItem({ label, value, icon }: { label: string, value: string, icon: React.ReactNode }) {
  return (
    <div className="flex justify-between items-center group">
      <div className="flex items-center gap-2">
        <div className="w-6 h-6 rounded-lg bg-zinc-50 dark:bg-zinc-900 flex items-center justify-center text-zinc-400 group-hover:text-zinc-900 dark:group-hover:text-zinc-100 transition-colors">
          {icon}
        </div>
        <span className="text-sm font-medium text-zinc-500">{label}</span>
      </div>
      <span className="font-black text-sm tracking-tight">{value}</span>
    </div>
  );
}

function QuickAction({ title, desc, icon, onClick }: { title: string, desc: string, icon: React.ReactNode, onClick: () => void }) {
  return (
    <button 
      onClick={onClick}
      className="p-6 bg-white dark:bg-zinc-950 rounded-2xl border border-zinc-100 dark:border-zinc-900 text-left hover:shadow-xl hover:-translate-y-1 transition-all group"
    >
      <div className="w-12 h-12 rounded-2xl bg-zinc-50 dark:bg-zinc-900 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
        {React.cloneElement(icon as React.ReactElement<{ className?: string }>, { className: "w-6 h-6" })}
      </div>
      <h4 className="font-black text-sm mb-1">{title}</h4>
      <p className="text-xs text-zinc-500 leading-tight">{desc}</p>
    </button>
  );
}
