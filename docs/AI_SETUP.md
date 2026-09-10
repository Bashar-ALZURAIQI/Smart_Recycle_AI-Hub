# AI Environment Setup

## Purpose

This document records the AI development environment used for the Smart Recycle AI-Hub project.

COCO classes are used only for environment and inference smoke testing.
COCO classes are NOT the Smart Recycle AI-Hub project classes.

### Smart Recycle AI-Hub V1 Classes

- Plastic
- Metal
- Glass
- Paper/Cardboard
- Unknown objects -> Reject

---

## Laptop A

### Software

- Python: 3.14.6
- PyTorch: 2.14.0+cu126
- PyTorch CUDA Runtime: 12.6
- CUDA Available in PyTorch: True
- Ultralytics: 8.4.142
- OpenCV: 5.0.0
- YOLO Model: YOLO26n

### Hardware

- GPU: NVIDIA GeForce RTX 4050 Laptop GPU
- NVIDIA Driver: 610.62
- NVIDIA-SMI CUDA Support: 13.3

### Python Environment

Virtual environment:

```text
.venv
```

Python executable:

```text
D:\Projects\Smart_Recycle_AI-Hub\.venv\Scripts\python.exe
```

Dependencies were exported to:

```text
requirements.txt
```

using:

```cmd
pip freeze > requirements.txt
```

### Library Verification

PyTorch import: PASS

CUDA available in PyTorch: PASS

GPU detection: PASS

Ultralytics import: PASS

OpenCV import: PASS

### YOLO26n Inference Verification

Status: PASS

Test image:

```text
docs/evidence/environment/laptop_a/bus.jpg
```

Model:

```text
yolo26n.pt
```

Device:

```text
CUDA GPU 0 - NVIDIA GeForce RTX 4050 Laptop GPU
```

Detection result:

```text
4 persons, 1 bus
```

Inference time:

```text
22.0 ms
```

The saved prediction image was opened and visually verified.

Bounding boxes and confidence scores were present, and the visual
result was consistent with the CLI output.

COCO detections from this test are used only for environment/inference
verification and must not be treated as Smart Recycle AI-Hub project classes.

### Evidence

Environment evidence:

```text
docs/evidence/environment/laptop_a/environment_check.txt
```

Input image:

```text
docs/evidence/environment/laptop_a/bus.jpg
```

Verified inference result:

```text
docs/evidence/environment/laptop_a/inference_result.jpg
```

Environment verification: PASS

YOLO26n inference verification: PASS
---

## Laptop B

Status: PENDING VERIFICATION

Laptop B information must be added only after its environment has been tested directly.