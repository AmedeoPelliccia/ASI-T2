# Deployment Configuration

## Deployment Method

This repository uses **GitHub Pages** for static site deployment, **NOT Vercel**.

### GitHub Pages Deployment

- **Workflow**: `.github/workflows/pages.yml` and `.github/workflows/static.yml`
- **Build Script**: `scripts/ghpages_build.py`
- **Output Directory**: `_site/` (generated, not committed)
- **Trigger**: Automatic on push to `main` or `master` branches
- **Configuration**: `pages.manifest.yaml`

### Vercel Configuration

The following files explicitly disable Vercel deployment:

- **`vercel.json`**: Disables Vercel GitHub integration
- **`.vercelignore`**: Ignores all files to prevent accidental deployment

## Why Not Vercel?

This repository is designed for GitHub Pages deployment because:

1. It generates static CAD and S1000D content viewers
2. The build process uses Python scripts optimized for GitHub Actions
3. All CI/CD workflows are configured for GitHub Actions
4. The repository structure and output format are tailored for GitHub Pages

## Vercel Bot Notifications

If you see Vercel bot notifications (e.g., deployment failures) in issues or pull requests:

1. These can be safely **ignored** - they indicate Vercel is trying to deploy but failing
2. The `vercel.json` configuration should prevent future deployments
3. Repository administrators should **remove the Vercel integration** from repository settings:
   - Go to: Repository Settings → Integrations → Vercel
   - Remove or disconnect the Vercel application

## Local Testing

To test the site locally:

```bash
# Build the site
python scripts/ghpages_build.py

# Serve locally
python -m http.server -d _site 8080

# Visit http://localhost:8080/
```

## See Also

- [README-PAGES.md](./README-PAGES.md) - Detailed GitHub Pages documentation
- [.github/workflows/pages.yml](./.github/workflows/pages.yml) - GitHub Pages workflow
- [scripts/ghpages_build.py](./scripts/ghpages_build.py) - Build script
