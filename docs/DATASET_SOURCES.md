# Smart Recycle AI-Hub - Dataset Sources

## Final V1 Classes

0 = plastic
1 = metal
2 = glass
3 = paper_cardboard

Reject is NOT a training class.

---

## Primary Dataset

Name:
Waste Management AI

Provider:
University of Tehran / Roboflow Universe

Task:
Object Detection

License:
CC BY 4.0

Classes:
- Paper
- Plastic
- Glass
- Metal
- Cardboard

Mapping:
Plastic -> plastic
Metal -> metal
Glass -> glass
Paper -> paper_cardboard
Cardboard -> paper_cardboard

Status:
SELECTED - PRIMARY

---

## Secondary Dataset

Name:
DWSD - Dense Waste Segmentation Dataset

Task:
Segmentation

License:
CC BY 4.0

Approved Mapping:
plastic containers -> plastic
plastic bottles -> plastic
plastic -> plastic
plastic cups -> plastic
metal bottles -> metal
glass -> glass
paper -> paper_cardboard

Other classes:
EXCLUDE / REVIEW

Status:
SELECTED - SECONDARY

---

## Optional Dataset

Name:
TACO - Trash Annotations in Context

Task:
Detection / Segmentation

Annotation Format:
COCO

Annotation License:
CC BY 4.0

Status:
OPTIONAL - DO NOT DOWNLOAD YET

Purpose:
Use later only for difficult real-world examples or negative/background cases.