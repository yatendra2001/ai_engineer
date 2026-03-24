import Link from "next/link";
import { listModules, listLessons } from "@/lib/content";

export default async function Home() {
  const modules = await listModules();

  const moduleLessons = await Promise.all(
    modules.map(async (mod) => ({
      module: mod,
      lessons: await listLessons(mod),
    }))
  );

  return (
    <main className="flex-1 flex items-center justify-center px-6 py-16">
      <div className="max-w-xl w-full">
        <h1 className="text-3xl font-semibold tracking-tight mb-2">Forge</h1>
        <p className="text-secondary mb-10 text-lg leading-relaxed">
          AI Engineering Learning Path
        </p>

        {moduleLessons.map(({ module: mod, lessons }) => (
          <div key={mod} className="mb-8">
            <h2 className="text-sm font-medium text-muted uppercase tracking-wide mb-3">
              {mod.replace(/^module-\d+-/, "").replace(/-/g, " ")}
            </h2>
            <ul className="space-y-2">
              {lessons.map((lesson, i) => (
                <li key={lesson}>
                  <Link
                    href={`/lesson/${mod}/${lesson}`}
                    className="group flex items-center gap-3 rounded-lg px-4 py-3 transition-colors duration-150 ease-out hover:bg-[#f8fafc]"
                    style={{ boxShadow: "0 0 0 1px rgba(0,0,0,0.06)" }}
                  >
                    <span className="flex-shrink-0 w-6 h-6 rounded-full bg-pastel-indigo-wash text-pastel-indigo text-xs font-semibold flex items-center justify-center">
                      {i + 1}
                    </span>
                    <span className="text-sm font-medium">
                      {lesson
                        .replace(/^lesson-\d+-/, "")
                        .replace(/-/g, " ")
                        .replace(/\b\w/g, (c) => c.toUpperCase())}
                    </span>
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </main>
  );
}
