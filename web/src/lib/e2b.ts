import { Sandbox } from "@e2b/code-interpreter";

export interface TestResult {
  name: string;
  passed: boolean;
  output: string;
}

export interface RunResult {
  tests: TestResult[];
  rawOutput: string;
}

export async function executeTests(
  challengeCode: string,
  testSuiteCode: string
): Promise<RunResult> {
  const sandbox = await Sandbox.create();

  try {
    await sandbox.files.write("challenge.py", challengeCode);
    await sandbox.files.write("test_suite.py", testSuiteCode);

    const result = await sandbox.commands.run(
      "python -m pytest test_suite.py -v --tb=short --no-header 2>&1",
      { timeoutMs: 30_000 }
    );

    const rawOutput = [result.stdout, result.stderr].filter(Boolean).join("\n");
    const tests = parseTestOutput(rawOutput);

    return { tests, rawOutput };
  } finally {
    await sandbox.kill();
  }
}

function parseTestOutput(output: string): TestResult[] {
  const tests: TestResult[] = [];
  const lines = output.split("\n");

  for (const line of lines) {
    // pytest -v outputs lines like: test_suite.py::test_name PASSED
    const match = line.match(
      /test_suite\.py::(\S+)\s+(PASSED|FAILED|ERROR)/
    );
    if (match) {
      tests.push({
        name: match[1],
        passed: match[2] === "PASSED",
        output: "",
      });
    }
  }

  // Attach failure details to failing tests
  let currentTest: string | null = null;
  let collecting = false;
  const failureOutput: Record<string, string[]> = {};

  for (const line of lines) {
    if (line.startsWith("FAILED") || line.startsWith("_")) {
      const nameMatch = line.match(/::(\S+)/);
      if (nameMatch) {
        currentTest = nameMatch[1];
        collecting = true;
        failureOutput[currentTest] = [];
      }
    } else if (collecting && currentTest) {
      if (line.startsWith("=") || line.startsWith("PASSED") || line.match(/::.*PASSED/)) {
        collecting = false;
        currentTest = null;
      } else {
        failureOutput[currentTest].push(line);
      }
    }
  }

  for (const test of tests) {
    if (!test.passed && failureOutput[test.name]) {
      test.output = failureOutput[test.name].join("\n").trim();
    }
  }

  return tests;
}
