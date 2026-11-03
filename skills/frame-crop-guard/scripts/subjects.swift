// Faces and whole people in each image (Apple Vision). One line per image:
// path <TAB> WxH <TAB> faces x0,y0,x1,y1;... <TAB> humans x0,y0,x1,y1;...   (normalised, origin top-left)
import Foundation
import Vision
import AppKit
func boxes(_ obs: [VNDetectedObjectObservation]) -> String {
  obs.map { let b = $0.boundingBox; return String(format: "%.4f,%.4f,%.4f,%.4f", b.minX, 1 - b.maxY, b.maxX, 1 - b.minY) }.joined(separator: ";")
}
for path in CommandLine.arguments.dropFirst() {
  guard let img = NSImage(contentsOfFile: path), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { print("\(path)\tERR\t\t"); continue }
  let faces = VNDetectFaceRectanglesRequest()
  let humans = VNDetectHumanRectanglesRequest()
  humans.upperBodyOnly = false
  let h = VNImageRequestHandler(cgImage: cg, options: [:])
  try? h.perform([faces, humans])
  print("\(path)\t\(cg.width)x\(cg.height)\t\(boxes(faces.results ?? []))\t\(boxes(humans.results ?? []))")
}
