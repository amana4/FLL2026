// Render PDF pages to PNG using macOS PDFKit. Companion to pdftext.swift, for
// the PDFs that carry their information as pictures rather than text — the Field
// Setup Reference Guide and the wireframe grid especially.
//
// `sips` only ever converts page 1 of a PDF, which is why this exists.
//
// Build once:
//   swiftc -O tools/pdfpage.swift -o /tmp/pdfpage
//
// Use:
//   /tmp/pdfpage in.pdf outdir            all pages at 2x
//   /tmp/pdfpage in.pdf outdir 3          page 3 only
//   /tmp/pdfpage in.pdf outdir 3 15       pages 3 to 15
//   /tmp/pdfpage in.pdf outdir 3 15 4     ...at 4x
//
// Writes outdir/page-03.png and so on. Page numbers are 1-based, matching the
// "=== PAGE n ===" markers pdftext.swift prints.

import Foundation
import PDFKit
import AppKit

let args = CommandLine.arguments
guard args.count >= 3 else {
    FileHandle.standardError.write(
        "usage: pdfpage <file.pdf> <outdir> [firstPage] [lastPage] [scale]\n"
            .data(using: .utf8)!)
    exit(2)
}

let path = args[1]
let outDir = args[2]

guard let doc = PDFDocument(url: URL(fileURLWithPath: path)) else {
    FileHandle.standardError.write("cannot open \(path)\n".data(using: .utf8)!)
    exit(1)
}

let total = doc.pageCount
let first = args.count > 3 ? max(1, Int(args[3]) ?? 1) : 1
let last = args.count > 4 ? min(total, Int(args[4]) ?? total) : total
let scale = args.count > 5 ? (Double(args[5]) ?? 2.0) : 2.0

try? FileManager.default.createDirectory(
    atPath: outDir, withIntermediateDirectories: true)

FileHandle.standardError.write("pages: \(total)\n".data(using: .utf8)!)

for n in first...last {
    guard let page = doc.page(at: n - 1) else { continue }
    let box = page.bounds(for: .mediaBox)
    let pixels = NSSize(width: box.width * scale, height: box.height * scale)

    let image = NSImage(size: pixels)
    image.lockFocus()
    // PDFs draw with transparency; a white ground keeps the output looking like
    // the printed page rather than like a checkerboard.
    NSColor.white.setFill()
    NSRect(origin: .zero, size: pixels).fill()
    if let ctx = NSGraphicsContext.current?.cgContext {
        ctx.scaleBy(x: CGFloat(scale), y: CGFloat(scale))
        ctx.translateBy(x: -box.origin.x, y: -box.origin.y)
        page.draw(with: .mediaBox, to: ctx)
    }
    image.unlockFocus()

    guard let tiff = image.tiffRepresentation,
          let rep = NSBitmapImageRep(data: tiff),
          let png = rep.representation(using: .png, properties: [:])
    else {
        FileHandle.standardError.write("page \(n): encode failed\n".data(using: .utf8)!)
        continue
    }

    let name = String(format: "page-%02d.png", n)
    let out = URL(fileURLWithPath: outDir).appendingPathComponent(name)
    try? png.write(to: out)
    print("\(out.path)  \(Int(pixels.width))x\(Int(pixels.height))")
}
