"use client";

import { useState, useCallback } from "react";
import { AnimatePresence, motion } from "framer-motion";
import dynamic from "next/dynamic";
import type { CodeReadBeat, Hints } from "@/lib/types";
import { runTests, type TestResult } from "@/app/actions/run-tests";

const MonacoEditor = dynamic(() => import("@monaco-editor/react"), {
  ssr: false,
  loading: () => (
    <div className="flex-1 flex items-center justify-center text-sm text-muted">
      Loading editor…
    </div>
  ),
});

interface CodePanelProps {
  codeReadBeat: CodeReadBeat | null;
  challengeCode: string;
  testSuiteCode: string;
  solutionCode: string;
  hints: Hints;
}

type Tab = "challenge" | "results" | "solution";

export function CodePanel({
  codeReadBeat,
  challengeCode,
  testSuiteCode,
  solutionCode,
  hints,
}: CodePanelProps) {
  const [code, setCode] = useState(challengeCode);
  const [activeTab, setActiveTab] = useState<Tab>("challenge");
  const [hintsRevealed, setHintsRevealed] = useState(0);
  const [testResults, setTestResults] = useState<TestResult[] | null>(null);
  const [testOutput, setTestOutput] = useState("");
  const [running, setRunning] = useState(false);
  const [allPassed, setAllPassed] = useState(false);
  const [showSolution, setShowSolution] = useState(false);

  const handleRun = useCallback(async () => {
    setRunning(true);
    setActiveTab("results");
    try {
      const result = await runTests(code, testSuiteCode);
      setTestResults(result.tests);
      setTestOutput(result.rawOutput);
      setAllPassed(result.tests.every((t) => t.passed));
    } catch {
      setTestOutput("Failed to connect to execution sandbox. Is E2B_API_KEY set?");
      setTestResults(null);
    } finally {
      setRunning(false);
    }
  }, [code, testSuiteCode]);

  const revealNextHint = () => {
    setHintsRevealed((n) => Math.min(n + 1, 3));
  };

  const hintList = [hints.hint_1, hints.hint_2, hints.hint_3];

  // When a CODE_READ beat is active, show its code read-only
  if (codeReadBeat) {
    return (
      <div className="flex flex-col h-full">
        <div className="px-5 pt-4 pb-3 border-b border-[rgba(0,0,0,0.06)]">
          <span className="text-xs font-medium text-muted uppercase tracking-wide">
            {codeReadBeat.language}
          </span>
        </div>
        <div className="flex-1">
          <MonacoEditor
            height="100%"
            language={codeReadBeat.language}
            value={codeReadBeat.code}
            theme="vs"
            options={{
              readOnly: true,
              minimap: { enabled: false },
              fontSize: 13,
              fontFamily: "var(--font-jetbrains-mono), monospace",
              lineNumbers: "on",
              scrollBeyondLastLine: false,
              renderLineHighlight: "none",
              overviewRulerBorder: false,
              hideCursorInOverviewRuler: true,
              padding: { top: 16 },
              scrollbar: {
                verticalScrollbarSize: 8,
                horizontalScrollbarSize: 8,
              },
            }}
          />
        </div>
      </div>
    );
  }

  // Default: challenge editor
  const tabs: { id: Tab; label: string }[] = [
    { id: "challenge", label: "Challenge" },
    { id: "results", label: `Results${testResults ? ` (${testResults.filter((t) => t.passed).length}/${testResults.length})` : ""}` },
    ...(allPassed || showSolution ? [{ id: "solution" as Tab, label: "Solution" }] : []),
  ];

  return (
    <div className="flex flex-col h-full">
      {/* Tab bar */}
      <div className="flex items-center gap-1 px-4 pt-3 pb-0 border-b border-[rgba(0,0,0,0.06)]">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-3 py-2 text-xs font-medium rounded-t-md transition-colors duration-150 ease-out ${
              activeTab === tab.id
                ? "text-foreground bg-white border-b-2 border-pastel-indigo"
                : "text-muted hover:text-secondary"
            }`}
          >
            {tab.label}
          </button>
        ))}

        <div className="flex-1" />

        <button
          onClick={handleRun}
          disabled={running}
          className="flex items-center gap-1.5 px-3.5 py-1.5 mb-1.5 text-xs font-medium text-white bg-pastel-indigo rounded-md transition-all duration-150 ease-out hover:opacity-90 disabled:opacity-50 active:scale-[0.97]"
        >
          {running ? (
            <>
              <span className="inline-block w-3 h-3 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              Running…
            </>
          ) : (
            <>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
                <polygon points="5 3 19 12 5 21" />
              </svg>
              Run Tests
            </>
          )}
        </button>
      </div>

      {/* Tab content */}
      <div className="flex-1 overflow-hidden">
        {activeTab === "challenge" && (
          <MonacoEditor
            height="100%"
            language="python"
            value={code}
            onChange={(v) => setCode(v ?? "")}
            theme="vs"
            options={{
              minimap: { enabled: false },
              fontSize: 13,
              fontFamily: "var(--font-jetbrains-mono), monospace",
              lineNumbers: "on",
              scrollBeyondLastLine: false,
              renderLineHighlight: "line",
              overviewRulerBorder: false,
              padding: { top: 16 },
              scrollbar: {
                verticalScrollbarSize: 8,
                horizontalScrollbarSize: 8,
              },
              tabSize: 4,
              wordWrap: "on",
            }}
          />
        )}

        {activeTab === "results" && (
          <div className="p-5 overflow-y-auto h-full">
            {running ? (
              <div className="flex items-center justify-center h-32 text-sm text-muted">
                <span className="inline-block w-4 h-4 border-2 border-pastel-indigo/30 border-t-pastel-indigo rounded-full animate-spin mr-2" />
                Running tests…
              </div>
            ) : testResults ? (
              <div className="space-y-3">
                {testResults.map((t, i) => (
                  <div
                    key={i}
                    className="rounded-lg px-4 py-3 text-sm"
                    style={{
                      backgroundColor: t.passed ? "#ecfdf5" : "#fff1f2",
                      boxShadow: `0 0 0 1px ${t.passed ? "#6ee7b7" : "#fda4af"}`,
                    }}
                  >
                    <div className="flex items-center gap-2 mb-1">
                      <span style={{ color: t.passed ? "#059669" : "#e11d48" }}>
                        {t.passed ? "✓" : "✗"}
                      </span>
                      <span className="font-mono font-medium">{t.name}</span>
                    </div>
                    {t.output && (
                      <pre className="text-xs text-secondary font-mono mt-1 whitespace-pre-wrap">
                        {t.output}
                      </pre>
                    )}
                  </div>
                ))}

                <details className="mt-4">
                  <summary className="text-xs font-medium text-muted cursor-pointer hover:text-secondary">
                    Raw output
                  </summary>
                  <pre className="mt-2 text-xs text-secondary font-mono bg-surface rounded-lg p-4 overflow-x-auto whitespace-pre-wrap">
                    {testOutput}
                  </pre>
                </details>
              </div>
            ) : testOutput ? (
              <pre className="text-sm text-secondary font-mono whitespace-pre-wrap">
                {testOutput}
              </pre>
            ) : (
              <p className="text-sm text-muted text-center pt-8">
                Run the tests to see results here.
              </p>
            )}
          </div>
        )}

        {activeTab === "solution" && (
          <MonacoEditor
            height="100%"
            language="python"
            value={solutionCode}
            theme="vs"
            options={{
              readOnly: true,
              minimap: { enabled: false },
              fontSize: 13,
              fontFamily: "var(--font-jetbrains-mono), monospace",
              lineNumbers: "on",
              scrollBeyondLastLine: false,
              renderLineHighlight: "none",
              overviewRulerBorder: false,
              padding: { top: 16 },
              scrollbar: {
                verticalScrollbarSize: 8,
                horizontalScrollbarSize: 8,
              },
            }}
          />
        )}
      </div>

      {/* Hints drawer */}
      <div className="border-t border-[rgba(0,0,0,0.06)] px-5 py-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-medium text-muted uppercase tracking-wide">
            Hints ({hintsRevealed}/3)
          </span>
          {hintsRevealed < 3 && (
            <button
              onClick={revealNextHint}
              className="text-xs font-medium text-pastel-indigo hover:opacity-80 transition-opacity duration-150"
            >
              Reveal hint {hintsRevealed + 1}
            </button>
          )}
          {!showSolution && !allPassed && (
            <button
              onClick={() => {
                setShowSolution(true);
                setActiveTab("solution");
              }}
              className="text-xs font-medium text-muted hover:text-secondary transition-colors duration-150 ml-3"
            >
              Show solution
            </button>
          )}
        </div>

        <AnimatePresence>
          {hintsRevealed > 0 && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              className="space-y-2 overflow-hidden"
            >
              {hintList.slice(0, hintsRevealed).map((hint, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 4 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.05 }}
                  className="rounded-lg bg-pastel-indigo-wash px-3 py-2.5 text-xs leading-relaxed text-secondary"
                >
                  <span className="font-semibold text-pastel-indigo mr-1">
                    Hint {i + 1}:
                  </span>
                  {hint}
                </motion.div>
              ))}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
