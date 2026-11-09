#!/usr/bin/env python3
"""Project a voyage / route onto a canvas for a period-map graphic.

Reads `content.route` from a shot-plan JSON (or a bare route JSON with --bare) and writes
route-coords.json: pixel position of every stop, one SVG path per leg, each leg's length and
its share of the drawn route, so the builder can time the ink line and the date stamps.

Two lanes:
  vector  - a projection ("mercator" or "equirect") fitted to `bounds` inside the canvas.
  raster  - a period map image (scan or generated plate) georeferenced by >= 3 control points
            (lon, lat -> x, y). An affine fit is solved by least squares and the RMS residual is
            reported in pixels; above --max-rms the script fails, because the line would miss
            the printed coastline.

Legs may be "great-circle" (densified along the sphere, then projected) or "straight"
(straight in the projected plane, i.e. a rhumb line on a Mercator chart). A leg with
"style": "intended" is a course that was planned but never sailed; it is kept out of the
drawn-length share so the solid line ends where the real voyage ended.

Pure Python 3, no dependencies.
Usage:
  python3 route_overlay.py SHOT_PLAN.json -o route-coords.json [--lane raster] [--max-rms 6]
  python3 route_overlay.py ROUTE.json --bare -o route-coords.json
"""
import argparse, json, math, sys


def proj(lon, lat, kind):
    if kind == "mercator":
        lat = max(min(lat, 85.0), -85.0)
        return math.radians(lon), -math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
    if kind == "equirect":
        return math.radians(lon), -math.radians(lat)
    sys.exit(f"unknown projection '{kind}' (use mercator or equirect)")


def fit_bounds(route, canvas, kind):
    b = route["bounds"]
    pad = route.get("padding_px", 0)
    (x0, y0), (x1, y1) = proj(b["lon"][0], b["lat"][1], kind), proj(b["lon"][1], b["lat"][0], kind)
    w, h = canvas["w"] - 2 * pad, canvas["h"] - 2 * pad
    s = min(w / (x1 - x0), h / (y1 - y0))
    ox = pad + (w - s * (x1 - x0)) / 2 - s * x0
    oy = pad + (h - s * (y1 - y0)) / 2 - s * y0

    def to_px(lon, lat):
        u, v = proj(lon, lat, kind)
        return s * u + ox, s * v + oy
    return to_px, None


def solve3(m, r):
    """Gaussian elimination for a 3x3 system."""
    a = [row[:] + [r[i]] for i, row in enumerate(m)]
    for c in range(3):
        p = max(range(c, 3), key=lambda i: abs(a[i][c]))
        if abs(a[p][c]) < 1e-12:
            sys.exit("control points are collinear or duplicated; pick 3+ points spread over the map")
        a[c], a[p] = a[p], a[c]
        for i in range(3):
            if i != c:
                f = a[i][c] / a[c][c]
                a[i] = [a[i][k] - f * a[c][k] for k in range(4)]
    return [a[i][3] / a[i][i] for i in range(3)]


def fit_affine(route, kind):
    cps = route.get("control_points", [])
    if len(cps) < 3:
        sys.exit("raster lane needs >= 3 control_points {lon, lat, x, y}")
    uv = [proj(p["lon"], p["lat"], kind) for p in cps]
    ata = [[0.0] * 3 for _ in range(3)]
    atx, aty = [0.0] * 3, [0.0] * 3
    for (u, v), p in zip(uv, cps):
        row = (u, v, 1.0)
        for i in range(3):
            for j in range(3):
                ata[i][j] += row[i] * row[j]
            atx[i] += row[i] * p["x"]
            aty[i] += row[i] * p["y"]
    cx, cy = solve3(ata, atx), solve3(ata, aty)

    def to_px(lon, lat):
        u, v = proj(lon, lat, kind)
        return cx[0] * u + cx[1] * v + cx[2], cy[0] * u + cy[1] * v + cy[2]
    res = [math.hypot(to_px(p["lon"], p["lat"])[0] - p["x"], to_px(p["lon"], p["lat"])[1] - p["y"]) for p in cps]
    rms = math.sqrt(sum(r * r for r in res) / len(res))
    return to_px, {"rms_px": round(rms, 2), "max_px": round(max(res), 2), "points": len(cps)}


def great_circle(a, b, step_deg=1.5):
    def vec(lon, lat):
        lo, la = math.radians(lon), math.radians(lat)
        return (math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la))
    va, vb = vec(*a), vec(*b)
    dot = max(-1.0, min(1.0, sum(x * y for x, y in zip(va, vb))))
    ang = math.acos(dot)
    n = max(1, int(math.degrees(ang) / step_deg))
    out = []
    for i in range(n + 1):
        t = i / n
        if ang < 1e-9:
            p = va
        else:
            s0, s1 = math.sin((1 - t) * ang) / math.sin(ang), math.sin(t * ang) / math.sin(ang)
            p = tuple(s0 * x + s1 * y for x, y in zip(va, vb))
        out.append((math.degrees(math.atan2(p[1], p[0])), math.degrees(math.asin(max(-1, min(1, p[2]))))))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("spec")
    ap.add_argument("-o", "--out", default="route-coords.json")
    ap.add_argument("--bare", action="store_true", help="the file is the route object itself")
    ap.add_argument("--lane", choices=["vector", "raster"], help="override route.lane")
    ap.add_argument("--max-rms", type=float, default=6.0, help="raster lane: fail above this RMS (px)")
    ap.add_argument("--safe", type=float, default=0.05, help="title-safe inset as a share of each side")
    a = ap.parse_args()

    spec = json.load(open(a.spec, encoding="utf-8"))
    route = spec if a.bare else spec.get("content", {}).get("route")
    if not route:
        sys.exit("no content.route in the spec (use --bare for a bare route file)")
    canvas = route.get("canvas") or spec.get("canvas")
    if not canvas:
        sys.exit("no canvas {w, h}")
    lane = a.lane or route.get("lane", "vector")
    kind = route.get("projection", "mercator")
    to_px, fit = fit_affine(route, kind) if lane == "raster" else fit_bounds(route, canvas, kind)

    stops = {s["id"]: s for s in route["stops"]}
    legs_out, warnings = [], []
    for leg in route["legs"]:
        pts = [(stops[leg["from"]]["lon"], stops[leg["from"]]["lat"])]
        pts += [tuple(p) for p in leg.get("via", [])]
        pts.append((stops[leg["to"]]["lon"], stops[leg["to"]]["lat"]))
        geo = []
        for i in range(len(pts) - 1):
            seg = great_circle(pts[i], pts[i + 1]) if leg.get("densify") == "great-circle" else [pts[i], pts[i + 1]]
            geo += seg if not geo else seg[1:]
        xy = [to_px(lon, lat) for lon, lat in geo]
        length = sum(math.hypot(x1 - x0, y1 - y0) for (x0, y0), (x1, y1) in zip(xy, xy[1:]))
        d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in xy)
        legs_out.append({"from": leg["from"], "to": leg["to"], "style": leg.get("style", "solid"),
                         "d": d, "length_px": round(length, 1)})

    drawn = sum(l["length_px"] for l in legs_out if l["style"] != "intended") or 1.0
    acc = 0.0
    for l in legs_out:
        if l["style"] == "intended":
            l["share"] = None
            continue
        l["frac_start"] = round(acc / drawn, 4)
        acc += l["length_px"]
        l["frac_end"] = round(acc / drawn, 4)
        l["share"] = round(l["length_px"] / drawn, 4)

    W, H = canvas["w"], canvas["h"]
    sx, sy = W * a.safe, H * a.safe
    stops_out = []
    for s in route["stops"]:
        x, y = to_px(s["lon"], s["lat"])
        solid = [l for l in legs_out if l.get("share") is not None]
        arrive = next((l["frac_end"] for l in solid if l["to"] == s["id"]), None)
        if arrive is None:  # the departure stop of the first solid leg, or a stop only reached by an intended leg
            arrive = next((l["frac_start"] for l in solid if l["from"] == s["id"]), None)
        item = {k: s[k] for k in s if k not in ("lon", "lat")}
        item.update({"x": round(x, 1), "y": round(y, 1), "arrive_frac": arrive})
        if not (sx <= x <= W - sx and sy <= y <= H - sy):
            warnings.append(f"stop '{s['id']}' at ({x:.0f}, {y:.0f}) is outside the title-safe area")
        stops_out.append(item)

    out = {"canvas": {"w": W, "h": H}, "lane": lane, "projection": kind, "stops": stops_out,
           "legs": legs_out, "drawn_length_px": round(drawn, 1), "warnings": warnings}
    if fit:
        out["fit"] = fit
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"route_overlay: {len(stops_out)} stops, {len(legs_out)} legs, drawn {drawn:.0f}px, lane={lane} -> {a.out}")
    if fit:
        print(f"  affine fit: RMS {fit['rms_px']}px, max {fit['max_px']}px over {fit['points']} control points")
    for w in warnings:
        print("  WARN", w)
    if fit and fit["rms_px"] > a.max_rms:
        print(f"FAIL fit RMS {fit['rms_px']}px > {a.max_rms}px: re-pick control points or the map is not this projection")
        sys.exit(1)


if __name__ == "__main__":
    main()
