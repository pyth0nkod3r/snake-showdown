# Render Deployment Setup Guide

This guide explains how to configure the CI/CD pipeline for automatic deployment to Render after tests pass.

## Current Behavior

The CI/CD pipeline now includes:

- ✅ **Backend tests** run automatically on every push to main
- ✅ **Frontend tests** run automatically on every push to main
- ✅ **Deployment** only triggers if all tests pass

## Deployment Options

You have two options for deployment:

### Option 1: Deploy Hook (Recommended)

This approach gives you full control - tests must pass before deployment happens.

**Setup Steps:**

1. **Get Deploy Hook URL from Render:**

   - Go to [Render Dashboard](https://dashboard.render.com)
   - Navigate to your `snake-showdown` service
   - Click **Settings** in the left sidebar
   - Scroll down to **Deploy Hook** section
   - Click **Create Deploy Hook**
   - Copy the generated URL (it will look like: `https://api.render.com/deploy/srv-xxxxx?key=xxxxx`)

2. **Add Secret to GitHub:**

   - Go to your GitHub repository
   - Navigate to **Settings** → **Secrets and variables** → **Actions**
   - Click **New repository secret**
   - Name: `RENDER_DEPLOY_HOOK_URL`
   - Value: Paste the deploy hook URL from step 1
   - Click **Add secret**

3. **Update render.yaml (Optional but Recommended):**
   - Set `autoDeploy: false` in `render.yaml` (line 11)
   - This prevents Render from deploying on every git push, ensuring only GitHub Actions can trigger deployments

**Result:** Deployments only happen when you push to main AND all tests pass. Full control via CI/CD.

---

### Option 2: Auto-Deploy (Current Default)

Keep the current setup where Render automatically deploys on every push to the main branch.

**Current Configuration:**

- `render.yaml` has `autoDeploy: true` (line 11)

**Pros:**

- ✅ No additional setup required
- ✅ Simple and automatic

**Cons:**

- ⚠️ Deployment happens even if local changes haven't been tested
- ⚠️ Cannot prevent deployment from GitHub Actions (Render watches the Git repository directly)

**Note:** Even with this option, the CI/CD pipeline will still run tests and report failures, but it won't prevent Render from deploying.

---

## Testing Your Setup

After configuring Option 1 or keeping Option 2:

1. **Make a test change:**

   ```bash
   # Create a test branch
   git checkout -b test-ci-pipeline

   # Make a small change (e.g., update README.md)
   echo "Testing CI/CD" >> README.md

   # Commit and push
   git add README.md
   git commit -m "test: verify CI/CD pipeline"
   git push origin test-ci-pipeline
   ```

2. **Create a Pull Request:**

   - Go to GitHub and create a PR from `test-ci-pipeline` to `main`
   - Check the **Actions** tab to see tests running
   - Verify both backend and frontend tests complete

3. **Merge and Deploy:**
   - Merge the PR to main
   - Check the **Actions** tab again
   - Verify the deploy job runs (if using Option 1)
   - Check [Render Dashboard](https://dashboard.render.com) for deployment status

## Workflow Status

You can view the CI/CD pipeline status:

- **GitHub Actions Tab:** See all workflow runs and job details
- **Pull Requests:** See test results inline before merging
- **Render Dashboard:** Monitor deployment progress and logs

## Troubleshooting

### Tests fail but deployment still happens

- You're likely using Option 2 (auto-deploy)
- Switch to Option 1 for proper CI/CD control

### Deploy job shows "RENDER_DEPLOY_HOOK_URL secret not configured"

- This is expected if you haven't set up the secret yet
- Follow Option 1 setup steps above
- Or continue using Option 2 (auto-deploy via Git)

### Deploy hook returns HTTP error

- Verify the deploy hook URL is correct
- Check that the secret in GitHub matches exactly (no extra spaces)
- Regenerate the deploy hook in Render if needed

### Pipeline runs on every branch

- Currently configured for `main` branch only
- To run tests on all PRs, add to workflow:
  ```yaml
  on:
    push:
      branches: [main]
    pull_request:
      branches: [main]
  ```

## Questions?

If you encounter issues or need to customize the pipeline further, refer to:

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Render Deploy Hooks Documentation](https://render.com/docs/deploy-hooks)
