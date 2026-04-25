# My Food Blog

A personal food blog built with [Hugo](https://gohugo.io/) and deployable to GitHub Pages.

## Local development

### One-time setup

1. Install Hugo (extended edition):
   - Windows (winget): `winget install Hugo.Hugo.Extended`
   - macOS (Homebrew): `brew install hugo`
   - Linux (snap): `snap install hugo`
   - Or download from [Hugo releases](https://github.com/gohugoio/hugo/releases)
2. Verify install:

```bash
hugo version
```

### Run locally

```bash
hugo server --buildDrafts
```

Site runs at `http://localhost:1313` with live reload.

### Create a post

```bash
hugo new content posts/my-new-recipe.md
```

## Writing posts

Posts live in `content/posts/`.

Example frontmatter:

```yaml
---
title: "My Amazing Recipe"
date: 2026-04-14
draft: false
description: "A short summary for cards and search results."
thumbnail: "/images/my-photo.jpg"
tags: ["italian", "pasta", "quick"]
---
```

### Images

- Put image files in `static/images/`
- Reference them as `/images/filename.jpg`
- Use normal Markdown in body content, for example `![Alt text](/images/filename.jpg)`

## GitHub Pages deployment

This repo includes [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml), which:

- Builds with Hugo Extended
- Runs Pagefind search indexing
- Deploys the `public/` artifact using official GitHub Pages actions

It is configured to work for both:

- User site: `https://mageden.github.io/`
- Project site: `https://mageden.github.io/food-blog/`

### One-time setup on GitHub

1. Create a GitHub repo and push this project.
2. In GitHub, open `Settings -> Pages`.
3. Set `Build and deployment -> Source` to `GitHub Actions`.
4. Ensure your default branch matches the workflow trigger (`main` by default in `.github/workflows/deploy.yml`).

### Required edit before publishing

Set the site URL in `hugo.toml`:

- User site repo named `mageden.github.io`:
  - `baseURL = 'https://mageden.github.io/'`
- Project site repo named `food-blog`:
  - `baseURL = 'https://mageden.github.io/food-blog/'`

Then commit and push.

### Deploy flow

- Every push to `main` triggers deployment.
- You can also run it manually from `Actions -> Deploy Hugo to GitHub Pages -> Run workflow`.
- After first successful run, open the URL shown in the `deploy` job output.

### Custom domain (optional)

If you use a custom domain, add a `static/CNAME` file with your domain and configure DNS in GitHub Pages settings.

## Project structure

```text
content/
  posts/                     # Blog posts
  search.md                  # Search page
static/
  images/                    # Static images
layouts/                     # Hugo templates
assets/css/                  # Styles
archetypes/                  # New-post template
hugo.toml                    # Hugo config
.github/workflows/deploy.yml # CI/CD deployment workflow
```
