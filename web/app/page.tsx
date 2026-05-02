"use client";

import React, { useState, useEffect } from "react";
import { api } from "@/lib/api/api";
import { NewsItem } from "@/types/api";
import { Sidebar } from "@/components/layout/sidebar";
import { NewsFeed } from "@/components/studio/news-feed";
import { ChatInterface } from "@/components/studio/chat-interface";
import { Console } from "@/components/layout/console";
import { HomeDashboard } from "@/components/studio/home-dashboard";
import { HistoryGallery } from "@/components/studio/history-gallery";
import { RagInterface } from "@/components/studio/rag-interface";
import { SettingsPanel } from "@/components/studio/settings-panel";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";
import { CheckCircle2, Settings2, Loader2, Sparkles } from "lucide-react";
import { toast } from "sonner";

export default function MemeStudio() {
  const [activeTab, setActiveTab] = useState("home");
  const [selectedNews, setSelectedNews] = useState<NewsItem | null>(null);
  const [showConsole, setShowConsole] = useState(false);
  
  // Scraper State
  const [isScraping, setIsScraping] = useState(false);
  const [scrapeProgress, setScrapeProgress] = useState<string[]>([]);
  const [pendingNews, setPendingNews] = useState<NewsItem[]>([]);
  const [news, setNews] = useState<NewsItem[]>([]);
  
  // Chat State
  const [messages, setMessages] = useState<{role: string, content: string}[]>([]);
  const [chatInput, setChatInput] = useState("");
  const [isChatLoading, setIsChatLoading] = useState(false);

  // WebSocket for Scraper
  useEffect(() => {
    const ws = new WebSocket("ws://localhost:5000/api/news/ws/scraper");
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.status === "starting") {
        setIsScraping(true);
        setScrapeProgress(["Starting scraper..."]);
        setPendingNews([]);
      } else if (data.status === "progress") {
        setScrapeProgress(prev => [...prev, data.message]);
      } else if (data.status === "pending") {
        setPendingNews(data.items);
      } else if (data.status === "complete") {
        setIsScraping(false);
        setScrapeProgress(prev => [...prev, "✓ Scrape complete!"]);
        fetchNews();
      }
    };
    return () => ws.close();
  }, []);

  const fetchNews = async () => {
    try {
      const res = await api.news.list();
      if (res.status === 1) setNews(res.data.content);
    } catch (e) {
      toast.error("Failed to load news feed");
    }
  };

  useEffect(() => { fetchNews(); }, []);

  const startScraper = async () => {
    try {
      await api.news.refresh();
      toast.info("Scraper started in background");
    } catch (e) {
      toast.error("Failed to start scraper");
    }
  };

  const sendMessage = async () => {
    if (!chatInput.trim() || isChatLoading) return;
    
    const userMsg = { role: "user", content: chatInput };
    setMessages(prev => [...prev, userMsg]);
    setChatInput("");
    setIsChatLoading(true);

    const systemPrompt = selectedNews 
      ? `You are an AI assistant helping to create a meme. Context News: "${selectedNews.title}" Content: "${selectedNews.content || ''}"`
      : "You are a helpful AI assistant.";

    try {
      const res = await api.chat.sendMessage({
        model: "gemma",
        system_prompt: systemPrompt,
        input: chatInput
      });
      if (res.status === 1) {
        setMessages(prev => [...prev, { role: "assistant", content: res.data.response }]);
        if (res.data.response.toLowerCase().includes("generate meme") && selectedNews) {
          generateMeme(selectedNews.news_id);
        }
      }
    } catch (e) {
      toast.error("AI connection lost");
    } finally {
      setIsChatLoading(false);
    }
  };

  const generateMeme = async (newsId: number) => {
    toast.promise(api.meme.generate(newsId), {
      loading: 'ComfyUI is rendering your meme...',
      success: 'Meme generated successfully!',
      error: 'ComfyUI failed to generate image',
    });
  };

  return (
    <div className="min-h-screen bg-[#fafafa] dark:bg-[#050505] flex flex-col font-sans">
      <header className="h-16 border-b border-zinc-100 dark:border-zinc-900 bg-white/80 dark:bg-black/80 backdrop-blur-xl sticky top-0 z-30 px-6 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-zinc-900 dark:bg-white rounded-lg flex items-center justify-center">
            <Sparkles className="w-4 h-4 text-white dark:text-zinc-900" />
          </div>
          <h1 className="font-bold text-lg tracking-tight">MemeStudio</h1>
        </div>
        <div className="flex items-center gap-4">
          {selectedNews && (
            <Badge variant="secondary" className="gap-2 px-3 py-1 bg-emerald-50 text-emerald-700 animate-in fade-in zoom-in border-emerald-100">
              <CheckCircle2 className="w-3 h-3" /> {selectedNews.title.slice(0, 30)}...
            </Badge>
          )}
          <Button variant="outline" size="sm" className="rounded-xl border-zinc-200 dark:border-zinc-800" onClick={() => setActiveTab('settings')}>
            <Settings2 className="w-4 h-4" />
          </Button>
        </div>
      </header>

      <main className="flex-1 flex overflow-hidden">
        <Sidebar 
          activeTab={activeTab} 
          setActiveTab={setActiveTab} 
          isScraping={isScraping} 
          onRefresh={startScraper} 
          showConsole={showConsole}
          setShowConsole={setShowConsole}
        />

        <div className="flex-1 overflow-hidden relative flex flex-col">
          {isScraping && (
            <div className="absolute top-4 left-4 right-4 z-20 animate-in slide-in-from-top-4">
              <Card className="bg-zinc-900/90 text-zinc-100 border-none backdrop-blur shadow-2xl">
                <CardContent className="p-4 flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <Loader2 className="animate-spin text-emerald-400" />
                    <div>
                      <p className="text-sm font-medium">Scraping...</p>
                      <p className="text-xs text-zinc-400">{scrapeProgress[scrapeProgress.length - 1]}</p>
                    </div>
                  </div>
                  {pendingNews.length > 0 && <Badge className="bg-emerald-500/20 text-emerald-400">{pendingNews.length} Found</Badge>}
                </CardContent>
              </Card>
            </div>
          )}

          <ScrollArea className="flex-1 p-8">
            <div className="max-w-6xl mx-auto">
              {activeTab === 'home' && <HomeDashboard news={news} onNavigate={setActiveTab} />}
              
              {activeTab === 'news' && (
                <NewsFeed 
                  news={news} 
                  pendingNews={pendingNews} 
                  selectedNews={selectedNews}
                  onSelect={(item) => { setSelectedNews(item); setActiveTab('chat'); }}
                  onGenerateMeme={generateMeme}
                />
              )}

              {activeTab === 'chat' && (
                <ChatInterface 
                  messages={messages}
                  input={chatInput}
                  setInput={setChatInput}
                  isLoading={isChatLoading}
                  onSendMessage={sendMessage}
                  selectedNews={selectedNews}
                  onGenerateMeme={generateMeme}
                />
              )}

              {activeTab === 'history' && <HistoryGallery />}

              {activeTab === 'rag' && <RagInterface />}

              {activeTab === 'settings' && <SettingsPanel />}
            </div>
          </ScrollArea>
          
          <Console isOpen={showConsole} onClose={() => setShowConsole(false)} />
        </div>
      </main>
    </div>
  );
}


