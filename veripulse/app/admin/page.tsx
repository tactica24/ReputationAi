const dashboardCards = [
  {
    title: 'Claims triage',
    value: '38 open',
    description: 'Automated extraction with uncertainty flags.'
  },
  {
    title: 'Evidence coverage',
    value: '62%',
    description: 'Claims with at least 2 evidence sources.'
  },
  {
    title: 'Bulletin readiness',
    value: 'Draft in progress',
    description: 'A4 layout seeded for tomorrow.'
  }
];

export default function AdminDashboardPage() {
  return (
    <div className="space-y-6">
      <header className="space-y-2">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Dashboard</p>
        <h1 className="text-3xl font-semibold text-slate-900">Admin Overview</h1>
        <p className="text-slate-600">Monitor the trust engine pipeline and publish bulletins.</p>
      </header>

      <div className="grid gap-4 md:grid-cols-3">
        {dashboardCards.map((card) => (
          <div key={card.title} className="card space-y-2">
            <p className="text-xs uppercase tracking-wide text-slate-500">{card.title}</p>
            <p className="text-2xl font-semibold text-slate-900">{card.value}</p>
            <p className="text-sm text-slate-600">{card.description}</p>
          </div>
        ))}
      </div>

      <div className="card space-y-4">
        <h2 className="text-lg font-semibold text-slate-900">Today’s pipeline</h2>
        <div className="grid gap-3 md:grid-cols-2">
          <div className="rounded-xl border border-slate-100 bg-slate-50 p-4 text-sm text-slate-700">
            12 sources scanned, 86 raw items ingested.
          </div>
          <div className="rounded-xl border border-slate-100 bg-slate-50 p-4 text-sm text-slate-700">
            23 claims extracted, 9 flagged for human review.
          </div>
          <div className="rounded-xl border border-slate-100 bg-slate-50 p-4 text-sm text-slate-700">
            41 evidence snippets attached, 5 conflicting.
          </div>
          <div className="rounded-xl border border-slate-100 bg-slate-50 p-4 text-sm text-slate-700">
            Bulletin sections compiled: Top claims, Watchlist, Policy.
          </div>
        </div>
      </div>
    </div>
  );
}
