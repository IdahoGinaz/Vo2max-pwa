# VO2 extractor for Garmin FIT

Drop a .fit or .zip exported from Garmin Connect. The page extracts the value stored in FIT message 140 field 7 and converts it to VO2 using vo2 = value * 3.5 / 65536. Runs entirely client side.

Install
1. Push files to a GitHub Pages repo (root).
2. Enable GitHub Pages for the main branch.
3. Open the published site and add to home screen on mobile.

Notes
- Some activities do not include the VO2 message; if missing try exporting the "original" activity from Garmin Connect.
- Works offline after first load when installed as a PWA.
