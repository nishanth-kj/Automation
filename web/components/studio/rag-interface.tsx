"use client";

import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { 
  Database, 
  Upload, 
  FileText, 
  Search, 
  Trash2, 
  Plus,
  ShieldCheck,
  Zap,
  CheckCircle2
} from "lucide-react";

export function RagInterface() {
  const documents = [
    { name: "Brand_Guidelines.pdf", size: "1.2 MB", date: "2d ago" },
    { name: "News_Style_Guide.docx", size: "450 KB", date: "5d ago" },
  ];

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 bg-emerald-500/10 rounded-2xl flex items-center justify-center text-emerald-500">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-3xl font-black tracking-tight">Knowledge Base</h2>
            <p className="text-sm text-zinc-500 font-medium">Manage RAG documents to provide context for AI generations.</p>
          </div>
        </div>
        <Button className="rounded-2xl h-12 px-6 bg-zinc-950 dark:bg-white text-white dark:text-zinc-950 font-bold gap-2">
          <Upload className="w-4 h-4" /> Upload Document
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-2 space-y-6">
          <Card className="border-zinc-100 dark:border-zinc-900 shadow-sm rounded-2xl bg-white dark:bg-zinc-950">
            <CardHeader className="pb-2">
              <div className="flex items-center justify-between">
                <CardTitle className="text-sm font-bold text-zinc-400 uppercase tracking-widest">Indexed Documents</CardTitle>
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-zinc-400" />
                  <Input placeholder="Filter files..." className="pl-9 h-8 w-48 text-xs bg-zinc-50 dark:bg-zinc-900 border-none rounded-lg" />
                </div>
              </div>
            </CardHeader>
            <CardContent className="p-0">
              <div className="divide-y divide-zinc-50 dark:divide-zinc-900">
                {documents.map((doc, i) => (
                  <div key={i} className="flex items-center justify-between p-4 hover:bg-zinc-50/50 dark:hover:bg-zinc-900/50 transition-colors group">
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded-xl bg-zinc-100 dark:bg-zinc-900 flex items-center justify-center text-zinc-400 group-hover:text-indigo-500 transition-colors">
                        <FileText className="w-5 h-5" />
                      </div>
                      <div>
                        <p className="font-bold text-sm">{doc.name}</p>
                        <p className="text-[10px] text-zinc-500 uppercase font-black tracking-widest">{doc.size} • {doc.date}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge variant="outline" className="bg-emerald-50 text-emerald-600 border-emerald-100 text-[9px] font-black">INDEXED</Badge>
                      <Button variant="ghost" size="icon" className="h-8 w-8 text-zinc-300 hover:text-rose-500">
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card className="bg-zinc-950 text-white border-none shadow-2xl overflow-hidden relative p-8">
            <div className="flex items-center justify-between relative z-10">
              <div className="space-y-2">
                <h3 className="text-xl font-bold">Query Knowledge</h3>
                <p className="text-zinc-400 text-sm">Test your RAG indexing by querying the database directly.</p>
              </div>
              <Button size="icon" variant="secondary" className="rounded-xl h-10 w-10">
                <Plus className="w-5 h-5" />
              </Button>
            </div>
            <div className="mt-6 flex gap-2 relative z-10">
              <Input placeholder="Ask about your documents..." className="bg-white/10 border-white/10 text-white placeholder:text-zinc-500 h-12 rounded-xl" />
              <Button className="h-12 w-12 rounded-xl bg-white text-zinc-900 hover:bg-zinc-100">
                <Zap className="w-4 h-4" />
              </Button>
            </div>
          </Card>
        </div>

        <div className="space-y-6">
          <Card className="border-zinc-100 dark:border-zinc-900 shadow-sm rounded-2xl bg-white dark:bg-zinc-950">
            <CardHeader>
              <CardTitle className="text-sm font-bold text-zinc-400 uppercase tracking-widest">RAG Statistics</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <RagStat label="Total Chunks" value="12,482" />
              <RagStat label="Embedding Model" value="nomic-embed-text" />
              <RagStat label="Vector Store" value="ChromaDB" />
              <div className="pt-4 border-t border-zinc-50 dark:border-zinc-900">
                <div className="flex items-center gap-2 text-emerald-500 mb-2">
                  <CheckCircle2 className="w-4 h-4" />
                  <span className="text-xs font-bold uppercase tracking-widest">Indexing Healthy</span>
                </div>
                <p className="text-[11px] text-zinc-500 leading-relaxed">
                  Automatic re-indexing is enabled. Changes to documents will be reflected within minutes.
                </p>
              </div>
            </CardContent>
          </Card>
          
          <Button variant="outline" className="w-full h-12 rounded-xl border-zinc-100 dark:border-zinc-900 font-bold gap-2">
             <Database className="w-4 h-4" /> Optimize Store
          </Button>
        </div>
      </div>
    </div>
  );
}

function RagStat({ label, value }: { label: string, value: string }) {
  return (
    <div className="flex justify-between items-center">
      <span className="text-sm text-zinc-500 font-medium">{label}</span>
      <span className="text-sm font-black tracking-tight">{value}</span>
    </div>
  );
}
