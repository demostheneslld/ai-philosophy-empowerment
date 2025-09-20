# Contributing to The Empowerment Economy

Thank you for helping shape the Empowerment Economy manifesto. The project is intentionally lightweight so policy makers, organisers, researchers, and curious readers can all participate without a heavy toolchain.

## Ways to contribute

- **Draft or extend manifesto chapters.** Deepen arguments, add case studies, or propose counter-arguments that sharpen the ideas.
- **Develop policy notes.** Translate principles into implementation guides, governance models, or funding mechanisms.
- **Map philosophical touchstones.** Add historical parallels, critiques, or references that broaden the intellectual foundation.
- **Spot issues.** Open GitHub Issues for typos, unclear passages, missing links, or accessibility gaps.

No coding skills are required—everything is Markdown.

## Workflow overview

1. **Fork or branch.** Work from your own fork or a feature branch.
2. **Edit Markdown in `content/`.** Follow the front-matter template shown below.
3. **Push your changes.** Open a pull request so others can review.
4. **Let GitHub Actions publish.** Every PR and push to `main` runs the build script and deploys the static site, so there is nothing to compile or upload manually.

GitHub’s web editor supports the full workflow: click the pencil icon on a file, make changes, and let the interface guide you through the pull request.

### Optional local preview

If you want to see the rendered HTML before opening a PR, run:

```bash
python scripts/build.py
```

The command writes output to a local `docs/` directory (ignored by git). Open `docs/index.html` in your browser to preview.

## Front-matter template

Each Markdown file begins with a short metadata block used for navigation and ordering:

```markdown
---
title: "Short Title"
category: "Manifesto Chapters"  # or Principles, Policy Architecture, etc.
order: 10                        # lower numbers float higher in lists
description: "One sentence shown on the index page."
---
```

- **`title`** appears at the top of the generated page.
- **`category`** groups related pieces on the index page. Feel free to suggest new categories in a pull request if the existing ones do not fit.
- **`order`** controls the sequence within a category (use whole numbers, decimals, or whatever fits).
- **`description`** is optional but helps readers decide what to open next.

## Writing guidelines

- Prefer clear, direct language. Assume readers may be encountering these ideas for the first time.
- Link to other sections using standard Markdown links if helpful (for example, `[see Principles](manifesto-05-principles.html)`).
- Cite external references inline. Example: `Rawls, *A Theory of Justice* (1971).`
- Keep formatting simple: headings, lists, and paragraphs render cleanly. Bold (`**text**`), italics (`*text*`), and inline code (``code``) are supported.
- When adding new policy proposals, describe implementation steps, risks, and open questions to invite collaboration.

## Proposing structure changes

If you want to:

- Introduce a new category
- Reorganise existing sections
- Change the navigation or build tooling

Open an Issue or Draft Pull Request summarising the idea before doing large-scale edits. Collective discussion keeps the structure coherent.

## Code of conduct

This project follows a simple rule: contribute in good faith. Discrimination, harassment, or manipulation of collaborators is not tolerated. If a problem arises, email the maintainers or open a confidential issue.

## Licence agreement

By contributing, you agree that your work will be released under the MIT Licence alongside the rest of the repository.

Thank you for making the Empowerment Economy a richer, more resilient framework.
