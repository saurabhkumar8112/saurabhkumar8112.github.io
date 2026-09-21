"""Encode browser-friendly copies with cwebp; preserve all original PNGs.

Run after changing article PNGs, then run build_site.py. The normal site
build does not need cwebp: derivatives are versioned with the originals.
"""
from pathlib import Path
import shutil
import struct
import subprocess

ROOT = Path(__file__).resolve().parent
encoder = shutil.which('cwebp')
if not encoder:
    raise SystemExit('Image optimization requires the cwebp command from libwebp.')

for source in sorted((ROOT / 'content').glob('*/assets/*.png')):
    width, height = struct.unpack('>II', source.read_bytes()[16:24])
    cover = source.stem == 'cover'
    options = ['-q', '86', '-m', '6'] if cover else ['-lossless', '-m', '6']
    output = source.with_suffix('.webp')
    subprocess.run([encoder, '-quiet', '-metadata', 'none', *options, str(source), '-o', str(output)], check=True)
    for target_width in ((640, 1280) if cover else (1280,)):
        if target_width >= width:
            continue
        derivative = source.with_name(f'{source.stem}-{target_width}.webp')
        subprocess.run([encoder, '-quiet', '-metadata', 'none', *options, '-resize', str(target_width), '0', str(source), '-o', str(derivative)], check=True)
    print(f'{source.name}: {source.stat().st_size:,} bytes PNG -> {output.stat().st_size:,} bytes WebP')
