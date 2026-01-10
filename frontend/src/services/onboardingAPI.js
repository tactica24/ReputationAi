import axios from 'axios';

export const onboardingAPI = {
  completeOnboarding: async (data, onboardingToken) => {
    // Prepare form data for file upload
    const formData = new FormData();
    formData.append('user_id', data.userId || '');
    formData.append('offer_id', data.offerId || '');
    formData.append('payment_method_id', data.paymentMethodId || '');
    formData.append('billing_address', JSON.stringify(data.billingAddress || {}));
    if (data.documentsUploaded) {
      data.documentsUploaded.forEach((file, idx) => {
        formData.append(`documents_uploaded`, file);
      });
    }
    formData.append('video_uploaded', data.videoUploaded ? 'true' : 'false');
    if (data.photosUploaded) {
      data.photosUploaded.forEach((file, idx) => {
        formData.append(`photos_uploaded`, file);
      });
    }
    // Add selfie as photo upload
    if (data.selfie) {
      formData.append('photos_uploaded', data.selfie);
    }
    // POST to backend
    const response = await axios.post(
      `/api/admin/onboarding/portal/complete?token=${onboardingToken}`,
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } }
    );
    return response.data;
  },
};
