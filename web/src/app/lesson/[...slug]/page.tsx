import { loadLesson } from "@/lib/content";
import { LessonRenderer } from "@/components/lesson/LessonRenderer";

interface LessonPageProps {
  params: Promise<{ slug: string[] }>;
}

export default async function LessonPage({ params }: LessonPageProps) {
  const { slug } = await params;

  if (slug.length < 2) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <p className="text-muted">Invalid lesson path.</p>
      </div>
    );
  }

  const [moduleSlug, lessonSlug] = slug;

  const lesson = await loadLesson(moduleSlug, lessonSlug);

  return <LessonRenderer lesson={lesson} />;
}
