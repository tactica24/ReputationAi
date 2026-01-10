import React, { useState } from 'react';
import { onboardingAPI } from '../../services/onboardingAPI';

// Professional Onboarding Portal: Step 1 - Admin Approval, Step 2 - User Info, Preferences, Selfie Upload
export default function OnboardingPortal({ onboardingToken }) {
  const [step, setStep] = useState(1);
  const [form, setForm] = useState({
    fullName: '',
    email: '',
    phone: '',
    preferences: {
      alertChannels: ['email'],
      digestFrequency: 'daily',
      vipConcierge: false,
      darkWebMonitoring: true,
    },
    selfie: null,
    selfiePreview: '',
    submitting: false,
    error: '',
    success: false,
  });

  // Handle input changes
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    if (name.startsWith('preferences.')) {
      const prefKey = name.split('.')[1];
      setForm((f) => ({ ...f, preferences: { ...f.preferences, [prefKey]: type === 'checkbox' ? checked : value } }));
    } else {
      setForm((f) => ({ ...f, [name]: value }));
    }
  };

  // Handle selfie upload
  const handleSelfie = (e) => {
    const file = e.target.files[0];
    if (file) {
      setForm((f) => ({ ...f, selfie: file }));
      const reader = new FileReader();
      reader.onload = (ev) => setForm((f) => ({ ...f, selfiePreview: ev.target.result }));
      reader.readAsDataURL(file);
    }
  };

  // Submit onboarding info
  const handleSubmit = async (e) => {
    e.preventDefault();
    setForm((f) => ({ ...f, submitting: true, error: '', success: false }));
    try {
      // Prepare data for backend
      const data = {
        userId: form.userId || '',
        offerId: form.offerId || '',
        paymentMethodId: form.paymentMethodId || '',
        billingAddress: form.billingAddress || {},
        documentsUploaded: form.documentsUploaded || [],
        videoUploaded: form.videoUploaded || false,
        photosUploaded: [],
        selfie: form.selfie,
        // Add additional fields as needed
      };
      // Call onboarding API
      await onboardingAPI.completeOnboarding(data, onboardingToken);
      setForm((f) => ({ ...f, submitting: false, success: true }));
    } catch (err) {
      setForm((f) => ({ ...f, submitting: false, error: 'Submission failed. Please try again.' }));
    }
  };

  if (form.success) {
    return (
      <div className="onboarding-success">
        <h2 className="text-2xl font-bold mb-4">Welcome!</h2>
        <p>Your onboarding is complete. Monitoring will begin shortly. You will receive an email with your credentials and next steps.</p>
      </div>
    );
  }

  return (
    <form className="onboarding-portal" onSubmit={handleSubmit}>
      <h1 className="text-2xl font-bold mb-6">Complete Your Onboarding</h1>
      <div className="mb-4">
        <label className="block font-medium mb-1">Full Name</label>
        <input type="text" name="fullName" value={form.fullName} onChange={handleChange} required className="input" />
      </div>
      <div className="mb-4">
        <label className="block font-medium mb-1">Email</label>
        <input type="email" name="email" value={form.email} onChange={handleChange} required className="input" />
      </div>
      <div className="mb-4">
        <label className="block font-medium mb-1">Phone</label>
        <input type="tel" name="phone" value={form.phone} onChange={handleChange} required className="input" />
      </div>
      <div className="mb-4">
        <label className="block font-medium mb-1">Notification Preferences</label>
        <div className="flex gap-4">
          <label><input type="checkbox" name="preferences.alertChannels" value="email" checked={form.preferences.alertChannels.includes('email')} onChange={handleChange} /> Email</label>
          <label><input type="checkbox" name="preferences.alertChannels" value="sms" checked={form.preferences.alertChannels.includes('sms')} onChange={handleChange} /> SMS</label>
          <label><input type="checkbox" name="preferences.alertChannels" value="push" checked={form.preferences.alertChannels.includes('push')} onChange={handleChange} /> Push</label>
        </div>
        <div className="mt-2">
          <label className="mr-2">Digest Frequency:</label>
          <select name="preferences.digestFrequency" value={form.preferences.digestFrequency} onChange={handleChange} className="input">
            <option value="none">None</option>
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
          </select>
        </div>
        <div className="mt-2">
          <label><input type="checkbox" name="preferences.vipConcierge" checked={form.preferences.vipConcierge} onChange={handleChange} /> VIP Concierge Service</label>
        </div>
        <div className="mt-2">
          <label><input type="checkbox" name="preferences.darkWebMonitoring" checked={form.preferences.darkWebMonitoring} onChange={handleChange} /> Enable Dark Web Monitoring</label>
        </div>
      </div>
      <div className="mb-4">
        <label className="block font-medium mb-1">Upload Selfie (for AI image monitoring)</label>
        <input type="file" accept="image/*" onChange={handleSelfie} required className="input" />
        {form.selfiePreview && <img src={form.selfiePreview} alt="Selfie preview" className="mt-2 rounded w-24 h-24 object-cover" />}
      </div>
      {form.error && <div className="text-red-600 mb-2">{form.error}</div>}
      <button type="submit" className="btn-primary" disabled={form.submitting}>{form.submitting ? 'Submitting...' : 'Complete Onboarding'}</button>
    </form>
  );
}
