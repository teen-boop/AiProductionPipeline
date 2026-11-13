{
  // ---------------------------------------------------------------- content: how a brief travels through the pipeline
  const TITLE = ['How a brief', 'becomes an ad'];
  const LAYERS = [
    { name: 'BRIEF', note: 'goes in, the ad comes out', diagram: 'brief' },
    { name: 'RESEARCH', note: "customers' own words", diagram: 'quotes' },
    { name: 'SCRIPT', note: 'beat by beat, per audience', diagram: 'script' },
    { name: 'REFERENCES', note: 'faces and product locked', diagram: 'refs' },
    { name: 'GENERATE', note: 'stills first, every frame checked', diagram: 'frames' },
    { name: 'EDIT', note: 'every format, every length', diagram: 'edit' },
  ];
  const N = LAYERS.length;

  // ---------------------------------------------------------------- timing (picture and sound share it)
  const LIFT = [0.5, 1.1, 1.6, 2.05, 2.45, 2.8];
  const FREQ = [0.6, 0.7, 0.8, 0.9, 1.0, 1.12];
  const labelAt = (i) => LIFT[i] + 0.5 / FREQ[i];
  const DOWN = 4.3, STEP_DOWN = 0.34;
  const UP = 6.4, STEP_UP = 0.2;
  const hitDown = (i) => DOWN + i * STEP_DOWN;
  const hitUp = (i) => (i === N - 1 ? UP - 0.14 : UP + (N - 1 - i) * STEP_UP);
  const ANSWER = hitUp(0);

  // ---------------------------------------------------------------- the stack
  const W = 5.4, D = 3.3, TH = 0.11, GAP = 1.0, BASE = 0.18;
  const closedY = (i) => BASE + (N - 1 - i) * (TH + 0.007) + TH / 2;
  const openY = (i) => BASE + 0.3 + (N - 1 - i) * GAP + TH / 2;
  const lift = (i, t) => K.spring(t - LIFT[i], FREQ[i], 0.78);
  const layerY = (i, t) => K.lerp(closedY(i), openY(i), lift(i, t));

  // ---------------------------------------------------------------- the printed diagrams (1000 x 611, white = ink)
  const PAD = [858, 486];
  const rr = (c, x, y, w, h, r) => { c.beginPath(); c.roundRect(x, y, w, h, r); };
  const dot = (c, x, y, r) => { c.beginPath(); c.arc(x, y, r, 0, Math.PI * 2); c.fill(); };
  const line = (c, pts, lw = 7) => { c.lineWidth = lw; c.beginPath(); pts.forEach((p, i) => (i ? c.lineTo(p[0], p[1]) : c.moveTo(p[0], p[1]))); c.stroke(); };
  const sheet = (c, i) => {
    c.lineCap = 'round'; c.lineJoin = 'round'; c.strokeStyle = '#fff'; c.fillStyle = '#fff';
    c.lineWidth = 7; c.beginPath(); c.arc(PAD[0], PAD[1], 21, 0, Math.PI * 2); c.stroke(); dot(c, PAD[0], PAD[1], 8);
    c.strokeStyle = c.fillStyle = '#8d8d8d';
    for (const [x, y, sx, sy] of [[44, 44, 1, 1], [956, 44, -1, 1], [44, 567, 1, -1]]) line(c, [[x + 24 * sx, y], [x, y], [x, y + 24 * sy]], 3);
    c.font = '500 20px "IBM Plex Mono"'; c.textBaseline = 'middle'; c.letterSpacing = '2px'; c.fillText(`0${i + 1} / ${LAYERS[i].name}`, 86, 45); c.letterSpacing = '0px';
    c.strokeStyle = c.fillStyle = '#fff';
  };
  const drawBrief = (c) => {   // a brief card on the left, an arrow, and an empty phone waiting for the ad
    c.lineWidth = 7; rr(c, 90, 110, 330, 400, 26); c.stroke();
    rr(c, 126, 150, 170, 22, 11); c.fill();
    for (let k = 0; k < 6; k++) { rr(c, 126, 214 + k * 44, k % 3 === 2 ? 160 : 250, 13, 6); c.fill(); }
    line(c, [[450, 310], [530, 310]], 7); line(c, [[512, 292], [532, 310], [512, 328]], 7);
    rr(c, 560, 92, 230, 440, 34); c.stroke(); rr(c, 640, 112, 70, 12, 6); c.fill();
    c.lineWidth = 5; rr(c, 588, 146, 174, 340, 14); c.stroke();
    line(c, [[790, 420], [830, 420], [858, 448], [858, 463]], 6);
  };
  const drawAnswer = (c) => {   // the finished ad on the phone screen (in colour)
    c.fillStyle = '#ff9426'; rr(c, 592, 150, 166, 332, 12); c.fill();
    c.fillStyle = '#6b3300'; rr(c, 650, 210, 50, 150, 22); c.fill(); rr(c, 660, 192, 30, 22, 6); c.fill();   // a bottle
    rr(c, 612, 400, 126, 14, 7); c.fill(); rr(c, 630, 428, 90, 14, 7); c.fill();
  };
  const drawQuotes = (c) => {   // three speech bubbles: what customers say
    for (let k = 0; k < 3; k++) {
      const x = 100 + k * 40, y = 110 + k * 132, w = 560 - k * 60;
      c.lineWidth = 7; rr(c, x, y, w, 96, 30); c.stroke();
      line(c, [[x + 40, y + 96], [x + 30, y + 124], [x + 74, y + 96]], 7);
      rr(c, x + 34, y + 30, w * 0.6, 12, 6); c.fill(); rr(c, x + 34, y + 56, w * 0.38, 12, 6); c.fill();
    }
    line(c, [[620, 450], [790, 450], [826, 486], [837, 486]], 6);
  };
  const drawScript = (c) => {   // a beat sheet: time, picture, words
    c.lineWidth = 6; rr(c, 90, 100, 700, 400, 18); c.stroke();
    line(c, [[90, 168], [790, 168]], 5); line(c, [[220, 100], [220, 500]], 5); line(c, [[500, 100], [500, 500]], 5);
    for (let r = 0; r < 4; r++) { const y = 200 + r * 76; rr(c, 116, y, 76, 12, 6); c.fill(); rr(c, 246, y, 220, 12, 6); c.fill(); rr(c, 526, y, 230 - r * 30, 12, 6); c.fill(); }
    line(c, [[790, 420], [830, 420], [858, 448], [858, 463]], 6);
  };
  const drawRefs = (c) => {   // three locked cards: a face, the bottle, a place
    for (let k = 0; k < 3; k++) {
      const x = 96 + k * 236, y = 120;
      c.lineWidth = 7; rr(c, x, y, 200, 260, 20); c.stroke();
      if (k === 0) { dot(c, x + 100, y + 96, 44); c.beginPath(); c.ellipse(x + 100, y + 230, 74, 56, 0, Math.PI, 0); c.fill(); }
      if (k === 1) { rr(c, x + 70, y + 76, 60, 150, 22); c.fill(); rr(c, x + 80, y + 46, 40, 30, 6); c.fill(); }
      if (k === 2) { line(c, [[x + 20, y + 210], [x + 76, y + 120], [x + 116, y + 170], [x + 146, y + 136], [x + 182, y + 210]], 7); dot(c, x + 150, y + 76, 18); }
      line(c, [[x + 100, y + 260], [x + 100, 440]], 6);
    }
    c.font = '700 40px "Space Grotesk"'; c.fillText('LOCKED', 100, 470);
    line(c, [[334, 440], [790, 440], [826, 476], [837, 486]], 6);
  };
  const drawFrames = (c) => {   // six frames with a tick on each
    for (let r = 0; r < 2; r++) for (let k = 0; k < 3; k++) {
      const x = 96 + k * 236, y = 104 + r * 176;
      c.lineWidth = 6; rr(c, x, y, 204, 140, 12); c.stroke();
      line(c, [[x + 14, y + 120], [x + 70, y + 60], [x + 110, y + 96], [x + 140, y + 74], [x + 190, y + 120]], 5);
      dot(c, x + 176, y + 30, 18); c.strokeStyle = '#000'; line(c, [[x + 168, y + 30], [x + 174, y + 37], [x + 186, y + 23]], 5); c.strokeStyle = '#fff';
    }
    line(c, [[804, 314], [858, 368], [858, 463]], 6);
  };
  const drawEdit = (c) => {   // a timeline with three tracks, a playhead, and three formats out
    c.lineWidth = 6;
    for (let r = 0; r < 3; r++) for (let k = 0; k < 5 - r; k++) { const x = 96 + k * 108 + r * 30, y = 120 + r * 72; rr(c, x, y, 96, 52, 8); r ? c.stroke() : c.fill(); }
    line(c, [[330, 96], [330, 340]], 6);
    const F = [[96, 380, 160, 90], [290, 360, 70, 124], [394, 374, 100, 100]];
    for (const [x, y, w, h] of F) { rr(c, x, y, w, h, 8); c.stroke(); }
    line(c, [[494, 424], [790, 424], [858, 463]], 6);
  };
  const DIAGRAMS = { brief: drawBrief, quotes: drawQuotes, script: drawScript, refs: drawRefs, frames: drawFrames, edit: drawEdit };

  registerStyle({
    id: 'layer-stack',
    name: 'Layer Stack',
    family: 'Diagrams with depth',
    topic: 'How a brief becomes an ad: research, script, references, generate, edit',
    duration: 9,
    fonts: ['700 150px "Space Grotesk"', '500 76px "Space Grotesk"', '700 40px "Space Grotesk"', '500 80px "Inter"', '500 20px "IBM Plex Mono"'],
    render: { samples: 48, shutter: 0.5, tone: 'neutral', exposure: 1.12, contrast: 1.06, bloom: 0.5, bloomThreshold: 1.5, vignette: 0.4, grain: 0.016, fov: 18, background: '#040506' },

    build(S) {
      const { THREE, K, scene, camera } = S;
      const AMBER = new THREE.Color('#ff9a2a'), WHITE = new THREE.Color('#eaf6ff'), AQUA = new THREE.Color('#7fe3d6'), GLASS = new THREE.Color('#8fded4'), EMBER = new THREE.Color('#5a2606');
      K.env(S, { top: '#090b0e', horizon: '#11141a', bottom: '#020203', intensity: 1, panels: [
        { pos: [-21, 13, -21], size: [7, 12], color: '#eaf3ff', power: 3.2 },
        { pos: [24, 6, -6], size: [3, 16], color: '#bfe0ff', power: 7 },
        { pos: [-22, 5, 12], size: [3, 12], color: '#ffe4c8', power: 3 },
      ] });
      K.spot(S, { pos: [-7, 16, -6], target: [0.5, 2.6, 0], color: '#fff2e2', power: 1250, angle: 0.4, penumbra: 1, soft: 0.25, mapSize: 4096 });
      K.spot(S, { pos: [12, 5, -12], target: [0, 2.8, 0], color: '#9cc6ff', power: 420, angle: 0.42, penumbra: 1, shadow: false });

      const glass = (m) => {
        m.transparent = true; m.premultipliedAlpha = true; m.depthWrite = false;
        m.onBeforeCompile = (sh) => {
          sh.fragmentShader = sh.fragmentShader
            .replace('#include <opaque_fragment>', 'outgoingLight = totalDiffuse * diffuseColor.a + totalSpecular + totalEmissiveRadiance;\n#include <opaque_fragment>')
            .replace('#include <premultiplied_alpha_fragment>', '');
        };
        return m;
      };
      const slabGeo = (w, d, h, r, bev) => {
        const s = new THREE.Shape(), x = w / 2 - bev, y = d / 2 - bev; r -= bev;
        s.moveTo(-x + r, -y); s.lineTo(x - r, -y); s.absarc(x - r, -y + r, r, -Math.PI / 2, 0); s.lineTo(x, y - r); s.absarc(x - r, y - r, r, 0, Math.PI / 2);
        s.lineTo(-x + r, y); s.absarc(-x + r, y - r, r, Math.PI / 2, Math.PI); s.lineTo(-x, -y + r); s.absarc(-x + r, -y + r, r, Math.PI, Math.PI * 1.5);
        const g = new THREE.ExtrudeGeometry(s, { depth: h - bev * 2, bevelEnabled: true, bevelThickness: bev, bevelSize: bev, bevelSegments: 3, curveSegments: 24 });
        g.center(); g.rotateX(-Math.PI / 2);
        return g;
      };
      const sheetGeo = slabGeo(W, D, TH, 0.3, 0.014);
      const TEXT_X = 1.24;
      const flatGeo = K.roundedRect(W, D, 0.3, 16); flatGeo.rotateX(-Math.PI / 2);

      K.mirrorFloor(S, { y: 0, color: '#474b52', surfaceRoughness: 0.6, roughness: 0.3, strength: 0.3, fresnel: false, fade: 9 });
      const plinth = new THREE.Mesh(slabGeo(W + 0.4, D + 0.4, BASE, 0.4, 0.03), new THREE.MeshStandardMaterial({ color: '#30333a', roughness: 0.36, metalness: 0.9 }));
      plinth.position.y = BASE / 2; plinth.castShadow = plinth.receiveShadow = true; scene.add(plinth);
      const seed = { value: new THREE.Vector2() };

      const layers = LAYERS.map((L, i) => {
        const g = new THREE.Group(); scene.add(g);
        const order = (N - i) * 10;
        const face = glass(new THREE.MeshPhysicalMaterial({ color: '#e6f2f1', roughness: 0.3, opacity: 0.06 }));
        const edge = glass(new THREE.MeshPhysicalMaterial({ color: '#8fded4', roughness: 0.24, opacity: 0.5, side: THREE.DoubleSide, emissive: '#000000' }));
        const body = new THREE.Mesh(sheetGeo, [face, edge]); body.receiveShadow = true; body.renderOrder = order; g.add(body);
        const mask = K.canvasTex(2048, 1252, (c, w) => { c.fillStyle = '#000'; c.fillRect(0, 0, 2048, 1252); c.scale(w / 1000, w / 1000); sheet(c, i); DIAGRAMS[L.diagram](c); });
        const u = { uPad: { value: new THREE.Vector2(PAD[0] / 1000, 1 - PAD[1] / 611) }, uSize: { value: new THREE.Vector2(W, D) }, uWave: { value: [new THREE.Vector3(), new THREE.Vector3()] }, uTint: { value: [WHITE, AMBER] } };
        const ink = new THREE.MeshStandardMaterial({ color: '#d3dbdb', alphaMap: mask, transparent: true, depthWrite: false, roughness: 0.8, emissive: '#ffffff', emissiveIntensity: 0.14 });
        ink.onBeforeCompile = (sh) => {
          Object.assign(sh.uniforms, u);
          sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nuniform vec2 uPad, uSize; uniform vec3 uWave[2], uTint[2];')
            .replace('#include <emissivemap_fragment>', `#include <emissivemap_fragment>
              float padDist = length((vAlphaMapUv - uPad) * uSize);
              for (int k = 0; k < 2; k++) {
                float behind = smoothstep(uWave[k].x, uWave[k].x - 0.6, padDist), front = exp(-pow((padDist - uWave[k].x) / 0.26, 2.0));
                totalEmissiveRadiance += uTint[k] * (behind * uWave[k].y + front * uWave[k].z);
              }`);
        };
        const print = new THREE.Mesh(flatGeo, ink); print.position.y = TH / 2 + 0.003; print.receiveShadow = true; print.renderOrder = order + 1; g.add(print);
        const density = { value: new THREE.Vector2(0.16, 0.62) };
        const caster = new THREE.Mesh(flatGeo, new THREE.MeshBasicMaterial({ alphaMap: mask, alphaTest: 0.5, colorWrite: false, depthWrite: false, side: THREE.DoubleSide }));
        caster.customDepthMaterial = new THREE.MeshDepthMaterial({ alphaMap: mask, alphaTest: 0.5, side: THREE.DoubleSide });
        caster.customDepthMaterial.onBeforeCompile = (sh) => {
          sh.uniforms.uSeed = seed; sh.uniforms.uDensity = density;
          sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nuniform vec2 uSeed, uDensity;')
            .replace('#include <alphatest_fragment>', 'if (fract(sin(dot(gl_FragCoord.xy + uSeed, vec2(12.9898, 78.233))) * 43758.5453) > mix(uDensity.x, uDensity.y, diffuseColor.a)) discard;');
        };
        caster.position.y = -TH / 2 + 0.004; caster.castShadow = true; g.add(caster);

        const label = new THREE.Group(); scene.add(label);
        const flat = (color) => new THREE.MeshBasicMaterial({ color, transparent: true, depthWrite: false, depthTest: false });
        const pin = new THREE.Mesh(new THREE.CircleGeometry(0.05, 24), flat('#ffffff'));
        const lead = new THREE.Mesh(new THREE.PlaneGeometry(1, 0.017).translate(0.5, 0, 0), flat('#ffffff')); lead.position.x = 0.13;
        const text = (str, font, height, color, x, y) => {
          const m = K.textPlane(str, { font, height, color, align: 'left', letterSpacing: font.includes('Grotesk') ? 5 : 0 });
          m.geometry.translate(m.userData.size[0] / 2 - height * 0.25, 0, 0); m.material.depthTest = false; m.position.set(x, y, 0); label.add(m); return m;
        };
        const title = text(L.name, '700 150px "Space Grotesk"', 0.56, '#ffffff', TEXT_X, 0.15);
        const note = text(L.note, '500 80px "Inter"', 0.28, '#c3cbd3', TEXT_X + 0.01, -0.25);
        label.add(pin, lead);
        label.traverse((o) => { o.layers.set(1); o.renderOrder = 300; });
        return { g, face, edge, ink, wave: u.uWave.value, density: density.value, label, pin, lead, title, note };
      });
      camera.layers.enable(1);

      const answerTex = K.canvasTex(2048, 1252, (c, w) => { c.fillStyle = 'rgba(255,148,38,0.004)'; c.fillRect(0, 0, 2048, 1252); c.scale(w / 1000, w / 1000); drawAnswer(c); });
      const answer = new THREE.Mesh(flatGeo, new THREE.MeshBasicMaterial({ map: answerTex, transparent: true, alphaTest: 0.02, depthWrite: false }));
      answer.position.y = TH / 2 + 0.006; answer.renderOrder = N * 10 + 2; layers[0].g.add(answer);

      const padX = (PAD[0] / 1000 - 0.5) * W, padZ = (PAD[1] / 611 - 0.5) * D;
      const add = (blend) => new THREE.MeshBasicMaterial({ transparent: true, blending: blend ? THREE.AdditiveBlending : THREE.NormalBlending, depthWrite: false });
      const bead = new THREE.Mesh(new THREE.SphereGeometry(0.085, 24, 12), add(false)); bead.renderOrder = 200; scene.add(bead);
      const rod = () => { const m = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 1, 8), add(true)); m.renderOrder = 190; scene.add(m); return m; };
      const wireDown = rod(), wireUp = rod();
      const span = (m, y0, y1) => { m.visible = y1 - y0 > 0.01; m.position.set(padX, (y0 + y1) / 2, padZ); m.scale.y = Math.max(0.01, y1 - y0); };
      const glow = new THREE.PointLight('#ffffff', 0, 8, 2); scene.add(glow);
      const glide = (f) => K.lerp(f, K.ease.inOut(f), 0.65);
      const pulseAt = (t) => {
        if (t < hitDown(N - 1)) { const q = Math.max(0, (t - DOWN) / STEP_DOWN), k = Math.floor(q); return k + glide(q - k); }
        if (t < UP) return N - 1;
        if (t < ANSWER) { const q = (t - UP) / STEP_UP, k = Math.floor(q); return N - 1 - k - glide(q - k); }
        return 0;
      };
      const yAt = (f) => { const k = Math.min(N - 2, Math.floor(f)); return K.lerp(openY(k), openY(k + 1), f - k) + TH / 2; };

      // camera: the reference move, pulled back a little further because this stack has six sheets
      const rad = Math.PI / 180;
      const shot = (t) => {
        const p = K.spring(t - 0.4, 0.6, 1), d = t / 9;
        const az = (K.lerp(36, 31, p) - 6 * d) * rad, el = K.lerp(21, 19.5, p) * rad, dist = K.lerp(15.5, 27.5, p) - 2 * d;
        const aim = [K.lerp(0.3, 1.9, p), K.lerp(1.3, 2.75, p * p), K.lerp(0, -0.95, p)];
        return { aim, pos: [aim[0] + dist * Math.sin(az) * Math.cos(el), aim[1] + dist * Math.sin(el), aim[2] + dist * Math.cos(az) * Math.cos(el)] };
      };
      const col = new THREE.Color(), tmp = new THREE.Color();
      const plus = (c, k) => { col.r += c.r * k; col.g += c.g * k; col.b += c.b * k; };
      const after = (t, t0, tau) => (t < t0 ? 0 : Math.exp(-(t - t0) / tau));

      return {
        update(t) {
          const { pos, aim } = shot(t);
          K.look(camera, pos, aim); K.focus(camera, [1.2, aim[1], 0], 0.07);
          seed.value.set(K.hash(t * 977.1, 1) * 64, K.hash(t * 977.1, 2) * 64);
          layers.forEach((o, i) => {
            const y = layerY(i, t), v = (layerY(i, t + 0.02) - layerY(i, t - 0.02)) / 0.04;
            o.g.position.y = y; o.g.rotation.set(-v * 0.004, 0, v * 0.0025);
            const open = i === 0 ? 1 : K.smooth(0.03, 0.8, layerY(i - 1, t) - y);
            o.ink.opacity = open; o.face.opacity = 0.06 * (0.2 + 0.8 * open); o.face.specularIntensity = 0.12 + 0.88 * open; o.density.y = K.lerp(o.density.x, 0.62, open);
            const a = t - hitDown(i), b = t - hitUp(i);
            o.wave[0].set(Math.max(0, a) * 10, a > 0 ? 0.22 + 1.1 * Math.exp(-a / 0.35) : 0, a > 0 ? 2.6 * Math.exp(-a / 0.3) : 0);
            o.wave[1].set(Math.max(0, b) * 10, b > 0 ? (i ? 0.1 : 0.4) + 1.3 * Math.exp(-b / 0.4) : 0, b > 0 ? 3.0 * Math.exp(-b / 0.3) : 0);
            if (b > 0) o.wave[0].y *= Math.exp(-b / 0.2);
            const fa = after(t, hitDown(i), 0.3), fb = after(t, hitUp(i), 0.4), fc = after(t, hitUp(i), 0.9), back = b > 0 ? 1 : 0;
            const kept = i ? fc : back;
            col.copy(AQUA).multiplyScalar(0.3 * (1 - kept * 0.7)); plus(WHITE, 2.4 * fa); plus(AMBER, 3.0 * fb + 1.1 * kept);
            o.edge.emissive.copy(col); o.edge.color.copy(GLASS).lerp(EMBER, kept);
            const s = t - labelAt(i);
            o.label.position.set(W / 2, y, 0); o.label.quaternion.copy(camera.quaternion);
            o.pin.scale.setScalar(K.seg(s, 0, 0.22, K.ease.outBack)); o.pin.material.color.copy(WHITE).lerp(AMBER, back).multiplyScalar(1.3 + 2 * (fa + fb));
            o.lead.scale.x = Math.max(0.001, 0.96 * K.seg(s, 0.05, 0.4, K.ease.inOut)); o.lead.material.opacity = 0.7 * K.seg(s, 0.05, 0.15);
            const ta = K.seg(s, 0.2, 0.55, K.ease.out), na = K.seg(s, 0.32, 0.7, K.ease.out);
            o.title.material.opacity = ta; o.title.position.x = TEXT_X - (1 - ta) * 0.22;
            o.title.material.color.setScalar(1.25).lerp(tmp.copy(AMBER).multiplyScalar(1.7), Math.min(1, fb * 1.2)).multiplyScalar(1 + 0.5 * fa);
            o.note.material.opacity = na; o.note.position.x = TEXT_X + 0.01 - (1 - na) * 0.22;
          });
          const ans = t - ANSWER;
          answer.visible = ans > 0; answer.material.opacity = K.seg(ans, 0, 0.18); answer.material.color.setScalar(1.7 + 2.2 * after(t, ANSWER, 0.3));
          const f = pulseAt(t), by = yAt(f), goingUp = t >= UP - 0.14;
          const on = K.seg(t, DOWN - 0.06, DOWN + 0.04) * (1 - K.seg(t, hitDown(N - 1), hitDown(N - 1) + 0.08)) + K.seg(t, UP - 0.06, UP + 0.04) * (1 - K.seg(t, ANSWER, ANSWER + 0.1));
          bead.position.set(padX, by, padZ); bead.scale.setScalar(Math.max(0.001, on)); bead.visible = on > 0.001;
          bead.material.color.copy(goingUp ? AMBER : WHITE).multiplyScalar(goingUp ? 9 : 6);
          const top = yAt(0), bottom = yAt(N - 1), upK = K.seg(t, UP, ANSWER);
          span(wireDown, t < DOWN ? top : t < UP ? by : bottom, top); wireDown.material.color.copy(WHITE).multiplyScalar(0.55 * (1 - upK));
          span(wireUp, bottom, t < UP ? bottom : by); wireUp.material.color.copy(AMBER).multiplyScalar(1.5 + 2 * after(t, ANSWER, 0.4));
          glow.position.set(padX, by + 0.12, padZ); glow.color.copy(goingUp ? AMBER : WHITE);
          glow.intensity = 7 * on + 5 * after(t, hitDown(N - 1), 0.25) + 3 * after(t, ANSWER, 0.5);
        },
        overlay(ctx, t) {
          const a = 1 - K.seg(t, 0.5, 0.95, K.ease.inOut);
          if (a <= 0) return;
          ctx.globalAlpha = a; ctx.fillStyle = '#f2f5f5'; ctx.textBaseline = 'alphabetic';
          ctx.font = '500 76px "Space Grotesk"'; ctx.fillText(TITLE[0], 118, 172 - (1 - a) * 26);
          ctx.font = '700 76px "Space Grotesk"'; ctx.fillText(TITLE[1], 118, 262 - (1 - a) * 26);
        },
      };
    },

    sound(k) {
      k.bed('room', 0, 9, { gain: 0.9 });
      const SCALE = ['E6', 'B5', 'G#5', 'E5', 'B4', 'G#4'];
      LAYERS.forEach((_, i) => {
        const pan = 0.25 - i * 0.03;
        k.play('whoosh', LIFT[i] - 0.03, { gain: 0.75 - i * 0.07, dur: 0.55 / FREQ[i], top: 1900 - i * 180, pan: -0.15 });
        k.play('ding', LIFT[i] + 0.62 / FREQ[i], { gain: 0.5, f: SCALE[i], pan: -0.15 });
        k.withMinor(() => { k.play('tick', labelAt(i) + 0.05, { gain: 0.7, f: 5200, pan }); k.play('click', labelAt(i) + 0.3, { gain: 0.45, pan }); });
      });
      LAYERS.forEach((_, i) => { k.tone(hitDown(i), { f: SCALE[i], type: 'sine', dur: 0.5, gain: 0.12, verb: 0.35, pan: 0.2 }); k.play('tock', hitDown(i), { gain: 0.36, f: 1500 - i * 170, pan: 0.2 }); });
      k.play('thud', hitDown(N - 1), { gain: 0.75, f: 110 });
      k.play('buzz', hitDown(N - 1) + 0.04, { gain: 0.5, dur: UP - hitDown(N - 1) - 0.1, f: 82 });
      k.play('riser', UP - 0.1, { gain: 0.4, dur: ANSWER - UP + 0.1 });
      for (let i = N - 2; i >= 0; i--) k.tone(hitUp(i), { f: SCALE[i], type: 'triangle', dur: 0.45, gain: 0.13, verb: 0.3, pan: 0.2 });
      k.play('success', ANSWER, { gain: 0.9, f: 'E6' });
      k.play('pop', ANSWER + 0.02, { gain: 0.5, f: 520, pan: -0.2 });
    },
  });
}
