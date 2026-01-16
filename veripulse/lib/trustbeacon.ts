export const trustBeaconConfig = {
  baseUrl: process.env.TRUSTBEACON_API_BASE ?? '',
  apiKey: process.env.TRUSTBEACON_API_KEY ?? ''
};

export function isTrustBeaconConfigured() {
  return Boolean(trustBeaconConfig.baseUrl && trustBeaconConfig.apiKey);
}

export async function fetchTrustBeacon(path: string, init?: RequestInit) {
  if (!trustBeaconConfig.baseUrl) {
    throw new Error('TRUSTBEACON_API_BASE is not configured');
  }

  const url = new URL(path.replace(/^\//, ''), trustBeaconConfig.baseUrl.endsWith('/')
    ? trustBeaconConfig.baseUrl
    : `${trustBeaconConfig.baseUrl}/`
  );

  const headers = new Headers(init?.headers);
  if (trustBeaconConfig.apiKey) {
    headers.set('Authorization', `Bearer ${trustBeaconConfig.apiKey}`);
  }

  const response = await fetch(url, {
    ...init,
    headers
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`TrustBeacon request failed (${response.status}): ${body}`);
  }

  return response;
}
