# Hasbi's portfolio

A light, minimal portfolio and Markdown blog built with Eleventy and published with GitHub Pages.

## Local preview

Requirements: Node.js 20 or newer.

```text
npm install
npm run dev
```

The production build is written to `_site/`:

```text
npm run build
```

## Writing a blog post

Create a lowercase kebab-case Markdown file directly under `blogs/`, for example `blogs/building-reliable-services.md`.

```markdown
---
title: Building Reliable Services
date: 2026-08-23
tags:
  - dotnet
  - architecture
---

The first paragraph becomes the post summary and metadata description.

Continue the article here.
```

`title` and a valid `YYYY-MM-DD` date are required. `tags` is optional and accepts either one value or a list. The filename determines the URL. Raw HTML is disabled.

Run `npm run build` before publishing. The build stops with a clear error if a post has an invalid filename, missing title, or invalid date.

## Updating the CV

The CV source is `scripts/generate_cv.py`; the public PDF is `output/pdf/hasbi-cv.pdf`.

```text
python -m pip install -r requirements-cv.txt
python scripts/generate_cv.py
```

## Publishing

The GitHub Actions workflow builds and deploys `_site/` whenever `main` is updated. In the repository settings, choose **GitHub Actions** as the Pages source.

The initial public address is `https://hasmbly.github.io`.

After `hasmbly.is-a.dev` has been approved and its DNS record is active:

1. Verify the domain in the GitHub account Pages settings.
2. Add a `CNAME` file under `public/` containing only `hasmbly.is-a.dev`.
3. Set `hasmbly.is-a.dev` as the repository's Pages custom domain.
4. Enable **Enforce HTTPS**.

Do not add the `CNAME` file before the is-a.dev registration is merged, because doing so can redirect the working GitHub Pages address to an inactive domain.
