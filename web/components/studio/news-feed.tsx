"use client";

import React from "react";
import { NewsItem } from "@/types/api";
import { Card, CardHeader, CardTitle, CardFooter, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { 
  ExternalLink, 
  Wand2, 
  ImageIcon, 
  CheckCircle2, 
  Calendar,
  Globe,
  ChevronLeft,
  ChevronRight,
  MoreHorizontal
} from "lucide-react";
import { cn } from "@/lib/utils";
import { 
  Pagination, 
  PaginationContent, 
  PaginationItem, 
  PaginationLink, 
  PaginationNext, 
  PaginationPrevious,
  PaginationEllipsis
} from "@/components/ui/pagination";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useStudio } from "@/context/StudioContext";

export function NewsFeed() {
  const { 
    news, 
    pendingNews, 
    selectedNews, 
    setSelectedNews, 
    generateMeme,
    currentPage,
    pageSize,
    totalPages,
    fetchNews
  } = useStudio() as any; 

  const handlePageChange = (page: number) => {
    if (page >= 0 && page < totalPages) {
      fetchNews(page, pageSize);
    }
  };

  const onSelect = (item: any) => {
    setSelectedNews(item);
  };

  return (
    <div className="animate-in fade-in duration-500 space-y-6 max-w-4xl mx-auto">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b pb-6">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">News Feed</h2>
          <p className="text-sm text-zinc-500">Transform trending stories into viral content.</p>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-xs font-medium text-zinc-400">Show:</span>
          <Select 
            value={pageSize.toString()} 
            onValueChange={(val) => fetchNews(0, parseInt(val))}
          >
            <SelectTrigger className="w-20 h-9 rounded-lg">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="10">10</SelectItem>
              <SelectItem value="20">20</SelectItem>
              <SelectItem value="50">50</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      <div className="space-y-4">
        {pendingNews.length > 0 && (
          <div className="space-y-4 opacity-50 animate-pulse">
            {pendingNews.map((item: any, i: number) => (
              <NewsListItem key={`pending-${i}`} item={item} isPending />
            ))}
          </div>
        )}

        {news.length === 0 && !pendingNews.length && (
          <div className="py-20 text-center border-2 border-dashed rounded-3xl border-zinc-100">
             <p className="text-zinc-400 font-medium">No news stories found. Try refreshing.</p>
          </div>
        )}

        {news.map((item: any) => (
          <NewsListItem 
            key={item.news_id} 
            item={item} 
            isSelected={selectedNews?.news_id === item.news_id}
            onSelect={() => onSelect(item)}
            onGenerateMeme={() => generateMeme(item.news_id)}
          />
        ))}
      </div>

      {totalPages > 1 && (
        <div className="pt-6 border-t">
          <Pagination>
            <PaginationContent>
              <PaginationItem>
                <PaginationPrevious 
                  onClick={() => handlePageChange(currentPage - 1)}
                  className={currentPage === 0 ? "pointer-events-none opacity-50" : "cursor-pointer"}
                />
              </PaginationItem>
              
              {/* Simple pagination logic */}
              {Array.from({ length: totalPages }).map((_, i) => {
                if (i === 0 || i === totalPages - 1 || (i >= currentPage - 1 && i <= currentPage + 1)) {
                  return (
                    <PaginationItem key={i}>
                      <PaginationLink 
                        isActive={currentPage === i}
                        onClick={() => handlePageChange(i)}
                        className="cursor-pointer"
                      >
                        {i + 1}
                      </PaginationLink>
                    </PaginationItem>
                  );
                } else if (i === currentPage - 2 || i === currentPage + 2) {
                  return <PaginationEllipsis key={i} />;
                }
                return null;
              })}

              <PaginationItem>
                <PaginationNext 
                  onClick={() => handlePageChange(currentPage + 1)}
                  className={currentPage === totalPages - 1 ? "pointer-events-none opacity-50" : "cursor-pointer"}
                />
              </PaginationItem>
            </PaginationContent>
          </Pagination>
        </div>
      )}
    </div>
  );
}

function NewsListItem({ item, isSelected, onSelect, onGenerateMeme, isPending }: any) {
  return (
    <Card 
      className={cn(
        "group flex flex-col md:flex-row overflow-hidden border-zinc-200/60 shadow-none hover:border-zinc-300 transition-all cursor-pointer rounded-2xl",
        isSelected && "border-zinc-950 ring-1 ring-zinc-950",
        isPending && "pointer-events-none opacity-60"
      )}
      onClick={onSelect}
    >
      <div className="w-full md:w-48 h-32 md:h-auto overflow-hidden relative shrink-0">
        {item.image_url ? (
          <img 
            src={item.image_url} 
            alt="" 
            className="w-full h-full object-cover grayscale-[0.5] group-hover:grayscale-0 transition-all duration-500" 
          />
        ) : (
          <div className="w-full h-full bg-zinc-50 flex items-center justify-center">
            <ImageIcon className="w-8 h-8 text-zinc-200" />
          </div>
        )}
      </div>

      <div className="flex-1 p-5 flex flex-col justify-between">
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <Badge variant="outline" className="text-[10px] font-bold uppercase tracking-widest text-zinc-500 border-zinc-200">
              {item.source}
            </Badge>
            <span className="text-[10px] text-zinc-400 font-medium">
              {new Date(item.created_at * 1000).toLocaleDateString()}
            </span>
          </div>
          <CardTitle className="text-lg font-bold leading-tight group-hover:text-zinc-900 transition-colors">
            {item.title}
          </CardTitle>
          <p className="text-xs text-zinc-500 line-clamp-1">{item.content}</p>
        </div>

        <div className="flex items-center justify-between mt-4">
          <div className="flex items-center gap-3">
             <Button 
                size="sm" 
                variant={isSelected ? "default" : "outline"}
                className="h-8 rounded-lg gap-2 text-xs font-bold"
              >
                {isSelected ? <CheckCircle2 className="w-3.5 h-3.5" /> : <Wand2 className="w-3.5 h-3.5" />}
                {isSelected ? "Selected" : "Select Story"}
              </Button>
              <Button 
                size="sm" 
                variant="ghost" 
                className="h-8 w-8 p-0"
                onClick={(e) => { e.stopPropagation(); onGenerateMeme(); }}
              >
                <ImageIcon className="w-4 h-4 text-zinc-400" />
              </Button>
          </div>
          <a 
            href={item.url} 
            target="_blank" 
            rel="noreferrer" 
            className="text-zinc-400 hover:text-zinc-900 transition-colors"
            onClick={(e) => e.stopPropagation()}
          >
            <ExternalLink className="w-4 h-4" />
          </a>
        </div>
      </div>
    </Card>
  );
}
