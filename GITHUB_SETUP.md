# GitHub Repository Setup Guide

Step-by-step instructions for publishing this project to GitHub.

## Prerequisites

- GitHub account
- Git installed locally
- Project files ready (✅ Complete!)

---

## Step 1: Create GitHub Repository

### Option A: Via GitHub Website

1. Go to https://github.com/new
2. Fill in repository details:
   - **Repository name**: `Differential-Gene-Expression`
   - **Description**: `Interactive web dashboard for differential gene expression analysis from RNA-seq data`
   - **Visibility**: Public (recommended) or Private
   - **Initialize**: 
     - ❌ Do NOT add README (we have one)
     - ❌ Do NOT add .gitignore (we have one)
     - ❌ Do NOT add license (we have one)
3. Click "Create repository"

### Option B: Via GitHub CLI

```bash
gh repo create Differential-Gene-Expression --public \
  --description "Interactive web dashboard for differential gene expression analysis" \
  --source=. \
  --push
```

---

## Step 2: Initial Git Setup (if not already done)

```bash
# Navigate to project directory
cd Differential-Gene-Expression

# Initialize git (if not already initialized)
git init

# Add all files
git add .

# Create initial commit
git commit -m "feat: initial commit - complete dashboard v2.0.0"
```

---

## Step 3: Connect to GitHub

```bash
# Add remote (replace 'yourusername' with your GitHub username)
git remote add origin https://github.com/yourusername/Differential-Gene-Expression.git

# Verify remote
git remote -v

# Push to GitHub
git push -u origin main
```

If using `master` branch instead of `main`:
```bash
# Rename branch to main (recommended)
git branch -M main
git push -u origin main
```

---

## Step 4: Configure Repository Settings

### A. About Section

1. Go to repository homepage
2. Click ⚙️ (gear icon) next to "About"
3. Add:
   - **Description**: `Interactive web dashboard for differential gene expression analysis`
   - **Website**: (leave empty or add GitHub Pages URL later)
   - **Topics**: `bioinformatics`, `genomics`, `rna-seq`, `data-visualization`, `streamlit`, `python`, `differential-expression`
   - ✅ **Releases**
   - ✅ **Packages**
4. Save changes

### B. Repository Settings

Go to Settings tab:

#### General
- ✅ **Allow issues**
- ✅ **Allow discussions** (recommended)
- ❌ **Allow projects** (optional)
- ❌ **Allow wiki** (we have docs/)

#### Features
- ✅ **Discussions** - Enable for community Q&A
- ✅ **Sponsorships** - Optional

#### Pull Requests
- ✅ **Allow squash merging**
- ✅ **Allow merge commits**
- ✅ **Allow rebase merging**
- ✅ **Automatically delete head branches**

### C. Branch Protection (for `main` branch)

1. Go to Settings → Branches
2. Add rule for `main`:
   - ✅ **Require pull request before merging**
   - ✅ **Require status checks to pass**
   - ✅ **Require branches to be up to date**
   - ✅ **Include administrators** (optional)

---

## Step 5: Set Up GitHub Actions

GitHub Actions are already configured in `.github/workflows/`:
- ✅ `tests.yml` - Runs tests on push/PR
- ✅ `lint.yml` - Checks code quality

### Verify Workflows

1. Go to "Actions" tab
2. You should see two workflows
3. They will run on next push/PR

---

## Step 6: Add Repository Secrets (if needed)

For future CI/CD (PyPI deployment, etc.):

1. Go to Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add secrets as needed:
   - `PYPI_API_TOKEN` (for future PyPI releases)
   - `CODECOV_TOKEN` (for code coverage)

---

## Step 7: Create First Release

### Tag the Current Version

```bash
# Create and push tag
git tag -a v2.0.0 -m "Release version 2.0.0 - Enhanced Dashboard"
git push origin v2.0.0
```

### Create GitHub Release

1. Go to "Releases" → "Create a new release"
2. Choose tag: `v2.0.0`
3. Release title: `v2.0.0 - Enhanced Dashboard`
4. Description: Copy from `CHANGELOG.md`
5. ✅ **Set as the latest release**
6. Publish release

---

## Step 8: Update Repository URLs

Update these files with your actual GitHub username:

### Files to Update

1. **README.md**
```markdown
Replace all instances of:
https://github.com/yourusername/Differential-Gene-Expression
with:
https://github.com/YOURACTUALUSERNAME/Differential-Gene-Expression
```

2. **setup.py**
```python
url="https://github.com/YOURACTUALUSERNAME/Differential-Gene-Expression"
```

3. **CONTRIBUTING.md**
```markdown
https://github.com/YOURACTUALUSERNAME/Differential-Gene-Expression
```

### Batch Replace (Linux/macOS)

```bash
# Replace all instances
find . -type f -name "*.md" -o -name "*.py" | \
  xargs sed -i 's/yourusername/YOURACTUALUSERNAME/g'

# Commit changes
git add .
git commit -m "docs: update repository URLs"
git push
```

### Manual Replace (Windows)

Use Find & Replace in your editor:
- Find: `yourusername`
- Replace: `YOURACTUALUSERNAME`
- Files: `*.md`, `*.py`

---

## Step 9: Create GitHub Pages (Optional)

For documentation hosting:

1. Go to Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main`, folder: `/docs`
4. Save

Your docs will be available at:
`https://YOURUSERNAME.github.io/Differential-Gene-Expression/`

---

## Step 10: Set Up Issue Templates

Create `.github/ISSUE_TEMPLATE/`:

### Bug Report Template

Create `.github/ISSUE_TEMPLATE/bug_report.md`:

```markdown
---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: 'bug'
assignees: ''
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Upload file '...'
2. Select columns '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
 - OS: [e.g. Windows 10]
 - Python Version: [e.g. 3.10.5]
 - Dashboard Version: [e.g. 2.0.0]

**Additional context**
Add any other context about the problem here.
```

### Feature Request Template

Create `.github/ISSUE_TEMPLATE/feature_request.md`:

```markdown
---
name: Feature request
about: Suggest an idea for this project
title: '[FEATURE] '
labels: 'enhancement'
assignees: ''
---

**Is your feature request related to a problem?**
A clear and concise description.

**Describe the solution you'd like**
What you want to happen.

**Describe alternatives you've considered**
Alternative solutions or features.

**Additional context**
Add any other context or screenshots.
```

---

## Step 11: Add Badges to README

Update README.md with actual badge URLs:

```markdown
[![Tests](https://github.com/YOURUSERNAME/Differential-Gene-Expression/workflows/Tests/badge.svg)](https://github.com/YOURUSERNAME/Differential-Gene-Expression/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
```

---

## Step 12: Promote Your Repository

### README Enhancements

Add these sections to README.md if desired:
- **Star History** chart
- **Contributors** section with avatars
- **Used By** section (as project grows)
- **Sponsors** section (if applicable)

### Social Promotion

- Share on Twitter/X with hashtags: #bioinformatics #rnaseq #streamlit
- Post on Reddit: r/bioinformatics, r/Python
- Share on LinkedIn
- Add to awesome lists (e.g., awesome-streamlit)

### Submit to Directories

- [Streamlit Gallery](https://streamlit.io/gallery)
- [Made with Streamlit](https://github.com/streamlit/streamlit/issues/new?assignees=&labels=app-submission&template=app_submission.yml)
- [Bioconda](https://bioconda.github.io/) (for package submission)

---

## Step 13: Monitor and Maintain

### Set Up Notifications

1. Watch your repository (top right)
2. Custom: All activity
3. Enable mobile notifications (GitHub app)

### Regular Maintenance

- **Weekly**: Check and respond to issues
- **Monthly**: Update dependencies
- **Quarterly**: Review and update documentation
- **Yearly**: Major version updates

### Analytics

Track repository insights:
- Go to Insights tab
- Monitor:
  - Traffic (views, clones)
  - Community (issues, PRs)
  - Commits
  - Dependencies

---

## Troubleshooting

### Issue: "Permission denied (publickey)"

**Solution:**
```bash
# Use HTTPS instead of SSH
git remote set-url origin https://github.com/YOURUSERNAME/Differential-Gene-Expression.git

# Or set up SSH keys
ssh-keygen -t ed25519 -C "your.email@example.com"
# Add to GitHub: Settings → SSH and GPG keys
```

### Issue: "Failed to push some refs"

**Solution:**
```bash
# Pull first
git pull origin main --rebase

# Then push
git push origin main
```

### Issue: Large file error

**Solution:**
```bash
# Remove from git
git rm --cached large_file.csv

# Add to .gitignore
echo "large_file.csv" >> .gitignore

# Commit
git add .gitignore
git commit -m "chore: remove large file"
git push
```

---

## Checklist

Before publicizing:

- [ ] All files committed and pushed
- [ ] Repository URLs updated
- [ ] README.md complete with badges
- [ ] LICENSE file present
- [ ] CONTRIBUTING.md in place
- [ ] Issue templates created
- [ ] GitHub Actions working
- [ ] First release created
- [ ] Topics/tags added
- [ ] Description set
- [ ] Tests passing
- [ ] Documentation complete
- [ ] Screenshots added
- [ ] Example data included

---

## Quick Command Reference

```bash
# Check status
git status

# Stage all changes
git add .

# Commit
git commit -m "type: description"

# Push
git push origin main

# Create tag
git tag -a v2.0.0 -m "Release v2.0.0"
git push origin v2.0.0

# Create branch
git checkout -b feature/new-feature

# Merge branch
git checkout main
git merge feature/new-feature
git push origin main
```

---

## Next Steps After Setup

1. **Announce**: Share on social media
2. **Document**: Add more examples
3. **Engage**: Respond to issues
4. **Improve**: Based on feedback
5. **Release**: Regular updates

---

**Your repository is now ready for the world!** 🚀

Good luck with your project! 🧬✨


