# Smart Recycle AI-Hub — V1 Project Scope

**Version:** 1.0  
**Status:** Scope Definition  
**Project Type:** University Prototype  

---

## 1. V1 Goal

The goal of Smart Recycle AI-Hub V1 is to build a working prototype
that uses computer vision and artificial intelligence to identify
selected recyclable waste materials and sort them automatically
using one robotic arm.

The prototype will use:

- A conveyor belt
- A fixed camera
- An AI object detection model
- Python-based decision logic
- Arduino-based hardware control
- One robotic arm
- Separate waste containers

V1 is a university-scale proof of concept and is not an industrial
municipal waste sorting system.

---

## 2. Waste Categories

Smart Recycle AI-Hub V1 will classify the following four categories:

1. Plastic
2. Metal
3. Glass
4. Paper / Cardboard

Unknown or unsupported objects will be treated as Reject.

### 2.1 Plastic

Accepted in V1:

- Plastic water bottles
- Plastic soft-drink bottles
- Plastic shampoo or detergent bottles
- Rigid plastic food containers
- Plastic cups

Out of Scope:

- Thin plastic bags
- Mixed-material plastic packaging

### 2.2 Metal

Accepted in V1:

- Aluminum beverage cans
- Steel food cans
- Small metal tins
- Metal bottle caps
- Clean rigid metal containers

Out of Scope:

- Batteries
- Electronic waste

### 2.3 Glass

Accepted in V1:

- Clear glass bottles
- Green glass bottles
- Brown glass bottles
- Glass jars
- Small intact glass containers

Out of Scope:

- Broken glass
- Mirrors, ceramics and porcelain

### 2.4 Paper / Cardboard

Accepted in V1:

- Office paper
- Newspaper
- Plain cardboard boxes
- Corrugated cardboard
- Paper bags

Out of Scope:

- Wet or food-contaminated paper/cardboard
- Composite packaging such as Tetra Pak

---

## 3. Reject Logic

An object will be treated as Reject if:

- The AI cannot identify it as one of the four supported classes.
- The confidence score is too low.
- The object belongs to a category intentionally excluded from V1.
- The object is unsafe or unsupported.

Examples:

- Batteries
- Organic waste
- Shoes
- Clothes
- Broken glass
- Electronic waste

---

## 4. V1 Success Criteria

Smart Recycle AI-Hub V1 will be considered successful when the
following conditions are achieved.

### 4.1 Vision Detection

The camera and AI model can detect and classify:

- Plastic
- Metal
- Glass
- Paper / Cardboard

Initial target:

- At least 90% correct classifications on the prototype test set.

### 4.2 Communication

The computer successfully sends the sorting decision to the
microcontroller.

Example:

SORT:PLASTIC

The microcontroller confirms that the command was received.

Example:

ACK

### 4.3 Robotic Pick

The robotic arm must:

1. Move to the defined pickup position.
2. Grip the detected object.
3. Lift the object without manual assistance.

### 4.4 Correct Sorting

The complete system must successfully perform:

Detect
→ Classify
→ Send Command
→ Pick
→ Move
→ Place

and place the object inside the correct waste container.

### 4.5 Reliability

Before V1 is considered complete:

- The system should complete at least 20 consecutive controlled
  sorting cycles without manual intervention.

Before the final university presentation:

- At least 100 documented sorting trials should be performed.

---

## 5. V1 Operating Mode

The first prototype will use the following operating cycle:

Object enters
↓
Conveyor stops
↓
Camera detects object
↓
AI classifies object
↓
Python sends decision
↓
Arduino receives command
↓
Robotic arm picks object
↓
Robot places object in correct bin
↓
Conveyor resumes

Operating strategy:

STOP → DETECT → CLASSIFY → PICK → PLACE → RESUME

---

## 6. Not Included in V1

The following features are intentionally excluded from V1:

- Organic waste classification
- Hazardous waste classification
- PET / HDPE / PVC polymer-level identification
- NIR spectroscopy
- Multiple robotic arms
- Delta robot
- Continuous high-speed sorting
- Industrial PLC control
- Industrial-scale throughput
- Cloud infrastructure
- Mobile application
- Full municipal waste processing

---

## 7. V1 Hardware Scope

The planned V1 hardware consists of:

- One conveyor belt
- One fixed USB camera
- Fixed LED lighting
- One laptop or computer
- One Arduino-compatible controller
- One robotic arm
- One gripper
- One conveyor motor and motor driver
- One object detection sensor
- Four recycling containers
- One Reject container or area
- Required power supplies
- Basic emergency stop and safety controls

---

## 8. V1 Software Scope

The planned software stack consists of:

- Python
- Ultralytics YOLO
- OpenCV
- PySerial
- Arduino firmware
- CSV-based logging
- Simple monitoring dashboard

---

## 9. Scope Approval

**Version:** V1.0  
**Scope Status:** Frozen after team approval

Team Members:

- Member 1: ______________________
- Member 2: ______________________

Any future change to the V1 scope must answer:

1. What is changing?
2. Why is the change necessary?
3. How many additional hours will it require?
4. Does it threaten the September prototype deadline?
5. Has the other team member approved the change?
