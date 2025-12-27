# Admin Guide: Managing Subscriptions & Onboarding

## Overview

As an admin, you now control subscription pricing and manage the complete onboarding process. Users can no longer see pricing on the website - instead, you create personalized offers after reviewing their applications.

## Process Flow

### 1. Receive Application Notification

When a user submits an application, you'll receive a notification with their details:
- Personal information
- Company details
- Protection needs
- Urgency level
- Current threats/concerns

**No pricing is shown to the user at this stage.**

### 2. Review Application

Review the application to determine:
- ✅ Is this a legitimate client?
- ✅ What tier fits their needs? (Professional/Enterprise/Custom)
- ✅ What should we charge them?
- ✅ Any discounts applicable?
- ✅ Any custom features needed?

### 3. Create Personalized Offer

Use the admin API to create a subscription offer:

**API Endpoint**: `POST /api/admin/onboarding/create-offer`

**Example Request**:
```bash
curl -X POST http://localhost:8080/api/admin/onboarding/create-offer \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -d '{
    "application_id": "APP-20251227-DOE1234",
    "user_email": "client@example.com",
    "tier": "enterprise",
    "monthly_price": 4997.00,
    "discount_percent": 10,
    "custom_features": [
      "Priority support",
      "Dedicated account manager"
    ],
    "notes": "High-value client - 10% discount approved",
    "include_trial_days": 0
  }'
```

**Pricing Guidelines**:
- **Professional**: Base $997/month (individuals, executives)
- **Enterprise**: Base $4,997/month (companies, multiple entities)
- **Custom**: Set your own price (large corporations, VIPs)

**Discount Authority**:
- Up to 10%: Account manager approval
- 10-20%: Director approval
- 20%+: Executive approval required

### 4. What Happens Next

Once you create the offer, the system automatically:

1. **Generates Secure Links**
   - Onboarding portal link (for documents, video, photos)
   - Payment setup link (for credit card)

2. **Sends Email to User** containing:
   - Subscription details and pricing
   - Secure onboarding portal link
   - Payment setup instructions
   - Timeline and next steps

3. **Creates Offer Record**
   - Offer ID for tracking
   - 7-day expiration
   - Status: pending

### 5. Monitor Onboarding Progress

Track user progress through the onboarding portal:

**Get Offer Status**: `GET /api/admin/onboarding/offers/{offer_id}`

Statuses:
- `pending`: Sent to user, awaiting completion
- `accepted`: User accepted offer
- `completed`: Payment setup complete, subscription active
- `expired`: 7 days passed without completion

### 6. Handle Special Cases

#### Urgent Cases (Active Crisis)
- Create offer within 4 hours
- Consider expedited onboarding
- Set up monitoring before payment if approved

#### Large Enterprises
- Custom pricing required
- Multiple stakeholder approval
- Potentially phased rollout

#### VIP/High-Profile Clients
- White-glove service
- Personal account manager assignment
- Custom features and integrations

## Onboarding Portal Features

Users complete these steps in the secure portal:

### Document Upload
- Identification (driver's license, passport)
- Business registration (if applicable)
- Any relevant legal documents
- All encrypted with AES-256

### Video Introduction
- 2-5 minute video
- Introduce themselves
- Explain their protection needs
- Optional but recommended

### Photo Upload
- Professional headshot
- Company logo (if applicable)
- Team photos (enterprise clients)

### Payment Setup
- Credit/debit card information
- Billing address
- Automatic monthly billing
- PCI DSS compliant processing

## API Reference

### Create Offer
```
POST /api/admin/onboarding/create-offer
```

**Request Body**:
```json
{
  "application_id": "string",
  "user_email": "string",
  "tier": "professional|enterprise|custom",
  "monthly_price": number,
  "discount_percent": number (0-100),
  "custom_features": ["string"],
  "notes": "string",
  "include_trial_days": number (default: 0)
}
```

**Response**:
```json
{
  "success": true,
  "offer_id": "string",
  "monthly_price": number,
  "portal_link": "string",
  "payment_link": "string",
  "expires_at": "datetime"
}
```

### Get Offer Details
```
GET /api/admin/onboarding/offers/{offer_id}
```

### Complete Onboarding
```
POST /api/admin/onboarding/portal/complete
```
(Called by user through onboarding portal)

## Best Practices

### ✅ Do's

1. **Review applications thoroughly**
   - Check for legitimacy
   - Verify business details
   - Assess actual needs

2. **Customize pricing appropriately**
   - Base on value provided
   - Consider client budget
   - Factor in complexity

3. **Communicate clearly**
   - Set expectations
   - Provide timeline
   - Be available for questions

4. **Document decisions**
   - Use notes field
   - Record discount reasons
   - Track special agreements

### ❌ Don'ts

1. **Don't rush the process**
   - Proper vetting is crucial
   - Quality over quantity

2. **Don't share portal links**
   - Links are user-specific
   - Security risk if shared

3. **Don't forget follow-up**
   - Check onboarding progress
   - Reach out if stuck
   - Provide assistance

## Troubleshooting

### User hasn't completed onboarding
- Check if email was delivered
- Verify links work
- Contact user directly
- Extend expiration if needed

### Payment setup failed
- Verify payment processor status
- Check card validity
- Confirm billing address
- Offer alternative payment method

### Documents not uploading
- Check file size limits
- Verify file formats
- Test upload endpoint
- Provide direct support

## Security Notes

- All portal links are tokenized and expire
- Payment information never stored by us
- Documents encrypted at rest and in transit
- Access logs maintained for audit

## Support Contacts

- Technical Issues: tech@reputationguardian.com
- Billing Questions: billing@reputationguardian.com
- Emergency: +1 (800) 555-GUARD

## Reporting

### Monthly Metrics
- Applications received
- Offers created
- Conversion rate
- Average pricing
- Discount usage

### Individual Performance
- Response time
- Approval rate
- Client satisfaction
- Revenue per client

---

**Last Updated**: December 27, 2025  
**Version**: 2.0
