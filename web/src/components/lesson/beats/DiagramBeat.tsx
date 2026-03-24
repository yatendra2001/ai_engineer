"use client";

import type { DiagramBeat as DiagramBeatType } from "@/lib/types";

interface Props {
  beat: DiagramBeatType;
}

function PipelineDiagram() {
  const stages = [
    { label: "Raw Text", content: '"Hello world!"', color: "#818cf8" },
    { label: "Tokens", content: "[15496, 1917, 0]", color: "#a78bfa" },
    { label: "Vectors", content: "[ 0.12, -0.34, … ]", color: "#7dd3fc" },
    { label: "Attention", content: "context mixing", color: "#6ee7b7" },
    { label: "Output", content: '"Hello world! How"', color: "#93c5fd" },
  ];

  const arrows = ["TOKENIZE", "EMBED", "ATTEND", "SAMPLE"];

  return (
    <svg viewBox="0 0 880 120" className="w-full" aria-label="LLM Processing Pipeline diagram">
      {stages.map((stage, i) => {
        const x = i * 180;
        return (
          <g key={stage.label}>
            <rect
              x={x}
              y={10}
              width={140}
              height={100}
              rx={8}
              fill="white"
              stroke={stage.color}
              strokeWidth={1.5}
            />
            <text
              x={x + 70}
              y={38}
              textAnchor="middle"
              className="text-[11px] font-semibold"
              fill="#1a1a2e"
              fontFamily="var(--font-sans)"
            >
              {stage.label}
            </text>
            <text
              x={x + 70}
              y={72}
              textAnchor="middle"
              className="text-[10px]"
              fill="#6b7280"
              fontFamily="var(--font-mono)"
            >
              {stage.content}
            </text>
            {i < stages.length - 1 && (
              <>
                <line
                  x1={x + 140}
                  y1={60}
                  x2={x + 180}
                  y2={60}
                  stroke="#d1d5db"
                  strokeWidth={1.5}
                  markerEnd="url(#arrowhead)"
                />
                <text
                  x={x + 160}
                  y={52}
                  textAnchor="middle"
                  className="text-[8px] font-medium"
                  fill="#9ca3af"
                  fontFamily="var(--font-sans)"
                >
                  {arrows[i]}
                </text>
              </>
            )}
          </g>
        );
      })}
      <defs>
        <marker
          id="arrowhead"
          markerWidth="8"
          markerHeight="6"
          refX="8"
          refY="3"
          orient="auto"
        >
          <polygon points="0 0, 8 3, 0 6" fill="#d1d5db" />
        </marker>
      </defs>
    </svg>
  );
}

export function DiagramBeat({ beat }: Props) {
  return (
    <div
      className="rounded-xl bg-white p-8 border-l-[3px] border-pastel-sky"
      style={{ boxShadow: "0 0 0 1px rgba(0,0,0,0.06)" }}
    >
      <span className="inline-flex items-center rounded-md bg-pastel-sky-wash px-2.5 py-1 text-xs font-semibold text-[#0284c7] mb-5">
        DIAGRAM
      </span>

      <div className="overflow-x-auto py-2">
        <PipelineDiagram />
      </div>

      <p className="text-sm text-muted mt-4 text-center">
        {beat.caption}
      </p>
    </div>
  );
}
