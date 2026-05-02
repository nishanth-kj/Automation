"use client";

import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
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
  Database,
  Monitor,
  Key
} from "lucide-react";

export function SettingsPanel() {
  return (
    <div className="max-w-4xl space-y-8 animate-in fade-in duration-500">
      <div className="flex items-center gap-3 mb-2">
        <div className="p-2 bg-zinc-900 rounded-xl">
          <Settings className="w-6 h-6 text-white" />
        </div>
        <div>
          <h2 className="text-3xl font-black tracking-tight">System Settings</h2>
          <p className="text-sm text-zinc-500 font-medium">Configure your studio environment and AI parameters.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="space-y-4">
          <SettingsNav icon={<Monitor />} label="General" active />
          <SettingsNav icon={<Cpu />} label="AI Models" />
          <SettingsNav icon={<Database />} label="Backend" />
          <SettingsNav icon={<Key />} label="API Keys" />
        </div>

        <div className="md:col-span-2 space-y-6">
          <Card className="border-zinc-100 dark:border-zinc-900 shadow-sm overflow-hidden rounded-2xl">
            <CardHeader className="bg-zinc-50/50 dark:bg-zinc-900/50 border-b border-zinc-100 dark:border-zinc-900">
              <CardTitle className="text-base font-bold">Studio Configuration</CardTitle>
            </CardHeader>
            <CardContent className="p-6 space-y-6">
              <div className="space-y-2">
                <label className="text-xs font-black text-zinc-400 uppercase tracking-widest">Application Theme</label>
                <div className="grid grid-cols-3 gap-4">
                  <ThemeOption icon={<Sun />} label="Light" />
                  <ThemeOption icon={<Moon />} label="Dark" active />
                  <ThemeOption icon={<Globe />} label="System" />
                </div>
              </div>

              <div className="space-y-4 pt-4 border-t border-zinc-50 dark:border-zinc-900">
                <div className="space-y-2">
                  <label className="text-xs font-black text-zinc-400 uppercase tracking-widest">LM Studio Base URL</label>
                  <Input defaultValue="http://localhost:1234/api/v1" className="bg-zinc-50 dark:bg-zinc-900 border-none rounded-xl h-11" />
                </div>
                <div className="space-y-2">
                  <label className="text-xs font-black text-zinc-400 uppercase tracking-widest">ComfyUI Base URL</label>
                  <Input defaultValue="http://localhost:8188" className="bg-zinc-50 dark:bg-zinc-900 border-none rounded-xl h-11" />
                </div>
              </div>

              <div className="pt-4">
                <Button className="w-full h-12 rounded-xl bg-zinc-950 dark:bg-white text-white dark:text-zinc-950 font-bold gap-2">
                  <Save className="w-4 h-4" /> Save Changes
                </Button>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-emerald-500/5 border-emerald-500/20 shadow-none rounded-2xl">
            <CardContent className="p-6 flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="w-10 h-10 rounded-full bg-emerald-500/20 flex items-center justify-center text-emerald-600">
                  <Cpu className="w-5 h-5" />
                </div>
                <div>
                  <p className="font-bold text-sm text-emerald-900 dark:text-emerald-100">AI Service Active</p>
                  <p className="text-xs text-emerald-600 font-medium">LM Studio is responding on port 1234.</p>
                </div>
              </div>
              <Badge className="bg-emerald-500 text-white border-none text-[10px] font-black">STABLE</Badge>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

function SettingsNav({ icon, label, active }: { icon: React.ReactNode, label: string, active?: boolean }) {
  return (
    <button className={`w-full flex items-center gap-3 p-4 rounded-2xl font-bold transition-all ${
      active 
      ? 'bg-zinc-900 text-white shadow-lg' 
      : 'text-zinc-500 hover:bg-zinc-100 dark:hover:bg-zinc-900'
    }`}>
      {React.cloneElement(icon as React.ReactElement<{ className?: string }>, { className: "w-5 h-5" })}
      <span>{label}</span>
    </button>
  );
}

function ThemeOption({ icon, label, active }: { icon: React.ReactNode, label: string, active?: boolean }) {
  return (
    <button className={`flex flex-col items-center justify-center gap-2 p-4 rounded-xl border-2 transition-all ${
      active 
      ? 'border-zinc-900 bg-zinc-900 text-white shadow-md' 
      : 'border-zinc-100 dark:border-zinc-800 text-zinc-500 hover:border-zinc-300'
    }`}>
      {React.cloneElement(icon as React.ReactElement<{ className?: string }>, { className: "w-5 h-5" })}
      <span className="text-[10px] font-black uppercase tracking-widest">{label}</span>
    </button>
  );
}
