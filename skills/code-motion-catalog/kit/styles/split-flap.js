{
  // ---------------------------------------------------------------- content
  // No per-stage numbers until real ones exist: each row says what the pipeline does; the claim is the last row.
  const HEADER = 'WHAT THE AI PIPELINE DOES';
  const ROWS = [
    ['RESEARCH', 'AUTO'],
    ['SCRIPT', 'TARGETED'],
    ['REFERENCES', 'LOCKED'],
    ['GENERATE', 'CHECKED'],
    ['EDIT', 'AUTO'],
    ['VERSIONS', 'ALL SIZES'],
    ['TIME SAVED', 'UP TO 62%'],
  ];
  const HERO_ROW = 6;
  const COLS = 20, NAME_COLS = 10;

  // ---------------------------------------------------------------- the mechanism (from the reference style)
  const DRUM = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-/%:';
  const CW = 0.5, CH = 0.8, PITCH_X = 0.56, PITCH_Y = 0.92;
  const ROW_START = (r) => -0.45 + r * 0.8;
  const cellX = (c) => (c - (COLS - 1) / 2) * PITCH_X + (c >= NAME_COLS ? 0.07 : -0.07);
  const cellY = (r) => ((ROWS.length - 1) / 2 - r) * PITCH_Y;

  function schedule(K) {
    const r = K.rng(11), cells = [];
    ROWS.forEach(([name, value], row) => {
      const text = name.padEnd(NAME_COLS, ' ') + value.padStart(COLS - NAME_COLS, ' ');
      for (let c = 0; c < COLS; c++) {
        const g = Math.max(0, DRUM.indexOf(text[c]));
        cells.push({ row, c, g, t0: ROW_START(row) + c * 0.022 + r.range(0, 0.12), dt: (g > 26 ? 0.036 : 0.047) + r.range(0, 0.008) });
      }
    });
    cells.forEach((q) => { q.end = q.t0 + q.g * q.dt; });
    return cells;
  }
  function cellState(q, t) {
    const e = (t - q.t0) / q.dt;
    if (e <= 0) return [0, 0, 0];
    const k = Math.floor(e);
    if (k >= q.g) return [q.g, q.g, 0];
    return [k, k + 1, Math.PI * Math.pow(e - k, 1.6)];
  }

  registerStyle({
    id: 'split-flap',
    name: 'Split-Flap Board',
    family: 'Flat content made physical',
    topic: 'Time saved at each stage of the AI production pipeline',
    duration: 8,
    fonts: ['500 200px "Oswald"', '600 120px "Oswald"'],
    render: { samples: 40, shutter: 0.6, tone: 'filmic', exposure: 1.05, bloom: 0.5, bloomThreshold: 1.1, vignette: 0.42, grain: 0.035, fov: 30, background: '#040405' },

    build(S) {
      const { THREE, K, scene, camera } = S;
      const cells = schedule(K);
      const rowEnd = ROWS.map((_, r) => Math.max(...cells.filter((q) => q.row === r).map((q) => q.end)));

      K.env(S, { top: '#07080a', horizon: '#0d0f13', bottom: '#020202', intensity: 0.9, panels: [
        { pos: [0, 10, 9], size: [16, 5], color: '#fff1dc', power: 5 },
        { pos: [-14, 2, 6], size: [2, 10], color: '#8fb4ff', power: 2.2 },
      ] });
      K.spot(S, { pos: [1.5, 9.5, 10.5], target: [0, 0, 0], color: '#ffe9cc', power: 1250, angle: 0.62, penumbra: 0.9, soft: 0.9 });
      K.spot(S, { pos: [-12, 1, 8], target: [0, 0, 0], color: '#7fa6ff', power: 420, angle: 0.7, penumbra: 1, shadow: false });

      const AC = 8, AR = 6, GW = 160, GH = 256;
      const atlas = K.canvasTex(AC * GW, AR * GH, (ctx) => {
        const rr = K.rng(5);
        for (let i = 0; i < DRUM.length; i++) {
          const x = (i % AC) * GW, y = Math.floor(i / AC) * GH;
          const g = ctx.createLinearGradient(0, y, 0, y + GH); g.addColorStop(0, '#1b1c1f'); g.addColorStop(0.5, '#151619'); g.addColorStop(0.5, '#1a1b1e'); g.addColorStop(1, '#121315');
          ctx.fillStyle = g; ctx.fillRect(x, y, GW, GH);
          ctx.save(); ctx.beginPath(); ctx.rect(x, y, GW, GH); ctx.clip();
          ctx.font = '500 200px "Oswald"'; ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic'; ctx.fillStyle = '#f1ede2';
          ctx.fillText(DRUM[i], x + GW / 2, y + GH * 0.5 + 73);
          ctx.globalCompositeOperation = 'source-atop';
          for (let k = 0; k < 26; k++) { ctx.fillStyle = `rgba(20,20,22,${rr.range(0.04, 0.16)})`; ctx.fillRect(x + rr.range(0, GW), y + rr.range(0, GH), rr.range(2, 14), rr.range(1, 3)); }
          ctx.restore();
          ctx.fillStyle = 'rgba(0,0,0,0.55)'; ctx.fillRect(x, y + GH / 2 - 3, GW, 6);
        }
      });
      const flapMat = () => {
        const m = new THREE.MeshStandardMaterial({ map: atlas, roughness: 0.46, metalness: 0.0 });
        m.onBeforeCompile = (sh) => {
          sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nattribute float aGlyph;')
            .replace('#include <uv_vertex>', `#include <uv_vertex>\nvMapUv = (vec2(mod(aGlyph, ${AC}.0), ${AR - 1}.0 - floor(aGlyph / ${AC}.0)) + uv) / vec2(${AC}.0, ${AR}.0);`);
        };
        return m;
      };
      const half = (top) => {
        const g = new THREE.PlaneGeometry(CW, CH / 2 - 0.006); g.translate(0, (top ? 1 : -1) * (CH / 4 + 0.003), 0);
        const uv = g.attributes.uv; for (let i = 0; i < uv.count; i++) uv.setY(i, top ? 0.5 + uv.getY(i) * 0.5 : uv.getY(i) * 0.5);
        g.setAttribute('aGlyph', new THREE.InstancedBufferAttribute(new Float32Array(cells.length), 1));
        return g;
      };
      const mk = (top, cast) => { const m = new THREE.InstancedMesh(half(top), flapMat(), cells.length); m.castShadow = cast; m.receiveShadow = true; m.frustumCulled = false; scene.add(m); return m; };
      const topStatic = mk(true, false), botStatic = mk(false, false), flapFront = mk(true, true), flapBack = mk(false, true);

      const BW = COLS * PITCH_X + 1.0, BH = ROWS.length * PITCH_Y + 0.5;
      const steel = new THREE.MeshStandardMaterial({ color: '#1d1f23', roughness: 0.38, metalness: 0.85 });
      const dark = new THREE.MeshStandardMaterial({ color: '#030303', roughness: 0.95 });
      const add = (geo, mat, x, y, z, cast = true) => { const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); m.castShadow = cast; m.receiveShadow = true; scene.add(m); return m; };
      add(new THREE.BoxGeometry(BW, BH, 0.2), dark, 0, 0, -0.16, false);
      for (let r = 0; r <= ROWS.length; r++) add(K.roundedBox(BW - 0.3, 0.07, 0.34, 0.02, 2), steel, 0, cellY(r) + PITCH_Y / 2, -0.02);
      const F = 0.42;
      add(K.roundedBox(BW + F * 2, F, 0.9, 0.06, 4), steel, 0, BH / 2 + F / 2 + 1.0, 0.1);
      add(K.roundedBox(BW + F * 2, F, 0.9, 0.06, 4), steel, 0, -BH / 2 - F / 2, 0.1);
      add(K.roundedBox(F, BH + F * 2 + 1.0, 0.9, 0.06, 4), steel, -BW / 2 - F / 2, 0.5, 0.1);
      add(K.roundedBox(F, BH + F * 2 + 1.0, 0.9, 0.06, 4), steel, BW / 2 + F / 2, 0.5, 0.1);
      add(new THREE.BoxGeometry(BW, 1.0, 0.2), dark, 0, BH / 2 + 0.5, -0.16, false);
      const head = K.textPlane(HEADER, { font: '600 120px "Oswald"', height: 0.46, color: '#ffb347', glow: 2.6, letterSpacing: 10 });
      head.position.set(0, BH / 2 + 0.5, 0.0); scene.add(head);
      add(new THREE.PlaneGeometry(60, 40), new THREE.MeshStandardMaterial({ color: '#0c0d10', roughness: 0.92 }), 0, 0, -0.7, false);

      const cam = {
        pos: K.track([[0, [-6.6, 3.05, 2.5]], [2.6, [-3.0, 2.2, 4.5], 'inOut'], [5.7, [1.2, 0.45, 17.2], 'inOutQuint'], [8, [0.8, 0.1, 15.4], 'out']]),
        aim: K.track([[0, [-3.3, 2.72, 0]], [2.6, [-1.0, 1.9, 0], 'inOut'], [5.7, [0, 0.5, 0], 'inOutQuint'], [8, [0, 0.3, 0], 'out']]),
        ap: K.track([[0, 0.06], [2.6, 0.06], [5.7, 0.03], [8, 0.03]]),
      };
      const white = new THREE.Color('#ffffff'), amber = new THREE.Color('#ffb648'), col = new THREE.Color(), meshes = [topStatic, botStatic, flapFront, flapBack];

      return {
        update(t) {
          cells.forEach((q, i) => {
            const [cur, next, ang] = cellState(q, t), x = cellX(q.c), y = cellY(q.row);
            topStatic.geometry.attributes.aGlyph.array[i] = next; botStatic.geometry.attributes.aGlyph.array[i] = cur;
            flapFront.geometry.attributes.aGlyph.array[i] = cur; flapBack.geometry.attributes.aGlyph.array[i] = next;
            K.place(topStatic, i, [x, y, 0]); K.place(botStatic, i, [x, y, 0]);
            K.place(flapFront, i, [x, y, 0.004], [ang, 0, 0]); K.place(flapBack, i, [x, y, 0.004], [ang - Math.PI, 0, 0]);
            const k = q.row === HERO_ROW ? K.seg(t, rowEnd[HERO_ROW] + 0.05, rowEnd[HERO_ROW] + 0.4, K.ease.out) : 0;
            col.copy(white).lerp(amber, k);
            for (const m of meshes) m.setColorAt(i, col);
          });
          for (const m of meshes) { m.geometry.attributes.aGlyph.needsUpdate = true; m.instanceMatrix.needsUpdate = true; m.instanceColor.needsUpdate = true; }
          head.material.color.setScalar(2.6 * (0.9 + 0.1 * Math.sin(t * 37) * Math.sin(t * 11.3)));
          K.look(camera, cam.pos(t), cam.aim(t)); K.focus(camera, cam.aim(t), cam.ap(t));
        },
      };
    },

    sound(k) {
      const K = globalThis.K, cells = schedule(K), bins = new Map();
      for (const q of cells) for (let i = 0; i < q.g; i++) { const t = q.t0 + (i + 1) * q.dt, b = Math.round(t / 0.028); const e = bins.get(b) || { n: 0, pan: 0 }; e.n++; e.pan += cellX(q.c) / 6; bins.set(b, e); }
      k.withMinor(() => { for (const [b, e] of bins) k.play(b % 3 ? 'tick' : 'tock', b * 0.028, { gain: Math.min(0.9, 0.3 + 0.16 * Math.sqrt(e.n)), pan: K.clamp(e.pan / e.n, -0.8, 0.8), f: b % 3 ? 3600 + (b * 53 % 900) : 900 + (b * 31 % 300) }); });
      ROWS.forEach((_, r) => { const end = Math.max(...cells.filter((q) => q.row === r).map((q) => q.end)); k.play('tock', end + 0.02, { gain: 0.9, f: 620 }); });
      const heroEnd = Math.max(...cells.filter((q) => q.row === HERO_ROW).map((q) => q.end));
      k.play('ding', heroEnd + 0.1, { gain: 0.8, f: 'A5' });
      k.play('thud', heroEnd + 0.1, { gain: 0.5 });
      k.bed('room', 0, 8, { gain: 1.2 }); k.bed('hum', 0, 8, { gain: 0.35 });
    },
  });
}
