"use client";

import { useState, useRef, useEffect } from "react";
import { api } from "@/lib/api/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Send, Bot, User, Sparkles } from "lucide-react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      const scrollContainer = scrollRef.current.querySelector('[data-radix-scroll-area-viewport]');
      if (scrollContainer) {
        scrollContainer.scrollTop = scrollContainer.scrollHeight;
      }
    }
  }, [messages, isLoading]);

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const data = await api.chat.sendMessage({
        model: "google/gemma-4-e4b",
        system_prompt: "You answer only in rhymes.",
        input: input,
      });

      if (data.status === 1) {
        setMessages((prev) => [...prev, { role: "assistant", content: data.data.response }]);
      } else {
        throw new Error(data.error?.message || "AI Error");
      }
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) => [...prev, { role: "assistant", content: "Oops! Something went wrong while connecting to the AI." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-[#fafafa] dark:bg-[#050505] p-4 md:p-8 font-sans">
      <Card className="w-full max-w-3xl h-[85vh] flex flex-col shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-[0_8px_30px_rgb(0,0,0,0.2)] border-zinc-200/50 dark:border-zinc-800/50 bg-white/80 dark:bg-zinc-900/80 backdrop-blur-xl overflow-hidden rounded-[2rem]">
        <CardHeader className="border-b border-zinc-100/50 dark:border-zinc-800/50 py-4 px-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center">
                <Bot className="w-6 h-6 text-zinc-100 dark:text-zinc-900" />
              </div>
              <div>
                <CardTitle className="text-lg font-semibold tracking-tight">Gemma AI</CardTitle>
                <p className="text-xs text-zinc-500 dark:text-zinc-400 flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-emerald-500" />
                  Online & Ready to Rhyme
                </p>
              </div>
            </div>
            <Sparkles className="w-5 h-5 text-zinc-400" />
          </div>
        </CardHeader>
        
        <CardContent className="flex-1 overflow-hidden p-0">
          <ScrollArea ref={scrollRef} className="h-full px-6 py-6">
            <div className="space-y-6 max-w-2xl mx-auto">
              {messages.length === 0 && (
                <div className="flex flex-col items-center justify-center h-[50vh] text-center space-y-4">
                  <div className="p-4 rounded-full bg-zinc-50 dark:bg-zinc-800/50">
                    <Bot className="w-12 h-12 text-zinc-300" />
                  </div>
                  <div className="space-y-2">
                    <h3 className="text-xl font-medium text-zinc-900 dark:text-zinc-100">Welcome to Gemma Chat</h3>
                    <p className="text-sm text-zinc-500 dark:text-zinc-400 max-w-[280px]">
                      Ask me anything, and I'll respond in poetic rhymes.
                    </p>
                  </div>
                </div>
              )}
              
              {messages.map((m, i) => (
                <div 
                  key={i} 
                  className={`flex items-start gap-3 ${m.role === "user" ? "flex-row-reverse" : "flex-row"} animate-in fade-in slide-in-from-bottom-2 duration-300`}
                >
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${m.role === "user" ? "bg-zinc-100 dark:bg-zinc-800" : "bg-zinc-900 dark:bg-zinc-100"}`}>
                    {m.role === "user" ? <User className="w-4 h-4 text-zinc-600 dark:text-zinc-300" /> : <Bot className="w-4 h-4 text-zinc-100 dark:text-zinc-900" />}
                  </div>
                  <div className={`group relative max-w-[85%] sm:max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                    m.role === "user" 
                      ? "bg-zinc-900 text-zinc-50 dark:bg-zinc-100 dark:text-zinc-900 rounded-tr-none" 
                      : "bg-zinc-100 text-zinc-900 dark:bg-zinc-800 dark:text-zinc-50 rounded-tl-none border border-zinc-200/50 dark:border-zinc-700/50"
                  }`}>
                    {m.content}
                  </div>
                </div>
              ))}
              
              {isLoading && (
                <div className="flex items-start gap-3 animate-in fade-in duration-300">
                  <div className="w-8 h-8 rounded-full bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center shrink-0">
                    <Bot className="w-4 h-4 text-zinc-100 dark:text-zinc-900" />
                  </div>
                  <div className="bg-zinc-100 dark:bg-zinc-800 rounded-2xl rounded-tl-none px-4 py-3 border border-zinc-200/50 dark:border-zinc-700/50">
                    <div className="flex gap-1">
                      <span className="w-1.5 h-1.5 rounded-full bg-zinc-400 animate-bounce" style={{ animationDelay: '0ms' }} />
                      <span className="w-1.5 h-1.5 rounded-full bg-zinc-400 animate-bounce" style={{ animationDelay: '150ms' }} />
                      <span className="w-1.5 h-1.5 rounded-full bg-zinc-400 animate-bounce" style={{ animationDelay: '300ms' }} />
                    </div>
                  </div>
                </div>
              )}
            </div>
          </ScrollArea>
        </CardContent>
        
        <CardFooter className="p-6 border-t border-zinc-100/50 dark:border-zinc-800/50">
          <form
            onSubmit={(e) => { e.preventDefault(); sendMessage(); }}
            className="flex w-full items-center gap-3 max-w-2xl mx-auto"
          >
            <div className="relative flex-1">
              <Input
                placeholder="Type your message..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                disabled={isLoading}
                className="w-full h-12 pl-4 pr-12 rounded-2xl border-zinc-200/50 dark:border-zinc-800/50 bg-zinc-50/50 dark:bg-zinc-950/50 focus-visible:ring-1 focus-visible:ring-zinc-400 focus-visible:border-zinc-400 transition-all"
              />
              <div className="absolute right-3 top-1/2 -translate-y-1/2">
                <Button 
                  type="submit" 
                  size="icon"
                  disabled={isLoading || !input.trim()} 
                  className="w-8 h-8 rounded-xl bg-zinc-900 hover:bg-zinc-800 dark:bg-zinc-100 dark:hover:bg-zinc-200 text-zinc-100 dark:text-zinc-900 transition-all duration-200"
                >
                  <Send className="w-4 h-4" />
                </Button>
              </div>
            </div>
          </form>
        </CardFooter>
      </Card>
    </div>
  );
}
