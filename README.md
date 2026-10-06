# Portfolio: Ifeoluwanimi Praise Shobayo

Personal portfolio website for an MSPH Epidemiology candidate. It's plain HTML, CSS, and a small amount of JavaScript, with no build step.

## Structure

- `index.html`: home page with an intro, research posters, projects, experience, publications, honors, skills, education, and contact
- `projects/`: one page per case study
- `assets/style.css`: shared styles, with light and dark mode
- `assets/charts.js`: small inline-SVG chart helpers (estimate + CI, line, and bar charts with hover tooltips)
- `assets/img/`: poster images and map screenshots

## Publish with GitHub Pages

1. Merge this branch into `main`.
2. In the repository, go to **Settings → Pages**, set **Source** to "Deploy from a branch", then choose `main` and `/ (root)`.
3. The site will be live at `https://adebowa96.github.io/Research/` within a few minutes.

## Updating the site

- **Add a downloadable CV:** save it as `resume.pdf` in the root folder, then add `<a class="btn ghost" href="resume.pdf">Download CV</a>` to the hero buttons in `index.html`. Consider removing your phone number from the public copy.
- **Add a project:** copy any page in `projects/`, edit the text, and add a card for it in `index.html`.
- **Charts:** each chart is a `Charts.forest`, `Charts.line`, or `Charts.hbar` call at the bottom of its page. The numbers in those calls should match the table shown beside the chart.
