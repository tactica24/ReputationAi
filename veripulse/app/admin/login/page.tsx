'use client';

import { useFormState } from 'react-dom';
import { loginAction } from './actions';

const initialState = { message: '' };

export default function AdminLoginPage() {
  const [state, formAction] = useFormState(loginAction, initialState);

  return (
    <div className="container">
      <div className="card mx-auto max-w-md space-y-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Admin Access</p>
          <h1 className="text-2xl font-semibold text-slate-900">Sign in to VeriPulse</h1>
          <p className="text-sm text-slate-600">Use the admin email/password from your env vars.</p>
        </div>

        <form action={formAction} className="space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-700" htmlFor="email">
              Email
            </label>
            <input
              id="email"
              name="email"
              type="email"
              required
              className="w-full rounded-xl border border-slate-200 px-3 py-2 text-sm"
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-700" htmlFor="password">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              required
              className="w-full rounded-xl border border-slate-200 px-3 py-2 text-sm"
            />
          </div>
          <button
            type="submit"
            className="w-full rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white"
          >
            Sign In
          </button>
        </form>

        {state.message && state.message !== 'success' && (
          <p className="rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
            {state.message}
          </p>
        )}
        {state.message === 'success' && (
          <p className="rounded-xl border border-emerald-200 bg-emerald-50 px-3 py-2 text-sm text-emerald-700">
            Signed in. Head to the dashboard.
          </p>
        )}
      </div>
    </div>
  );
}
