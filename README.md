# critical line

Live: https://echul-seal.github.io/critical-line/
Video (30 s, portrait 780×1688): https://renders.heyseal.ai/deliverables/3af6dff4-961b-47d5-840c-77eaf506f998/c7ff5cdc-e626-480f-b10c-e6bbfafcc998.mp4
IPFS: `bafybeid6j5he5ul34nwlv2ruiob4c3ohn4endzwbu6bp4g2aw47ubabena`

## What it is

A point moves in the complex plane. Its position is ζ(½ + it), and t climbs from 0 to 150. Behind it the path it has drawn stays on screen: recent path bright and warm, older path faint and blue. A small fixed ring marks 0. Each time t reaches a nontrivial zero of ζ, the point passes exactly through that ring, the ring fills and blooms, and the zero's value of t shows in the top-left corner. A thin ruler on the right edge runs from t = 0 at the top to t = 150 at the bottom, with one tick for each zero passed so far. At t = 150 the whole path brightens once, fades, and the piece starts over.

The Riemann Hypothesis says every nontrivial zero of ζ has real part ½. This piece only looks along that line, so every zero it shows is one of those. Between t = 0 and 150 there are 52 of them. The camera fits the recent part of the path, one axis at a time. In portrait the real axis runs down the screen.

Hold to slow down. Tap to toggle a 3× hurry. `?hurry` opens it already hurried.

## The math

Everything runs in the browser with no network. ζ(½ + it) is computed from the alternating series η(s) = Σ (−1)^k (k+1)^−s with Borwein's algorithm 2 (N = 180 terms, weights computed once at load), then ζ(s) = η(s) / (1 − 2^(1−s)). The error bound is about e^(πt/2) / (3+√8)^N, below 1e−12 for every t up to 150.

The path is sampled every Δt = 0.004 (37,500 samples), filled ahead of the playhead in small slices per frame. Zeros are found as local minima of |ζ| between samples, refined by ternary search, and kept only when |ζ| < 1e−6 there.

## Verification

`tools/render.py verify` loads the page in headless Chromium and checks it against mpmath at 30 digits:
- the zero finder returns all 52 zeros below t = 150, matching `mpmath.zetazero(n)` with worst error 4.3e−14
- ζ(½ + it) at t = 1, 10, 50, 100, 149 matches `mpmath.zeta` to rounding error

## Versions

- v0.1: first sketch. Borwein eta evaluation, fading trail, a pulse at each zero, plus the render and verify tool.
- v0.2: plane turned for portrait, camera fits each axis on its own, fixed origin ring that blooms at each zero, zero's t in a fixed corner, legible caption, longer glowing trail.
- v0.3: t-ruler on the right edge, one tick per zero passed, the newest tick glowing. `?hurry` start state. At the end the whole path brightens once before the loop, so the full shape is seen before it clears. (Rebuilt after the first v0.3 was lost with its render machine.)

## Tools

`python tools/render.py verify | stills [times] | desktop | video [secs] [skip]`, run from the repo root. `HURRY=1` renders the hurried state. The video above is `HURRY=1 python tools/render.py video 30 4`, encoded with ffmpeg (libx264, crf 18).

Seal, Nov 2026.
