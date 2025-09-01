# A Heuristic Scheduling Mechanism for Networked Mobile Robots

## Abstract
Many real-world control systems tolerate delays, jitter, and data loss far beyond what they were formally designed for. However, there is no clear method for defining the threshold for these irregularities while maintaining stability. This project proposes a simple heuristic mechanism that signals the scheduler on the current situation of the system: when the robot is tracking its reference well, it asks the scheduler to lower the input rate; when error begins to grow, it asks for a higher rate again. The goal is to save resources without losing safety or stability.

---

## 1. Context

### Field
Controller and scheduler codesign, cyber-physical systems, robotics.

### Relevance
Autonomous robots and vehicles increasingly rely on wireless communication and shared processors. Having inputs delivered at a fixed, high rate can waste energy and network bandwidth, especially when the robot is already stable. A more adaptive approach could free up resources while still maintaining safety.

### Open Problems
- How to decide in real time when it is safe to lower the input rate.
- How to make this decision with simple heuristics, without requiring mathematical proofs.

### What We Address
We propose and test a lightweight scheduling mechanism that lets the controller itself decide when the sensor input rate can safely go down and when it needs to go up again.

---

## 2. Problem Statement
Can we design and validate a simple, empirical scheduling strategy for a PID-controlled mobile robot that can control the priority of related processes while keeping the robot stable?

---

## 3. Envisioned Solution

### Control Core
- Two PID loops: one for speed, one for heading (steering).
- A predictor that estimates the robot’s state for decreased reliance on sensor readings.

### Heuristic Scheduler
- The controller keeps track of metrics such as:
  - Derivative of error
  - Control saturation
  - Predictor state
  
- From these, it computes a simple **robustness score**, where a high score represents that it is safe to reduce the input rate.

- The controller then requests a new sampling period within safe limits.

### Interfaces
- Controller → Scheduler: current score and requested rate.
- Controller → Other modules: predicted state for safety.

### Validation Plan
- First test in Carla simulation under artificial delays, jitter, and packet losses.
- Then deploy on a car with IMU + wheel encoders.
- Compare adaptive scheduling against a fixed-rate baseline.

---

## 4. Hypothesis
We expect that an adaptive-rate controller will use fewer samples on average (saving CPU and bandwidth) while still keeping the robot stable and within acceptable error margins, even under realistic communication delays and losses.

---

## 5. Methodology

### What We Already Have
- PID controllers for heading and speed.
- Simulation tools and robot hardware with sensors.
- Knowledge of basic system identification and control tuning.
- A simple model of the robot to use in the predictor.
- Tools for injecting artificial delays and packet losses in experiments.

### What Is Missing
- The heuristic mechanism for deciding when to slow down or speed up.

### How We Will Build It
1. Implement the heuristic scheduler inside the controller code.
2. Add safety limits so that if the error grows too large, the system always returns to the highest frequency.
3. Run simulation tests, then controlled experiments on the robot.

### Experiments
- Compare adaptive scheduling vs fixed-rate control.
- Perform tasks such as straight-line driving, curves, and waypoint following.

**Metrics:**
- Tracking error (how close the robot follows the reference).
- Number of instability or safety incidents.
- Resource savings (CPU usage, communication load).

---

## 6. Safety Considerations
- Always enforce a minimum safe frequency.
- Include a watchdog that forces the maximum rate if the error grows too large.
- Test in simulation and controlled environments before physical trials.

---

## 7. Expected Contributions
- A practical, heuristic scheduling mechanism for adaptive-rate control.
- Experimental evidence of resource savings without sacrificing stability.
- Open-source code and datasets for reproducibility.

---
