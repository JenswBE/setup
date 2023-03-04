# How-to: Scan documents recto-verso

**Note: SimpleScan supports this out of the box nowadays!**

## 1. Scanning

1. Scan all front sides from feeder
2. Scan all back sides from feeder (these will be in reverse order compared to front sides. That's is fine.)

## 2. Merging into single document

### Using PDF Arranger

1. Open PDF with front sides
2. Import PDF with back sides
3. Select all sides
4. Rotate all sides if required using "Rotate left" or "Rotate right"
5. Select all back sides
6. Reverse sides using "Reverse Order"
7. Cut all back sides
8. Right click first front side and use "Paste Special" => "Paste As Even Pages"

### Using pdftk

```bash
# Reverse back sides order and interleave pages
# Based on https://unix.stackexchange.com/a/92593
pdftk A=front-sides.pdf B=back-sides.pdf shuffle A Bend-1 output result.pdf

# Rotate all pages left
pdftk result.pdf cat 1-endleft output rotated.pdf
```
