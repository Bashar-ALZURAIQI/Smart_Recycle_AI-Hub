# Smart Recycle AI-Hub - Labeling Guide

**Version:** 1.0
**Purpose:** Define consistent annotation rules for the V1 waste detection dataset.

---

## 1. Training Classes

The V1 object detection model will use four classes only:

| Class ID | Class Name |
|---|---|
| 0 | plastic |
| 1 | metal |
| 2 | glass |
| 3 | paper_cardboard |

Reject is NOT a training class.

Unsupported or unknown objects are treated as background during
annotation and may later be handled as Reject by the decision logic.

---

## 2. Plastic

Label as `plastic`:

- Plastic water bottles
- Plastic soft-drink bottles
- Plastic shampoo bottles
- Plastic detergent bottles
- Rigid plastic food containers
- Plastic cups

Do NOT label as `plastic`:

- Thin plastic bags
- Mixed-material plastic packaging
- Objects where the material cannot be identified confidently

---

## 3. Metal

Label as `metal`:

- Aluminum beverage cans
- Steel food cans
- Small metal tins
- Metal bottle caps
- Clean rigid metal containers

Do NOT label as `metal`:

- Batteries
- Electronic waste
- Mixed-material objects where metal is not the main visible material

---

## 4. Glass

Label as `glass`:

- Clear glass bottles
- Green glass bottles
- Brown glass bottles
- Glass jars
- Small intact glass containers

Do NOT label as `glass`:

- Broken glass
- Mirrors
- Ceramics
- Porcelain

Broken glass is intentionally excluded from V1.

---

## 5. Paper / Cardboard

Label as `paper_cardboard`:

- Office paper
- Newspaper
- Plain cardboard boxes
- Corrugated cardboard
- Paper bags

Do NOT label as `paper_cardboard`:

- Wet paper
- Food-contaminated paper/cardboard
- Composite packaging
- Tetra Pak

Tetra Pak is intentionally excluded from V1.

---

## 6. Bounding Box Rules

For every supported object:

1. Draw one bounding box around the complete visible object.
2. Keep the box as tight as practical around the object.
3. Do not include large unnecessary areas of background.
4. Do not cut off clearly visible parts of the object.
5. Use one box for each separate physical object.
6. Do not create multiple boxes for different parts of the same object.
7. If two objects overlap, label each supported object separately when each one can still be identified.
8. Label only objects whose class can be determined with reasonable confidence.

---

## 7. Partially Visible Objects

Label a partially visible object only when:

- Enough of the object is visible to identify its class reliably.
- The visible part provides meaningful training information.

Do not label an object when only a very small or ambiguous fragment is visible.

The bounding box should cover only the visible portion of an object
when the rest is outside the image.

---

## 8. Multiple Objects

If an image contains multiple supported objects:

- Label every clearly visible supported object.
- Each object receives its own bounding box.
- Objects may belong to the same or different classes.

Example:

A plastic bottle, a metal can, and a cardboard box in one image
must receive three separate bounding boxes.

---

## 9. Unsupported / Reject Objects

Examples of unsupported objects:

- Organic waste
- Batteries
- Electronic waste
- Shoes
- Clothes
- Broken glass
- Tetra Pak
- Thin plastic bags

Do not assign these objects to one of the four V1 classes.

They may appear in images as background or negative examples.

If an image contains both supported and unsupported objects,
label only the supported objects.

---

## 10. Ambiguous Material

Do NOT guess.

If the annotator cannot confidently decide whether an object is
plastic, metal, glass, or paper/cardboard:

- Do not label it.
- Flag the image for review if needed.

Consistency is more important than forcing every object into a class.

---

## 11. Mixed-Material Objects

Do not label objects whose main material cannot be determined clearly.

Examples:

- Composite packaging
- Plastic-metal combinations
- Paper-plastic laminated packaging

These objects are outside the initial V1 training scope unless the
team explicitly approves them later.

---

## 12. Image Quality

Prefer images where:

- The object is reasonably visible.
- The image is not severely blurred.
- Lighting allows the material or object to be identified.
- The object is not completely hidden.
- Resolution is sufficient for annotation.

Images with difficult lighting or partial occlusion may still be useful,
but they must remain identifiable.

---

## 13. Duplicate Images

Avoid exact duplicates.

Near-duplicate images should be limited so that the dataset does not
become dominated by almost identical examples.

---

## 14. Annotation Consistency

Both team members must follow the same rules.

Before large-scale labeling:

1. Both members label a small shared sample.
2. Compare the annotations.
3. Resolve disagreements.
4. Update this guide if a repeated ambiguity is discovered.
5. Only then continue with large-scale annotation.

---

## 15. Label Review Checklist

Before accepting an annotated image, verify:

- Correct class selected
- Tight bounding box
- No supported object was accidentally missed
- No unsupported object was assigned a V1 class
- No broken glass labeled as glass
- No Tetra Pak labeled as paper_cardboard
- No duplicate boxes on the same object
- Ambiguous objects were not guessed

---

## 16. Scope Reminder

V1 classes:

- plastic
- metal
- glass
- paper_cardboard

Unknown or unsupported objects -> Reject

This guide follows the frozen Smart Recycle AI-Hub V1 scope.
