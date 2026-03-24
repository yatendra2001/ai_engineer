"use client";

import type { CodeReadBeat as CodeReadBeatType } from "@/lib/types";

interface Props {
  beat: CodeReadBeatType;
}

export function CodeReadBeat({ beat }: Props) {
  return (
    <div
      className="rounded-xl bg-white p-8 border-l-[3px] border-pastel-slate"
      style={{ boxShadow: "0 0 0 1px rgba(0,0,0,0.06)" }}
    >
      <span className="inline-flex items-center rounded-md bg-pastel-slate-wash px-2.5 py-1 text-xs font-semibold text-pastel-slate mb-5">
        READ THE CODE &rarr;
      </span>

      <p className="text-sm text-secondary mb-5">
        Study the code in the right panel. Here are the key things to notice:
      </p>

      <div className="space-y-3">
        {beat.annotations.map((annotation, i) => (
          <div
            key={i}
            className="flex gap-3 rounded-lg bg-pastel-slate-wash p-4"
          >
            <span className="flex-shrink-0 inline-flex items-center justify-center rounded-md bg-pastel-slate/15 px-2 py-0.5 text-xs font-mono font-medium text-pastel-slate">
              L{annotation.line_range[0]}&ndash;{annotation.line_range[1]}
            </span>
            <p className="text-sm leading-relaxed text-foreground">
              {annotation.note}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
