"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import type { SocraticBeat as SocraticBeatType } from "@/lib/types";

interface Props {
  beat: SocraticBeatType;
}

export function SocraticBeat({ beat }: Props) {
  const [revealed, setRevealed] = useState(false);

  return (
    <div
      className="rounded-xl bg-white p-8 border-l-[3px] border-pastel-emerald"
      style={{ boxShadow: "0 0 0 1px rgba(0,0,0,0.06)" }}
    >
      <span className="inline-flex items-center rounded-md bg-pastel-emerald-wash px-2.5 py-1 text-xs font-semibold text-[#059669] mb-4">
        THINK
      </span>

      <p className="text-base font-medium leading-[1.7] text-foreground mb-3">
        {beat.question}
      </p>

      <p className="text-sm italic text-muted mb-5">
        {beat.think_prompt}
      </p>

      {!revealed ? (
        <button
          onClick={() => setRevealed(true)}
          className="inline-flex items-center gap-1.5 rounded-lg bg-pastel-emerald-wash px-4 py-2.5 text-sm font-medium text-[#059669] transition-colors duration-150 ease-out hover:bg-pastel-emerald/20 active:scale-[0.97]"
        >
          Reveal answer
        </button>
      ) : (
        <AnimatePresence>
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            transition={{ duration: 0.15, ease: [0.25, 0.46, 0.45, 0.94] }}
          >
            <div className="rounded-lg bg-pastel-emerald-wash p-5 space-y-3">
              <p className="text-base leading-[1.7] text-foreground">
                {beat.answer}
              </p>
              <p className="text-sm text-secondary leading-relaxed">
                <span className="font-medium">Why this matters:</span>{" "}
                {beat.why_this_matters}
              </p>
            </div>
          </motion.div>
        </AnimatePresence>
      )}
    </div>
  );
}
