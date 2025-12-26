# GitHub Actions Setup Guide

## Firebase Deployment via GitHub Actions

To enable automatic deployments when you push to GitHub, you need to configure a Firebase token.

### Option 1: Using Firebase Token (Simpler)

#### 1. Generate Firebase CI Token
```bash
firebase login:ci
```

This will output a token like: `1//abc123def456...`

#### 2. Add Token to GitHub Secrets
1. Go to your repository: https://github.com/tactica24/ReputationAi
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `FIREBASE_TOKEN`
5. Value: Paste the token from step 1
6. Click **Add secret**

#### 3. Push to Main Branch
```bash
git push origin main
```

The app will automatically deploy to Firebase! 🚀

---

### Option 2: Using Service Account (More Secure)

#### 1. Generate Service Account
1. Go to https://console.firebase.google.com/project/reputationai-70092432/settings/serviceaccounts/adminsdk
2. Click **Generate new private key**
3. Save the JSON file securely

#### 2. Add to GitHub Secrets
1. Go to repository settings
2. Add secret named `FIREBASE_SERVICE_ACCOUNT`
3. Paste the entire JSON content as the value

#### 3. Update Workflow
Use this version in `.github/workflows/deploy-firebase.yml`:

```yaml
- name: Deploy to Firebase
  uses: FirebaseExtended/action-hosting-deploy@v0
  with:
    repoToken: '${{ secrets.GITHUB_TOKEN }}'
    firebaseServiceAccount: '${{ secrets.FIREBASE_SERVICE_ACCOUNT }}'
    projectId: reputationai-70092432
    channelId: live
```

---

## Manual Deployment (No GitHub Actions)

If you prefer not to use GitHub Actions:

```bash
# Deploy web app
./deploy-firebase.sh

# Or manually
firebase login
firebase deploy --only hosting
```

---

## Testing GitHub Actions Locally

Install act to test workflows locally:
```bash
brew install act  # macOS
# or
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run the workflow
act -j deploy
```

---

## Troubleshooting

### Token Expired
```bash
firebase logout
firebase login:ci
# Update the token in GitHub secrets
```

### Permission Denied
Make sure your Firebase account has:
- Owner or Editor role on the project
- Firebase Hosting enabled

### Workflow Not Running
- Check GitHub Actions tab for errors
- Verify secrets are set correctly
- Ensure workflow file is in `.github/workflows/`

---

## Current Status

✅ Workflow file created  
⚠️ **Action Required**: Add `FIREBASE_TOKEN` secret to GitHub  

Once the secret is added, every push to `main` will automatically deploy your app!
