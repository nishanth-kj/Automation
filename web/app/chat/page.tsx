"use client";

import React from "react";
import { useStudio } from "@/context/StudioContext";
import { ChatInterface } from "@/components/studio/chat-interface";

export default function ChatPage() {
  const { 
    messages, 
    chatInput, 
    setChatInput, 
    isChatLoading, 
    sendMessage, 
    selectedNews, 
    generateMeme,
    selectedModel,
    setSelectedModel
  } = useStudio();

  return (
    <ChatInterface 
      messages={messages}
      input={chatInput}
      setInput={setChatInput}
      isLoading={isChatLoading}
      onSendMessage={sendMessage}
      selectedNews={selectedNews}
      onGenerateMeme={generateMeme}
      selectedModel={selectedModel}
      setSelectedModel={setSelectedModel}
    />
  );
}
