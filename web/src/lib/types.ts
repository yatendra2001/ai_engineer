export interface DemoBeat {
  type: "DEMO";
  description: string;
}

export interface HookBeat {
  type: "HOOK";
  body: string;
}

export interface ConceptBeat {
  type: "CONCEPT";
  title: string;
  body: string;
  key_term: string;
  definition: string;
}

export interface DiagramBeat {
  type: "DIAGRAM";
  caption: string;
  description: string;
}

export interface SocraticBeat {
  type: "SOCRATIC";
  question: string;
  think_prompt: string;
  answer: string;
  why_this_matters: string;
}

export interface CodeReadBeat {
  type: "CODE_READ";
  language: string;
  code: string;
  annotations: {
    line_range: [number, number];
    note: string;
  }[];
}

export interface GotchaBeat {
  type: "GOTCHA";
  wrong: string;
  right: string;
  why: string;
}

export interface AnalogyBeat {
  type: "ANALOGY";
  collapsed_by_default: boolean;
  analogy: string;
  where_it_breaks: string;
}

export interface CheckpointQuestion {
  question: string;
  options: string[];
  correct_index: number;
  explanation: string;
}

export interface CheckpointBeat {
  type: "CHECKPOINT";
  questions: CheckpointQuestion[];
}

export type Beat =
  | DemoBeat
  | HookBeat
  | ConceptBeat
  | DiagramBeat
  | SocraticBeat
  | CodeReadBeat
  | GotchaBeat
  | AnalogyBeat
  | CheckpointBeat;

export type BeatType = Beat["type"];

export interface LessonFrontmatter {
  lesson_id: string;
  title: string;
  concept: string;
}

export interface LessonMeta {
  id: string;
  module_slug: string;
  lesson_number: number;
  lesson_slug: string;
  title: string;
  concept: string;
  primary_question: string;
  what_gets_built: string;
  xp_reward: number;
  estimated_minutes: number;
  lesson_type: string;
  module_type: string;
  last_researched: string;
  prereqs: string[];
  concepts_introduced: string[];
  challenge: {
    function_name: string;
    difficulty: string;
    time_estimate_minutes: number;
    runs_in_browser: boolean;
  };
  status: string;
  generated_at: string;
}

export interface Hints {
  hint_1: string;
  hint_2: string;
  hint_3: string;
}

export interface LessonData {
  frontmatter: LessonFrontmatter;
  beats: Beat[];
  meta: LessonMeta;
  challengeCode: string;
  testSuiteCode: string;
  solutionCode: string;
  hints: Hints;
}
