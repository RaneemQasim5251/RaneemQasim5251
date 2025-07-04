# 🚀 Dynamic GitHub Profile Setup Guide

This repository contains a dynamic GitHub profile generator that automatically updates your profile README with live GitHub statistics in a beautiful terminal-style format.

## 📋 Features

- **🖥️ Terminal-style design** with authentic command prompts
- **🌓 Dark/Light mode support** that adapts to GitHub theme
- **📊 Live GitHub statistics** (repos, stars, commits, followers)
- **🤖 Automatic updates** via GitHub Actions
- **🧠 Neural network ASCII art** for AI/tech aesthetic
- **🏆 Custom achievements** showcase

## 🛠️ Setup Instructions

### 1. Fork/Clone this Repository

```bash
git clone https://github.com/RaneemQasim5251/RaneemQasim5251.git
cd RaneemQasim5251
```

### 2. Customize Your Information

Edit `today.py` to update your personal information:

```python
# Line 313: Update your birth date
age_data, age_time = perf_counter(daily_readme, datetime.datetime(1995, 1, 1))  # Change this date

# Update achievements in the SVG generation functions (lines 130-200)
# Modify achievements.txt section to reflect your accomplishments
```

### 3. Set Up GitHub Token (Optional)

For live statistics, you'll need a GitHub Personal Access Token:

1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate a new token with these permissions:
   - `read:user` - Read user profile information
   - `repo` - Access repository information
3. Add the token to your repository secrets as `GITHUB_TOKEN`

### 4. Enable GitHub Actions

1. Go to your repository Settings > Actions > General
2. Enable "Allow all actions and reusable workflows"
3. Save changes

### 5. Manual Run (Optional)

To test locally or run manually:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export ACCESS_TOKEN=your_github_token_here
export USER_NAME=your_username_here

# Run the script
python today.py
```

## 🎨 Customization Options

### Achievements Section

Update the achievements in the SVG generation functions:

```python
# In create_dark_mode_svg() and create_light_mode_svg()
<tspan class="highlight">🏆 Your Achievement:</tspan> <tspan class="value">Your Description</tspan>
<tspan class="highlight">🤖 Your Project:</tspan> <tspan class="value">Your Project Name</tspan>
<tspan class="highlight">💓 Your Research:</tspan> <tspan class="value">Your Research Topic</tspan>
<tspan class="highlight">🇸🇦 Your Impact:</tspan> <tspan class="value">Your Contribution</tspan>
```

### Colors and Styling

Modify the CSS classes in the SVG generation functions:

```python
# Dark mode colors
.key { fill: #ffd700; }      # Gold for keys
.value { fill: #7dd3fc; }    # Light blue for values
.highlight { fill: #3fb950; } # Green for highlights
.comment { fill: #8b949e; }  # Gray for comments
.prompt { fill: #ffd700; }   # Gold for prompts
```

### ASCII Art

The neural network ASCII art can be modified in the SVG generation functions around lines 145-175.

## 🔧 Troubleshooting

### SVG Not Displaying

1. **Check GitHub Actions**: Ensure the workflow is running successfully
2. **Verify token permissions**: Make sure your GitHub token has the correct permissions
3. **Clear browser cache**: Sometimes GitHub CDN caches old versions

### API Rate Limits

The script includes error handling for GitHub API rate limits. If you hit limits:

- Wait for the limit to reset (usually 1 hour)
- Reduce the frequency of updates in the workflow
- Use a more specific token with only required permissions

### Manual Update

If automatic updates aren't working, you can trigger a manual update:

1. Go to Actions tab in your repository
2. Click "Update GitHub Profile" workflow
3. Click "Run workflow" button

## 📊 Statistics Included

- **Repositories**: Total public repositories
- **Stars**: Total stars earned across all repositories
- **Commits**: Total commits made this year
- **Followers**: Current follower count
- **Age**: Dynamically calculated age
- **Custom achievements**: Your personal accomplishments

## 🕐 Update Schedule

The profile automatically updates daily at midnight UTC. You can modify this in `.github/workflows/update-profile.yml`:

```yaml
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight UTC
    # - cron: '0 */6 * * *'  # Every 6 hours
    # - cron: '0 9 * * 1'    # Every Monday at 9 AM
```

## 🎉 Final Result

Your GitHub profile will display a beautiful terminal-style interface showing:

- **Terminal window** with realistic command prompts
- **Neural network ASCII art** for the AI aesthetic
- **Live GitHub statistics** updated automatically
- **Personal achievements** and accomplishments
- **Professional motto** and information
- **Automatic theme switching** between dark and light modes

## 🐛 Issues and Support

If you encounter any issues:

1. Check the GitHub Actions logs for error messages
2. Verify your environment variables are set correctly
3. Ensure your GitHub token has the required permissions
4. Try running the script locally to debug

## 🌟 Credits

Inspired by [Andrew Grant's dynamic GitHub profile](https://github.com/Andrew6rant/Andrew6rant), adapted for AI/tech professionals with terminal-style aesthetics.

---

**Happy coding! 🚀** 