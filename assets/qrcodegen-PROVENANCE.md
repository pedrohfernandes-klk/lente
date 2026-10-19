# QR generator

`qrcodegen.js` is the official Project Nayuki QR Code generator, vendored locally.

- Source: https://github.com/nayuki/QR-Code-generator/blob/master/typescript-javascript/qrcodegen.ts
- Exact source Git blob: `c4191ac0b5f8a24d87fd9340ceaa2d3b07d0231a`.
- MIT license and copyright are preserved at the beginning of the generated file.
- Build: Node.js v22.23.3 `stripTypeScriptTypes(source, {mode: 'transform'})`; no dependencies installed.
- Rebuild from the saved source: `node work/projection/qr-tests/build-vendor.cjs`.

Load as a classic browser script. Public API:

```javascript
const qr = qrcodegen.QrCode.encodeText(url, qrcodegen.QrCode.Ecc.MEDIUM);
const dark = qr.getModule(x, y);
const size = qr.size;
```

The matrix contains no quiet zone. The renderer must add an opaque white margin
of at least **four modules** on every side, use black modules, preserve square
proportions, and avoid cropping. The fixture SVG demonstrates these requirements.
No URL is sent to an external QR service.

## Verification

- `node --check work/projection/vendor/qrcodegen.js`
- `node work/projection/qr-tests/test-qr.cjs`
- `python -X utf8 work/projection/qr-tests/compare-reference.py`

Seven cases include PT and LENTE URLs, fragments, accented query parameters,
Portuguese text, Chinese, emoji, empty/numeric content, and a 344-character URL.
All matrices match the official independent Python implementation module for
module, including chosen mask and version. The Python reference Git blob is
`0eb24eaee4c4a164ec4c332ec87428630883c317`; its MIT license is retained.
Finder patterns, dimensions, mask bounds, invalid mask rejection and the fixture's
four-module quiet zone are also checked.

These checks are **not QR decoding** or a scan with a physical device. The final
projection renderer must be tested separately, including size, contrast, mobile
camera access and the actual destination URL.
