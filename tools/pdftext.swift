// Extract text from a PDF using macOS PDFKit. No dependencies, no network,
// nothing to install — macOS ships the framework.
//
// Build once:
//   swiftc -O tools/pdftext.swift -o /tmp/pdftext
//
// Use:
//   /tmp/pdftext docs/official-materials/fll-challenge-bioglow-rgr.pdf
//   /tmp/pdftext docs/official-materials/fll-challenge-bioglow-rgr.pdf 9 12
//
// Page count goes to stderr; text goes to stdout with "=== PAGE n ===" markers,
// so you can pipe it through grep without the count getting in the way.
//
// Image-only PDFs (scans, building instructions) yield nothing — there is no OCR
// here. Open those in Preview.

import Foundation
import PDFKit

let args = CommandLine.arguments

guard args.count > 1 else {
    FileHandle.standardError.write("usage: pdftext <file.pdf> [startPage] [endPage]\n".data(using: .utf8)!)
    exit(2)
}

guard let doc = PDFDocument(url: URL(fileURLWithPath: args[1])) else {
    FileHandle.standardError.write("cannot open \(args[1])\n".data(using: .utf8)!)
    exit(1)
}

let start = args.count > 2 ? (Int(args[2]) ?? 1) : 1
let end = args.count > 3 ? (Int(args[3]) ?? doc.pageCount) : doc.pageCount

FileHandle.standardError.write("pages: \(doc.pageCount)\n".data(using: .utf8)!)

for i in (start - 1)..<min(end, doc.pageCount) {
    guard let page = doc.page(at: i), let text = page.string else { continue }
    print("\n=== PAGE \(i + 1) ===")
    print(text)
}
