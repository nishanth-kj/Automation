"use client";

import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { 
  TrendingUp, 
  Clock, 
  ShieldCheck, 
  ArrowRight,
  Newspaper
} from "lucide-react";
import { NewsItem } from "@/types/api";

interface HomeDashboardProps {
  news: NewsItem[];
  onNavigate: (tab: string) => void;
}

export function HomeDashboard({ news, onNavigate }: HomeDashboardProps) {
  return (
    <div className="space-y-6">
      <div className="border-b pb-4">
        <h2 className="text-2xl font-semibold tracking-tight">Dashboard</h2>
        <p className="text-sm text-muted-foreground text-zinc-500">Overview of your meme studio activity.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="shadow-none border-zinc-200">
          <CardHeader className="p-4">
            <CardTitle className="text-sm font-medium">News Items</CardTitle>
          </CardHeader>
          <CardContent className="p-4 pt-0">
            <div className="text-2xl font-bold">{news.length}</div>
          </CardContent>
        </Card>
        <Card className="shadow-none border-zinc-200">
          <CardHeader className="p-4">
            <CardTitle className="text-sm font-medium">Generations</CardTitle>
          </CardHeader>
          <CardContent className="p-4 pt-0">
            <div className="text-2xl font-bold">128</div>
          </CardContent>
        </Card>
        <Card className="shadow-none border-zinc-200">
          <CardHeader className="p-4">
            <CardTitle className="text-sm font-medium">Status</CardTitle>
          </CardHeader>
          <CardContent className="p-4 pt-0">
            <div className="text-sm text-emerald-600 font-medium">System Online</div>
          </CardContent>
        </Card>
      </div>

      <div className="space-y-2">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-zinc-400">Quick Links</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          <button onClick={() => onNavigate('news')} className="flex items-center justify-between p-4 border rounded-lg hover:bg-zinc-50 text-left transition-colors">
            <div className="flex items-center gap-3">
              <Newspaper className="w-5 h-5" />
              <span className="font-medium">Browse News Feed</span>
            </div>
            <ArrowRight className="w-4 h-4" />
          </button>
          <button onClick={() => onNavigate('history')} className="flex items-center justify-between p-4 border rounded-lg hover:bg-zinc-50 text-left transition-colors">
            <div className="flex items-center gap-3">
              <Clock className="w-5 h-5" />
              <span className="font-medium">View History</span>
            </div>
            <ArrowRight className="w-4 h-4" />
          </button>
          <button onClick={() => onNavigate('rag')} className="flex items-center justify-between p-4 border rounded-lg hover:bg-zinc-50 text-left transition-colors">
            <div className="flex items-center gap-3">
              <ShieldCheck className="w-5 h-5" />
              <span className="font-medium">Knowledge Base</span>
            </div>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
