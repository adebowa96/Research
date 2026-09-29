// Renders Fig 3 (geographic distribution of included studies) to figures/fig3_geographic_map.png
// Usage: cd scripts && npm install && node make_map.js
const fs = require("fs");
const path = require("path");
const topojson = require("topojson-client");
const d3 = require("d3-geo");
const isoCountries = require("i18n-iso-countries");
const { countries } = require("countries-list");

const data = JSON.parse(fs.readFileSync(path.join(__dirname, "data.json"), "utf8"));
const total = data.total_included;
const world = JSON.parse(
  fs.readFileSync(require.resolve("world-atlas/countries-110m.json"), "utf8")
);
const features = topojson.feature(world, world.objects.countries).features;

// Sequential single-hue ramp (light = few studies, dark = many)
const steps = ["#cde2fb", "#9ec5f4", "#6da7ec", "#2a78d6", "#104281"];
const maxN = Math.max(...data.regions.map((r) => r[1]));
// Map a count onto the ramp; 0 falls back to the no-data grey
const shade = (n) => (n > 0 ? steps[Math.min(steps.length - 1, Math.ceil((n / maxN) * steps.length) - 1)] : null);
const noData = "#e4e3df";
const countByContinent = {};
for (const [name, n, code] of data.regions) countByContinent[code] = { name, n };

function continentOf(f) {
  const a2 = isoCountries.numericToAlpha2(String(f.id).padStart(3, "0"));
  if (a2 && countries[a2]) return countries[a2].continent;
  // A few 110m features have no ISO numeric id
  const byName = { Kosovo: "EU", "N. Cyprus": "AS", Somaliland: "AF" };
  return byName[f.properties.name] || null;
}

const W = 1600, H = 820;
const projection = d3.geoNaturalEarth1().fitExtent(
  [[20, 20], [W - 20, H - 20]],
  { type: "FeatureCollection", features: features.filter((f) => f.properties.name !== "Antarctica") }
);
const geoPath = d3.geoPath(projection);

let paths = "";
for (const f of features) {
  if (f.properties.name === "Antarctica") continue;
  const c = continentOf(f);
  const entry = c && countByContinent[c];
  const fill = (entry && shade(entry.n)) || noData;
  // France's feature includes French Guiana; shade that polygon with South America
  if (f.properties.name === "France" && f.geometry.type === "MultiPolygon") {
    for (const poly of f.geometry.coordinates) {
      const part = { type: "Polygon", coordinates: poly };
      const lon = d3.geoCentroid(part)[0];
      const partFill = lon < -30 ? (shade(countByContinent.SA.n) || noData) : fill;
      paths += `<path d="${geoPath(part)}" fill="${partFill}" stroke="#ffffff" stroke-width="0.6"/>`;
    }
    continue;
  }
  paths += `<path d="${geoPath(f)}" fill="${fill}" stroke="#ffffff" stroke-width="0.6"/>`;
}

// Label anchors [lon, lat] placed over each continent's landmass
const anchors = { EU: [-32, 44], NA: [-102, 45], AS: [95, 40], AF: [20, 5], SA: [-60, -16] };
let labels = "";
for (const [name, n, code] of data.regions) {
  if (!anchors[code] || n === 0) continue;
  const [x, y] = projection(anchors[code]);
  const pct = Math.round((n / total) * 100);
  const dark = n / maxN >= 0.5;
  const ink = dark ? "#ffffff" : "#0b0b0b";
  if (code === "EU") {
    const [tx, ty] = projection([8, 49]);
    labels += `<line x1="${(x + 120).toFixed(1)}" y1="${y.toFixed(1)}" x2="${tx.toFixed(1)}" y2="${ty.toFixed(1)}" stroke="#0d366b" stroke-width="2.5"/><circle cx="${tx.toFixed(1)}" cy="${ty.toFixed(1)}" r="5" fill="#0d366b"/>`;
  }
  labels += `
    <g transform="translate(${x.toFixed(1)},${y.toFixed(1)})">
      <rect x="-120" y="-50" width="240" height="100" rx="12" fill="${dark ? "#0d366b" : "#ffffff"}" fill-opacity="${dark ? 0.85 : 0.92}" stroke="#0d366b" stroke-width="1.5"/>
      <text x="0" y="-10" text-anchor="middle" font-size="31" font-weight="600" fill="${ink}">${name}</text>
      <text x="0" y="33" text-anchor="middle" font-size="38" font-weight="700" fill="${ink}">n = ${n} (${pct}%)</text>
    </g>`;
}

const zero = data.regions.filter((r) => r[1] === 0).map((r) => r[0]);
const intl = data.regions.find((r) => r[2] === "INT");
const legendNote = [`No included studies${zero.length ? " (" + zero.join(", ") + ", Oceania)" : " (Oceania)"}`,
  intl && intl[1] ? `${intl[1]} multinational studies not mapped` : "", "Darker = more studies"]
  .filter(Boolean).join(". ") + ".";

const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" font-family="Arial, Helvetica, sans-serif">
  <rect width="${W}" height="${H}" fill="#ffffff"/>
  ${paths}
  ${labels}
  <g transform="translate(40,${H - 60})">
    <rect y="-4" width="30" height="30" fill="${noData}" stroke="#9a9993"/>
    <text x="36" y="20" font-size="26" fill="#52514e">${legendNote}</text>
  </g>
</svg>`;

const outDir = path.join(__dirname, "..", "figures");
fs.writeFileSync(path.join(outDir, "fig3_geographic_map.svg"), svg);

(async () => {
  const { chromium } = require("/opt/node22/lib/node_modules/playwright");
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 2 });
  await page.setContent(`<html><body style="margin:0">${svg}</body></html>`);
  await page.locator("svg").screenshot({ path: path.join(outDir, "fig3_geographic_map.png") });
  await browser.close();
  console.log("wrote figures/fig3_geographic_map.png");
})();
