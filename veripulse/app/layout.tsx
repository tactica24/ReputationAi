import './globals.css';
import type { ReactNode } from 'react';

export const metadata = {
  title: 'VeriPulse — Trust Engine',
  description: 'Trust Engine + Daily A4 Bulletin platform'
};

const navLinks = [
  { href: '/', label: 'Home' },
  { href: '/bulletins', label: 'Bulletins' },
  { href: '/admin', label: 'Admin' }
];

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="font-sans">
        <div className="border-b border-slate-200 bg-white">
          <div className="container flex items-center justify-between py-4">
            <div className="flex items-center gap-3">
              <span className="rounded-full bg-slate-900 px-3 py-1 text-sm font-semibold uppercase tracking-wide text-white">
                VeriPulse
              </span>
              <p className="text-sm text-slate-600">Trust Engine + Daily A4 Bulletin</p>
            </div>
            <nav className="flex items-center gap-4 text-sm text-slate-600">
              {navLinks.map((link) => (
                <a key={link.href} href={link.href} className="hover:text-slate-900">
                  {link.label}
                </a>
              ))}
            </nav>
          </div>
        </div>
        <main className="py-10">{children}</main>
      </body>
    </html>
  );
}
