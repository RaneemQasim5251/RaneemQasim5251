# GitHub Profile Setup Guide

## Overview
This repository contains a dynamic GitHub profile generator that creates SVG files with ASCII art on the left and terminal interface on the right, displaying real-time GitHub statistics.

## Features
- **ASCII Art**: Green matrix-style art positioned on the left
- **Terminal Interface**: Interactive terminal display on the right
- **Real-time Stats**: GitHub repos, stars, commits, followers
- **Dual Theme**: Dark and light mode support
- **Professional Layout**: Clean, modern design with proper spacing

## Setup Instructions

### 1. Environment Variables
Create a `.env` file in your local development environment (DO NOT commit to repository):

```bash
export ACCESS_TOKEN='your_github_personal_access_token_here'
export USER_NAME='RaneemQasim5251'
```

### 2. GitHub Personal Access Token
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with these permissions:
   - `public_repo`
   - `read:user`
   - `read:org`
3. Copy the token and add it to your environment

### 3. GitHub Actions (Recommended)
For automated updates, add these secrets to your GitHub repository:
1. Go to Settings → Secrets and variables → Actions
2. Add repository secrets:
   - `ACCESS_TOKEN`: Your GitHub personal access token
   - `USER_NAME`: Your GitHub username

### 4. Manual Generation
Run locally with environment variables:
```bash
# Set environment variables
export ACCESS_TOKEN='your_token_here'
export USER_NAME='RaneemQasim5251'

# Generate SVG files
python today.py
```

### 5. GitHub Repository Setup
1. Create a repository named exactly as your GitHub username: `RaneemQasim5251`
2. Add the `README.md` file with proper SVG references
3. Ensure the repository is public
4. Files should be in the main branch

## File Structure
```
RaneemQasim5251/
├── README.md           # Profile display file
├── today.py           # SVG generator script
├── dark_mode.svg      # Generated dark theme SVG
├── light_mode.svg     # Generated light theme SVG
├── requirements.txt   # Python dependencies
└── SETUP.md          # This setup guide
```

## SVG Specifications
- **Dimensions**: 1000x600 pixels
- **ASCII Art**: Font size 7px, positioned at x=15
- **Terminal**: Font size 16px, positioned at x=520
- **Colors**: GitHub-compatible color scheme
- **Spacing**: Optimized for readability

## Troubleshooting

### Common Issues:
1. **401 Bad Credentials**: Check your GitHub token and environment variables
2. **SVG Not Displaying**: Ensure repository is public and files are in main branch
3. **Old Data**: GitHub may cache images, add `?v=timestamp` to force refresh
4. **Layout Issues**: Verify SVG dimensions and positioning

### GitHub Profile Not Updating:
1. Check that your repository name matches your username exactly
2. Ensure README.md is in the root directory
3. Make sure the repository is public
4. Try adding a cache-busting parameter to image URLs

## Manual Testing
Test your setup locally:
```bash
# Verify environment variables
echo $ACCESS_TOKEN
echo $USER_NAME

# Test API connectivity
curl -H "Authorization: token $ACCESS_TOKEN" https://api.github.com/user

# Generate SVG files
python today.py

# Check generated files
ls -la *.svg
```

## Dependencies
Install required packages:
```bash
pip install -r requirements.txt
```

## GitHub Actions Workflow (Optional)
Create `.github/workflows/update-profile.yml` for automated updates:
```yaml
name: Update Profile
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Generate SVG
      env:
        ACCESS_TOKEN: ${{ secrets.ACCESS_TOKEN }}
        USER_NAME: ${{ secrets.USER_NAME }}
      run: python today.py
    - name: Commit files
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add -A
        git diff --staged --quiet || git commit -m "Update profile SVG files"
        git push
```

## Support
If you encounter issues:
1. Check this setup guide
2. Verify all environment variables are set
3. Test API connectivity
4. Ensure repository permissions are correct

---
*Profile last updated: Dynamic via GitHub Actions* 