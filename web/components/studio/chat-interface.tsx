"use client";

import React from "react";
import { NewsItem } from "@/types/api";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Bot, User, Send, Image as ImageIcon } from "lucide-react";

interface ChatInterfaceProps {
  messages: { role: string; content: string }[];
  input: string;
  setInput: (val: string) => void;
  isLoading: boolean;
  onSendMessage: () => void;
  selectedNews: NewsItem | null;
  onGenerateMeme: (id: number) => void;
}

export function ChatInterface({ 
  messages, input, setInput, isLoading, onSendMessage, selectedNews, onGenerateMeme 
}: ChatInterfaceProps) {
  return (
    <div className="max-w-3xl mx-auto h-[75vh] flex flex-col animate-in fade-in duration-500">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Studio Chat</h2>
          <p className="text-sm text-zinc-500">
            {selectedNews ? `Chatting about: ${selectedNews.source}` : "Select news from the feed to get started."}
          </p>
        </div>
        {selectedNews && (
          <Button variant="outline" className="rounded-xl gap-2" onClick={() => onGenerateMeme(selectedNews.news_id)}>
            <ImageIcon className="w-4 h-4" /> Generate Meme
          </Button>
        )}
      </div>
      
      <Card className="flex-1 flex flex-col bg-white dark:bg-zinc-900/50 border-zinc-100 dark:border-zinc-800 shadow-xl rounded-3xl overflow-hidden">
        <ScrollArea className="flex-1 p-6">
          <div className="space-y-6">
            {messages.length === 0 && (
              <div className="text-center py-20 space-y-4">
                <Bot className="w-12 h-12 mx-auto text-zinc-200" />
                <p className="text-zinc-400">Discuss the news and I'll help you craft the perfect meme.</p>
              </div>
            )}
            {messages.map((m, i) => (
              <div key={i} className={`flex items-start gap-4 ${m.role === 'user' ? 'flex-row-reverse' : ''}`}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${m.role === 'user' ? 'bg-zinc-100 dark:bg-zinc-800' : 'bg-zinc-900 dark:bg-zinc-100'}`}>
                  {m.role === 'user' ? <User className="w-4 h-4 text-zinc-600" /> : <Bot className="w-4 h-4 text-zinc-100 dark:text-zinc-900" />}
                </div>
                <div className={`max-w-[80%] px-4 py-3 rounded-2xl text-sm leading-relaxed ${
                  m.role === 'user' 
                  ? 'bg-zinc-900 text-white dark:bg-zinc-100 dark:text-zinc-900 rounded-tr-none' 
                  : 'bg-zinc-100 text-zinc-900 dark:bg-zinc-800 dark:text-zinc-100 rounded-tl-none'
                }`}>
                  {m.content}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex items-start gap-4">
                <div className="w-8 h-8 rounded-full bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center shrink-0">
                  <Bot className="w-4 h-4 text-zinc-100 dark:text-zinc-900" />
                </div>
                <div className="bg-zinc-100 dark:bg-zinc-800 rounded-2xl rounded-tl-none px-4 py-2 flex gap-1">
                  <span className="w-1 h-1 bg-zinc-400 rounded-full animate-bounce" />
                  <span className="w-1 h-1 bg-zinc-400 rounded-full animate-bounce [animation-delay:0.2s]" />
                  <span className="w-1 h-1 bg-zinc-400 rounded-full animate-bounce [animation-delay:0.4s]" />
                </div>
              </div>
            )}
          </div>
        </ScrollArea>
        <CardFooter className="p-4 border-t border-zinc-100 dark:border-zinc-800">
          <div className="relative w-full flex items-center gap-2">
            <Input 
              value={input} 
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && onSendMessage()}
              placeholder="Type your message..." 
              className="flex-1 h-12 rounded-2xl bg-zinc-50 dark:bg-zinc-950 border-none focus-visible:ring-1 focus-visible:ring-zinc-300"
            />
            <Button onClick={onSendMessage} disabled={isLoading || !input.trim()} className="rounded-xl h-12 px-6">
              <Send className="w-4 h-4" />
            </Button>
          </div>
        </CardFooter>
      </Card>
    </div>
  );
}
