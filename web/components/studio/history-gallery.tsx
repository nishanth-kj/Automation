"use client";

import React from "react";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { 
  History as HistoryIcon, 
  Download, 
  Share2, 
  Trash2, 
  Eye,
  Filter,
  Search
} from "lucide-react";
import { Input } from "@/components/ui/input";

export function HistoryGallery() {
  const mockMemes = [1, 2, 3, 4, 5, 6];

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-3xl font-black tracking-tight">Generation History</h2>
          <p className="text-sm text-zinc-500 font-medium">Your collection of AI-generated memes and content.</p>
        </div>
        <div className="flex items-center gap-2">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-400" />
            <Input placeholder="Search memes..." className="pl-9 w-64 h-10 bg-white dark:bg-zinc-950 border-zinc-100 dark:border-zinc-900 rounded-xl" />
          </div>
          <Button variant="outline" size="icon" className="rounded-xl h-10 w-10 border-zinc-100 dark:border-zinc-900">
            <Filter className="w-4 h-4" />
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {mockMemes.map((m) => (
          <Card key={m} className="group overflow-hidden border-zinc-100 dark:border-zinc-900 shadow-sm hover:shadow-xl transition-all duration-500 rounded-2xl bg-white dark:bg-zinc-950">
            <div className="aspect-square relative overflow-hidden bg-zinc-100 dark:bg-zinc-900">
              <div className="absolute inset-0 flex items-center justify-center opacity-20 group-hover:opacity-40 transition-opacity">
                 <HistoryIcon className="w-12 h-12" />
              </div>
              <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2">
                <Button size="sm" variant="secondary" className="rounded-lg h-9 w-9 p-0 bg-white/20 backdrop-blur-md border-white/10 hover:bg-white/40">
                  <Eye className="w-4 h-4 text-white" />
                </Button>
                <Button size="sm" variant="secondary" className="rounded-lg h-9 w-9 p-0 bg-white/20 backdrop-blur-md border-white/10 hover:bg-white/40">
                  <Download className="w-4 h-4 text-white" />
                </Button>
                <Button size="sm" variant="secondary" className="rounded-lg h-9 w-9 p-0 bg-white/20 backdrop-blur-md border-white/10 hover:bg-white/40">
                  <Share2 className="w-4 h-4 text-white" />
                </Button>
              </div>
              <Badge className="absolute top-3 left-3 bg-white/90 dark:bg-zinc-900/90 backdrop-blur text-zinc-900 dark:text-zinc-100 border-none text-[9px] font-black tracking-widest">
                MEME #{1024 + m}
              </Badge>
            </div>
            <CardContent className="p-4">
              <p className="font-bold text-xs text-zinc-400 uppercase tracking-tighter mb-1">Generated 2h ago</p>
              <p className="font-bold text-sm line-clamp-1">AI Regulation Headline Meme</p>
            </CardContent>
            <CardFooter className="p-4 pt-0 flex justify-between items-center">
              <Badge variant="outline" className="text-[9px] bg-zinc-50 dark:bg-zinc-900 border-zinc-100 dark:border-zinc-800">
                Gemma-7b
              </Badge>
              <button className="text-zinc-400 hover:text-rose-500 transition-colors">
                <Trash2 className="w-4 h-4" />
              </button>
            </CardFooter>
          </Card>
        ))}
      </div>

      {mockMemes.length === 0 && (
        <div className="py-20 text-center space-y-4">
          <div className="w-16 h-16 bg-zinc-100 dark:bg-zinc-900 rounded-full flex items-center justify-center mx-auto text-zinc-300">
            <HistoryIcon className="w-8 h-8" />
          </div>
          <div className="space-y-1">
            <p className="font-bold">No generations yet</p>
            <p className="text-sm text-zinc-500">Start creating memes from the news feed to see them here.</p>
          </div>
          <Button className="rounded-xl px-8" variant="outline">Browse News</Button>
        </div>
      )}
    </div>
  );
}
