import fs from "fs";
import path from "path";
import matter from "gray-matter";
import type { Beat, LessonData, LessonFrontmatter, LessonMeta, Hints } from "./types";

const CONTENT_DIR = path.join(process.cwd(), "..", "content");

function parseMdxBeats(content: string): Beat[] {
  const match = content.match(/export\s+const\s+beats\s*=\s*(\[[\s\S]*\])/);
  if (!match) throw new Error("Could not find beats array in lesson.mdx");

  // The beats array is valid JSON (double-quoted keys and values)
  try {
    return JSON.parse(match[1]);
  } catch {
    // If JSON.parse fails, try evaluating as JS (handles trailing commas etc.)
    // eslint-disable-next-line no-eval
    return eval(`(${match[1]})`);
  }
}

export async function loadLesson(
  moduleSlug: string,
  lessonSlug: string
): Promise<LessonData> {
  const lessonDir = path.join(CONTENT_DIR, moduleSlug, lessonSlug);

  const [mdxRaw, metaRaw, challengeCode, testSuiteCode, solutionCode, hintsRaw] =
    await Promise.all([
      fs.promises.readFile(path.join(lessonDir, "lesson.mdx"), "utf-8"),
      fs.promises.readFile(path.join(lessonDir, "meta.json"), "utf-8"),
      fs.promises.readFile(path.join(lessonDir, "challenge.py"), "utf-8"),
      fs.promises.readFile(path.join(lessonDir, "test_suite.py"), "utf-8"),
      fs.promises.readFile(path.join(lessonDir, "solution.py"), "utf-8"),
      fs.promises.readFile(path.join(lessonDir, "hints.json"), "utf-8"),
    ]);

  const { data: frontmatter, content } = matter(mdxRaw);
  const beats = parseMdxBeats(content);
  const meta: LessonMeta = JSON.parse(metaRaw);
  const hints: Hints = JSON.parse(hintsRaw);

  return {
    frontmatter: frontmatter as LessonFrontmatter,
    beats,
    meta,
    challengeCode,
    testSuiteCode,
    solutionCode,
    hints,
  };
}

export async function listModules(): Promise<string[]> {
  const entries = await fs.promises.readdir(CONTENT_DIR, { withFileTypes: true });
  return entries.filter((e) => e.isDirectory()).map((e) => e.name);
}

export async function listLessons(moduleSlug: string): Promise<string[]> {
  const moduleDir = path.join(CONTENT_DIR, moduleSlug);
  const entries = await fs.promises.readdir(moduleDir, { withFileTypes: true });
  return entries
    .filter((e) => e.isDirectory() && e.name.startsWith("lesson-"))
    .map((e) => e.name)
    .sort();
}
