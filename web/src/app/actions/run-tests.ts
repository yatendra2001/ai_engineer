"use server";

import { executeTests } from "@/lib/e2b";

export type { TestResult, RunResult } from "@/lib/e2b";

export async function runTests(
  challengeCode: string,
  testSuiteCode: string
) {
  return executeTests(challengeCode, testSuiteCode);
}
