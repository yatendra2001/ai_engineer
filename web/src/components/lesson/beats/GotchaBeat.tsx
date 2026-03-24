"use client";

import type { GotchaBeat as GotchaBeatType } from "@/lib/types";

interface Props {
  beat: GotchaBeatType;
}

export function GotchaBeat({ beat }: Props) {
  return (
    <div
      className="rounded-xl bg-white p-8 border-l-[3px] border-pastel-rose"
      style={{ boxShadow: "0 0 0 1px rgba(0,0,0,0.06)" }}
    >
      <span className="inline-flex items-center rounded-md bg-pastel-rose-wash px-2.5 py-1 text-xs font-semibold text-[#e11d48] mb-5">
        COMMON MISTAKE
      </span>

      <div className="space-y-4">
        <div>
          <p className="text-xs font-medium text-muted uppercase tracking-wide mb-1">
            What people do
          </p>
          <p className="text-base leading-[1.7] text-muted line-through decoration-pastel-rose/60">
            {beat.wrong}
          </p>
        </div>

        <div>
          <p className="text-xs font-medium text-[#059669] uppercase tracking-wide mb-1">
            What you should do
          </p>
          <p className="text-base leading-[1.7] text-foreground font-medium">
            {beat.right}
          </p>
        </div>

        <div className="rounded-lg bg-pastel-rose-wash p-4">
          <p className="text-sm leading-relaxed text-secondary">
            <span className="font-medium text-foreground">Why:</span> {beat.why}
          </p>
        </div>
      </div>
    </div>
  );
}
