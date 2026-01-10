import React from 'react';
import OnboardingPortal from './OnboardingPortal';

// Standalone page for onboarding via secure link (after admin approval)
export default function OnboardingPage() {
  // In production, onboardingToken would be parsed from URL (e.g., /onboarding/:token)
  // For now, just pass a placeholder
  const onboardingToken = 'demo-token';
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <div className="w-full max-w-lg bg-white rounded-lg shadow p-8">
        <OnboardingPortal onboardingToken={onboardingToken} />
      </div>
    </div>
  );
}
