"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import type { AnalogyBeat as AnalogyBeatType } from "@/lib/types";

interface Props {
  beat: AnalogyBeatType;
}

export function AnalogyBeat({ beat }: Props) {
  const [expanded, setExpanded] = useState(!beat.collapsed_by_default);

  return (
    <div
      className="rounded-xl bg-white p-8 border-l-[3px] border-pastel-lavender"
      style={{ boxShadow: "0 0 0 1px rgba(0,0,0,0.06)" }}
    >
      <div className="flex items-center justify-between mb-4">
        <span className="inline-flex items-center rounded-md bg-pastel-lavender-wash px-2.5 py-1 text-xs font-semibold text-[#7c3aed]">
          ANALOGY
        </span>

        <button
          onClick={() => setExpanded((v) => !v)}
          className="text-sm font-medium text-secondary transition-colors duration-150 ease-out hover:text-foreground"
          aria-expanded={expanded}
        >
          {expanded ? "Hide" : "Show analogy"}
        </button>
      </div>

      <AnimatePresence initial={false}>
        {expanded && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.15, ease: [0.25, 0.46, 0.45, 0.94] }}
            className="overflow-hidden"
          >
            <p className="text-base leading-[1.7] text-foreground mb-4">
              {beat.analogy}
            </p>
            <div className="rounded-lg bg-pastel-lavender-wash p-4">
              <p className="text-sm leading-relaxed text-secondary">
                <span className="font-medium text-foreground">
                  Where this breaks down:
                </span>{" "}
                {beat.where_it_breaks}
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
