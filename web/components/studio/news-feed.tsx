"use client";

import React from "react";
import { NewsItem } from "@/types/api";
import { Card, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ExternalLink, Wand2, Image as ImageIcon, CheckCircle2 } from "lucide-react";

interface NewsFeedProps {
  news: NewsItem[];
  pendingNews: NewsItem[];
  selectedNews: NewsItem | null;
  onSelect: (item: NewsItem) => void;
  onGenerateMeme: (id: number) => void;
}

export function NewsFeed({ news, pendingNews, selectedNews, onSelect, onGenerateMeme }: NewsFeedProps) {
  return (
    <div className="animate-in fade-in duration-500 space-y-8">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Discover News</h2>
        <p className="text-zinc-500">Select a story to start creating your meme.</p>
      </div>

      {pendingNews.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-pulse">
          {pendingNews.map((item, i) => (
            <NewsCard key={`pending-${i}`} item={item} isPending />
          ))}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {news.map(item => (
          <NewsCard 
            key={item.news_id} 
            item={item} 
            isSelected={selectedNews?.news_id === item.news_id}
            onSelect={() => onSelect(item)}
            onGenerateMeme={() => onGenerateMeme(item.news_id)}
          />
        ))}
      </div>
    </div>
  );
}

function NewsCard({ item, isSelected, onSelect, onGenerateMeme, isPending }: { 
  item: NewsItem, 
  isSelected?: boolean, 
  onSelect?: () => void, 
  onGenerateMeme?: () => void,
  isPending?: boolean
}) {
  return (
    <Card className={`group overflow-hidden border-zinc-100 dark:border-zinc-800 shadow-sm transition-all duration-300 ${isSelected ? 'ring-2 ring-zinc-900 dark:ring-zinc-100 scale-[1.02]' : 'hover:scale-[1.01] hover:shadow-md'} ${isPending ? 'opacity-50 grayscale' : ''}`}>
      {item.image_url && (
        <div className="h-44 overflow-hidden relative">
          <img src={item.image_url} alt={item.title} className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" />
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-4">
             <Button size="sm" variant="secondary" className="w-full rounded-lg gap-2" onClick={(e) => { e.stopPropagation(); onGenerateMeme?.(); }}>
              <ImageIcon className="w-3 h-3" /> Quick Meme
            </Button>
          </div>
        </div>
      )}
      <CardHeader className="p-5">
        <div className="flex justify-between items-start gap-2 mb-2">
          <Badge variant="outline" className="text-[10px] uppercase tracking-wider bg-zinc-50 dark:bg-zinc-900">{item.source}</Badge>
          <div className="flex gap-2">
            <a href={item.url} target="_blank" rel="noreferrer" className="text-zinc-400 hover:text-zinc-900">
              <ExternalLink className="w-4 h-4" />
            </a>
          </div>
        </div>
        <CardTitle className="text-base font-semibold leading-tight mb-2 group-hover:text-zinc-600 dark:group-hover:text-zinc-300 transition-colors">{item.title}</CardTitle>
      </CardHeader>
      <CardFooter className="p-5 pt-0">
        <Button 
          variant={isSelected ? "default" : "outline"} 
          className="w-full rounded-xl gap-2 font-medium"
          onClick={onSelect}
          disabled={isPending}
        >
          {isSelected ? <CheckCircle2 className="w-4 h-4" /> : <Wand2 className="w-4 h-4" />}
          {isSelected ? "Selected" : "Select Story"}
        </Button>
      </CardFooter>
    </Card>
  );
}
