import Cocoa
import WebKit
// Render an SVG diagram to PNG using macOS WebKit. PowerPoint cannot place an
// SVG reliably, so tools/make-exceeds-pptx.py uses PNG copies of the diagrams
// in robot-design/diagrams/png/. Quick Look (qlmanage) cannot do this here.
//
// Build once:
//   swiftc -O tools/svg2png.swift -o /tmp/svg2png
//
// Use:
//   /tmp/svg2png robot-design/diagrams/face-square.svg robot-design/diagrams/png/face-square.png 1400
//
// The last number is the width in pixels. The height follows the SVG's shape.
let a = CommandLine.arguments
let inURL = URL(fileURLWithPath: a[1]); let out = a[2]; let width = Double(a[3]) ?? 1600
let app = NSApplication.shared
class D: NSObject, WKNavigationDelegate {
  var wv: WKWebView!
  func start() {
    wv = WKWebView(frame: NSRect(x: 0, y: 0, width: width, height: 800))
    wv.navigationDelegate = self
    let svg = try! String(contentsOf: inURL)
    let html = "<html><body style='margin:0;background:#fff'><div style='width:\(Int(width))px'>" +
      svg.replacingOccurrences(of: "<svg ", with: "<svg width='100%' height='auto' style='display:block' ") + "</div></body></html>"
    wv.loadHTMLString(html, baseURL: inURL.deletingLastPathComponent())
  }
  func webView(_ w: WKWebView, didFinish n: WKNavigation!) {
    DispatchQueue.main.asyncAfter(deadline: .now() + 0.8) {
      w.evaluateJavaScript("document.querySelector('svg').getBoundingClientRect().height") { h, _ in
        let hh = (h as? Double) ?? 800
        w.frame = NSRect(x: 0, y: 0, width: width, height: hh)
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.8) {
          let c = WKSnapshotConfiguration(); c.rect = NSRect(x: 0, y: 0, width: width, height: hh)
          w.takeSnapshot(with: c) { img, _ in
            if let img = img, let t = img.tiffRepresentation, let b = NSBitmapImageRep(data: t) {
              try! b.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: out))
            }
            exit(0)
          }
        }
      }
    }
  }
}
let d = D(); d.start(); app.run()
