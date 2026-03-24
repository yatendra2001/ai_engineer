"use client";

import type { DemoBeat as DemoBeatType } from "@/lib/types";

interface Props {
  beat: DemoBeatType;
}

export function DemoBeat({ beat }: Props) {
  return (
    <div
      className="rounded-xl bg-white p-8 border-l-[3px] border-pastel-indigo"
      style={{ boxShadow: "0 0 0 1px rgba(0,0,0,0.06)" }}
    >
      <div className="flex items-center gap-2 mb-4">
        <span className="inline-flex items-center rounded-md bg-pastel-indigo-wash px-2.5 py-1 text-xs font-semibold text-pastel-indigo">
          DEMO
        </span>
      </div>
      <p className="text-base leading-[1.7] text-foreground">
        {beat.description}
      </p>
    </div>
  );
}
