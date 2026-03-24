"use client";

import type { HookBeat as HookBeatType } from "@/lib/types";

interface Props {
  beat: HookBeatType;
}

export function HookBeat({ beat }: Props) {
  return (
    <div
      className="rounded-xl bg-white p-8 border-l-[3px] border-pastel-amber"
      style={{ boxShadow: "0 0 0 1px rgba(0,0,0,0.06)" }}
    >
      <span className="inline-flex items-center rounded-md bg-pastel-amber-wash px-2.5 py-1 text-xs font-semibold text-[#b45309] mb-4">
        WHY THIS MATTERS
      </span>
      <p className="text-[17px] leading-[1.8] text-foreground">
        {beat.body}
      </p>
    </div>
  );
}
