"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import type { CheckpointBeat as CheckpointBeatType } from "@/lib/types";

interface Props {
  beat: CheckpointBeatType;
  onPass: () => void;
}

export function CheckpointBeat({ beat, onPass }: Props) {
  const { questions } = beat;
  const [currentQ, setCurrentQ] = useState(0);
  const [selected, setSelected] = useState<number | null>(null);
  const [answered, setAnswered] = useState(false);
  const [correctCount, setCorrectCount] = useState(0);

  const q = questions[currentQ];
  const isCorrect = selected === q.correct_index;
  const isLastQuestion = currentQ === questions.length - 1;
  const allPassed = correctCount === questions.length;

  useEffect(() => {
    if (allPassed) onPass();
  }, [allPassed, onPass]);

  function handleSubmit() {
    if (selected === null) return;
    setAnswered(true);
    if (isCorrect) {
      setCorrectCount((c) => c + 1);
    }
  }

  function handleNext() {
    setCurrentQ((i) => i + 1);
    setSelected(null);
    setAnswered(false);
  }

  return (
    <div
      className="rounded-xl bg-white p-8 border-l-[3px] border-pastel-blue"
      style={{ boxShadow: "0 0 0 1px rgba(0,0,0,0.06)" }}
    >
      <div className="flex items-center justify-between mb-5">
        <span className="inline-flex items-center rounded-md bg-pastel-blue-wash px-2.5 py-1 text-xs font-semibold text-[#2563eb]">
          CHECKPOINT
        </span>
        <span className="text-xs font-medium text-muted">
          {currentQ + 1} / {questions.length}
        </span>
      </div>

      {allPassed ? (
        <div className="text-center py-6">
          <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-pastel-emerald-wash mb-3">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#059669" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="20 6 9 17 4 12" />
            </svg>
          </div>
          <p className="text-base font-semibold text-foreground mb-1">
            Checkpoint passed
          </p>
          <p className="text-sm text-secondary">
            All {questions.length} questions correct. Continue to the next beat.
          </p>
        </div>
      ) : (
        <AnimatePresence mode="wait">
          <motion.div
            key={currentQ}
            initial={{ opacity: 0, x: 12 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -12 }}
            transition={{ duration: 0.15, ease: [0.25, 0.46, 0.45, 0.94] }}
          >
            <p className="text-base font-medium leading-[1.7] text-foreground mb-5">
              {q.question}
            </p>

            <div className="space-y-2.5 mb-5">
              {q.options.map((option, i) => {
                let ringColor = "rgba(0,0,0,0.08)";
                let bg = "transparent";

                if (answered && i === q.correct_index) {
                  ringColor = "#6ee7b7";
                  bg = "#ecfdf5";
                } else if (answered && i === selected && !isCorrect) {
                  ringColor = "#fda4af";
                  bg = "#fff1f2";
                } else if (!answered && i === selected) {
                  ringColor = "#93c5fd";
                  bg = "#eff6ff";
                }

                return (
                  <button
                    key={i}
                    onClick={() => !answered && setSelected(i)}
                    disabled={answered}
                    className="w-full text-left rounded-lg px-4 py-3 text-sm leading-relaxed transition-all duration-150 ease-out disabled:cursor-default"
                    style={{
                      boxShadow: `0 0 0 1.5px ${ringColor}`,
                      backgroundColor: bg,
                    }}
                  >
                    <span className="inline-flex items-center justify-center w-5 h-5 rounded-full text-xs font-medium mr-2.5 bg-[rgba(0,0,0,0.04)] text-secondary">
                      {String.fromCharCode(65 + i)}
                    </span>
                    {option}
                  </button>
                );
              })}
            </div>

            {!answered ? (
              <button
                onClick={handleSubmit}
                disabled={selected === null}
                className="px-4 py-2.5 text-sm font-medium text-white bg-pastel-blue rounded-lg transition-all duration-150 ease-out hover:opacity-90 disabled:opacity-30 disabled:cursor-not-allowed active:scale-[0.97]"
              >
                Check answer
              </button>
            ) : (
              <div className="space-y-4">
                <div
                  className="rounded-lg p-4"
                  style={{
                    backgroundColor: isCorrect ? "#ecfdf5" : "#fff1f2",
                  }}
                >
                  <p className="text-sm font-medium mb-1" style={{ color: isCorrect ? "#059669" : "#e11d48" }}>
                    {isCorrect ? "Correct" : "Not quite"}
                  </p>
                  <p className="text-sm leading-relaxed text-secondary">
                    {q.explanation}
                  </p>
                </div>

                {!isLastQuestion && (
                  <button
                    onClick={handleNext}
                    className="px-4 py-2.5 text-sm font-medium text-white bg-pastel-blue rounded-lg transition-all duration-150 ease-out hover:opacity-90 active:scale-[0.97]"
                  >
                    Next question &rarr;
                  </button>
                )}
                {isLastQuestion && !allPassed && (
                  <button
                    onClick={() => {
                      setCurrentQ(0);
                      setSelected(null);
                      setAnswered(false);
                      setCorrectCount(0);
                    }}
                    className="px-4 py-2.5 text-sm font-medium text-[#2563eb] bg-pastel-blue-wash rounded-lg transition-all duration-150 ease-out hover:opacity-90 active:scale-[0.97]"
                  >
                    Retry checkpoint
                  </button>
                )}
              </div>
            )}
          </motion.div>
        </AnimatePresence>
      )}
    </div>
  );
}
