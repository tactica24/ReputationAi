interface ClaimDetailPageProps {
  params: { id: string };
}

const evidenceList = [
  {
    title: 'Vendor status update',
    stance: 'Supports',
    credibility: 'Tier 1',
    snippet: 'Official status page confirms partial outage tied to upstream provider.'
  },
  {
    title: 'Industry analyst note',
    stance: 'Neutral',
    credibility: 'Tier 2',
    snippet: 'Analyst highlights multiple potential causes; needs confirmation.'
  }
];

export default function ClaimDetailPage({ params }: ClaimDetailPageProps) {
  return (
    <div className="space-y-6">
      <header className="space-y-2">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Case File</p>
        <h1 className="text-3xl font-semibold text-slate-900">Claim {params.id}</h1>
        <p className="text-slate-600">Review extracted claim, evidence, and assessment.</p>
      </header>

      <div className="card space-y-4">
        <div>
          <p className="text-xs uppercase tracking-wide text-slate-500">Claim Text</p>
          <p className="text-lg font-semibold text-slate-900">
            Payment rail disruption linked to third-party vendor outage.
          </p>
        </div>
        <div className="grid gap-3 md:grid-cols-3">
          <div className="rounded-xl border border-slate-100 bg-slate-50 p-4 text-sm text-slate-700">
            Claim Type: Factual
          </div>
          <div className="rounded-xl border border-slate-100 bg-slate-50 p-4 text-sm text-slate-700">
            Risk Level: High
          </div>
          <div className="rounded-xl border border-slate-100 bg-slate-50 p-4 text-sm text-slate-700">
            Confidence: 72% accurate
          </div>
        </div>
      </div>

      <div className="card space-y-4">
        <h2 className="text-lg font-semibold text-slate-900">Evidence</h2>
        <div className="grid gap-4 md:grid-cols-2">
          {evidenceList.map((item) => (
            <div key={item.title} className="rounded-xl border border-slate-100 bg-slate-50 p-4">
              <p className="text-sm font-semibold text-slate-900">{item.title}</p>
              <p className="text-xs uppercase tracking-wide text-slate-500">
                {item.stance} · {item.credibility}
              </p>
              <p className="mt-2 text-sm text-slate-600">{item.snippet}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="card space-y-4">
        <h2 className="text-lg font-semibold text-slate-900">Assessment</h2>
        <p className="text-sm text-slate-600">
          Model: gpt-4.1 | Prompt version: v0.1 | Reason codes: SOURCE_CONFIRM, VENDOR_STATUS
        </p>
        <p className="text-sm text-slate-700">
          Evidence is credible but limited to vendor channels. Recommend secondary confirmation from industry reporting.
        </p>
        <button className="rounded-full bg-slate-900 px-4 py-2 text-sm text-white">Mark as reviewed</button>
      </div>
    </div>
  );
}
