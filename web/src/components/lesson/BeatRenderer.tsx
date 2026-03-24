"use client";

import type { Beat } from "@/lib/types";
import { DemoBeat } from "./beats/DemoBeat";
import { HookBeat } from "./beats/HookBeat";
import { ConceptBeat } from "./beats/ConceptBeat";
import { DiagramBeat } from "./beats/DiagramBeat";
import { SocraticBeat } from "./beats/SocraticBeat";
import { CodeReadBeat } from "./beats/CodeReadBeat";
import { GotchaBeat } from "./beats/GotchaBeat";
import { AnalogyBeat } from "./beats/AnalogyBeat";
import { CheckpointBeat } from "./beats/CheckpointBeat";

interface BeatRendererProps {
  beat: Beat;
  onCheckpointPass: () => void;
}

export function BeatRenderer({ beat, onCheckpointPass }: BeatRendererProps) {
  switch (beat.type) {
    case "DEMO":
      return <DemoBeat beat={beat} />;
    case "HOOK":
      return <HookBeat beat={beat} />;
    case "CONCEPT":
      return <ConceptBeat beat={beat} />;
    case "DIAGRAM":
      return <DiagramBeat beat={beat} />;
    case "SOCRATIC":
      return <SocraticBeat beat={beat} />;
    case "CODE_READ":
      return <CodeReadBeat beat={beat} />;
    case "GOTCHA":
      return <GotchaBeat beat={beat} />;
    case "ANALOGY":
      return <AnalogyBeat beat={beat} />;
    case "CHECKPOINT":
      return <CheckpointBeat beat={beat} onPass={onCheckpointPass} />;
    default:
      return null;
  }
}
