"use client"

import { ConfidenceLevel } from "@/types/analysis";

interface Props {
  level: ConfidenceLevel;
  score: number;
}

export default function ConfidenceBadge({ level, score }: Props) {
  const percentage = Math.round(score * 100);
  
  let colors = "bg-gray-500/10 text-gray-500 border-gray-500/20";
  let fillColors = "bg-gray-500";
  let icon = null;

  if (level === "HIGH") {
    colors = "bg-emerald-500/10 text-emerald-600 border-emerald-500/20 dark:text-emerald-400";
    fillColors = "bg-emerald-500";
    icon = <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M20 6L9 17l-5-5"/></svg>;
  } else if (level === "MEDIUM") {
    colors = "bg-amber-500/10 text-amber-600 border-amber-500/20 dark:text-amber-400";
    fillColors = "bg-amber-500";
    icon = <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v4"/><path d="M12 16h.01"/></svg>;
  } else if (level === "LOW") {
    colors = "bg-red-500/10 text-red-600 border-red-500/20 dark:text-red-400";
    fillColors = "bg-red-500";
    icon = <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>;
  }

  return (
    <div className="flex flex-col gap-2">
      <div className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full border text-xs font-semibold w-max ${colors}`}>
        {icon}
        {level} CONFIDENCE
      </div>
      
      <div className="flex items-center gap-3">
        <div className="h-2 w-full bg-secondary rounded-full overflow-hidden">
          <div 
            className={`h-full ${fillColors} transition-all duration-1000 ease-out`} 
            style={{ width: `${percentage}%` }}
          />
        </div>
        <span className="text-sm font-medium">{percentage}%</span>
      </div>
    </div>
  );
}
