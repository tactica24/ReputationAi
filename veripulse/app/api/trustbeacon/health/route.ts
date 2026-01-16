import { NextResponse } from 'next/server';
import { fetchTrustBeacon, isTrustBeaconConfigured } from '@/lib/trustbeacon';

export async function GET() {
  if (!isTrustBeaconConfigured()) {
    return NextResponse.json({ status: 'not_configured' }, { status: 503 });
  }

  const response = await fetchTrustBeacon('/health');
  const payload = await response.json();
  return NextResponse.json({ status: 'ok', trustbeacon: payload });
}
