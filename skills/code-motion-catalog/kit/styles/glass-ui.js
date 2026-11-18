{
  // ---------------------------------------------------------------- content: one camera take through an invented editing app
  // The app's panels are dark frosted glass floating in a warm void. The camera dives into the timeline (a playhead wipe
  // over a glowing audio wave), pulls back to the window (the active tab moves to NODES), slides onto the node panel
  // (two inputs fuse into one node) and ends on the export pill. One red accent for whatever is active.
  const TABS = ['EDIT', 'NODES', 'EXPORT'];
  const SLIDERS = ['EXPOSURE', 'CONTRAST', 'GRAIN', 'SHARPEN'];
  const INPUTS = ['CLIP A', 'GRADE'], NODE = 'MERGE';
  const PILL = ['EXPORTING', 'DONE'];
  const WORDS = ['Edit.', 'Fuse.', 'Export.'];        // red-lead word reveal at the end

  // ---------------------------------------------------------------- timing (picture and sound share it)
  const WIPE = [1.25, 3.05];                           // playhead crosses the timeline
  const TAB = 3.85;                                    // the active tab slides EDIT -> NODES
  const FUSE = [5.55, 6.35];                           // fuse lines grow, the node lights at the end
  const EXPORT = [7.35, 8.45];                         // the pill fills, then DONE
  const WORD = [7.55, 7.9, 8.25];
  const DUR = 9;

  // ---------------------------------------------------------------- layout (world units; canvases at 384 px per unit)
  const U = 384;
  const WIN = { w: 8, h: 4.6 };                         // main window, centred at the origin
  const TL = { x0: 0.95, x1: 7.6, top: 2.95, rows: [3.2, 3.62, 4.08] };   // timeline area inside the window (units from top-left)
  const NP = { w: 4.6, h: 3.4, pos: [8.6, -0.15, -1.5], ry: -0.36 };      // node panel
  const CHIP = [[0.35, 0.72], [0.35, 1.68]], CHIP_W = 1.25, CHIP_H = 0.48;
  const NODE_AT = [2.75, 1.3], NODE_W = 1.3, NODE_H = 0.62;
  const PILL_AT = [2.5, 2.75], PILL_W = 1.75, PILL_H = 0.36;
  const BARS = { x: 0.35, y: 2.62, w: 1.7, h: 0.56, n: 7 };

  registerStyle({
    id: 'glass-ui',
    name: 'Glass UI Explainer',
    family: 'Products and screens',
    topic: 'One continuous camera take through an invented editing app: timeline dive, tab change, fuse node, export pill',
    duration: DUR,
    fonts: ['600 46px "Inter"', '500 40px "Inter"', '500 34px "IBM Plex Mono"', '600 64px "Inter"'],
    render: { samples: 40, shutter: 0.5, tone: 'neutral', exposure: 1.0, contrast: 1.05, bloom: 0.55, bloomThreshold: 1.0, vignette: 0.4, grain: 0.018, fov: 30, background: '#0a0807' },

    build(S) {
      const { THREE, K, scene, camera } = S;
      const RED = new THREE.Color('#ff3b2f');
      const px = (u) => u * U;
      const rr = (c, x, y, w, h, r) => { c.beginPath(); c.roundRect(px(x), px(y), px(w), px(h), px(r)); };
      const glassBase = (c, w, h) => {
        rr(c, 0.02, 0.02, w - 0.04, h - 0.04, 0.14); c.fillStyle = 'rgba(20,21,26,0.8)'; c.fill();
        const g = c.createLinearGradient(0, 0, 0, px(h)); g.addColorStop(0, 'rgba(255,255,255,0.06)'); g.addColorStop(0.3, 'rgba(255,255,255,0)'); c.fillStyle = g; c.fill();
        c.strokeStyle = 'rgba(255,255,255,0.16)'; c.lineWidth = 3; c.stroke();
      };
      const label = (c, s, x, y, o = {}) => { c.font = o.font || '500 40px "Inter"'; c.fillStyle = o.color || 'rgba(235,236,240,0.82)'; c.textBaseline = 'middle'; c.letterSpacing = (o.ls || 3) + 'px'; c.fillText(s, px(x), px(y)); c.letterSpacing = '0px'; };
      const plane = (tex, w, h) => new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false }));
      const flat = (color, k = 1, add = false) => new THREE.MeshBasicMaterial({ color: new THREE.Color(color).multiplyScalar(k), transparent: true, depthWrite: false, blending: add ? THREE.AdditiveBlending : THREE.NormalBlending });

      // ---- the void: warm and nearly black, with two blurred orbs so the frosted panels have something behind them
      const orb = (x, y, z, r, col, k) => {
        const m = new THREE.Mesh(new THREE.PlaneGeometry(r * 2, r * 2), new THREE.ShaderMaterial({ transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
          uniforms: { c: { value: new THREE.Color(col).multiplyScalar(k) } },
          vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
          fragmentShader: 'uniform vec3 c; varying vec2 vUv; void main(){ float d = length(vUv - 0.5) * 2.0; gl_FragColor = vec4(c * exp(-d * d * 3.5), 1.0); }' }));
        m.position.set(x, y, z); m.renderOrder = -5; scene.add(m);
      };
      orb(-3, 1.5, -7, 7, '#ff5a2a', 0.16); orb(9, -2, -9, 8, '#ff2a4a', 0.12); orb(3, 4, -12, 9, '#5a3aff', 0.05);

      // ---- main window
      const winTex = K.canvasTex(px(WIN.w), px(WIN.h), (c) => {
        glassBase(c, WIN.w, WIN.h);
        c.fillStyle = 'rgba(255,255,255,0.1)'; c.fillRect(px(0.02), px(0.42), px(WIN.w - 0.04), 3);
        [0, 1, 2].forEach((k) => { c.fillStyle = ['#ff5f57', '#febc2e', '#28c840'][k]; c.globalAlpha = 0.55; c.beginPath(); c.arc(px(0.3 + k * 0.2), px(0.21), px(0.055), 0, 7); c.fill(); c.globalAlpha = 1; });
        TABS.forEach((s, k) => label(c, s, 1.3 + k * 1.05, 0.22, { font: '600 46px "Inter"' }));
        // viewer
        const vx = 0.35, vy = 0.62, vw = 4.75, vh = 2.1;
        rr(c, vx, vy, vw, vh, 0.06); const g = c.createLinearGradient(0, px(vy), 0, px(vy + vh)); g.addColorStop(0, '#2a1c3c'); g.addColorStop(0.55, '#e0703a'); g.addColorStop(0.56, '#3a2420'); g.addColorStop(1, '#140e0c'); c.fillStyle = g; c.fill();
        c.fillStyle = '#0c0808'; c.beginPath(); c.roundRect(px(vx + vw * 0.55), px(vy + vh * 0.32), px(0.24), px(0.95), px(0.1)); c.fill(); c.beginPath(); c.arc(px(vx + vw * 0.55 + 0.12), px(vy + vh * 0.27), px(0.11), 0, 7); c.fill();
        // inspector: labels and sliders, no numbers
        label(c, 'INSPECTOR', 5.45, 0.72, { font: '500 34px "IBM Plex Mono"', color: 'rgba(255,255,255,0.45)' });
        SLIDERS.forEach((s, k) => {
          const y = 1.12 + k * 0.42; label(c, s, 5.45, y, { font: '500 34px "IBM Plex Mono"', color: 'rgba(255,255,255,0.7)' });
          c.fillStyle = 'rgba(255,255,255,0.16)'; c.fillRect(px(5.45), px(y + 0.17), px(2.15), 4);
          const f = [0.62, 0.48, 0.3, 0.55][k]; c.fillStyle = 'rgba(255,255,255,0.75)'; c.fillRect(px(5.45), px(y + 0.17), px(2.15 * f), 4);
          c.beginPath(); c.arc(px(5.45 + 2.15 * f), px(y + 0.17) + 2, px(0.045), 0, 7); c.fill();
        });
        // timeline: ruler, two video tracks of clips, one audio track (the wave itself is 3D points)
        c.fillStyle = 'rgba(255,255,255,0.08)'; c.fillRect(px(0.02), px(TL.top - 0.12), px(WIN.w - 0.04), 3);
        for (let x = TL.x0; x <= TL.x1; x += 0.2) { c.fillStyle = 'rgba(255,255,255,0.22)'; c.fillRect(px(x), px(TL.top - 0.02), 2, px(Math.round((x - TL.x0) / 0.2) % 5 ? 0.05 : 0.1)); }
        ['V2', 'V1', 'A1'].forEach((s, k) => label(c, s, 0.4, TL.rows[k], { font: '500 34px "IBM Plex Mono"', color: 'rgba(255,255,255,0.5)' }));
        const r = K.rng(4);
        [[0, 1], [1, 0]].forEach(([row, warm]) => {
          let x = TL.x0 + (row ? 0 : 0.6);
          while (x < TL.x1 - 0.4) {
            const w = Math.min(TL.x1 - x, r.range(0.7, 1.6)); rr(c, x, TL.rows[row] - 0.17, w - 0.05, 0.34, 0.05);
            c.fillStyle = warm ? `hsla(${r.range(12, 32)},55%,${r.range(32, 44)}%,0.85)` : `hsla(${r.range(250, 280)},35%,${r.range(30, 40)}%,0.8)`; c.fill();
            c.strokeStyle = 'rgba(255,255,255,0.25)'; c.lineWidth = 2; c.stroke(); x += w + (row ? r.range(0.4, 0.9) : 0);
          }
        });
        rr(c, TL.x0, TL.rows[2] - 0.2, TL.x1 - TL.x0, 0.4, 0.05); c.fillStyle = 'rgba(255,255,255,0.04)'; c.fill();
      });
      const win = plane(winTex, WIN.w, WIN.h); scene.add(win);
      const wx = (x) => x - WIN.w / 2, wy = (y) => WIN.h / 2 - y;          // window canvas units -> world

      const playhead = new THREE.Group(); scene.add(playhead);
      const phLine = new THREE.Mesh(new THREE.PlaneGeometry(0.014, 1.5), flat('#ff3b2f', 2.2)); phLine.position.y = -0.75; playhead.add(phLine);
      const phCap = new THREE.Mesh(new THREE.CircleGeometry(0.05, 3), flat('#ff3b2f', 2.2)); phCap.rotation.z = -Math.PI / 2; phCap.position.y = 0.02; playhead.add(phCap);
      playhead.position.set(wx(TL.x0), wy(TL.top - 0.06), 0.02); playhead.renderOrder = 10; phLine.renderOrder = phCap.renderOrder = 10;
      const played = new THREE.Mesh(new THREE.PlaneGeometry(1, 1.25).translate(0.5, 0, 0), flat('#ff3b2f', 0.12, true)); played.position.set(wx(TL.x0), wy(3.62), 0.012); scene.add(played);
      const tabLine = new THREE.Mesh(new THREE.PlaneGeometry(0.62, 0.028), flat('#ff3b2f', 2)); scene.add(tabLine);

      // the audio wave: warm points inside a waveform envelope, brighter where the playhead has passed
      const NW = 2600, ax = new Float32Array(NW), ar = new Float32Array(NW), wpos = new Float32Array(NW * 3), rw = K.rng(21);
      for (let i = 0; i < NW; i++) { ax[i] = rw(); ar[i] = rw(); }
      const wg = new THREE.BufferGeometry(); wg.setAttribute('position', new THREE.BufferAttribute(wpos, 3)); wg.setAttribute('aX', new THREE.BufferAttribute(ax, 1)); wg.setAttribute('aR', new THREE.BufferAttribute(ar, 1));
      const wu = { uTime: { value: 0 }, uX0: { value: wx(TL.x0 + 0.05) }, uW: { value: TL.x1 - TL.x0 - 0.1 }, uY: { value: wy(TL.rows[2]) }, uHead: { value: 0 }, uPx: { value: S.H / 1080 } };
      const wave = new THREE.Points(wg, new THREE.ShaderMaterial({ uniforms: wu, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
        vertexShader: `uniform float uTime, uX0, uW, uY, uHead, uPx; attribute float aX, aR; varying vec3 vC; varying float vA;
          void main(){
            float env = 0.25 + 0.75 * pow(abs(sin(aX * 23.0) * sin(aX * 7.1 + 1.3) * (0.6 + 0.4 * sin(aX * 61.0))), 0.8);
            float yy = (aR * 2.0 - 1.0) * env * 0.16 + 0.006 * sin(uTime * 4.0 + aR * 50.0);
            vec4 mv = modelViewMatrix * vec4(uX0 + aX * uW, uY + yy, 0.025, 1.0); gl_Position = projectionMatrix * mv;
            float lit = step(aX, uHead);
            gl_PointSize = uPx * (1.5 + 2.5 * fract(aR * 7.31)) * 9.0 / -mv.z;
            vC = mix(vec3(1.0, 0.45, 0.2), vec3(1.0, 0.85, 0.7), fract(aR * 3.7)) * (0.55 + 1.6 * lit);
            vA = 0.55 + 0.45 * sin(uTime * 2.0 + aR * 30.0);
          }`,
        fragmentShader: 'varying vec3 vC; varying float vA; void main(){ float d = length(gl_PointCoord - 0.5); gl_FragColor = vec4(vC * vA * smoothstep(0.5, 0.1, d), 1.0); }' }));
      wave.frustumCulled = false; wave.renderOrder = 8; scene.add(wave);

      // ---- node panel (its own group, turned toward the camera path)
      const node = new THREE.Group(); node.position.set(...NP.pos); node.rotation.y = NP.ry; scene.add(node);
      const nx = (x) => x - NP.w / 2, ny = (y) => NP.h / 2 - y;
      const npTex = K.canvasTex(px(NP.w), px(NP.h), (c) => {
        glassBase(c, NP.w, NP.h);
        label(c, 'NODES', 0.35, 0.3, { font: '600 46px "Inter"' });
        c.fillStyle = 'rgba(255,255,255,0.05)'; for (let x = 0.2; x < NP.w; x += 0.25) for (let y = 0.6; y < NP.h - 0.1; y += 0.25) c.fillRect(px(x), px(y), 4, 4);
        INPUTS.forEach((s, k) => { rr(c, CHIP[k][0], CHIP[k][1], CHIP_W, CHIP_H, 0.1); c.fillStyle = 'rgba(40,42,50,0.95)'; c.fill(); c.strokeStyle = 'rgba(255,255,255,0.3)'; c.lineWidth = 3; c.stroke(); label(c, s, CHIP[k][0] + 0.18, CHIP[k][1] + CHIP_H / 2, { font: '600 46px "Inter"' }); c.fillStyle = '#fff'; c.beginPath(); c.arc(px(CHIP[k][0] + CHIP_W), px(CHIP[k][1] + CHIP_H / 2), px(0.05), 0, 7); c.fill(); });
        rr(c, NODE_AT[0], NODE_AT[1], NODE_W, NODE_H, 0.12); c.fillStyle = 'rgba(46,30,30,0.95)'; c.fill(); c.strokeStyle = 'rgba(255,255,255,0.35)'; c.lineWidth = 3; c.stroke();
        label(c, NODE, NODE_AT[0] + 0.22, NODE_AT[1] + NODE_H / 2, { font: '600 46px "Inter"' });
        label(c, 'OUTPUT', BARS.x, BARS.y - 0.18, { font: '500 34px "IBM Plex Mono"', color: 'rgba(255,255,255,0.5)' });
        rr(c, PILL_AT[0], PILL_AT[1], PILL_W, PILL_H, PILL_H / 2); c.fillStyle = 'rgba(255,255,255,0.06)'; c.fill(); c.strokeStyle = 'rgba(255,255,255,0.25)'; c.lineWidth = 3; c.stroke();
      });
      const np = plane(npTex, NP.w, NP.h); node.add(np);

      // fuse lines: tubes that grow along their length (draw range), from each input to the node
      const fuses = CHIP.map(([x, y]) => {
        const a = [nx(x + CHIP_W), ny(y + CHIP_H / 2)], b = [nx(NODE_AT[0]), ny(NODE_AT[1] + NODE_H / 2)], m = (a[0] + b[0]) / 2;
        const g = K.tube([[a[0], a[1], 0.03], [m - 0.15, a[1], 0.03], [m + 0.15, b[1], 0.03], [b[0], b[1], 0.03]], 0.014, { segments: 80, radial: 8 });
        const mesh = new THREE.Mesh(g, flat('#ffffff', 1.6)); mesh.renderOrder = 6; node.add(mesh); return mesh;
      });
      // the node lights as an outline glow (a canvas stroke with shadow blur), so its label stays readable
      const G = 0.3, glowTex = K.canvasTex(px(NODE_W + G * 2), px(NODE_H + G * 2), (c) => { c.strokeStyle = '#fff'; c.lineWidth = 7; c.shadowColor = '#fff'; c.shadowBlur = 50; for (let k = 0; k < 3; k++) { rr(c, G, G, NODE_W, NODE_H, 0.12); c.stroke(); } });
      const nodeGlow = new THREE.Mesh(new THREE.PlaneGeometry(NODE_W + G * 2, NODE_H + G * 2), new THREE.MeshBasicMaterial({ map: glowTex, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending }));
      nodeGlow.position.set(nx(NODE_AT[0] + NODE_W / 2), ny(NODE_AT[1] + NODE_H / 2), 0.008); nodeGlow.renderOrder = 4; node.add(nodeGlow);

      // glow bars: a gradient times a soft vertical falloff, pushed above 1 so bloom catches the tops
      const barMat = new THREE.ShaderMaterial({ transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, uniforms: { k: { value: 1 } },
        vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
        fragmentShader: 'uniform float k; varying vec2 vUv; void main(){ float x = abs(vUv.x - 0.5) * 2.0; float side = exp(-x * x * 4.0); vec3 c = mix(vec3(1.0, 0.25, 0.12), vec3(1.0, 0.8, 0.6), vUv.y) * (0.35 + 1.6 * pow(vUv.y, 3.0)); gl_FragColor = vec4(c * side * k, 1.0); }' });
      const bars = Array.from({ length: BARS.n }, (_, i) => {
        const b = new THREE.Mesh(new THREE.PlaneGeometry(BARS.w / BARS.n * 0.6, 1).translate(0, 0.5, 0), barMat); b.renderOrder = 5;
        b.position.set(nx(BARS.x + (i + 0.5) * BARS.w / BARS.n), ny(BARS.y + BARS.h), 0.01); node.add(b); return b;
      });

      // export pill: SDF pill with a red fill that grows; two labels cross-fade
      const pu = { uP: { value: 0 }, uSize: { value: new THREE.Vector2(PILL_W, PILL_H) }, uDone: { value: 0 } };
      const pill = new THREE.Mesh(new THREE.PlaneGeometry(PILL_W, PILL_H), new THREE.ShaderMaterial({ uniforms: pu, transparent: true, depthWrite: false,
        vertexShader: 'varying vec2 vP; uniform vec2 uSize; void main(){ vP = position.xy; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
        fragmentShader: `uniform float uP, uDone; uniform vec2 uSize; varying vec2 vP;
          void main(){ float r = uSize.y * 0.5 - 0.02; vec2 d = abs(vP) - vec2(uSize.x * 0.5 - r - 0.02, 0.0); float sd = length(max(d, 0.0)) - r, aa = fwidth(sd);
            float inside = 1.0 - smoothstep(-aa, aa, sd); float fill = step(vP.x / uSize.x + 0.5, uP);
            vec3 c = mix(vec3(1.0, 0.23, 0.18) * 1.15, vec3(1.0, 0.3, 0.22) * 1.6, uDone);
            gl_FragColor = vec4(c * inside * fill * 0.85, inside * fill * 0.85); }` }));
      pill.position.set(nx(PILL_AT[0] + PILL_W / 2), ny(PILL_AT[1] + PILL_H / 2), 0.012); pill.renderOrder = 6; node.add(pill);
      const pillText = PILL.map((s) => { const m = K.textPlane(s, { font: '600 46px "Inter"', height: 0.15, letterSpacing: 4 }); m.position.set(pill.position.x, pill.position.y, 0.02); m.renderOrder = 7; node.add(m); return m; });

      // ---- the camera: moves of 0.6-1.0 s (ease in-out) between slow drifts, one continuous take
      const toWorld = (x, y, z = 0) => { node.updateMatrixWorld(); const v = new THREE.Vector3(nx(x), ny(y), z).applyMatrix4(node.matrixWorld); return [v.x, v.y, v.z]; };
      const NN = toWorld(2.05, 1.3), NPill = toWorld(2.3, 2.8);
      const nrm = [Math.sin(NP.ry), 0, Math.cos(NP.ry)];
      const off = (p, d, dx = 0, dy = 0) => [p[0] + nrm[0] * d + dx, p[1] + dy, p[2] + nrm[2] * d];
      const POS = K.track([
        [0, [-1.2, 1.0, 11.2]], [1.15, [-0.9, 0.9, 10.8]],
        [2.05, [-0.6, -0.6, 4.9]], [3.0, [1.3, -0.6, 4.7]],
        [3.85, [0.6, 0.5, 10.6]], [4.65, [0.9, 0.45, 10.3]],
        [5.55, off(NN, 4.6, -0.45, 0.3)], [6.6, off(NN, 4.4, -0.3, 0.28)],
        [7.4, off(NPill, 4.0, -0.3, 0.3)], [9, off(NPill, 3.75, -0.2, 0.25)],
      ]);
      const AIM = K.track([
        [0, [0, 0, 0]], [1.15, [0.15, 0, 0]],
        [2.05, [-0.3, -1.3, 0]], [3.0, [1.6, -1.3, 0]],
        [3.85, [0.6, 0.0, 0]], [4.65, [0.9, 0.0, 0]],
        [5.55, NN], [6.6, toWorld(2.15, 1.3)],
        [7.4, NPill], [9, toWorld(2.4, 2.75)],
      ]);

      return {
        update(t) {
          const pos = POS(t), aim = AIM(t);
          // during the dive the camera rides with the playhead, so the wipe stays in frame
          const ride = K.seg(t, 1.6, 2.2, K.ease.inOut) * (1 - K.seg(t, 3.0, 3.7, K.ease.inOut));
          const head = wx(TL.x0 + (TL.x1 - TL.x0) * K.seg(t, WIPE[0], WIPE[1], K.ease.inOut)) - 0.9;
          const dx = (head - aim[0]) * ride; pos[0] += dx; aim[0] += dx;
          K.look(camera, pos, aim, 30); K.focus(camera, aim, 0.025);

          const w = K.seg(t, WIPE[0], WIPE[1], K.ease.inOut);
          playhead.position.x = wx(TL.x0 + (TL.x1 - TL.x0) * w);
          played.scale.x = Math.max(0.001, (TL.x1 - TL.x0) * w); played.visible = w > 0.001;
          wu.uHead.value = w; wu.uTime.value = t;
          const tab = K.seg(t, TAB, TAB + 0.35, K.ease.inOut);
          tabLine.position.set(wx(1.3 + 0.5 + tab * 1.05 + (tab > 0 ? 0 : 0)) - 0.05, wy(0.4), 0.02);

          fuses.forEach((f, i) => { const p = K.seg(t, FUSE[0] + i * 0.12, FUSE[1] - 0.1 + i * 0.1, K.ease.inOut); const per = 8 * 6; f.geometry.setDrawRange(0, Math.floor(f.geometry.index.count / per * p) * per); f.material.color.setRGB(1, 1, 1).lerp(RED, K.seg(t, FUSE[1], FUSE[1] + 0.4)).multiplyScalar(1.6); });
          const lit = K.seg(t, FUSE[1], FUSE[1] + 0.12), flash = t > FUSE[1] ? Math.exp(-(t - FUSE[1]) / 0.25) : 0;
          nodeGlow.material.color.copy(RED).multiplyScalar(0.9 * lit + 2.5 * flash); nodeGlow.scale.setScalar(1 + 0.04 * flash);

          const ex = K.seg(t, EXPORT[0], EXPORT[1], K.ease.inOut), done = K.seg(t, EXPORT[1], EXPORT[1] + 0.2);
          pu.uP.value = ex; pu.uDone.value = done;
          pillText[0].material.opacity = (1 - done) * (0.5 + 0.5 * K.seg(t, EXPORT[0] - 0.3, EXPORT[0])); pillText[1].material.opacity = done;
          bars.forEach((b, i) => { const n = 0.5 + 0.5 * Math.sin(t * 9 + i * 1.7) * Math.sin(t * 5.3 + i); const h = BARS.h * (0.12 + 0.88 * n * K.seg(t, EXPORT[0] - 0.4 + i * 0.04, EXPORT[0] + 0.2) * (1 - 0.7 * done)); b.scale.y = Math.max(0.001, h); });
          barMat.uniforms.k.value = 1 + 1.5 * done;
        },
        overlay(ctx, t, W, H) {
          if (window.NO_TEXT) return;
          // red-lead reveal: the newest word arrives red and turns white when the next word lands
          ctx.font = '600 64px "Inter"'; ctx.textBaseline = 'alphabetic';
          let x = 128;
          WORDS.forEach((s, i) => {
            const a = K.seg(t, WORD[i], WORD[i] + 0.18, K.ease.out);
            const next = i < WORDS.length - 1 ? WORD[i + 1] : WORD[i] + 0.5;
            const white = K.seg(t, next, next + 0.12);
            if (a > 0) {
              ctx.globalAlpha = a; ctx.fillStyle = `rgb(255,${Math.round(59 + 183 * white)},${Math.round(47 + 192 * white)})`;
              ctx.fillText(s, x, H - 110 + (1 - a) * 18);
            }
            x += ctx.measureText(s + ' ').width;
          });
          ctx.globalAlpha = 1;
        },
      };
    },

    sound(k) {
      k.bed('room', 0, DUR, { gain: 0.75 });
      [1.15, 3.0, 4.65, 6.6].forEach((t) => k.play('whoosh', t - 0.05, { gain: 0.55, dur: 0.85, top: 1500 }));
      k.play('tape', WIPE[0], { gain: 0.5, dur: WIPE[1] - WIPE[0] });
      k.withMinor(() => { k.play('click', TAB, { gain: 0.6 }); k.play('blip', TAB + 0.3, { gain: 0.3, f: 'A6' }); });
      k.play('riser', FUSE[0], { gain: 0.45, dur: FUSE[1] - FUSE[0] });
      k.play('stamp', FUSE[1], { gain: 0.7 });
      k.play('roller', EXPORT[0], { gain: 0.4, dur: EXPORT[1] - EXPORT[0] });
      k.play('success', EXPORT[1], { gain: 0.8, f: 'E6' });
      WORD.forEach((t, i) => k.play('tick', t, { gain: 0.7, f: 4200 + i * 400 }));
    },
  });
}
