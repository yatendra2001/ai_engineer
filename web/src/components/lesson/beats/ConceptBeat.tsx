"use client";

import type { ConceptBeat as ConceptBeatType } from "@/lib/types";

interface Props {
  beat: ConceptBeatType;
}

export function ConceptBeat({ beat }: Props) {
  return (
    <div
      className="rounded-xl bg-white p-8 border-l-[3px] border-pastel-violet"
      style={{ boxShadow: "0 0 0 1px rgba(0,0,0,0.06)" }}
    >
      <h3 className="text-lg font-semibold tracking-tight mb-3">
        {beat.title}
      </h3>
      <p className="text-base leading-[1.7] text-foreground mb-5">
        {beat.body}
      </p>
      <div className="rounded-lg bg-pastel-violet-wash px-4 py-3">
        <span className="inline-block rounded-md bg-pastel-violet/20 px-2 py-0.5 text-xs font-semibold text-pastel-violet mb-1.5">
          {beat.key_term}
        </span>
        <p className="text-sm leading-relaxed text-secondary">
          {beat.definition}
        </p>
      </div>
    </div>
  );
}
