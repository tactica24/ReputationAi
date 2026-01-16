import type { ReactNode } from 'react';

const adminLinks = [
  { href: '/admin', label: 'Dashboard' },
  { href: '/admin/claims', label: 'Claims Queue' },
  { href: '/admin/sources', label: 'Sources' },
  { href: '/admin/bulletins', label: 'Bulletins' }
];

export default function AdminLayout({ children }: { children: ReactNode }) {
  return (
    <div className="container grid gap-6 lg:grid-cols-[240px,1fr]">
      <aside className="card h-fit space-y-3">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Admin</p>
        <nav className="space-y-2 text-sm">
          {adminLinks.map((link) => (
            <a key={link.href} href={link.href} className="block rounded-lg px-3 py-2 text-slate-700 hover:bg-slate-100">
              {link.label}
            </a>
          ))}
        </nav>
      </aside>
      <div className="space-y-6">{children}</div>
    </div>
  );
}
