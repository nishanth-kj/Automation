"use client";

import React from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { 
  Settings, 
  Cpu, 
  Globe, 
  Moon, 
  Sun, 
  Save, 
  Monitor,
  Key,
  CheckCircle2
} from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useStudio } from "@/context/StudioContext";

export function SettingsPanel() {
  const { 
    selectedModel, 
    setSelectedModel, 
    availableModels 
  } = useStudio() as any;

  return (
    <div className="max-w-3xl space-y-8 animate-in fade-in duration-500">
      <div className="flex items-center gap-3 mb-2">
        <h2 className="text-3xl font-bold tracking-tight">Settings</h2>
      </div>

      <div className="grid grid-cols-1 gap-8">
        <Card className="border-zinc-200 shadow-none rounded-2xl">
          <CardHeader>
            <CardTitle>AI Configuration</CardTitle>
            <CardDescription>Select and configure your AI model parameters.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-2">
              <label className="text-xs font-bold text-zinc-400 uppercase tracking-widest">Active Model (LM Studio)</label>
              <Select value={selectedModel} onValueChange={setSelectedModel}>
                <SelectTrigger className="w-full h-11 rounded-xl">
                  <SelectValue placeholder="Select a model" />
                </SelectTrigger>
                <SelectContent>
                  {availableModels.map((m: string) => (
                    <SelectItem key={m} value={m}>{m}</SelectItem>
                  ))}
                  {availableModels.length === 0 && (
                    <SelectItem value="loading" disabled>Loading models...</SelectItem>
                  )}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-4 pt-4 border-t">
              <div className="space-y-2">
                <label className="text-xs font-bold text-zinc-400 uppercase tracking-widest">LM Studio URL</label>
                <Input defaultValue="http://localhost:1234/api/v1" className="bg-zinc-50 border-zinc-200 rounded-xl h-11" />
              </div>
              <div className="space-y-2">
                <label className="text-xs font-bold text-zinc-400 uppercase tracking-widest">ComfyUI URL</label>
                <Input defaultValue="http://localhost:8188" className="bg-zinc-50 border-zinc-200 rounded-xl h-11" />
              </div>
            </div>

            <div className="pt-2">
               <Button className="w-full h-11 rounded-xl bg-zinc-900 text-white font-bold gap-2">
                  <Save className="w-4 h-4" /> Save Configuration
               </Button>
            </div>
          </CardContent>
        </Card>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
           <Card className="border-zinc-200 shadow-none rounded-2xl bg-zinc-50/50">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="w-10 h-10 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-600">
                  <CheckCircle2 className="w-5 h-5" />
                </div>
                <div>
                  <p className="font-bold text-sm">LM Studio Status</p>
                  <p className="text-xs text-zinc-500">Connected to local instance</p>
                </div>
              </div>
            </CardContent>
          </Card>
          <Card className="border-zinc-200 shadow-none rounded-2xl bg-zinc-50/50">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="w-10 h-10 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-600">
                  <CheckCircle2 className="w-5 h-5" />
                </div>
                <div>
                  <p className="font-bold text-sm">ComfyUI Status</p>
                  <p className="text-xs text-zinc-500">Flux Workflow detected</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
