"""Wrap flat print artwork onto a cylinder: aluminium cans and PET water bottles, transparent WebP/PNG."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SS = 2  # supersample factor


def shade(nx):
    """Lighting across the cylinder; nx in [-1,1] (left..right)."""
    th = np.arcsin(np.clip(nx, -1, 1))
    lam = 0.38 + 0.62 * np.clip(np.cos(th - 0.25), 0, 1) ** 0.8
    spec = 0.55 * np.exp(-((nx + 0.42) / 0.10) ** 2) + 0.18 * np.exp(-((nx - 0.62) / 0.07) ** 2)
    edge = 1 - 0.55 * np.clip((np.abs(nx) - 0.82) / 0.18, 0, 1) ** 1.5
    return lam * edge, spec


def metal(nx):
    base = 0.62 + 0.25 * np.cos(np.arcsin(np.clip(nx, -1, 1)) * 1.2 - 0.3)
    return base


def can(label, out, uc, body_mm=(66, 168), label_mm=161.5, width=300):
    W = width * SS
    D_mm, H_mm = body_mm
    k = W / D_mm
    neck_h, lid_h, bot_h = 0.10 * W, 0.045 * W, 0.07 * W
    body_h = H_mm * k - neck_h - bot_h
    Ht = int(neck_h + body_h + bot_h + lid_h)
    tex = np.asarray(label.convert("RGB")).astype(np.float32) / 255
    th_, tw_ = tex.shape[:2]
    lab_h = label_mm * k
    lab_y0 = lid_h + neck_h + (body_h - lab_h) / 2 if lab_h < body_h else lid_h + neck_h - (lab_h - body_h) / 2

    ys = np.arange(Ht)[:, None] + 0.5
    xs = np.arange(W)[None, :] + 0.5
    R = W / 2
    # half-width profile
    y_body0, y_body1 = lid_h + neck_h, lid_h + neck_h + body_h
    hw = np.full((Ht, 1), R)
    t = np.clip((ys - lid_h) / neck_h, 0, 1)
    hw = np.where(ys < y_body0, R * (0.84 + 0.16 * (1 - (1 - t) ** 2)), hw)
    tb = np.clip((ys - y_body1) / bot_h, 0, 1)
    hw = np.where(ys > y_body1, R * (1 - 0.10 * tb ** 1.6), hw)
    hw = np.where(ys < lid_h, R * 0.84, hw)
    nx = (xs - R) / hw
    inside = np.abs(nx) <= 1
    nxc = np.clip(nx, -1, 1)
    lam, spec = shade(nxc)

    # texture lookup (front-centred at uc)
    theta = np.arcsin(nxc)
    u = (uc + theta / (2 * np.pi)) % 1.0
    v = (ys - lab_y0) / lab_h
    on_label = (v >= 0) & (v < 1) & (ys >= y_body0 - 0.02 * W) & (ys <= y_body1)
    ui = np.clip((u * tw_).astype(int), 0, tw_ - 1)
    vi = np.clip((v * th_).astype(int), 0, th_ - 1)
    vi = np.broadcast_to(vi, ui.shape)
    col = tex[vi, ui]
    m = metal(nxc)[..., None] * np.array([0.93, 0.95, 0.97])
    rgb = np.where(on_label[..., None], col, m)
    rgb = rgb * lam[..., None] + spec[..., None] * np.where(on_label[..., None], 0.85, 1.0)
    # neck rings / bottom rim darker bands
    ring = (np.abs(ys - (y_body0 - 0.01 * W)) < 0.012 * W) | (np.abs(ys - y_body1) < 0.010 * W)
    rgb = np.where(ring[..., None], rgb * 0.75, rgb)
    rgb = np.clip(rgb, 0, 1)
    alpha = inside.astype(np.float32)
    img = np.dstack([rgb, alpha])
    im = Image.fromarray((img * 255).astype(np.uint8), "RGBA")
    # lid: ellipse on top
    d = ImageDraw.Draw(im)
    lw = R * 0.84
    d.ellipse([R - lw, lid_h * 0.15, R + lw, lid_h * 1.85], fill=(214, 222, 224, 255))
    d.ellipse([R - lw * 0.88, lid_h * 0.42, R + lw * 0.88, lid_h * 1.6], fill=(176, 186, 189, 255))
    d.ellipse([R - lw * 0.2 + lw * 0.15, lid_h * 0.8, R + lw * 0.2 + lw * 0.15, lid_h * 1.2], fill=(140, 150, 153, 255))
    im = im.resize((width, Ht // SS), Image.LANCZOS)
    im.save(out, "WEBP", quality=88, method=6)
    im.save(out.replace(".webp", ".png"))
    return im.size


def bottle(label, out, kind, width=360):
    """Generic PET bottle (5 L with handle, 10 L) with the front label wrapped on."""
    W = width * SS
    R = W / 2
    if kind == "10":
        Hmm, Dmm, lab_w_mm, lab_h_mm = 400, 205, 90, 147
    else:
        Hmm, Dmm, lab_w_mm, lab_h_mm = 310, 160, 90, 115
    k = W / Dmm
    Ht = int(Hmm * k)
    cap_h, neck_h, sh_h = 0.055 * Ht, 0.035 * Ht, 0.24 * Ht
    neck_w = 0.30 * R if kind == "10" else 0.34 * R
    ys = np.arange(Ht)[:, None] + 0.5
    xs = np.arange(W)[None, :] + 0.5
    y_sh0 = cap_h + neck_h
    y_sh1 = y_sh0 + sh_h
    hw = np.full((Ht, 1), R * 0.985)
    t = np.clip((ys - y_sh0) / sh_h, 0, 1)
    s = 1 - (1 - t) ** 2.2
    hw = np.where(ys < y_sh1, neck_w + (R * 0.985 - neck_w) * s, hw)
    hw = np.where(ys < y_sh0, neck_w * 0.92, hw)
    hw = np.where(ys < cap_h, neck_w * 1.05, hw)
    rb = 0.06 * Ht
    tb = np.clip((ys - (Ht - rb)) / rb, 0, 1)
    hw = np.where(ys > Ht - rb, R * 0.985 * np.sqrt(np.clip(1 - tb ** 2, 0, 1)) * 0.25 + R * 0.985 * 0.75 * (1 - tb ** 3), hw)
    nx = (xs - R) / hw
    inside = np.abs(nx) <= 1
    nxc = np.clip(nx, -1, 1)
    lam, spec = shade(nxc)
    water = np.array([0.70, 0.88, 0.95])
    rgb = np.ones(nx.shape + (3,)) * water
    # subtle horizontal ribs
    ribs = np.zeros_like(nx)
    if kind == "10":
        for p in (0.36, 0.86):
            ribs += np.exp(-((ys - p * Ht) / (0.006 * Ht)) ** 2)
    rgb = rgb * (1 - 0.18 * ribs[..., None])
    # label on the front (texture spans +-phi)
    tex = np.asarray(label.convert("RGB")).astype(np.float32) / 255
    th_, tw_ = tex.shape[:2]
    Rmm = Dmm / 2
    phi = (lab_w_mm / 2) / Rmm
    theta = np.arcsin(nxc)
    u = (theta + phi) / (2 * phi)
    lab_y0 = Ht * (0.45 if kind == "10" else 0.47)
    lab_h = lab_h_mm * k
    v = (ys - lab_y0) / lab_h
    on = (u >= 0) & (u < 1) & (v >= 0) & (v < 1)
    ui = np.clip((u * tw_).astype(int), 0, tw_ - 1)
    vi = np.broadcast_to(np.clip((v * th_).astype(int), 0, th_ - 1), ui.shape)
    col = tex[vi, ui]
    # rounded label corners
    cu, cv = np.minimum(u, 1 - u) * lab_w_mm, np.minimum(v, 1 - v) * lab_h_mm
    rr = 6.0
    corner = (cu < rr) & (cv < rr) & (((rr - cu) ** 2 + (rr - cv) ** 2) > rr ** 2)
    on &= ~corner
    rgb = np.where(on[..., None], col, rgb)
    lamw = 0.55 + 0.45 * lam
    rgb = rgb * np.where(on[..., None], lam[..., None], lamw[..., None]) + spec[..., None] * np.where(on[..., None], 0.5, 0.9)
    capm = ys < cap_h
    rgb = np.where(capm[..., None], np.array([0.12, 0.42, 0.82]) * (0.5 + 0.6 * lam[..., None]) + 0.3 * spec[..., None], rgb)
    rgb = np.clip(rgb, 0, 1)
    alpha = np.where(on | capm, 1.0, 0.93) * inside
    im = Image.fromarray((np.dstack([rgb, alpha]) * 255).astype(np.uint8), "RGBA")
    if kind == "5":
        d = ImageDraw.Draw(im)
        hx0, hy0 = R + neck_w * 0.7, y_sh0 + sh_h * 0.08
        d.line([(hx0, hy0), (R + R * 0.86, y_sh0 + sh_h * 0.25), (R + R * 0.9, y_sh1 + 0.02 * Ht)], fill=(110, 170, 200, 255), width=int(0.035 * W), joint="curve")
    im = im.resize((width, Ht // SS), Image.LANCZOS)
    im.save(out, "WEBP", quality=88, method=6)
    im.save(out.replace(".webp", ".png"))
    return im.size


if __name__ == "__main__":
    import os
    os.makedirs("out", exist_ok=True)
    crops = {
        "mustang-classic": ("h7.png", (421, 274, 1985, 1543), 0.27, "45"),
        "mustang-exotic": ("h5.png", (868, 650, 2362, 1863), 0.25, "45"),
        "anarfresh-045": ("h1.png", (1027, 276, 2593, 1545), 0.66, "45"),
        "anarfresh-033": ("h2.png", (995, 825, 2568, 1539), 0.72, "33"),
        "xurmofresh": ("h6.png", (1029, 276, 2593, 1545), 0.66, "45"),
        "moxito-lime": ("h3.png", (389, 200, 1956, 1494), 0.70, "45"),
        "moxito-strawberry": ("h4.png", (389, 200, 1956, 1494), 0.70, "45"),
    }
    for name, (f, bb, uc, sz) in crops.items():
        lab = Image.open(f).convert("RGB").crop(bb)
        if sz == "45":
            print(name, can(lab, f"out/{name}.webp", uc, (66, 170), 161.5))
        else:
            print(name, can(lab, f"out/{name}.webp", uc, (66, 115), 99 * 1.0 * 0 + (bb[3] - bb[1]) / (bb[2] - bb[0]) * 208))
    print("zamzam-10", bottle(Image.open("zz10.png"), "out/zamzam-10l.webp", "10"))
    print("zamzam-5", bottle(Image.open("zz5.png"), "out/zamzam-5l.webp", "5"))
