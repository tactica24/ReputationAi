interface BulletinPageProps {
  params: { date: string };
}

const sampleSections = [
  {
    title: 'Top Claims',
    bullets: [
      'Major bank outages linked to third-party vendor error — confidence 72%.',
      'Global shipping delay reports tied to port strikes — confidence 61%.',
      'Public health advisory overstated hospitalization numbers — confidence 58%.',
      'Energy grid upgrade announced, timeline partially verified — confidence 64%.'
    ]
  },
  {
    title: 'Needs Human Review',
    bullets: [
      'Claim of new AI regulation passage lacks corroborating sources.',
      'Conflicting reports about water quality levels in regional update.'
    ]
  }
];

export default function BulletinDetailPage({ params }: BulletinPageProps) {
  return (
    <div className="container space-y-6">
      <header className="space-y-2">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Daily Bulletin</p>
        <h1 className="text-3xl font-semibold text-slate-900">Bulletin for {params.date}</h1>
        <p className="text-slate-600">Single-page A4 summary, exported in HTML + PDF.</p>
      </header>

      <div className="grid gap-4">
        {sampleSections.map((section) => (
          <div key={section.title} className="card">
            <h2 className="text-lg font-semibold text-slate-900">{section.title}</h2>
            <ul className="mt-3 list-disc space-y-2 pl-6 text-sm text-slate-700">
              {section.bullets.map((bullet) => (
                <li key={bullet}>{bullet}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      <div className="card flex flex-wrap items-center gap-4">
        <button className="rounded-full bg-slate-900 px-4 py-2 text-sm text-white">Download PDF</button>
        <button className="rounded-full border border-slate-200 px-4 py-2 text-sm text-slate-700">
          Share Public Link
        </button>
        <p className="text-sm text-slate-500">Public URL and PDF URL will be generated on publish.</p>
      </div>
    </div>
  );
}
