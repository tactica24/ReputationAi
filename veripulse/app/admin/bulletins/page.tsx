const bulletins = [
  {
    date: '2024-06-01',
    status: 'Draft',
    publishTime: 'Tomorrow 07:00',
    sections: 4
  },
  {
    date: '2024-05-31',
    status: 'Published',
    publishTime: 'May 31 07:00',
    sections: 5
  }
];

export default function AdminBulletinsPage() {
  return (
    <div className="space-y-6">
      <header className="space-y-2">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Bulletins</p>
        <h1 className="text-3xl font-semibold text-slate-900">Manage Bulletins</h1>
        <p className="text-slate-600">Configure daily sections, publish time, and public URLs.</p>
      </header>

      <div className="card space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <h2 className="text-lg font-semibold text-slate-900">Daily bulletins</h2>
          <button className="rounded-full border border-slate-200 px-4 py-2 text-sm text-slate-700">
            Generate new bulletin
          </button>
        </div>
        <div className="space-y-3">
          {bulletins.map((bulletin) => (
            <div key={bulletin.date} className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-slate-100 bg-slate-50 p-4">
              <div>
                <p className="text-sm font-semibold text-slate-900">{bulletin.date}</p>
                <p className="text-xs text-slate-500">Publish: {bulletin.publishTime}</p>
              </div>
              <div className="text-xs text-slate-500">Sections: {bulletin.sections}</div>
              <span className="rounded-full border border-slate-200 px-3 py-1 text-xs text-slate-600">
                {bulletin.status}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
