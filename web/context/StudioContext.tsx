"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { NewsItem } from "@/types/api";
import { api } from "@/lib/api/api";
import { toast } from "sonner";

interface StudioContextType {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  selectedNews: NewsItem | null;
  setSelectedNews: (news: NewsItem | null) => void;
  news: NewsItem[];
  fetchNews: (page?: number, size?: number) => void;
  isScraping: boolean;
  startScraper: () => void;
  messages: { role: string; content: string }[];
  setMessages: React.Dispatch<React.SetStateAction<{ role: string; content: string }[]>>;
  chatInput: string;
  setChatInput: (val: string) => void;
  isChatLoading: boolean;
  sendMessage: () => void;
  generateMeme: (id: number) => void;
  showConsole: boolean;
  setShowConsole: (val: boolean) => void;
  selectedModel: string;
  setSelectedModel: (val: string) => void;
  availableModels: string[];
  scrapeProgress: string[];
  pendingNews: NewsItem[];
  currentPage: number;
  pageSize: number;
  totalPages: number;
}

const StudioContext = createContext<StudioContextType | undefined>(undefined);

export function StudioProvider({ children }: { children: React.ReactNode }) {
  const [activeTab, setActiveTab] = useState("home");
  const [selectedNews, setSelectedNews] = useState<NewsItem | null>(null);
  const [news, setNews] = useState<NewsItem[]>([]);
  const [isScraping, setIsScraping] = useState(false);
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
  const [chatInput, setChatInput] = useState("");
  const [isChatLoading, setIsChatLoading] = useState(false);
  const [showConsole, setShowConsole] = useState(false);
  const [selectedModel, setSelectedModel] = useState("google/gemma-4-e4b");
  const [availableModels, setAvailableModels] = useState<string[]>([]);
  const [scrapeProgress, setScrapeProgress] = useState<string[]>([]);
  const [pendingNews, setPendingNews] = useState<NewsItem[]>([]);
  
  const [currentPage, setCurrentPage] = useState(0);
  const [pageSize, setPageSize] = useState(12);
  const [totalPages, setTotalPages] = useState(0);

  const fetchNews = async (page = currentPage, size = pageSize) => {
    try {
      const res = await api.news.list(page, size);
      if (res.status === 1) {
        setNews(res.data.content);
        setTotalPages(Math.ceil(res.data.totalElements / size));
        setCurrentPage(page);
        setPageSize(size);
      }
    } catch (e) {
      toast.error("Failed to load news feed");
    }
  };

  const fetchModels = async () => {
    try {
      const res = await api.system.listModels();
      if (res.status === 1) {
        setAvailableModels(res.data.models);
        if (res.data.models.length > 0 && !res.data.models.includes(selectedModel)) {
          setSelectedModel(res.data.models[0]);
        }
      }
    } catch (e) {
      console.error("Failed to fetch models");
    }
  };

  useEffect(() => {
    fetchNews();
    fetchModels();
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
        model: selectedModel,
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
    <StudioContext.Provider value={{
      activeTab, setActiveTab, selectedNews, setSelectedNews, news, fetchNews,
      isScraping, startScraper, messages, setMessages, chatInput, setChatInput,
      isChatLoading, sendMessage, generateMeme, showConsole, setShowConsole,
      selectedModel, setSelectedModel, availableModels, scrapeProgress, pendingNews,
      currentPage, pageSize, totalPages
    }}>
      {children}
    </StudioContext.Provider>
  );
}

export function useStudio() {
  const context = useContext(StudioContext);
  if (context === undefined) {
    throw new Error("useStudio must be used within a StudioProvider");
  }
  return context;
}
