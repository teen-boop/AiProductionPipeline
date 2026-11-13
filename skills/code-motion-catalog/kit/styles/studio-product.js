{
  // ---------------------------------------------------------------- content (TIDE demo campaign, invented brand)
  const COPY = {
    mark: 'TIDE',                         // debossed on the bottle and set above the line in the lock-up
    line: ['DAWN', 'TO DUSK.'],
    from: 6, to: 22, unit: 'DAWN TO NIGHT', // the clock runs 06:00 -> 22:00 while the light goes round
  };
  const FINISH = { coat: '#7d917b', steel: '#cfd3d8', silicone: '#0a0a0b' };   // finishes of the sample product

  // ---------------------------------------------------------------- the schedule (picture and sound share it)
  // The light is the clock: the key strip crosses the bottle four times while its colour runs through one day and the
  // clock on screen runs from dawn to night. The bottle never changes.
  const DAY = [0.2, 6.3];
  const SWEEPS = [[0, -26], [1.75, 62], [2.9, -64], [4.25, 60], [6.8, -52], [9.6, -34]];
  const LOCK = 5.25;
  const hourAt = (K, t) => K.lerp(COPY.from, COPY.to, K.seg(t, DAY[0], DAY[1]));

  // ================================================================ softbox rig (from the reference style, unchanged)
  function softboxRig(S, boxes, aim) {
    const { THREE } = S, N = boxes.length, vecs = () => boxes.map(() => new THREE.Vector3());
    const U = { rigC: { value: vecs() }, rigN: { value: vecs() }, rigU: { value: vecs() }, rigV: { value: vecs() }, rigL: { value: vecs() }, rigFeather: { value: boxes.map(() => 0) } };
    const PARS = `
      #define RIG_N ${N}
      uniform vec3 rigC[RIG_N], rigN[RIG_N], rigU[RIG_N], rigV[RIG_N], rigL[RIG_N];
      uniform float rigFeather[RIG_N];
      uniform vec4 rigFinish;
      varying vec3 vRigP;
      float rigBand(float a, float w) { float k = clamp((min(a + w, 1.0) - max(a - w, -1.0)) / (2.0 * w), 0.0, 1.0); return k * k * (3.0 - 2.0 * k); }
      vec3 rigMirror(vec3 P, vec3 R, float rough) {
        vec3 sum = vec3(0.0);
        for (int i = 0; i < RIG_N; i++) {
          float dn = dot(R, rigN[i]); if (dn > -1e-3) continue;
          float s = dot(rigC[i] - P, rigN[i]) / dn; if (s <= 0.0) continue;
          vec3 d = P + R * s - rigC[i];
          float hu = length(rigU[i]), hv = length(rigV[i]), a = dot(d, rigU[i]) / (hu * hu), b = dot(d, rigV[i]) / (hv * hv);
          float w = s * (0.004 + 1.5 * rough * rough);
          float grade = mix(1.0, 0.12 + 0.88 * smoothstep(-1.0, 0.85, clamp(a, -1.0, 1.0)), rigFeather[i]);
          sum += rigL[i] * rigBand(a, w / hu) * rigBand(b, w / hv) * grade;
        }
        return sum;
      }
      vec3 rigWash(vec3 P, vec3 N) {
        vec3 sum = vec3(0.0);
        for (int i = 0; i < RIG_N; i++) {
          vec3 L = rigC[i] - P; float d2 = dot(L, L); L *= inversesqrt(d2);
          float area = 4.0 * length(rigU[i]) * length(rigV[i]);
          vec3 white = mix(vec3(dot(rigL[i], vec3(0.2126, 0.7152, 0.0722))), rigL[i], 0.35);
          sum += white * area * clamp((dot(N, L) + 0.06) / 1.06, 0.0, 1.0) * max(dot(-L, rigN[i]), 0.0) / (PI * d2);
        }
        return sum;
      }`;
    const SHADE = `{
        vec3 rN = inverseTransformDirection(normal, viewMatrix), rV = normalize(cameraPosition - vRigP), rR = reflect(-rV, rN);
        float rF = pow(1.0 - saturate(dot(rN, rV)), 5.0);
        vec3 rF0 = mix(vec3(0.04), diffuseColor.rgb, metalnessFactor);
        outgoingLight += rigWash(vRigP, rN) * diffuseColor.rgb * (1.0 - metalnessFactor) * rigFinish.z;
        float rRough = material.roughness;
        outgoingLight += rigMirror(vRigP, rR, rRough) * (rF0 + (max(vec3(1.0 - rRough), rF0) - rF0) * rF) * rigFinish.w;
        outgoingLight += rigMirror(vRigP, rR, max(rigFinish.y, rRough - roughnessFactor)) * (0.04 + 0.96 * rF) * rigFinish.x;
      }
      #include <opaque_fragment>`;
    const at = (v, t) => (typeof v === 'function' ? v(t) : v), col = new THREE.Color(), up = new THREE.Vector3(0, 1, 0), rad = Math.PI / 180;
    return {
      light(mat, finish = {}) {
        const f = new THREE.Vector4(finish.coat || 0, finish.coatRoughness == null ? 0.15 : finish.coatRoughness, finish.diffuse == null ? 1 : finish.diffuse, finish.specular == null ? 1 : finish.specular);
        mat.onBeforeCompile = (sh) => {
          Object.assign(sh.uniforms, U, { rigFinish: { value: f } });
          sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nvarying vec3 vRigP;').replace('#include <begin_vertex>', '#include <begin_vertex>\nvRigP = (modelMatrix * vec4(transformed, 1.0)).xyz;');
          sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\n' + PARS).replace('#include <opaque_fragment>', SHADE);
        };
        return mat;
      },
      update(t, lensAz) {
        boxes.forEach((b, i) => {
          const az = lensAz + at(b.az, t) * rad, el = at(b.el || 0, t) * rad, d = at(b.dist, t), c = U.rigC.value[i], n = U.rigN.value[i], sz = at(b.size, t), rgb = at(b.color, t);
          c.set(aim[0] + d * Math.cos(el) * Math.sin(az), aim[1] + d * Math.sin(el), aim[2] + d * Math.cos(el) * Math.cos(az));
          n.set(aim[0], aim[1], aim[2]).sub(c).normalize();
          U.rigU.value[i].crossVectors(up, n).normalize(); U.rigV.value[i].crossVectors(n, U.rigU.value[i]).multiplyScalar(sz[1] / 2); U.rigU.value[i].multiplyScalar(sz[0] / 2);
          (Array.isArray(rgb) ? col.setRGB(rgb[0], rgb[1], rgb[2]) : col.set(rgb)); U.rigL.value[i].set(col.r, col.g, col.b).multiplyScalar(at(b.power, t));
          U.rigFeather.value[i] = at(b.feather || 0, t);
        });
      },
    };
  }

  // ================================================================ turned parts (from the reference style)
  function turned(THREE, corners, uvR = 0.5, seg = 160) {
    const pts = [];
    corners.forEach(([r, y, f], i) => {
      const a = corners[i - 1], c = corners[i + 1];
      if (!f || !a || !c) { pts.push([r, y]); return; }
      const u1 = [a[0] - r, a[1] - y], u2 = [c[0] - r, c[1] - y], l1 = Math.hypot(u1[0], u1[1]), l2 = Math.hypot(u2[0], u2[1]);
      const half = Math.acos(Math.max(-1, Math.min(1, (u1[0] * u2[0] + u1[1] * u2[1]) / (l1 * l2)))) / 2, d = Math.min(f / Math.tan(half), l1 * 0.48, l2 * 0.48);
      const p1 = [r + u1[0] / l1 * d, y + u1[1] / l1 * d], p2 = [r + u2[0] / l2 * d, y + u2[1] / l2 * d], n = 7;
      for (let k = 0; k <= n; k++) { const s = k / n, q = 1 - s; pts.push([q * q * p1[0] + 2 * q * s * r + s * s * p2[0], q * q * p1[1] + 2 * q * s * y + s * s * p2[1]]); }
    });
    const g = new THREE.LatheGeometry(pts.map(([r, y]) => new THREE.Vector2(Math.max(r, 1e-4), y)), seg), uv = g.attributes.uv, arc = [0];
    for (let j = 1; j < pts.length; j++) arc.push(arc[j - 1] + Math.hypot(pts[j][0] - pts[j - 1][0], pts[j][1] - pts[j - 1][1]));
    for (let i = 0; i <= seg; i++) for (let j = 0; j < pts.length; j++) uv.setXY(i * pts.length + j, (i / seg) * 2 * Math.PI * uvR, arc[j]);
    return g.rotateY(Math.PI);
  }

  // ================================================================ the studio (from the reference style)
  function seamlessStudio(S) {
    const { THREE, K, scene } = S;
    const glowTex = K.canvasTex(512, 512, (ctx, w, h) => {
      const g = ctx.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, w / 2);
      g.addColorStop(0, '#fff'); g.addColorStop(0.25, '#9a9a9a'); g.addColorStop(0.55, '#2c2c2c'); g.addColorStop(1, '#000');
      ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    });
    const backdrop = new THREE.Mesh(new THREE.PlaneGeometry(30, 15), new THREE.MeshBasicMaterial({ map: glowTex }));
    backdrop.position.set(0.6, 3.6, -11); scene.add(backdrop);
    K.mirrorFloor(S, { y: 0, color: '#030304', roughness: 0.14, surfaceRoughness: 0.5, strength: 1.3, fresnel: true });
    const poolTex = K.canvasTex(512, 512, (ctx, w, h) => {
      const g = ctx.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, w / 2);
      g.addColorStop(0, '#000'); g.addColorStop(0.075, '#000'); g.addColorStop(0.16, '#8c8c8c'); g.addColorStop(0.3, '#555'); g.addColorStop(0.6, '#161616'); g.addColorStop(1, '#000');
      ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    });
    const pool = new THREE.Mesh(new THREE.PlaneGeometry(13, 13), new THREE.MeshBasicMaterial({ map: poolTex, blending: THREE.AdditiveBlending, transparent: true, depthWrite: false }));
    pool.rotation.x = -Math.PI / 2; pool.position.set(0, 0.002, 0); scene.add(pool);
    return { tint(rgb, level) { backdrop.material.color.setRGB(rgb[0], rgb[1], rgb[2]).multiplyScalar(0.05 + 0.085 * level); pool.material.color.setRGB(rgb[0], rgb[1], rgb[2]).multiplyScalar(0.03 + 0.045 * level); } };
  }

  // ================================================================ the product: the TIDE Flask
  // Same frame as the reference: 2.67 units tall, standing on y = 0, wordmark facing +z. Differences, from the product
  // card: no rubber foot (the coat runs under), a thin brushed steel band instead of a knurled collar, a natural bamboo
  // screw cap, a black silicone carry loop on the right of the cap, and a wordmark pressed into the coat (debossed).
  function buildProduct(S, rig) {
    const { THREE, K, scene } = S;
    const peel = K.canvasTex(512, 512, (ctx, w, h) => {
      const r = K.rng(3); ctx.fillStyle = '#808080'; ctx.fillRect(0, 0, w, h);
      for (let i = 0; i < 9000; i++) { const v = r() < 0.5 ? 255 : 0; ctx.fillStyle = `rgba(${v},${v},${v},${r.range(0.05, 0.22)})`; ctx.beginPath(); ctx.arc(r() * w, r() * h, r.range(1.2, 4.5), 0, 7); ctx.fill(); }
    }, { data: true, repeat: [1 / 0.11, 1 / 0.11] });
    const lathe = K.canvasTex(4, 128, (ctx, w, h) => { const r = K.rng(8); for (let y = 0; y < h; y++) { const v = Math.round(128 + r.range(-1, 1) * 90); ctx.fillStyle = `rgb(${v},${v},${v})`; ctx.fillRect(0, y, w, 1); } }, { data: true, repeat: [1, 1 / 0.085] });
    // bamboo: pale straw with fine darker grain and the nodes of the laminated strips
    const bamboo = K.canvasTex(1024, 256, (ctx, w, h) => {
      const r = K.rng(21); ctx.fillStyle = '#c9a774'; ctx.fillRect(0, 0, w, h);
      for (let i = 0; i < 260; i++) { const x = r() * w; ctx.fillStyle = `rgba(${r() < 0.5 ? '120,84,40' : '232,206,160'},${r.range(0.08, 0.3)})`; ctx.fillRect(x, 0, r.range(1, 3), h); }
      for (let s = 0; s < w; s += 64) { ctx.fillStyle = 'rgba(110,76,36,0.35)'; ctx.fillRect(s, 0, 2, h); }
      for (let i = 0; i < 18; i++) { const x = r() * w, y = r() * h; ctx.fillStyle = 'rgba(120,84,40,0.25)'; ctx.fillRect(x, y, 30, 3); }
    }, { repeat: [1 / 0.6, 1 / 0.15] });
    const M = {
      coat: rig.light(new THREE.MeshStandardMaterial({ color: FINISH.coat, roughness: 0.55, bumpMap: peel, bumpScale: 0.55 }), { coat: 0.55, coatRoughness: 0.3, diffuse: 0.95 }),
      steel: rig.light(new THREE.MeshStandardMaterial({ color: FINISH.steel, roughness: 0.22, metalness: 1, bumpMap: lathe, bumpScale: 0.35 })),
      wood: rig.light(new THREE.MeshStandardMaterial({ color: '#ffffff', map: bamboo, roughness: 0.62 }), { coat: 0.25, coatRoughness: 0.35, diffuse: 1.0 }),
      silicone: rig.light(new THREE.MeshStandardMaterial({ color: FINISH.silicone, roughness: 0.5 }), { coat: 0.35, coatRoughness: 0.4, diffuse: 1.2 }),
    };
    const product = new THREE.Group(); scene.add(product);
    const part = (geo, mat, parent = product) => { const m = new THREE.Mesh(geo, mat); parent.add(m); return m; };
    const R = 0.44, NECK = 0.37, C0 = 2.0, c = (r, y, f) => [r, C0 + y, f];

    part(turned(THREE, [[0.0, 0.0], [R - 0.06, 0.0, 0.03], [R, 0.05, 0.05], [R, 0.2, 0.004], [R - 0.006, 0.205, 0.003], [R - 0.006, 0.212, 0.003], [R, 0.217, 0.004],   // body: rounded base, seam,
      c(R, -0.255, 0.34), c(NECK - 0.004, -0.045, 0.07), c(NECK - 0.004, 0.007)], R), M.coat);                                                                         //   wall, shoulder
    part(turned(THREE, [c(NECK - 0.03, 0.0), c(NECK + 0.004, 0.003, 0.004), c(NECK + 0.004, 0.072, 0.006), c(NECK - 0.03, 0.078)], NECK), M.steel);                  // the thin steel band
    part(turned(THREE, [c(NECK - 0.03, 0.074), c(NECK + 0.002, 0.078, 0.01), c(NECK + 0.002, 0.33, 0.03), c(NECK - 0.02, 0.35, 0.02), c(0.0, 0.352)], NECK), M.wood); // bamboo cap

    // the black silicone loop: a band round the neck under the cap, and a D-shaped loop standing out to the right
    const LB = C0 + 0.04, ring = [];
    for (let i = 0; i <= 48; i++) { const a = (i / 48) * Math.PI * 2; ring.push([Math.cos(a) * (NECK + 0.03), LB, Math.sin(a) * (NECK + 0.03)]); }
    part(K.tube(ring, 0.026, { closed: true, segments: 96, radial: 16 }), M.silicone);
    const loop = [[NECK + 0.02, LB, 0], [NECK + 0.2, LB + 0.02, 0], [NECK + 0.3, LB + 0.12, 0], [NECK + 0.27, LB + 0.27, 0], [NECK + 0.13, LB + 0.33, 0], [NECK + 0.0, LB + 0.3, 0]];
    part(K.tube(loop, 0.03, { segments: 80, radial: 16 }), M.silicone);

    // the wordmark pressed into the coat: a slightly darker, slightly glossier patch in the shape of the letters, low on the front
    const tex = K.canvasTex(1024, 256, (ctx, w, h) => {
      ctx.fillStyle = '#000'; ctx.fillRect(0, 0, w, h); ctx.fillStyle = '#fff';
      ctx.font = '500 170px "Space Grotesk"'; ctx.letterSpacing = '40px'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(COPY.mark, w / 2 + 20, h / 2 + 8);
    });
    const deboss = part(new THREE.CylinderGeometry(R + 0.0008, R + 0.0008, 0.11, 64, 1, true, -0.5 / R / 2, 0.5 / R),
      rig.light(new THREE.MeshStandardMaterial({ color: '#56664f', roughness: 0.4, alphaMap: tex, transparent: true, depthWrite: false }), { coat: 0.4, coatRoughness: 0.25, diffuse: 0.9 }));
    deboss.position.y = 0.55;
    return product;
  }

  registerStyle({
    id: 'studio-product',
    name: 'Studio Product',
    family: 'Products and screens',
    topic: 'TIDE (invented sample bottle): the light is the clock, dawn to dusk',
    duration: 8,
    fonts: ['600 128px "Inter"', '300 132px "Inter"', '500 46px "Space Grotesk"', '500 54px "Space Grotesk"', '500 170px "Space Grotesk"'],
    render: { samples: 96, shutter: 0.5, tone: 'filmic', exposure: 1.0, bloom: 0.42, bloomThreshold: 1.25, vignette: 0.34, grain: 0.012, fov: 24, background: '#010102' },

    build(S) {
      const { THREE, K, camera } = S;
      const rgb = (hex) => new THREE.Color(hex).toArray();
      // one continuous move: macro on the bamboo cap and loop -> down the shoulder -> macro on the pressed wordmark ->
      // pull back to the whole bottle left of centre -> a slow push that is still moving on the last frame
      const cam = {
        pos: K.path([[0, [0.95, 2.62, 1.45]], [1.6, [0.45, 2.25, 1.62]], [3.0, [-0.22, 0.72, 1.42]], [3.7, [-0.28, 0.66, 1.5]], [4.15, [-0.32, 0.7, 1.64]], [5.0, [0.36, 1.0, 5.5]], [5.9, [0.92, 0.86, 7.5]], [9.6, [0.6, 0.8, 6.75]]]),
        aim: K.path([[0, [0.25, 2.2, 0.3]], [1.6, [0.12, 2.1, 0.37]], [3.0, [-0.02, 0.6, 0.44]], [3.7, [0.0, 0.57, 0.44]], [4.15, [0.03, 0.6, 0.44]], [5.0, [0.8, 1.18, 0]], [5.9, [1.22, 1.2, 0]], [9.6, [1.16, 1.23, 0]]]),
        focus: K.path([[0, [0.3, 2.18, 0.33]], [1.6, [0.12, 2.12, 0.36]], [3.0, [0.0, 0.56, 0.44]], [9.6, [0.0, 0.6, 0.44]]]),
        ap: K.track([[0, 0.036], [4.15, 0.032], [5.7, 0.02], [8, 0.014]]),
      };
      const dayColor = K.track([[0, rgb('#ffae6e')], [1.4, rgb('#fff3e2'), 'inOut'], [2.4, rgb('#ff9a5c'), 'inOut'], [3.5, rgb('#9fc0ff'), 'inOut'], [5.6, rgb('#eaf3ff'), 'inOut']]);
      const hero = (t) => K.seg(t, 4.15, 5.9, K.ease.inOut);
      const rig = softboxRig(S, [
        { size: (t) => [K.lerp(0.62, 1.05, hero(t)), 3.6], dist: 3.3, az: K.track(SWEEPS.map(([t, a]) => [t, a, 'inOut'])), el: 6, power: (t) => K.lerp(9, 10, hero(t)), color: dayColor, feather: 0.75 },
        { size: [0.34, 3.8], dist: 3.5, az: (t) => K.lerp(146, 128, hero(t)) - 6 * Math.sin(t * 0.5), el: 4, power: (t) => K.lerp(7, 13, hero(t)), color: (t) => dayColor(t).map((c, i) => K.lerp(c, [0.8, 0.9, 1][i], 0.5)) },
        { size: [0.3, 3.8], dist: 3.5, az: (t) => K.lerp(-150, -134, hero(t)), el: 4, power: (t) => K.lerp(1.5, 10, hero(t)), color: '#dcebff' },
        { size: [2.4, 1.6], dist: 3.4, az: 25, el: 70, power: (t) => K.lerp(2.0, 2.6, hero(t)), color: (t) => dayColor(t).map((c) => K.lerp(c, 1, 0.5)) },
      ], [0, 1.4, 0]);
      K.env(S, { top: '#06080b', horizon: '#0a0d11', bottom: '#010101', intensity: 1, panels: [{ pos: [0, 12, 3], size: [10, 8], color: '#cfe0f2', power: 0.9 }] });
      const studio = seamlessStudio(S);
      buildProduct(S, rig);

      const INK = '244,247,250';
      // the clock: HH:00 with the hour digits rolling like an odometer
      const clock = (ctx, value, x, y, size) => {
        const dw = ctx.measureText('0').width * 1.02, n = Math.min(COPY.to, Math.floor(value)), f = n >= COPY.to ? 0 : value - n, roll = K.seg(f, 0.7, 1, K.ease.inOut);
        ctx.save(); ctx.textAlign = 'center'; ctx.beginPath(); ctx.rect(x - 4, y - size * 0.8, dw * 2 + 8, size * 0.84); ctx.clip();
        for (let d = 0; d < 2; d++) {
          const dg = (v) => String(Math.floor(v / (d ? 1 : 10)) % 10), a = dg(n), b = dg(n + 1), p = a === b ? 0 : roll, cx = x + dw * (d + 0.5);
          ctx.fillText(a, cx, y - p * size); if (p > 0) ctx.fillText(b, cx, y + (1 - p) * size);
        }
        ctx.restore(); ctx.textAlign = 'left'; ctx.fillText(':00', x + dw * 2 + 4, y);
        return dw * 2 + ctx.measureText(':00').width;
      };
      const rise = (ctx, t, t0, y, size, draw) => {
        const e = K.seg(t, t0, t0 + 0.75, K.ease.outQuint); if (e <= 0) return;
        ctx.save(); ctx.beginPath(); ctx.rect(0, y - size * 1.05, ctx.canvas.width, size * 1.32); ctx.clip(); ctx.globalAlpha = Math.min(1, e * 1.6); ctx.translate(0, (1 - e) * size * 0.7); draw(); ctx.restore();
      };

      return {
        update(t) {
          const p = cam.pos(t), day = dayColor(t), h = hero(t);
          K.look(camera, p, cam.aim(t)); K.focus(camera, cam.focus(t), cam.ap(t));
          rig.update(t, Math.atan2(p[0], p[2]));
          studio.tint(day, h);
        },
        overlay(ctx, t, W, H) {
          if (window.NO_TEXT) return;   // narrow ad versions set their own type over the bottle
          const hour = hourAt(K, t);
          const a = 1 - K.seg(t, LOCK - 0.5, LOCK - 0.1);
          if (a > 0) {
            ctx.globalAlpha = a; ctx.fillStyle = `rgb(${INK})`; ctx.textBaseline = 'alphabetic';
            ctx.font = '300 132px "Inter"'; const w = clock(ctx, hour, 112, H - 118, 132);
            ctx.font = '500 46px "Space Grotesk"'; ctx.letterSpacing = '9px'; ctx.textAlign = 'left'; ctx.fillStyle = `rgba(${INK},0.78)`; ctx.fillText(COPY.unit, 112 + w + 30, H - 122); ctx.letterSpacing = '0px';
            const k = (hour - COPY.from) / (COPY.to - COPY.from);
            ctx.fillStyle = `rgba(${INK},0.22)`; ctx.fillRect(116, H - 86, 420, 3); ctx.fillStyle = `rgb(${INK})`; ctx.fillRect(116, H - 86, 420 * k, 3);
            ctx.globalAlpha = 1;
          }
          const X = 800, Y = 540;
          rise(ctx, t, LOCK, Y - 206, 54, () => {
            ctx.fillStyle = `rgba(${INK},0.8)`;
            ctx.font = '500 54px "Space Grotesk"'; ctx.letterSpacing = '19px'; ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic'; ctx.fillText(COPY.mark, X + 4, Y - 201); ctx.letterSpacing = '0px';
          });
          COPY.line.forEach((line, i) => rise(ctx, t, LOCK + 0.14 + i * 0.13, Y + i * 150, 128, () => {
            ctx.font = '600 128px "Inter"'; ctx.letterSpacing = '-2px'; ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic'; ctx.fillStyle = `rgb(${INK})`;
            ctx.fillText(line, X, Y + i * 150); ctx.letterSpacing = '0px';
          }));
        },
      };
    },

    sound(k) {
      k.bed('room', 0, 8, { gain: 0.6 });
      k.music('pad', 0, 8, { bpm: 60, gain: 0.7, chords: [['D3', 'A3', 'F#4', 'A4'], ['B2', 'F#3', 'D4', 'A4']] });
      for (let i = 1; i < SWEEPS.length - 1; i++) { const [t0, a0] = SWEEPS[i - 1], [t1, a1] = SWEEPS[i]; k.play('whoosh', t0 + (t1 - t0) * 0.22, { dur: (t1 - t0) * 0.7, gain: 0.55, top: 1500, pan: a1 > a0 ? 0.35 : -0.35 }); }
      k.withMinor(() => { for (let h = COPY.from + 1; h <= COPY.to; h++) k.play('tick', DAY[0] + (DAY[1] - DAY[0]) * (h - COPY.from) / (COPY.to - COPY.from), { gain: 0.3, f: 5200 + (h % 2) * 500 }); });
      k.tone(3.45, { f: 'A5', dur: 1.4, gain: 0.05, a: 0.4, verb: 0.5 });
      k.play('swish', LOCK + 0.1, { gain: 0.35, dur: 0.4 });
      k.play('thud', DAY[1], { gain: 0.5, f: 90 }); k.play('ding', DAY[1], { gain: 0.55, f: 'D6' }); k.play('ding', DAY[1] + 0.02, { gain: 0.3, f: 'A6' });
    },
  });
}
