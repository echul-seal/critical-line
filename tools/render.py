#!/usr/bin/env python3
"""critical line: verification + stills + frames, headless Chromium.
usage: python render.py verify|stills|desktop|video  (run from the repo root, index.html beside tools/)
"""
import sys, json, os, threading, http.server, functools
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mode = sys.argv[1] if len(sys.argv) > 1 else 'verify'

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
def serve():
    h = functools.partial(Q, directory=ROOT)
    http.server.ThreadingHTTPServer(('127.0.0.1', 8765), h).serve_forever()
threading.Thread(target=serve, daemon=True).start()

def verify(page):
    import mpmath as mp
    mp.mp.dps = 30
    zs = page.evaluate('window.__zeros')
    rows, worst = [], 0
    for n in range(1, len(zs) + 1):
        ref = float(mp.zetazero(n).imag)
        err = abs(zs[n - 1] - ref); worst = max(worst, err)
        rows.append([n, zs[n - 1], ref, err])
    vals = []
    for t in [1.0, 10.0, 50.0, 100.0, 149.0]:
        got = page.evaluate(f'window.__zeta({t})')
        r = mp.zeta(mp.mpc(0.5, t))
        err = abs(complex(got[0], got[1]) - complex(r))
        vals.append([t, got, [float(r.real), float(r.imag)], err])
    out = {'zeros_found': len(zs), 'worst_zero_err': worst, 'zeros': rows, 'values': vals}
    json.dump(out, open(os.path.join(ROOT, 'verify.json'), 'w'), indent=1)
    print(json.dumps({'zeros_found': len(zs), 'worst_zero_err': worst, 'value_errs': [v[3] for v in vals]}))
    for r in rows[:10]: print(r)

with sync_playwright() as p:
    b = p.chromium.launch()
    W, H, D = (1440, 900, 1) if mode == 'desktop' else (390, 844, 2)
    page = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=D)
    page.goto('http://127.0.0.1:8765/index.html?rec')
    page.wait_for_function('window.__ready === true', timeout=120000)
    if mode == 'verify':
        verify(page)
    elif mode in ('stills', 'desktop'):
        os.makedirs(os.path.join(ROOT, 'stills'), exist_ok=True)
        times = [float(x) for x in (sys.argv[2].split(',') if len(sys.argv) > 2 else
                 '1,4,6,6.6,7.5,9,12,15,18,22,26,30,40,50,60,70')]
        cur, fps = 0.0, 30
        for i, ts in enumerate(times):
            n = int(round((ts - cur) * fps))
            if n > 0: page.evaluate(f'for(let i=0;i<{n};i++) window.__frame(1/{fps})')
            cur = ts
            st = page.evaluate('window.__state()')
            page.screenshot(path=os.path.join(ROOT, 'stills', f'{mode}_{i:02d}.png'))
            print(i, ts, json.dumps(st), flush=True)
    elif mode == 'video':
        secs = float(sys.argv[2]) if len(sys.argv) > 2 else 26
        skip = float(sys.argv[3]) if len(sys.argv) > 3 else 0
        fps = 30
        if skip: page.evaluate(f'for(let i=0;i<{int(skip*fps)};i++) window.__frame(1/{fps})')
        os.makedirs(os.path.join(ROOT, 'frames'), exist_ok=True)
        for i in range(int(secs * fps)):
            page.evaluate(f'window.__frame(1/{fps})')
            page.screenshot(path=os.path.join(ROOT, 'frames', f'{i:05d}.png'))
            if i % 60 == 0: print('frame', i, page.evaluate('window.__state()'), flush=True)
    b.close()
