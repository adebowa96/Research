// Small inline-SVG chart helpers: forest (estimate + 95% CI), line, and horizontal bars.
// Each chart renders at its container's real width, re-renders on resize and on
// light/dark changes, and has a hover/focus tooltip. Values are also in a table on the page.
(function () {
  const NS = 'http://www.w3.org/2000/svg';
  const css = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();

  function el(tag, attrs, parent) {
    const node = document.createElementNS(NS, tag);
    for (const k in attrs) node.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(node);
    return node;
  }

  function text(parent, x, y, str, attrs) {
    const t = el('text', Object.assign({ x, y, fill: css('--muted'), 'font-size': 13 }, attrs || {}), parent);
    t.textContent = str;
    return t;
  }

  function niceTicks(min, max, count) {
    const span = max - min;
    const raw = span / count;
    const mag = Math.pow(10, Math.floor(Math.log10(raw)));
    const step = [1, 2, 2.5, 5, 10].map((m) => m * mag).find((s) => span / s <= count) || 10 * mag;
    const ticks = [];
    for (let v = Math.ceil(min / step) * step; v <= max + 1e-9; v += step) ticks.push(+v.toFixed(10));
    return ticks;
  }

  function tooltip(container) {
    let tip = container.querySelector('.chart-tip');
    if (!tip) {
      tip = document.createElement('div');
      tip.className = 'chart-tip';
      tip.hidden = true;
      container.appendChild(tip);
    }
    return {
      show(x, y, value, label) {
        tip.replaceChildren();
        const v = document.createElement('strong');
        v.textContent = value;
        const l = document.createElement('span');
        l.textContent = label;
        tip.append(v, l);
        tip.hidden = false;
        const w = container.clientWidth;
        const left = Math.min(Math.max(x - tip.offsetWidth / 2, 0), w - tip.offsetWidth);
        tip.style.left = left + 'px';
        tip.style.top = Math.max(y - tip.offsetHeight - 10, 0) + 'px';
      },
      hide() { tip.hidden = true; },
    };
  }

  function mount(selector, draw) {
    const container = document.querySelector(selector);
    if (!container) return;
    const render = () => {
      container.querySelectorAll('svg').forEach((s) => s.remove());
      draw(container, container.clientWidth);
    };
    render();
    let raf;
    window.addEventListener('resize', () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(render); });
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', render);
  }

  function hover(target, tip, getPos, value, label) {
    target.setAttribute('tabindex', '0');
    target.setAttribute('aria-label', label + ': ' + value);
    const on = () => { const p = getPos(); tip.show(p.x, p.y, value, label); target.classList.add('hot'); };
    const off = () => { tip.hide(); target.classList.remove('hot'); };
    target.addEventListener('pointerenter', on);
    target.addEventListener('pointerleave', off);
    target.addEventListener('focus', on);
    target.addEventListener('blur', off);
  }

  // rows: [{label, est, lo, hi, note}]
  function forest(selector, rows, opts) {
    mount(selector, (c, width) => {
      const accent = css('--accent'), surface = css('--surface'), grid = css('--border'), ink = css('--text');
      const stacked = width < 520;
      const labelW = stacked ? 0 : Math.min(170, width * 0.38);
      const m = { top: 8, right: 16, bottom: 40, left: labelW };
      const rowH = stacked ? 52 : 44;
      const h = m.top + rows.length * rowH + m.bottom;
      const lo = Math.min(0, ...rows.map((r) => r.lo)), hi = Math.max(0, ...rows.map((r) => r.hi));
      const pad = (hi - lo) * 0.08;
      const x0 = lo - pad, x1 = hi + pad;
      const sx = (v) => m.left + ((v - x0) / (x1 - x0)) * (width - m.left - m.right);
      const svg = el('svg', { width, height: h, role: 'img', 'aria-label': opts.title }, c);
      const tip = tooltip(c);

      niceTicks(x0, x1, width < 420 ? 4 : 6).forEach((t) => {
        el('line', { x1: sx(t), x2: sx(t), y1: m.top, y2: h - m.bottom, stroke: grid, 'stroke-width': 1 }, svg);
        text(svg, sx(t), h - m.bottom + 18, String(t), { 'text-anchor': 'middle', 'font-size': 12 });
      });
      el('line', { x1: sx(0), x2: sx(0), y1: m.top, y2: h - m.bottom, stroke: css('--muted'), 'stroke-width': 1 }, svg);
      text(svg, (m.left + width - m.right) / 2, h - 4, opts.xLabel, { 'text-anchor': 'middle', 'font-size': 12 });

      rows.forEach((r, i) => {
        const cy = stacked ? m.top + i * rowH + rowH - 14 : m.top + i * rowH + rowH / 2;
        text(svg, 0, stacked ? cy - 16 : cy + 4, r.label, { fill: ink, 'font-size': 13 });
        const g = el('g', { class: 'mark' }, svg);
        el('rect', { x: m.left, y: cy - rowH / 2, width: width - m.left - m.right, height: rowH, fill: 'transparent' }, g);
        el('line', { x1: sx(r.lo), x2: sx(r.hi), y1: cy, y2: cy, stroke: accent, 'stroke-width': 2, 'stroke-linecap': 'round' }, g);
        el('circle', { cx: sx(r.est), cy, r: 5, fill: accent, stroke: surface, 'stroke-width': 2 }, g);
        hover(g, tip, () => ({ x: sx(r.est), y: cy - 6 }),
          `β = ${r.est} (95% CI ${r.lo} to ${r.hi})`, r.label + (r.note ? ' · ' + r.note : ''));
      });
    });
  }

  // points: [{x, y}], opts: {yFormat, yMin, yMax, label}
  function line(selector, points, opts) {
    mount(selector, (c, width) => {
      const accent = css('--accent'), surface = css('--surface'), grid = css('--border');
      const m = { top: 24, right: 56, bottom: 32, left: 44 };
      const h = 260;
      const xs = points.map((p) => p.x);
      const sx = (v) => m.left + ((v - xs[0]) / (xs[xs.length - 1] - xs[0])) * (width - m.left - m.right);
      const sy = (v) => h - m.bottom - ((v - opts.yMin) / (opts.yMax - opts.yMin)) * (h - m.top - m.bottom);
      const svg = el('svg', { width, height: h, role: 'img', 'aria-label': opts.title }, c);
      const tip = tooltip(c);

      niceTicks(opts.yMin, opts.yMax, 4).forEach((t) => {
        el('line', { x1: m.left, x2: width - m.right, y1: sy(t), y2: sy(t), stroke: grid, 'stroke-width': 1 }, svg);
        text(svg, m.left - 8, sy(t) + 4, opts.yFormat(t), { 'text-anchor': 'end', 'font-size': 12 });
      });
      xs.forEach((x) => text(svg, sx(x), h - 10, String(x), { 'text-anchor': 'middle', 'font-size': 12 }));

      el('path', {
        d: points.map((p, i) => (i ? 'L' : 'M') + sx(p.x) + ',' + sy(p.y)).join(' '),
        fill: 'none', stroke: accent, 'stroke-width': 2, 'stroke-linejoin': 'round', 'stroke-linecap': 'round',
      }, svg);
      const last = points[points.length - 1];
      const fmt = opts.valueFormat || opts.yFormat;
      text(svg, sx(last.x) + 10, sy(last.y) + 4, fmt(last.y), { fill: css('--text'), 'font-weight': 600 });

      const cross = el('line', { y1: m.top, y2: h - m.bottom, stroke: css('--muted'), 'stroke-width': 1, visibility: 'hidden' }, svg);
      points.forEach((p, i) => {
        const g = el('g', { class: 'mark' }, svg);
        const half = (width - m.left - m.right) / (points.length - 1) / 2;
        el('rect', { x: sx(p.x) - half, y: m.top, width: half * 2, height: h - m.top - m.bottom, fill: 'transparent' }, g);
        el('circle', { cx: sx(p.x), cy: sy(p.y), r: 4.5, fill: accent, stroke: surface, 'stroke-width': 2 }, g);
        hover(g, tip, () => {
          cross.setAttribute('x1', sx(p.x)); cross.setAttribute('x2', sx(p.x)); cross.setAttribute('visibility', 'visible');
          return { x: sx(p.x), y: sy(p.y) - 6 };
        }, fmt(p.y), String(p.x) + ' · ' + opts.label);
        g.addEventListener('pointerleave', () => cross.setAttribute('visibility', 'hidden'));
        g.addEventListener('blur', () => cross.setAttribute('visibility', 'hidden'));
      });
    });
  }

  // rows: [{label, value}], opts: {min, max, format}
  // On narrow screens labels sit above their bar so long names are never clipped.
  function hbar(selector, rows, opts) {
    mount(selector, (c, width) => {
      const accent = css('--accent'), grid = css('--border'), ink = css('--text');
      const stacked = width < 520;
      const labelW = stacked ? 0 : Math.min(190, width * 0.38);
      const m = { top: 4, right: 44, bottom: 28, left: labelW };
      const band = stacked ? 50 : 36, thick = 20;
      const h = m.top + rows.length * band + m.bottom;
      const sx = (v) => m.left + ((v - opts.min) / (opts.max - opts.min)) * (width - m.left - m.right);
      const svg = el('svg', { width, height: h, role: 'img', 'aria-label': opts.title }, c);
      const tip = tooltip(c);

      niceTicks(opts.min, opts.max, stacked ? 4 : 5).forEach((t) => {
        el('line', { x1: sx(t), x2: sx(t), y1: m.top, y2: h - m.bottom, stroke: grid, 'stroke-width': 1 }, svg);
        text(svg, sx(t), h - 8, opts.format(t), { 'text-anchor': 'middle', 'font-size': 12 });
      });
      el('line', { x1: sx(0), x2: sx(0), y1: m.top, y2: h - m.bottom, stroke: css('--muted'), 'stroke-width': 1 }, svg);

      rows.forEach((r, i) => {
        const top = m.top + i * band;
        const cy = stacked ? top + band - thick / 2 - 4 : top + band / 2;
        if (stacked) text(svg, 0, top + 14, r.label, { fill: ink, 'font-size': 13 });
        else text(svg, 0, cy + 4, r.label, { fill: ink, 'font-size': 13 });
        const g = el('g', { class: 'mark' }, svg);
        el('rect', { x: m.left, y: top, width: width - m.left - m.right, height: band, fill: 'transparent' }, g);
        const a = sx(Math.min(0, r.value)), b = sx(Math.max(0, r.value));
        const w = Math.max(b - a, 2), rad = Math.min(4, w / 2);
        // Rounded at the data end, square at the baseline.
        const pos = r.value >= 0;
        const x = a, y = cy - thick / 2;
        const d = pos
          ? `M${x},${y} H${x + w - rad} Q${x + w},${y} ${x + w},${y + rad} V${y + thick - rad} Q${x + w},${y + thick} ${x + w - rad},${y + thick} H${x} Z`
          : `M${x + w},${y} H${x + rad} Q${x},${y} ${x},${y + rad} V${y + thick - rad} Q${x},${y + thick} ${x + rad},${y + thick} H${x + w} Z`;
        el('path', { d, fill: accent }, g);
        text(svg, b + 6, cy + 4, opts.format(r.value), { fill: ink, 'font-size': 12 });
        hover(g, tip, () => ({ x: b, y: cy - thick / 2 }), opts.format(r.value), r.label);
      });
    });
  }

  window.Charts = { forest, line, hbar };
})();
