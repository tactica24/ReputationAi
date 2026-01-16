const bulletins = [
  {
    date: '2024-06-01',
    title: 'Daily Bulletin — June 1, 2024',
    status: 'Draft',
    summary: 'Claims flagged across fintech, public health, and energy sectors.'
  },
  {
    date: '2024-05-31',
    title: 'Daily Bulletin — May 31, 2024',
    status: 'Published',
    summary: 'Highlights include verified infrastructure updates and policy rollbacks.'
  }
];

export default function BulletinsPage() {
  return (
    <div className="container space-y-6">
      <header className="space-y-2">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Archive</p>
        <h1 className="text-3xl font-semibold text-slate-900">Bulletin Archive</h1>
        <p className="text-slate-600">Browse published and draft bulletins by date.</p>
      </header>

      <div className="grid gap-4">
        {bulletins.map((bulletin) => (
          <div key={bulletin.date} className="card">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-semibold text-slate-900">{bulletin.title}</h2>
                <p className="text-sm text-slate-600">{bulletin.summary}</p>
              </div>
              <span className="rounded-full border border-slate-200 px-3 py-1 text-xs text-slate-500">
                {bulletin.status}
              </span>
            </div>
            <div className="mt-4">
              <a className="text-sm font-semibold text-slate-900" href={`/bulletins/${bulletin.date}`}>
                View bulletin →
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
