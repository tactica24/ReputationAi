import React from 'react';

export default function OnboardingAdminApproval({ application, onApprove, onReject }) {
  return (
    <div className="onboarding-admin-approval">
      <h2 className="text-xl font-bold mb-4">New User Application</h2>
      <div className="mb-2"><b>Name:</b> {application.fullName}</div>
      <div className="mb-2"><b>Email:</b> {application.email}</div>
      <div className="mb-2"><b>Phone:</b> {application.phone}</div>
      <div className="mb-2"><b>Entities to Monitor:</b> {application.entities?.join(', ')}</div>
      <div className="mb-4"><b>Message:</b> {application.message}</div>
      <div className="flex gap-4">
        <button className="btn-primary" onClick={onApprove}>Approve</button>
        <button className="btn-secondary" onClick={onReject}>Reject</button>
      </div>
    </div>
  );
}
