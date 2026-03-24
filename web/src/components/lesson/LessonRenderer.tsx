"use client";

import { useState, useCallback, useEffect } from "react";
import { AnimatePresence, motion } from "framer-motion";
import type { LessonData, Beat, CodeReadBeat as CodeReadBeatType } from "@/lib/types";
import { SplitPane } from "./SplitPane";
import { BeatRenderer } from "./BeatRenderer";
import { CodePanel } from "./CodePanel";

interface LessonRendererProps {
  lesson: LessonData;
}

export function LessonRenderer({ lesson }: LessonRendererProps) {
  const { beats, meta, frontmatter, challengeCode, testSuiteCode, solutionCode, hints } = lesson;
  const [currentBeat, setCurrentBeat] = useState(0);
  const [checkpointPassed, setCheckpointPassed] = useState(false);

  const beat = beats[currentBeat];
  const isFirst = currentBeat === 0;
  const isLast = currentBeat === beats.length - 1;
  const isCheckpoint = beat.type === "CHECKPOINT";
  const canAdvance = !isLast && (!isCheckpoint || checkpointPassed);

  const codeReadBeat =
    beat.type === "CODE_READ" ? (beat as CodeReadBeatType) : null;

  const goNext = useCallback(() => {
    if (canAdvance) {
      setCurrentBeat((i) => i + 1);
      setCheckpointPassed(false);
    }
  }, [canAdvance]);

  const goPrev = useCallback(() => {
    if (!isFirst) {
      setCurrentBeat((i) => i - 1);
      setCheckpointPassed(false);
    }
  }, [isFirst]);

  useEffect(() => {
    function handleKey(e: KeyboardEvent) {
      if (e.key === "ArrowRight" || e.key === "ArrowDown") {
        e.preventDefault();
        goNext();
      }
      if (e.key === "ArrowLeft" || e.key === "ArrowUp") {
        e.preventDefault();
        goPrev();
      }
    }
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [goNext, goPrev]);

  const left = (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="px-8 pt-8 pb-4">
        <p className="text-xs font-medium text-muted uppercase tracking-wide mb-1">
          Lesson {meta.lesson_number} &middot; {meta.estimated_minutes} min
        </p>
        <h1 className="text-2xl font-semibold tracking-tight leading-tight">
          {frontmatter.title}
        </h1>
      </div>

      {/* Beat area */}
      <div className="flex-1 px-8 py-4 overflow-y-auto">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentBeat}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.2, ease: [0.25, 0.46, 0.45, 0.94] }}
          >
            <BeatRenderer
              beat={beat}
              onCheckpointPass={() => setCheckpointPassed(true)}
            />
          </motion.div>
        </AnimatePresence>
      </div>

      {/* Navigation */}
      <div className="px-8 py-4 flex items-center justify-between border-t border-[rgba(0,0,0,0.06)]">
        <button
          onClick={goPrev}
          disabled={isFirst}
          className="px-4 py-2 text-sm font-medium text-secondary rounded-lg transition-colors duration-150 ease-out hover:bg-[#f8fafc] disabled:opacity-30 disabled:cursor-not-allowed active:scale-[0.97]"
          aria-label="Previous beat"
        >
          &larr; Back
        </button>

        {/* Progress dots */}
        <div className="flex gap-1.5" role="progressbar" aria-valuenow={currentBeat + 1} aria-valuemin={1} aria-valuemax={beats.length}>
          {beats.map((_, i) => (
            <button
              key={i}
              onClick={() => { setCurrentBeat(i); setCheckpointPassed(false); }}
              className={`w-2 h-2 rounded-full transition-all duration-200 ease-out ${
                i === currentBeat
                  ? "bg-pastel-indigo scale-125"
                  : i < currentBeat
                    ? "bg-pastel-indigo/40"
                    : "bg-[rgba(0,0,0,0.1)]"
              }`}
              aria-label={`Go to beat ${i + 1}`}
            />
          ))}
        </div>

        <button
          onClick={goNext}
          disabled={!canAdvance}
          className="px-4 py-2 text-sm font-medium text-white bg-pastel-indigo rounded-lg transition-all duration-150 ease-out hover:opacity-90 disabled:opacity-30 disabled:cursor-not-allowed active:scale-[0.97]"
          aria-label="Next beat"
        >
          Continue &rarr;
        </button>
      </div>
    </div>
  );

  const right = (
    <CodePanel
      codeReadBeat={codeReadBeat}
      challengeCode={challengeCode}
      testSuiteCode={testSuiteCode}
      solutionCode={solutionCode}
      hints={hints}
    />
  );

  return <SplitPane left={left} right={right} />;
}
