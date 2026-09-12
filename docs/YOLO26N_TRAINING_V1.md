\# YOLO26n V1 Training



\## 1. Purpose



This document records the first official YOLO26n training baseline for the Smart Recycle AI-Hub V1 prototype.



The purpose of this model is to detect four waste categories:



\- plastic

\- metal

\- glass

\- paper\_cardboard



Reject is not a YOLO training class. Unknown or low-confidence objects will be handled later by the Python decision logic.



\---



\## 2. Model



Pretrained model:



```text

yolo26n.pt

```



The pretrained model was adapted from its original class configuration to the four waste classes used by Smart Recycle AI-Hub.



During training, Ultralytics reported:



```text

Overriding model.yaml nc=80 with nc=4

```



\---



\## 3. Training Command



The official V1 baseline was trained using:



```cmd

yolo detect train model=yolo26n.pt data=data\\processed\\waste\_v1\\data.yaml epochs=80 patience=15 imgsz=640 batch=16 device=0 workers=0 project=runs\\waste\_v1 name=yolo26n\_v1\_baseline

```



\### Training Parameters



| Parameter | Value |

|---|---|

| Model | yolo26n.pt |

| Dataset config | data\\processed\\waste\_v1\\data.yaml |

| Epochs | 80 |

| Patience | 15 |

| Image size | 640 |

| Batch size | 16 |

| Device | 0 |

| Workers | 0 |

| Project | runs\\waste\_v1 |

| Run name | yolo26n\_v1\_baseline |



\---



\## 4. Training Environment



The training environment was:



```text

Python: 3.14.6

Ultralytics: 8.4.142

PyTorch: 2.14.0+cu126

CUDA: Enabled

GPU: NVIDIA GeForce RTX 4050 Laptop GPU

VRAM: approximately 6 GB

```



Automatic Mixed Precision (AMP) checks passed successfully.



\---



\## 5. Dataset Used



Training split:



```text

Images: 15,148

Objects: 83,850

```



Training class distribution:



```text

plastic: 18,785

metal: 13,018

glass: 18,480

paper\_cardboard: 33,567

```



Validation split:



```text

Images: 1,268

Objects: 2,086

```



Validation class distribution:



```text

plastic: 497

metal: 298

glass: 456

paper\_cardboard: 835

```



The dataset had already passed validation checks before training, including:



\- invalid label checks

\- invalid class ID checks

\- bounding box checks

\- empty label checks

\- duplicate label checks

\- train/validation source leakage checks



The final checks reported:



```text

EMPTY: 0

BAD\_LINES: 0

BAD\_CLASS: 0

BAD\_BOX: 0



FILES WITH DUPLICATES: 0

TOTAL DUPLICATE LINES: 0



OVERLAPPING SOURCE GROUPS: 0

```



For full dataset preparation details, see:



```text

docs/DATASET\_PREPARATION\_V1.md

```



\---



\## 6. Training Completion



Training completed successfully:



```text

80 / 80 epochs

```



Total training time:



```text

24.163 hours

```



The final weights generated were:



```text

best.pt

last.pt

```



Each weight file was approximately:



```text

5.4 MB

```



The model weights are intentionally not tracked by Git because `.pt` files are excluded by `.gitignore`.



The training output was stored locally under the Ultralytics run directory.



\---



\## 7. Final Validation Results



After training, Ultralytics automatically validated the saved `best.pt` model.



The final overall results were:



| Metric | Result |

|---|---:|

| Precision | 0.809 |

| Recall | 0.747 |

| mAP50 | 0.802 |

| mAP50-95 | 0.452 |



\---



\## 8. Per-Class Results



| Class | Precision | Recall | mAP50 | mAP50-95 |

|---|---:|---:|---:|---:|

| plastic | 0.802 | 0.767 | 0.831 | 0.459 |

| metal | 0.877 | 0.861 | 0.902 | 0.498 |

| glass | 0.819 | 0.601 | 0.693 | 0.381 |

| paper\_cardboard | 0.738 | 0.760 | 0.783 | 0.470 |



\---



\## 9. Current Model Assessment



Metal currently shows the strongest validation performance.



Its results were:



```text

Precision: 0.877

Recall: 0.861

mAP50: 0.902

mAP50-95: 0.498

```



Glass currently has the weakest recall:



```text

Recall: 0.601

```



Its complete results were:



```text

Precision: 0.819

Recall: 0.601

mAP50: 0.693

mAP50-95: 0.381

```



This means missed glass detections must receive special attention during real-world testing.



However, the model will not be retrained only because glass has lower validation performance.



Retraining will only be considered if real-world testing shows that the AI model itself is causing significant failures.



Possible non-AI causes must also be considered, including:



\- lighting

\- camera position

\- camera quality

\- object orientation

\- conveyor positioning

\- physical object appearance



\---



\## 10. Inference Speed



Final validation reported approximately:



```text

Preprocess: 0.2 ms/image

Inference: 6.2 ms/image

Postprocess: 0.8 ms/image

```



These measurements were produced during validation using the NVIDIA GeForce RTX 4050 Laptop GPU.



\---



\## 11. Reproducible Training Script



A Python version of the official V1 training configuration is stored at:



```text

scripts/train\_yolo26n\_v1.py

```



Its purpose is to preserve the exact baseline training configuration in source control.



The script should not be executed unless retraining is intentionally required.



The original training was executed using the Ultralytics CLI command documented in Section 3.



\---



\## 12. Git Tracking Policy



The following project assets are intentionally not committed to GitHub:



```text

\*.pt

runs/

data/processed/

data/raw/

```



This prevents large generated datasets, training outputs, and model weights from being stored directly in the Git repository.



The repository instead tracks:



\- training scripts

\- dataset preparation scripts

\- project configuration

\- documentation

\- validation methodology

\- source code



\---



\## 13. Training Milestone Status



The YOLO26n V1 baseline training milestone is complete.



Current status:



```text

Dataset preparation: DONE

Dataset validation: DONE

Duplicate checks: DONE

Split leakage checks: DONE

YOLO26n training: DONE

80/80 epochs: DONE

best.pt generated: DONE

Final validation: DONE

```



\---



\## 14. Next Development Phase



The next phase is real-world testing and software integration.



The planned flow is:



```text

best.pt

&#x20;  ↓

real-world image testing

&#x20;  ↓

Streamlit test interface

&#x20;  ↓

live camera inference

&#x20;  ↓

Python class / Reject decision logic

&#x20;  ↓

PySerial communication

&#x20;  ↓

Arduino integration

&#x20;  ↓

conveyor + sensor + robotic arm

&#x20;  ↓

physical waste sorting

```



The immediate next step is to build a simple Streamlit interface that loads `best.pt`, accepts real-world waste images, runs YOLO26n inference, and displays:



\- detected class

\- confidence score

\- bounding box

\- annotated image



The first Streamlit version is a testing tool and is not intended to be the final user interface.



\---



\## 15. Retraining Decision Rule



Retraining is not currently planned.



The current `best.pt` model will first be tested using real physical waste objects.



Retraining will only be considered if documented real-world tests show that the AI model is a significant source of failure.



A mechanical, camera, lighting, sensor, serial communication, or Arduino problem must not be solved by retraining YOLO.



\---



\## 16. V1 Classes



The V1 model is frozen to four YOLO classes:



```text

0: plastic

1: metal

2: glass

3: paper\_cardboard

```



Reject is handled by application logic and is not a fifth YOLO class.



No additional waste categories should be added before the V1 prototype is successfully integrated and tested.

