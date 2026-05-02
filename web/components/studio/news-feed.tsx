import React, { useState } from "react";
import { NewsItem } from "@/types/api";
import { Card, CardHeader, CardTitle, CardFooter, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { 
  ExternalLink, 
  Wand2, 
  Image as ImageIcon, 
  CheckCircle2, 
  LayoutGrid, 
  List,
  Calendar,
  Globe
} from "lucide-react";
import { cn } from "@/lib/utils";

interface NewsFeedProps {
  news: NewsItem[];
  pendingNews: NewsItem[];
  selectedNews: NewsItem | null;
  onSelect: (item: NewsItem) => void;
  onGenerateMeme: (id: number) => void;
}

export function NewsFeed({ news, pendingNews, selectedNews, onSelect, onGenerateMeme }: NewsFeedProps) {
  const [viewMode, setViewMode] = useState<"grid" | "table">("grid");

  return (
    <div className="animate-in fade-in duration-700 space-y-8">
      <div className="flex items-end justify-between">
        <div className="space-y-1">
          <h2 className="text-4xl font-black tracking-tight text-zinc-900 dark:text-white">Discover News</h2>
          <p className="text-zinc-500 font-medium">Select a trending story to transform into a viral meme.</p>
        </div>
        <div className="flex bg-zinc-100 dark:bg-zinc-900 p-1 rounded-xl border border-zinc-200 dark:border-zinc-800">
          <Button 
            variant={viewMode === "grid" ? "secondary" : "ghost"} 
            size="sm" 
            className={cn("rounded-lg h-8 w-8 p-0", viewMode === "grid" && "bg-white dark:bg-zinc-800 shadow-sm")}
            onClick={() => setViewMode("grid")}
          >
            <LayoutGrid className="w-4 h-4" />
          </Button>
          <Button 
            variant={viewMode === "table" ? "secondary" : "ghost"} 
            size="sm" 
            className={cn("rounded-lg h-8 w-8 p-0", viewMode === "table" && "bg-white dark:bg-zinc-800 shadow-sm")}
            onClick={() => setViewMode("table")}
          >
            <List className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {pendingNews.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-pulse opacity-60">
          {pendingNews.map((item, i) => (
            <NewsCard key={`pending-${i}`} item={item} isPending />
          ))}
        </div>
      )}

      {viewMode === "grid" ? (
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
      ) : (
        <Card className="border-zinc-100 dark:border-zinc-800 overflow-hidden rounded-2xl shadow-sm bg-white dark:bg-zinc-950">
          <Table>
            <TableHeader className="bg-zinc-50/50 dark:bg-zinc-900/50">
              <TableRow className="hover:bg-transparent border-zinc-100 dark:border-zinc-800">
                <TableHead className="w-[400px]">Headline</TableHead>
                <TableHead>Source</TableHead>
                <TableHead>Category</TableHead>
                <TableHead className="text-right">Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {news.map((item) => (
                <TableRow 
                  key={item.news_id} 
                  className={cn(
                    "cursor-pointer transition-colors border-zinc-100 dark:border-zinc-800",
                    selectedNews?.news_id === item.news_id ? "bg-zinc-50 dark:bg-zinc-900/50" : "hover:bg-zinc-50/50 dark:hover:bg-zinc-900/30"
                  )}
                  onClick={() => onSelect(item)}
                >
                  <TableCell className="font-semibold text-zinc-900 dark:text-zinc-100 py-4">
                    <div className="flex items-center gap-3">
                      {item.image_url && (
                        <img src={item.image_url} className="w-10 h-10 rounded-lg object-cover bg-zinc-100" alt="" />
                      )}
                      <span className="line-clamp-1">{item.title}</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant="outline" className="font-medium bg-zinc-50 dark:bg-zinc-900 border-zinc-200 dark:border-zinc-800">
                      {item.source}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-zinc-500 capitalize">{item.category}</TableCell>
                  <TableCell className="text-right">
                    <Button 
                      size="sm" 
                      variant={selectedNews?.news_id === item.news_id ? "default" : "outline"}
                      className="rounded-lg h-8 gap-2"
                    >
                      {selectedNews?.news_id === item.news_id ? <CheckCircle2 className="w-3 h-3" /> : <Wand2 className="w-3 h-3" />}
                      {selectedNews?.news_id === item.news_id ? "Selected" : "Select"}
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>
      )}
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
    <Card 
      className={cn(
        "group overflow-hidden border-zinc-200/60 dark:border-zinc-800/60 shadow-sm transition-all duration-500 relative flex flex-col",
        "hover:shadow-2xl hover:shadow-zinc-200/50 dark:hover:shadow-black/50 hover:-translate-y-1",
        isSelected ? "ring-2 ring-zinc-950 dark:ring-zinc-200 ring-offset-2 dark:ring-offset-black" : "",
        isPending && "opacity-50 grayscale pointer-events-none"
      )}
      onClick={onSelect}
    >
      <div className="h-52 overflow-hidden relative">
        {item.image_url ? (
          <img 
            src={item.image_url} 
            alt={item.title} 
            className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" 
          />
        ) : (
          <div className="w-full h-full bg-zinc-100 dark:bg-zinc-900 flex items-center justify-center">
            <ImageIcon className="w-10 h-10 text-zinc-300" />
          </div>
        )}
        
        <div className="absolute top-3 left-3 flex gap-2">
          <Badge className="bg-black/60 backdrop-blur-md border-none text-white text-[10px] uppercase font-bold tracking-widest px-2 py-0.5">
            {item.source}
          </Badge>
        </div>

        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 flex items-end p-4">
           <Button 
            size="sm" 
            variant="secondary" 
            className="w-full rounded-xl gap-2 font-bold backdrop-blur-xl bg-white/20 hover:bg-white/40 text-white border-white/20" 
            onClick={(e) => { e.stopPropagation(); onGenerateMeme?.(); }}
          >
            <ImageIcon className="w-4 h-4" /> Quick Meme
          </Button>
        </div>
      </div>

      <CardHeader className="p-5 flex-1">
        <div className="flex items-center gap-2 mb-3">
          <div className="flex items-center gap-1 text-[10px] font-bold text-zinc-400 uppercase tracking-tighter">
            <Calendar className="w-3 h-3" />
            {new Date(item.created_at * 1000).toLocaleDateString()}
          </div>
          <span className="w-1 h-1 rounded-full bg-zinc-200" />
          <div className="flex items-center gap-1 text-[10px] font-bold text-zinc-400 uppercase tracking-tighter">
            <Globe className="w-3 h-3" />
            {item.category}
          </div>
        </div>
        <CardTitle className="text-lg font-bold leading-tight line-clamp-2 group-hover:text-zinc-600 dark:group-hover:text-zinc-300 transition-colors">
          {item.title}
        </CardTitle>
      </CardHeader>

      <CardFooter className="p-5 pt-0 mt-auto">
        <div className="flex gap-2 w-full">
          <Button 
            variant={isSelected ? "default" : "outline"} 
            className={cn(
              "flex-1 rounded-xl gap-2 font-bold transition-all",
              isSelected ? "bg-zinc-900 dark:bg-white text-white dark:text-zinc-900" : "hover:bg-zinc-50 dark:hover:bg-zinc-900"
            )}
            onClick={(e) => { e.stopPropagation(); onSelect?.(); }}
          >
            {isSelected ? <CheckCircle2 className="w-4 h-4" /> : <Wand2 className="w-4 h-4" />}
            {isSelected ? "Selected" : "Select Story"}
          </Button>
          <a 
            href={item.url} 
            target="_blank" 
            rel="noreferrer" 
            className="h-10 w-10 flex items-center justify-center rounded-xl border border-zinc-200 dark:border-zinc-800 text-zinc-400 hover:text-zinc-900 dark:hover:text-white hover:bg-zinc-50 dark:hover:bg-zinc-900 transition-all"
            onClick={(e) => e.stopPropagation()}
          >
            <ExternalLink className="w-4 h-4" />
          </a>
        </div>
      </CardFooter>
    </Card>
  );
}

