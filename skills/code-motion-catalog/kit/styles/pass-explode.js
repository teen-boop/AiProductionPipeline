{
  // ---------------------------------------------------------------- content: one shot opened into its render passes
  // Invented sample: a dusk street plate (built in the shader, no image) that opens into depth, position, solve and a
  // point cloud, then telescopes back and lands on the next shot. Every pass reads the SAME scene function, so the
  // silhouettes line up across the stack.
  const PASSES = [
    { label: '01  PLATE', mode: 0 },
    { label: '02  DEPTH', mode: 1 },
    { label: '03  POSITION', mode: 2 },
    { label: '04  SOLVE', mode: 3 },
    { label: '05  POINT CLOUD', mode: 4 },
  ];
  const N = PASSES.length;

  // ---------------------------------------------------------------- timing (picture and sound share it)
  const TURN = 0.8, TURN_LEN = 0.55;          // the card yaws and pitches
  const SLIDE = 0.95, STAGGER = 0.05;          // passes slide back on springs
  const LABEL = [1.55, 2.15, 2.75, 3.35, 3.95];
  const CLOSE = 4.55, CLOSE_LEN = 0.6;         // the stack telescopes back into one card
  const SWAP = CLOSE + CLOSE_LEN - 0.05;       // lands on the next shot
  const DUR = 6;

  // ---------------------------------------------------------------- the card
  const CW = 3.6, CH = CW * 9 / 16, PADW = 0.5, RAD = 0.16, GAP = CW * 0.55;
  const YAW = -35 * Math.PI / 180, PITCH = 8 * Math.PI / 180;

  // the shared scene: depth 0 near .. 1 far, a subject matte and an albedo, all from uv. uShot blends to the next shot.
  const SCENE = `
    float sdBox(vec2 p, vec2 b){ vec2 d = abs(p) - b; return length(max(d, 0.0)) + min(max(d.x, d.y), 0.0); }
    float sdCapsule(vec2 p, vec2 a, vec2 b, float r){ vec2 pa = p - a, ba = b - a; float h = clamp(dot(pa, ba) / dot(ba, ba), 0.0, 1.0); return length(pa - ba * h) - r; }
    float h12(vec2 p){ p = fract(p * vec2(123.34, 456.21)); p += dot(p, p + 45.32); return fract(p.x * p.y); }
    void sceneAt(vec2 uv, float shot, out float depth, out float matte, out vec3 alb, out float lit){
      uv = clamp(uv, 0.0, 1.0);   // the card plane has a glow margin: uv outside 0..1 would make pow() return NaN
      float hor = mix(0.52, 0.46, shot);
      // sky and ground
      depth = 1.0; matte = 0.0; lit = 0.0;
      alb = mix(mix(vec3(1.0, 0.42, 0.18), vec3(0.95, 0.55, 0.32), shot), mix(vec3(0.16, 0.08, 0.22), vec3(0.06, 0.1, 0.22), shot), smoothstep(hor, 1.0, uv.y));
      if (uv.y < hor) { depth = mix(0.12, 0.98, pow(uv.y / hor, 1.6)); alb = vec3(0.13, 0.09, 0.08) * (0.6 + 0.6 * uv.y / hor);
        float lane = abs(abs(uv.x - 0.5) - (hor - uv.y) * 0.9); alb += vec3(0.5, 0.3, 0.18) * 0.35 * (1.0 - smoothstep(0.0, 0.004, lane)); }
      // buildings, left and right, stepping back toward the horizon
      for (int k = 0; k < 6; k++) {
        float fk = float(k), side = k < 3 ? -1.0 : 1.0, j = mod(fk, 3.0);
        float cx = 0.5 + side * (0.42 - j * 0.11), w = 0.1 - j * 0.02, top = hor + 0.36 - j * 0.1 + 0.05 * h12(vec2(fk, 3.0));
        float bd = 0.35 + j * 0.2;
        if (abs(uv.x - cx) < w && uv.y > hor - 0.05 * (1.0 - j * 0.3) && uv.y < top && bd < depth) {
          depth = bd; alb = vec3(0.07, 0.05, 0.06) + 0.02 * j;
          vec2 g = vec2((uv.x - cx) / w * 4.0, uv.y * 40.0); vec2 c = fract(g) - 0.5;
          float win = step(abs(c.x), 0.25) * step(abs(c.y), 0.22) * step(0.55, h12(floor(g) + fk + floor(shot * 3.0)));
          alb += win * mix(vec3(1.0, 0.7, 0.35), vec3(0.6, 0.8, 1.0), shot) * 0.9; lit = max(lit, win);
        }
      }
      // a street lamp
      float lampX = mix(0.66, 0.3, shot);
      if (abs(uv.x - lampX) < 0.004 && uv.y < hor + 0.3 && uv.y > hor - 0.12 && 0.3 < depth) { depth = 0.3; alb = vec3(0.05); }
      float bulb = length((uv - vec2(lampX, hor + 0.3)) * vec2(16.0 / 9.0, 1.0));
      if (bulb < 0.018 && 0.3 < depth) { depth = 0.3; alb = vec3(3.0, 2.2, 1.4); lit = 1.0; }
      // the subject: a walking figure, nearest thing in the frame
      vec2 fp = vec2(mix(0.42, 0.6, shot), 0.0);
      vec2 q = (uv - fp) * vec2(16.0 / 9.0, 1.0);
      float body = sdCapsule(q, vec2(0.0, 0.14), vec2(0.0, 0.43), 0.06);
      body = min(body, length(q - vec2(0.0, 0.51)) - 0.045);
      body = min(body, sdCapsule(q, vec2(0.0, 0.16), vec2(-0.05, 0.02), 0.028));
      body = min(body, sdCapsule(q, vec2(0.0, 0.16), vec2(0.06, 0.03), 0.028));
      if (body < 0.0) { depth = 0.18 + 0.02 * q.y; matte = 1.0; alb = vec3(0.04, 0.03, 0.035) + vec3(1.0, 0.25, 0.15) * 0.6 * smoothstep(-0.015, 0.0, body); }
    }`;

  const CARD_VS = `varying vec2 vP; void main(){ vP = position.xy; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`;
  const CARD_FS = SCENE + `
    uniform vec2 uSize; uniform float uRad, uMode, uShot, uOpacity, uRim, uGlow, uFlash; uniform vec3 uRimCol;
    varying vec2 vP;
    float sdRound(vec2 p, vec2 b, float r){ vec2 d = abs(p) - b + r; return length(max(d, 0.0)) + min(max(d.x, d.y), 0.0) - r; }
    void main(){
      float d = sdRound(vP, uSize * 0.5, uRad), px = fwidth(d);
      float inside = 1.0 - smoothstep(-px, px, d);
      vec2 uv = vP / uSize + 0.5;
      float depth, matte, lit; vec3 alb; sceneAt(uv, uShot, depth, matte, alb, lit);
      vec3 c;
      if (uMode < 0.5) c = alb * 1.15;
      else if (uMode < 1.5) c = vec3(pow(1.0 - depth, 1.4)) * 0.95 + matte * 0.08;
      else if (uMode < 2.5) { vec3 a = vec3(0.95, 0.12, 0.55), b = vec3(0.32, 0.12, 0.95); c = mix(a, b, depth) * (0.35 + 0.75 * uv.x) + vec3(0.0, 0.0, 0.25) * uv.y; c *= 0.85; }
      else if (uMode < 3.5) {   // solve: a coarse mesh bent by depth, plus tracked corners
        vec2 g = uv * vec2(32.0, 18.0) + vec2(0.0, (1.0 - depth) * 3.0);
        vec2 f = abs(fract(g) - 0.5); float line = max(smoothstep(0.46, 0.5, f.x), smoothstep(0.46, 0.5, f.y));
        c = vec3(0.03, 0.04, 0.05) + vec3(0.35, 0.85, 1.0) * line * (0.25 + 0.75 * (1.0 - depth)) + vec3(1.0, 0.35, 0.25) * matte * line * 1.2;
      } else c = vec3(0.01, 0.015, 0.03);
      c *= 1.0 + uFlash * 2.5;
      float rim = exp(-abs(d) / 0.008) * uRim;
      float glow = exp(-max(d, 0.0) / 0.12) * (1.0 - inside) * uGlow;
      vec3 col = c * inside + uRimCol * (rim * 1.4 + glow * 0.6);
      float a = max(inside, max(rim, glow * 0.5)) * uOpacity;
      gl_FragColor = vec4(col * uOpacity, a);
    }`;

  registerStyle({
    id: 'pass-explode',
    name: 'Pass Explode',
    family: 'Diagrams with depth',
    topic: 'One footage card opens into its render passes (depth, position, solve, point cloud) and lands on the next shot',
    duration: DUR,
    fonts: ['500 22px "IBM Plex Mono"', '600 64px "Inter"'],
    render: { samples: 40, shutter: 0.5, tone: 'neutral', exposure: 1.0, contrast: 1.04, bloom: 0.45, bloomThreshold: 1.1, vignette: 0.45, grain: 0.02, fov: 30, background: '#0c0a09' },

    build(S) {
      const { THREE, K, scene, camera } = S;
      const RED = new THREE.Color('#ff3b2f');

      // a warm, almost black void with one soft pool of light behind the stack
      const back = new THREE.Mesh(new THREE.PlaneGeometry(60, 34), new THREE.ShaderMaterial({
        depthWrite: false,
        vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
        fragmentShader: 'varying vec2 vUv; void main(){ float r = length((vUv - vec2(0.52, 0.5)) * vec2(1.6, 1.0)); gl_FragColor = vec4(mix(vec3(0.075, 0.05, 0.04), vec3(0.012, 0.01, 0.009), smoothstep(0.0, 0.42, r)), 1.0); }',
      }));
      back.position.z = -14; back.renderOrder = -10; scene.add(back);

      const stack = new THREE.Group(); scene.add(stack);
      const geo = new THREE.PlaneGeometry(CW + PADW * 2, CH + PADW * 2);
      const cards = PASSES.map((P, i) => {
        const u = { uSize: { value: new THREE.Vector2(CW, CH) }, uRad: { value: RAD }, uMode: { value: P.mode }, uShot: { value: 0 }, uOpacity: { value: 1 }, uRim: { value: 0.5 }, uGlow: { value: 0.3 }, uFlash: { value: 0 }, uRimCol: { value: RED.clone() } };
        const m = new THREE.Mesh(geo, new THREE.ShaderMaterial({ vertexShader: CARD_VS, fragmentShader: CARD_FS, uniforms: u, transparent: true, depthWrite: false, extensions: { derivatives: true } }));
        m.renderOrder = (N - i) * 2; stack.add(m);
        return { m, u };
      });

      // the point cloud pass: real points pushed back by the same depth, so it has volume when the stack turns
      const GX = 176, GY = 99, pos = new Float32Array(GX * GY * 3), rnd = new Float32Array(GX * GY);
      const r = K.rng(7);
      for (let y = 0, k = 0; y < GY; y++) for (let x = 0; x < GX; x++, k++) { pos.set([(x + r.range(-0.4, 0.4)) / (GX - 1) - 0.5, (y + r.range(-0.4, 0.4)) / (GY - 1) - 0.5, 0], k * 3); rnd[k] = r(); }
      const pg = new THREE.BufferGeometry(); pg.setAttribute('position', new THREE.BufferAttribute(pos, 3)); pg.setAttribute('rnd', new THREE.BufferAttribute(rnd, 1));
      const pu = { uSize: { value: new THREE.Vector2(CW, CH) }, uShot: { value: 0 }, uOpacity: { value: 1 }, uPush: { value: 0.9 }, uPx: { value: S.H / 1080 } };
      const cloud = new THREE.Points(pg, new THREE.ShaderMaterial({
        uniforms: pu, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
        vertexShader: SCENE + `
          uniform vec2 uSize; uniform float uShot, uPush, uPx; attribute float rnd; varying float vA; varying vec3 vC;
          void main(){
            vec2 uv = position.xy + 0.5; float depth, matte, lit; vec3 alb; sceneAt(uv, uShot, depth, matte, alb, lit);
            vec3 p = vec3(position.xy * uSize, (1.0 - depth) * uPush);   // near points come forward off the card
            vec4 mv = modelViewMatrix * vec4(p, 1.0); gl_Position = projectionMatrix * mv;
            gl_PointSize = uPx * (1.4 + 2.6 * (1.0 - depth) + 2.0 * matte) * (0.7 + 0.6 * rnd) * 8.0 / -mv.z;
            vA = (0.35 + 0.65 * (1.0 - depth)) * (depth > 0.99 ? 0.12 : 1.0);
            vC = mix(vec3(0.25, 0.55, 1.0), vec3(0.75, 0.9, 1.0), matte + lit * 0.6);
          }`,
        fragmentShader: 'uniform float uOpacity; varying float vA; varying vec3 vC; void main(){ vec2 d = gl_PointCoord - 0.5; float a = smoothstep(0.5, 0.15, length(d)); gl_FragColor = vec4(vC * a * vA * uOpacity * 2.2, 1.0); }',
      }));
      cloud.renderOrder = 3; cards[N - 1].m.add(cloud); cloud.position.z = 0.002;   // drawn after its own card, before the next one

      // timing helpers
      const turn = (t) => K.seg(t, TURN, TURN + TURN_LEN, K.ease.inOut) * (1 - K.seg(t, CLOSE, CLOSE + CLOSE_LEN, K.ease.inOut));
      const slide = (i, t) => {
        if (i === 0) return 0;
        const out = K.spring(t - SLIDE - (i - 1) * STAGGER, 1.1, 0.72);
        const back = K.seg(t, CLOSE + (N - 1 - i) * 0.03, CLOSE + CLOSE_LEN - 0.08, K.ease.in);
        return out * (1 - back);
      };
      const open = (t) => K.seg(t, SLIDE, SLIDE + 0.5, K.ease.out) * (1 - K.seg(t, CLOSE, CLOSE + CLOSE_LEN, K.ease.in));
      const v3 = new THREE.Vector3(), mid = new THREE.Vector3(), eul = new THREE.Euler();
      const anchors = [];

      return {
        update(t) {
          // camera: almost still; a slow truck (about 3% of frame width per second) while the stack is open
          const a = turn(t), o = open(t);
          // aim at the middle of the open stack, so the stack stays centred while it opens and closes
          mid.set(0, 0, -(N - 1) * 0.36 * GAP * o).applyEuler(eul.set(PITCH * a, YAW * a, 0));
          const truck = 0.22 * (Math.max(0, Math.min(t, CLOSE) - SLIDE) - (CLOSE - SLIDE) / 2) * o;
          const drift = 0.04 * Math.sin(t * 0.9), dist = 8.6 + 2.6 * o - 0.25 * t / DUR;
          K.look(camera, [mid.x + truck, 0.3 + drift, mid.z + dist], [mid.x + truck * 0.9, 0.22 * o, mid.z], 30);
          K.focus(camera, dist, 0.015);

          stack.rotation.set(PITCH * a, YAW * a, 0);
          stack.position.set(0.15 * Math.sin(t * 0.7), 0.05 * Math.sin(t * 1.1), 0);
          const shot = K.seg(t, SWAP - 0.08, SWAP + 0.12, K.ease.inOut);
          const flash = Math.exp(-Math.abs(t - SWAP) / 0.07);
          anchors.length = 0;
          cards.forEach((c, i) => {
            const s = slide(i, t);
            c.m.position.set(0, 0, -i * GAP * s);
            c.u.uShot.value = shot;
            c.u.uOpacity.value = i === 0 ? 1 : K.smooth(0.02, 0.25, s);
            c.u.uRim.value = 0.35 + 0.5 * flash;
            c.u.uGlow.value = (i === 0 ? 0.35 : 0.2) + 0.6 * flash;
            c.u.uFlash.value = i === 0 ? flash * 0.5 : 0;
            c.m.visible = c.u.uOpacity.value > 0.003;
            c.m.updateMatrixWorld();
            v3.set(CW / 2 - 0.12, CH / 2, 0).applyMatrix4(c.m.matrixWorld).project(camera);
            anchors.push([(v3.x + 1) / 2, (1 - v3.y) / 2, c.u.uOpacity.value]);
          });
          pu.uShot.value = shot; pu.uOpacity.value = cards[N - 1].u.uOpacity.value; pu.uPush.value = 0.4 + 1.4 * open(t);
        },
        overlay(ctx, t, W, H) {
          if (window.NO_TEXT) return;
          ctx.font = '500 22px "IBM Plex Mono"'; ctx.textBaseline = 'middle'; ctx.letterSpacing = '2px';
          PASSES.forEach((P, i) => {
            const s = t - LABEL[i], gone = K.seg(t, CLOSE - 0.05, CLOSE + 0.25);
            const a = K.seg(s, 0, 0.25, K.ease.out) * (1 - gone) * anchors[i][2];
            if (a <= 0.01) return;
            // a staircase: the front card's label sits highest, so the labels never cover each other
            const x = anchors[i][0] * W, y = anchors[i][1] * H, w = ctx.measureText(P.label).width + 36, h = 40;
            const ly = Math.min(y, anchors[0][1] * H) - 36 - (N - 1 - i) * 42;
            ctx.save(); ctx.globalAlpha = a;
            ctx.strokeStyle = 'rgba(255,255,255,0.35)'; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(x, y - 4); ctx.lineTo(x, ly + h / 2); ctx.stroke();
            ctx.fillStyle = '#ff3b2f'; ctx.beginPath(); ctx.arc(x, y - 4, 3.5, 0, Math.PI * 2); ctx.fill();
            ctx.translate(x - 14, ly - (1 - a) * 10);
            ctx.fillStyle = 'rgba(16,13,12,0.86)'; ctx.beginPath(); ctx.roundRect(0, -h / 2, w, h, 8); ctx.fill();
            ctx.strokeStyle = 'rgba(255,255,255,0.16)'; ctx.lineWidth = 1; ctx.stroke();
            // red glow sweep across the chip as it lands
            const sw = K.seg(s, 0.05, 0.55, K.ease.inOut);
            if (sw > 0 && sw < 1) { const g = ctx.createLinearGradient(w * sw - 60, 0, w * sw + 60, 0); g.addColorStop(0, 'rgba(255,59,47,0)'); g.addColorStop(0.5, 'rgba(255,59,47,0.55)'); g.addColorStop(1, 'rgba(255,59,47,0)'); ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(0, -h / 2, w, h, 8); ctx.fill(); }
            ctx.fillStyle = '#ff3b2f'; ctx.beginPath(); ctx.arc(14, 0, 4, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#f3efec'; ctx.fillText(P.label, 26, 1);
            ctx.restore();
          });
        },
      };
    },

    sound(k) {
      k.bed('room', 0, DUR, { gain: 0.8 });
      k.play('swish', TURN - 0.05, { gain: 0.6, dur: 0.4 });
      k.play('whoosh', SLIDE - 0.05, { gain: 0.7, dur: 0.7, top: 1600 });
      for (let i = 1; i < N; i++) k.play('tock', SLIDE + 0.2 + (i - 1) * STAGGER * 2, { gain: 0.3, f: 1300 - i * 160, pan: 0.1 * i });
      LABEL.forEach((t, i) => k.withMinor(() => { k.play('tick', t, { gain: 0.6, f: 5000 }); k.play('blip', t + 0.06, { gain: 0.35, f: ['E6', 'G6', 'A6', 'B6', 'D7'][i] }); }));
      k.play('riser', CLOSE - 0.3, { gain: 0.45, dur: CLOSE_LEN + 0.25 });
      k.play('impact', SWAP, { gain: 0.8, f: 120 });
      k.play('ding', SWAP + 0.05, { gain: 0.4, f: 'B5' });
    },
  });
}
