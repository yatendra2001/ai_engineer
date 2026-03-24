"use client";

import { type ReactNode } from "react";

interface SplitPaneProps {
  left: ReactNode;
  right: ReactNode;
}

export function SplitPane({ left, right }: SplitPaneProps) {
  return (
    <div className="flex h-screen w-full overflow-hidden">
      {/* Left pane — lesson narrative */}
      <div className="flex flex-col w-[55%] min-w-[400px] max-w-[720px] h-full border-r border-[rgba(0,0,0,0.06)]">
        {left}
      </div>

      {/* Right pane — code panel */}
      <div className="flex-1 flex flex-col h-full min-w-[480px] bg-[#fafafa]">
        {right}
      </div>
    </div>
  );
}
