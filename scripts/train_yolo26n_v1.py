from ultralytics import YOLO


MODEL_NAME = "yolo26n.pt"
DATA_CONFIG = r"data\processed\waste_v1\data.yaml"


model = YOLO(MODEL_NAME)

model.train(
    data=DATA_CONFIG,
    epochs=80,
    patience=15,
    imgsz=640,
    batch=16,
    device=0,
    workers=0,
    project=r"runs\waste_v1",
    name="yolo26n_v1_baseline",
)