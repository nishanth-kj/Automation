"use client";

import React from "react";
import { useStudio } from "@/context/StudioContext";
import { HomeDashboard } from "@/components/studio/home-dashboard";
import { useRouter } from "next/navigation";

export default function HomePage() {
  const { news } = useStudio();
  const router = useRouter();

  return <HomeDashboard news={news} onNavigate={(tab) => router.push(`/${tab === 'home' ? '' : tab}`)} />;
}
