const quickStats = [
  { label: 'Sources monitored', value: '12 (RSS + Web)' },
  { label: 'Claims in queue', value: '38 pending' },
  { label: 'Bulletin status', value: 'Draft for tomorrow' }
];

const workflowSteps = [
  {
    title: 'Ingest & Normalize',
    description: 'RSS + web sources stream into Raw Items with hashes and metadata.'
  },
  {
    title: 'Extract Claims',
    description: 'OpenAI extracts claim candidates and tags type + risk.'
  },
  {
    title: 'Attach Evidence',
    description: 'Evidence snippets and stance are scored across credibility tiers.'
  },
  {
    title: 'Score Trust',
    description: 'Confidence, uncertainty, and reason codes drive a human review queue.'
  },
  {
    title: 'Publish Bulletin',
    description: 'A single A4 summary is generated in HTML + PDF each day.'
  }
];

export default function HomePage() {
  return (
    <div className="container space-y-10">
      <section className="grid gap-6 lg:grid-cols-[2fr,1fr]">
        <div className="card space-y-4">
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">MVP Overview</p>
          <h1 className="text-3xl font-semibold text-slate-900">VeriPulse Trust Engine</h1>
          <p className="text-base text-slate-600">
            A lightweight pipeline that ingests sources, extracts claims, attaches evidence, and
            ships a daily A4 bulletin with transparent scoring and audit trails.
          </p>
          <div className="flex flex-wrap gap-3 text-sm">
            <a className="rounded-full bg-slate-900 px-4 py-2 text-white" href="/admin">
              Open Admin Dashboard
            </a>
            <a className="rounded-full border border-slate-200 px-4 py-2 text-slate-700" href="/bulletins">
              View Bulletins
            </a>
          </div>
        </div>
        <div className="card space-y-3">
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Today</p>
          <div className="space-y-3">
            {quickStats.map((item) => (
              <div key={item.label} className="rounded-xl border border-slate-100 bg-slate-50 p-4">
                <p className="text-xs uppercase tracking-wide text-slate-500">{item.label}</p>
                <p className="text-lg font-semibold text-slate-900">{item.value}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="space-y-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Pipeline</p>
          <h2 className="text-2xl font-semibold text-slate-900">From signal to bulletin</h2>
        </div>
        <div className="grid gap-4 md:grid-cols-2">
          {workflowSteps.map((step, index) => (
            <div key={step.title} className="card">
              <p className="text-sm font-semibold text-slate-900">
                {index + 1}. {step.title}
              </p>
              <p className="mt-2 text-sm text-slate-600">{step.description}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
