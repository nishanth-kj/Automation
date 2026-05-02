"use client";

import React from "react";
import { Geist, Geist_Mono, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";
import { TooltipProvider } from "@/components/ui/tooltip";
import { Toaster } from "@/components/ui/sonner";
import { StudioProvider, useStudio } from "@/context/StudioContext";
import { Sidebar } from "@/components/layout/sidebar";
import { Console } from "@/components/layout/console";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Sparkles, Loader2, Settings2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";

const jetbrainsMono = JetBrains_Mono({subsets:['latin'],variable:'--font-mono'});
const geistSans = Geist({ variable: "--font-geist-sans", subsets: ["latin"] });
const geistMono = Geist_Mono({ variable: "--font-geist-mono", subsets: ["latin"] });

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={cn("h-full antialiased", geistSans.variable, geistMono.variable, jetbrainsMono.variable)} suppressHydrationWarning>
      <body className="h-full bg-white dark:bg-zinc-950 flex flex-col overflow-hidden" suppressHydrationWarning>
        <StudioProvider>
          <TooltipProvider>
            <StudioLayoutInner>{children}</StudioLayoutInner>
          </TooltipProvider>
        </StudioProvider>
        <Toaster />
      </body>
    </html>
  );
}

function StudioLayoutInner({ children }: { children: React.ReactNode }) {
  const { 
    selectedNews, 
    isScraping, 
    startScraper, 
    showConsole, 
    setShowConsole,
    scrapeProgress,
    pendingNews
  } = useStudio();

  return (
    <div className="flex flex-col h-full">
      <header className="h-14 border-b border-zinc-100 dark:border-zinc-900 bg-white dark:bg-black sticky top-0 z-30 px-6 flex items-center justify-between shrink-0">
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-zinc-900 dark:text-white" />
          <h1 className="font-semibold text-base tracking-tight">MemeStudio</h1>
        </div>
        <div className="flex items-center gap-2">
          {selectedNews && (
            <Badge variant="outline" className="text-[10px] font-medium border-zinc-200">
              {selectedNews.title.slice(0, 30)}...
            </Badge>
          )}
          <Link href="/settings">
            <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
              <Settings2 className="w-4 h-4" />
            </Button>
          </Link>
        </div>
      </header>

      <div className="flex-1 flex overflow-hidden">
        <Sidebar 
          isScraping={isScraping} 
          onRefresh={startScraper} 
          showConsole={showConsole}
          setShowConsole={setShowConsole}
        />

        <div className="flex-1 overflow-hidden relative flex flex-col bg-zinc-50/30">
          {isScraping && (
            <div className="p-4 bg-zinc-900 text-white flex items-center justify-between shrink-0">
              <div className="flex items-center gap-3">
                <Loader2 className="w-4 h-4 animate-spin text-emerald-400" />
                <span className="text-xs font-medium">{scrapeProgress[scrapeProgress.length - 1]}</span>
              </div>
              {pendingNews.length > 0 && <span className="text-[10px] font-bold">{pendingNews.length} FOUND</span>}
            </div>
          )}

          <ScrollArea className="flex-1">
            <div className="p-6 max-w-5xl mx-auto">
              {children}
            </div>
          </ScrollArea>
          
          <Console isOpen={showConsole} onClose={() => setShowConsole(false)} />
        </div>
      </div>
    </div>
  );
}
