# GitHub Repository Setup for PAID LLC Website

This guide explains how to set up your GitHub repository and deploy your PAID LLC website to GitHub Pages.

## Prerequisites

1. **GitHub Account**: You already have the username `ArtiIntel1955`
2. **Git Installed**: Ensure Git is installed on your system
3. **Personal Access Token (PAT)**: Required for authentication

## Step 1: Create a GitHub Personal Access Token

1. Go to GitHub Settings
2. Navigate to "Developer settings" > "Personal access tokens" > "Tokens (classic)"
3. Click "Generate new token"
4. Select the "public_repo" scope (for public repositories) or "repo" for private repositories
5. Click "Generate token"
6. **Important**: Copy the generated token immediately - you won't see it again!

## Step 2: Set Up Authentication

You have several options to provide the token:

### Option A: Environment Variable (Recommended)
```bash
export GITHUB_TOKEN="your_actual_token_here"
```

### Option B: OpenClaw Configuration
Add the token to your OpenClaw configuration file.

### Option C: Temporary Environment Variable
Set the token just for the current session before running the setup script.

## Step 3: Run the Setup Script

Once you have your token ready, run the setup script:

```bash
python setup_github_repo.py
```

This script will:
- Create a new git repository
- Copy your premium website files
- Initialize the repository with proper GitHub Pages files
- Push the content to `https://github.com/ArtiIntel1955/ArtiIntel1955.github.io`
- Deploy your site to `https://ArtiIntel1955.github.io/`

## Alternative Manual Setup

If you prefer to set up manually:

1. Create a new repository named `ArtiIntel1955.github.io` on GitHub
2. Clone the repository:
   ```bash
   git clone https://github.com/ArtiIntel1955/ArtiIntel1955.github.io.git
   cd ArtiIntel1955.github.io
   ```

3. Copy your website files:
   ```bash
   cp ../index_premium.html index.html
   touch .nojekyll  # Allow files/folders starting with underscore
   echo "User-agent: *\nAllow: /" > robots.txt
   ```

4. Commit and push:
   ```bash
   git add .
   git config user.name "ArtiIntel1955"
   git config user.email "artiintel1955@users.noreply.github.com"
   git commit -m "Initial commit: PAID LLC website"
   git branch -M main
   git push -u origin main
   ```

## Expected Outcome

Once completed, your website will be available at:
- Repository: https://github.com/ArtiIntel1955/ArtiIntel1955.github.io
- Live Site: https://ArtiIntel1955.github.io/

The site will feature your premium PAID LLC website with all the professional design elements we created.

## Troubleshooting

- If you get authentication errors, verify your token has the correct scopes
- If the site doesn't appear immediately, GitHub Pages may take a few minutes to activate
- Ensure your repository name follows the pattern `username.github.io`
- Make sure you're pushing to the `main` branch (or `master`)