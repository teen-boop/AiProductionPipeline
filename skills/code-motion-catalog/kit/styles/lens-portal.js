{
  // ---------------------------------------------------------------- content: a footage card swallowed by a lens
  // Invented sample: a night-street footage card closes inside a dark iris; on the switch frame the iris is exactly the
  // lens barrel of an invented five-lens sensor bar, so the cut is invisible; then a fast pull back to the whole product.
  const HEADLINE = ['Five lenses.', 'One take.'];
  const LENS_X = [-2.4, -1.2, 0, 1.2, 2.4];
  const HERO = 2;                                   // the lens the card falls into

  // ---------------------------------------------------------------- timing (picture and sound share it)
  const CLOSE = 0.35, SWITCH = 0.95;               // iris closes 0.6 s, ease in
  const PULL = SWITCH + 0.12, PULL_LEN = 0.9;       // pull back 0.9 s, ease out expo
  const RINGS = 2.05, RING_STEP = 0.1;              // the five red rings light one after another
  const TYPE = 2.15, DUR = 3.2;

  // ---------------------------------------------------------------- the product (dimensions in world units)
  const BODY = [6.2, 1.5, 1.1], FRONT = BODY[2] / 2;
  const GLASS_R = 0.33, RING_R = 0.355, BARREL_R = 0.46, GLASS_Z = FRONT + 0.2;
  const SWITCH_FOV = 20, IRIS_R = 0.3;             // iris radius on the switch frame, as a fraction of half the frame height
  const SWITCH_DIST = GLASS_R / (IRIS_R * Math.tan((SWITCH_FOV / 2) * Math.PI / 180));   // so the glass fills the iris exactly
  const CARD_END = 1.25;                            // card half-height at the switch, in iris radii

  const IRIS_FS = `
    uniform sampler2D uCard; uniform float uR, uAspect, uScale, uShow, uLines, uSeed; varying vec2 vUv;
    float h11(float x){ return fract(sin(x * 127.1) * 43758.5453); }
    void main(){
      vec2 p = (vUv - 0.5) * 2.0; p.x *= uAspect; float r = length(p), px = 2.0 / 1080.0;
      if (uShow > 0.5) {
        vec2 cuv = vec2(p.x / (uAspect * uScale), p.y / uScale) * 0.5 + 0.5;
        vec3 card = texture2D(uCard, clamp(cuv, 0.0, 1.0)).rgb;
        float inside = 1.0 - smoothstep(uR - px, uR + px, r);
        float ringR = uR * ${(RING_R / GLASS_R).toFixed(4)};
        vec3 dark = vec3(0.012, 0.011, 0.012) * (1.0 - 0.4 * smoothstep(0.4, 2.0, r));
        vec3 red = vec3(1.0, 0.13, 0.08);
        float ring = exp(-pow((r - ringR) / (0.0035 + 0.03 * (uR - ${IRIS_R.toFixed(3)})), 2.0));   // thin like the real ring on the switch frame
        float halo = exp(-max(r - uR, 0.0) / (0.04 + 0.1 * uR)) * (1.0 - inside);
        vec3 c = mix(dark + red * (ring * 2.0 + halo * 0.18), card, inside);
        gl_FragColor = vec4(c, 1.0);
      } else {
        // radial speed lines after the switch, strength = camera speed
        float a = atan(p.y, p.x) / 6.2831853 * 90.0, k = floor(a);
        float line = smoothstep(0.42, 0.5, abs(fract(a) - 0.5)) * step(0.6, h11(k + uSeed));
        float l = line * smoothstep(0.35, 1.4, r) * uLines;
        gl_FragColor = vec4(vec3(1.0, 0.92, 0.88) * l, l * 0.6);
      }
    }`;

  registerStyle({
    id: 'lens-portal',
    name: 'Lens Portal',
    family: 'Transitions',
    topic: 'A footage card closes inside a dark iris that is exactly the product lens, then a fast pull back to the product',
    duration: DUR,
    fonts: ['600 72px "Inter"', '300 72px "Inter"', '500 22px "IBM Plex Mono"'],
    render: { samples: 40, shutter: 0.6, tone: 'filmic', exposure: 1.1, contrast: 1.05, bloom: 0.5, bloomThreshold: 1.0, vignette: 0.4, grain: 0.022, fov: SWITCH_FOV, background: '#050505' },

    build(S) {
      const { THREE, K, scene, camera } = S;
      const aspect = S.W / S.H;

      // ---- the footage card (canvas): a wet night street with bokeh, a figure and a small slate
      const cardTex = K.canvasTex(1920, 1080, (c, w, h) => {
        const r = K.rng(11);
        const g = c.createLinearGradient(0, 0, 0, h); g.addColorStop(0, '#0b1430'); g.addColorStop(0.55, '#1d2347'); g.addColorStop(1, '#0a0c16');
        c.fillStyle = g; c.fillRect(0, 0, w, h);
        for (let i = 0; i < 70; i++) {   // bokeh
          const x = r() * w, y = r.range(0.15, 0.6) * h, rad = r.range(14, 60), hue = r.pick(['255,150,70', '255,80,60', '120,170,255', '255,220,160']);
          const b = c.createRadialGradient(x, y, 0, x, y, rad); b.addColorStop(0, `rgba(${hue},0.55)`); b.addColorStop(0.7, `rgba(${hue},0.25)`); b.addColorStop(1, `rgba(${hue},0)`);
          c.fillStyle = b; c.beginPath(); c.arc(x, y, rad, 0, Math.PI * 2); c.fill();
          if (i % 2 === 0) {   // its smeared reflection on the wet street
            const ry = h * 0.64 + (h * 0.6 - y) * 0.3, s = c.createLinearGradient(0, ry, 0, ry + rad * 5);
            s.addColorStop(0, `rgba(${hue},0.22)`); s.addColorStop(1, `rgba(${hue},0)`);
            c.filter = 'blur(10px)'; c.fillStyle = s; c.fillRect(x - rad * 0.25, ry, rad * 0.5, rad * 5); c.filter = 'none';
          }
        }
        const wet = c.createLinearGradient(0, h * 0.62, 0, h); wet.addColorStop(0, 'rgba(255,120,70,0.22)'); wet.addColorStop(1, 'rgba(40,60,140,0.1)');
        c.fillStyle = wet; c.fillRect(0, h * 0.62, w, h);
        c.fillStyle = '#05060a'; c.beginPath(); c.ellipse(w * 0.52, h * 0.38, 34, 40, 0, 0, Math.PI * 2); c.fill();   // a figure
        c.beginPath(); c.roundRect(w * 0.52 - 62, h * 0.43, 124, 330, 50); c.fill();
        c.fillStyle = 'rgba(255,90,60,0.5)'; c.fillRect(w * 0.52 + 52, h * 0.44, 6, 300);                         // red rim light
        c.font = '500 30px "IBM Plex Mono"'; c.fillStyle = 'rgba(255,255,255,0.75)'; c.fillText('PLATE 014   TAKE 3', 70, 90);
        c.fillStyle = '#ff3b2f'; c.beginPath(); c.arc(50, 80, 9, 0, Math.PI * 2); c.fill();
      });

      // ---- studio
      K.env(S, { top: '#08090b', horizon: '#121317', bottom: '#030303', intensity: 1, panels: [
        { pos: [-9, 8, 7], size: [7, 3], color: '#fff1e4', power: 5 },
        { pos: [10, 3, 4], size: [2, 9], color: '#cfe0ff', power: 6 },
        { pos: [0, 12, -6], size: [12, 2], color: '#ffffff', power: 3 },
        { pos: [0, 5, 13], size: [12, 4], color: '#e8ecf2', power: 1.6 },   // broad front panel: a soft gradient on the front face
      ] });
      const key = K.spot(S, { pos: [-6, 9, 8], target: [0, 0, 0], color: '#fff3e6', power: 1400, angle: 0.45, penumbra: 1, soft: 0.6, mapSize: 2048 });
      const rim = K.spot(S, { pos: [8, 2, -5], target: [0, 0.3, 0], color: '#ff5a40', power: 260, angle: 0.5, penumbra: 1, shadow: false });
      K.mirrorFloor(S, { y: -BODY[1] / 2 - 0.02, color: '#0c0c0d', surfaceRoughness: 0.5, roughness: 0.25, strength: 0.35, fade: 10 });

      // ---- the sensor bar
      const graphite = new THREE.MeshPhysicalMaterial({ color: '#2b2d33', roughness: 0.36, metalness: 0.3, clearcoat: 0.6, clearcoatRoughness: 0.25 });
      const body = new THREE.Mesh(K.roundedBox(BODY[0], BODY[1], BODY[2], 0.36, 8), graphite); body.castShadow = body.receiveShadow = true; scene.add(body);
      const anod = new THREE.MeshPhysicalMaterial({ color: '#0c0c0e', roughness: 0.3, metalness: 0.85 });
      const lathe = (pts) => new THREE.LatheGeometry(pts.map(([r, z]) => new THREE.Vector2(r, z)), 96).rotateX(Math.PI / 2);
      const barrelGeo = lathe([[GLASS_R - 0.01, GLASS_Z - 0.02], [RING_R + 0.02, GLASS_Z + 0.01], [0.42, GLASS_Z + 0.03], [BARREL_R, GLASS_Z + 0.01], [BARREL_R + 0.02, FRONT + 0.02], [BARREL_R + 0.06, FRONT - 0.01]]);
      const lenses = LENS_X.map((x, i) => {
        const g = new THREE.Group(); g.position.x = x; scene.add(g);
        const barrel = new THREE.Mesh(barrelGeo, anod); barrel.castShadow = true; g.add(barrel);
        const tex = cardTex.clone(); tex.needsUpdate = true;
        const fx = 1 / (CARD_END * aspect), fy = 1 / CARD_END;          // the part of the card the iris showed on the switch frame
        tex.repeat.set(fx, fy); tex.offset.set((1 - fx) / 2, (1 - fy) / 2);
        const glass = new THREE.MeshPhysicalMaterial({ color: '#030406', roughness: 0.04, metalness: 0, clearcoat: 1, clearcoatRoughness: 0.02, emissive: '#ffffff', emissiveMap: tex, emissiveIntensity: 0 });
        const disc = new THREE.Mesh(new THREE.CircleGeometry(GLASS_R, 96), glass); disc.position.z = GLASS_Z - 0.03; g.add(disc);
        const coat = new THREE.Mesh(new THREE.RingGeometry(0.1, GLASS_R * 0.92, 96), new THREE.MeshBasicMaterial({ color: '#3a2a6a', transparent: true, opacity: 0.18, blending: THREE.AdditiveBlending, depthWrite: false }));
        coat.position.z = GLASS_Z - 0.025; g.add(coat);
        const ring = new THREE.Mesh(new THREE.TorusGeometry(RING_R, 0.008, 12, 128), new THREE.MeshBasicMaterial({ color: '#ff2a1a' }));
        ring.position.z = GLASS_Z; g.add(ring);
        return { glass, ring, i };
      });

      // ---- the iris: a full-screen quad drawn last (the vertex shader ignores the camera)
      const iu = { uCard: { value: cardTex }, uR: { value: 3 }, uAspect: { value: aspect }, uScale: { value: 1 }, uShow: { value: 1 }, uLines: { value: 0 }, uSeed: { value: 0 } };
      const iris = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), new THREE.ShaderMaterial({
        uniforms: iu, fragmentShader: IRIS_FS, transparent: true, depthTest: false, depthWrite: false,
        vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }',
      }));
      iris.frustumCulled = false; iris.renderOrder = 1000; scene.add(iris);

      // ---- camera: the switch pose looks straight into the hero lens; then the pull back
      const hx = LENS_X[HERO];
      const P0 = [hx, 0, GLASS_Z + SWITCH_DIST], A0 = [hx, 0, GLASS_Z];
      const P1 = [2.6, 1.35, 8.4], A1 = [0, -0.05, 0.1], P2 = [2.25, 1.2, 7.7];
      const pose = (t) => {
        const u = K.seg(t, PULL, PULL + PULL_LEN, K.ease.outExpo), v = K.seg(t, PULL + PULL_LEN, DUR, K.ease.inOut);
        const pos = P0.map((a, k) => K.lerp(K.lerp(a, P1[k], u), P2[k], v));
        pos[2] -= 0.04 * K.seg(t, SWITCH, PULL);                          // a hair of push on the hold
        return { pos, aim: A0.map((a, k) => K.lerp(a, A1[k], u)), fov: K.lerp(SWITCH_FOV, 35, u) };
      };

      return {
        update(t) {
          const { pos, aim, fov } = pose(t);
          K.look(camera, pos, aim, fov);
          K.focus(camera, aim, t < PULL + 0.5 ? 0 : 0.02);

          // iris: from beyond the frame corners down to the glass radius, ease in
          const c = K.seg(t, CLOSE, SWITCH, K.ease.in);
          iu.uShow.value = t < SWITCH ? 1 : 0;
          iu.uR.value = K.lerp(2.2, IRIS_R, c);
          iu.uScale.value = K.lerp(1 + 0.04 * K.seg(t, 0, CLOSE), IRIS_R * CARD_END, K.seg(t, CLOSE, SWITCH, K.ease.inOut));
          const a = pose(t + 0.01).pos, b = pose(t - 0.01).pos, speed = Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]) / 0.02;
          iu.uLines.value = t >= SWITCH ? K.clamp(speed / 30) : 0;
          iu.uSeed.value = Math.floor(t * 30) * 13.1;

          // the lights come up only after the switch, so nothing new pops in on the cut frame
          const up = K.seg(t, SWITCH + 0.05, PULL + 0.45, K.ease.inOut);
          scene.environmentIntensity = 0.08 + 0.92 * up; key.intensity = 1400 * up; rim.intensity = 260 * up;
          lenses.forEach((L) => {
            L.glass.emissiveIntensity = L.i === HERO ? Math.exp(-Math.max(0, t - SWITCH) / 0.18) * (t >= SWITCH ? 1 : 0) : 0;
            const on = K.seg(t, RINGS + L.i * RING_STEP, RINGS + L.i * RING_STEP + 0.12);
            const hit = Math.exp(-Math.max(0, t - RINGS - L.i * RING_STEP) / 0.25) * (on > 0 ? 1 : 0);
            L.ring.material.color.setRGB(1, 0.16, 0.1).multiplyScalar((L.i === HERO ? 2.0 : 0.9 * up) + on * 1.6 + hit * 4);
          });
        },
        overlay(ctx, t, W, H) {
          if (window.NO_TEXT) return;
          const a = K.seg(t, TYPE, TYPE + 0.35, K.ease.out);
          if (a <= 0) return;
          ctx.textBaseline = 'alphabetic';
          ctx.globalAlpha = a; ctx.fillStyle = '#f4f1ee';
          ctx.font = '600 72px "Inter"'; ctx.fillText(HEADLINE[0], 128, H - 210 + (1 - a) * 24);
          const b = K.seg(t, TYPE + 0.2, TYPE + 0.55, K.ease.out);
          ctx.globalAlpha = b; ctx.font = '300 72px "Inter"'; ctx.fillText(HEADLINE[1], 128, H - 128 + (1 - b) * 24);
        },
      };
    },

    sound(k) {
      k.bed('room', 0, DUR, { gain: 0.7 });
      k.play('riser', CLOSE - 0.1, { gain: 0.55, dur: SWITCH - CLOSE + 0.1 });
      k.play('impact', SWITCH, { gain: 0.9, f: 90 });
      k.play('whoosh', PULL - 0.05, { gain: 0.9, dur: 0.8, top: 2400 });
      LENS_X.forEach((_, i) => k.withMinor(() => k.play('blip', RINGS + i * RING_STEP, { gain: 0.35, f: ['E5', 'G5', 'B5', 'D6', 'E6'][i], type: 'sine' })));
      k.play('ding', TYPE, { gain: 0.45, f: 'E6' });
    },
  });
}
