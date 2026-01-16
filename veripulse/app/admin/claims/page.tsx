const claimsQueue = [
  {
    id: 'clm_101',
    subject: 'Fintech outage',
    claim: 'Payment rail disruption linked to third-party vendor.',
    risk: 'High',
    status: 'Needs review'
  },
  {
    id: 'clm_102',
    subject: 'Public health update',
    claim: 'Hospitalization figures inflated in regional report.',
    risk: 'Medium',
    status: 'Auto-scored'
  },
  {
    id: 'clm_103',
    subject: 'Energy grid upgrade',
    claim: 'New substation will be online within 30 days.',
    risk: 'Low',
    status: 'Auto-scored'
  }
];

export default function AdminClaimsPage() {
  return (
    <div className="space-y-6">
      <header className="space-y-2">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Claims Queue</p>
        <h1 className="text-3xl font-semibold text-slate-900">Claim Review</h1>
        <p className="text-slate-600">Triage extracted claims and attach evidence.</p>
      </header>

      <div className="card overflow-hidden">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-4 py-3">Subject</th>
              <th className="px-4 py-3">Claim</th>
              <th className="px-4 py-3">Risk</th>
              <th className="px-4 py-3">Status</th>
              <th className="px-4 py-3"></th>
            </tr>
          </thead>
          <tbody>
            {claimsQueue.map((item) => (
              <tr key={item.id} className="border-t border-slate-100">
                <td className="px-4 py-3 font-medium text-slate-900">{item.subject}</td>
                <td className="px-4 py-3 text-slate-600">{item.claim}</td>
                <td className="px-4 py-3 text-slate-600">{item.risk}</td>
                <td className="px-4 py-3 text-slate-600">{item.status}</td>
                <td className="px-4 py-3 text-right">
                  <a className="text-sm font-semibold text-slate-900" href={`/admin/claims/${item.id}`}>
                    Open →
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
