const sources = [
  {
    name: 'Global Finance RSS',
    url: 'https://example.com/rss/finance',
    status: 'Enabled',
    section: 'Finance'
  },
  {
    name: 'Policy Tracker',
    url: 'https://example.com/policy',
    status: 'Enabled',
    section: 'Policy'
  },
  {
    name: 'Infrastructure Brief',
    url: 'https://example.com/infra',
    status: 'Paused',
    section: 'Infrastructure'
  }
];

export default function AdminSourcesPage() {
  return (
    <div className="space-y-6">
      <header className="space-y-2">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Sources</p>
        <h1 className="text-3xl font-semibold text-slate-900">Manage Sources</h1>
        <p className="text-slate-600">Enable or disable RSS/web sources and map bulletin sections.</p>
      </header>

      <div className="card space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <h2 className="text-lg font-semibold text-slate-900">Active sources</h2>
          <button className="rounded-full border border-slate-200 px-4 py-2 text-sm text-slate-700">
            Add source
          </button>
        </div>
        <div className="space-y-3">
          {sources.map((source) => (
            <div key={source.url} className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-slate-100 bg-slate-50 p-4">
              <div>
                <p className="text-sm font-semibold text-slate-900">{source.name}</p>
                <p className="text-xs text-slate-500">{source.url}</p>
              </div>
              <div className="text-xs text-slate-500">Section: {source.section}</div>
              <span className="rounded-full border border-slate-200 px-3 py-1 text-xs text-slate-600">
                {source.status}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
