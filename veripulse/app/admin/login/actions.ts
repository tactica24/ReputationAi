'use server';

import { cookies } from 'next/headers';

interface LoginState {
  message?: string;
}

export async function loginAction(_: LoginState, formData: FormData): Promise<LoginState> {
  const email = String(formData.get('email') ?? '').trim();
  const password = String(formData.get('password') ?? '');

  const adminEmail = process.env.ADMIN_EMAIL ?? '';
  const adminPassword = process.env.ADMIN_PASSWORD ?? '';

  if (!adminEmail || !adminPassword) {
    return { message: 'Admin credentials are not configured.' };
  }

  if (email !== adminEmail || password !== adminPassword) {
    return { message: 'Invalid credentials. Please try again.' };
  }

  cookies().set('veripulse_admin', 'true', {
    httpOnly: true,
    sameSite: 'lax',
    path: '/'
  });

  return { message: 'success' };
}
