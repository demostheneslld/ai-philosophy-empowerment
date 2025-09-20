# The Empowerment Economy

The Empowerment Economy is a community-managed manifesto, philosophy, and policy playbook for the AI age. It documents how universal guarantees, distributed intelligence, and personal agency can replace the collapsing social contract of the 20th century.

The repository stays radically simple: contributors only touch Markdown in `content/`. A GitHub Actions workflow renders everything into minimalist HTML, copies shared assets, and publishes the result with GitHub Pages. No local tooling or manual build steps are required, though an optional script is available if you want to preview changes offline.

## How it works

- **Write Markdown.** Add or edit files under `content/` using the front-matter template described in `CONTRIBUTING.md`.
- **Open a pull request.** The workflow runs on every PR and push to `main`, rendering the site, generating a sitemap and `llms.txt`, and surfacing build results automatically.
- **Automatic publishing.** When changes land on `main`, the workflow deploys the generated HTML to GitHub Pages. The latest manifesto is always live without extra steps.

## Optional local preview

If you prefer to check your changes before pushing, run the bundled script:

```bash
python scripts/build.py
```

It converts Markdown to HTML inside a local `docs/` directory (ignored by git). Open `docs/index.html` in your browser to preview.

Configuration lives in `scripts/config.py`. Adjust `SITE_BASE_URL` if you host the site somewhere other than GitHub Pages, and update `REPO_URL` if the repository moves.

## Customising the look

- Global styles live in `scripts/resources/style.css`. Tweak colours, spacing, or typography there and rerun the build.
- The placeholder favicon is `scripts/resources/favicon.svg`. Replace it with any SVG and rebuild.
- Additional static assets can be dropped into `scripts/resources/`; they are copied verbatim into the published site.

## Repository layout

- `content/` – Source Markdown organised by category with front-matter metadata.
- `scripts/build.py` – Dependency-free static site generator used by CI and optional local previews.
- `scripts/config.py` – Base URL and repository constants used during the build.
- `scripts/resources/` – Shared assets (CSS, favicon, etc.) copied into the published site.
- `.github/workflows/publish.yml` – GitHub Actions workflow that builds, generates supporting files (`sitemap.xml`, `llms.txt`), and deploys the site.
- `LICENSE` – MIT Licence so the ideas stay open and remixable.

## Publishing setup

1. Push this repository to GitHub (for example `https://github.com/demostheneslld/ai-philosophy-empowerment`).
2. In **Settings → Pages**, choose **GitHub Actions** as the build source (one-time step).
3. Merge to `main` and the workflow will deploy automatically. The published URL appears in the workflow summary under the `github-pages` environment.

## Licence

Released under the MIT Licence. Contributions are accepted under the same terms so the project remains open source and remix-friendly.
