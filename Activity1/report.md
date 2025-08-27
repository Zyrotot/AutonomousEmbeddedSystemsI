# Exercise 1

## 1. Configuration and Documentation

### Simulator Parameters
The parameters are passed to ROS during initialization. By default, the configuration file used is `example_config.yml`.

- **Vehicle Mass**: Defined in the configuration file under `m` (kg).  
- **Center of Mass (CoM)**: Defined as `l_f`, representing the distance from the center of mass to the front axle of the vehicle.

To modify these parameters, simply edit the config file and restart ROS.

---

## 2. Simulations with Variations

### Parameter Variations
| Mass (kg)  | CoM Position |
|------------|--------------|
| 800        | 1.8 ± 0.2 m  |
| 1000       | 1.8 ± 0.2 m  |
| 1200       | 1.8 ± 0.2 m  |
| 1400       | 1.8 ± 0.2 m  |

### Results

#### Center of Mass at 1.6 m

![Velocity graph for 1.6m and 4 masses](plot_figures/E1/velocity_1_6.png)

From the velocity graph, we can clearly see the effect of changing the vehicle mass: heavier vehicles take longer to accelerate **and** also take longer to decelerate.  

![Spring displacement graph for 1.6m and 4 masses](plot_figures/E1/spring_displacement_1_6.png)

In the spring displacement graph, the curve shapes are very similar across all weights; the main difference is the magnitude of displacement. Heavier vehicles put more strain on the springs, and due to their slower deceleration, the stopping force is observed later in the heavier vehicles.

#### Center of Mass at 1.8 m

![Velocity graph for 1.8m and 4 masses](plot_figures/E1/velocity_1_8.png)

The same observations apply: changing the center of mass has minimal effect on velocity response.  

![Spring displacement graph for 1.8m and 4 masses](plot_figures/E1/spring_displacement_1_8.png)

With the center of mass shifted slightly rearward, we notice a redistribution of suspension load: rear springs experience higher displacement, while front springs experience slightly less. The overall curve shape remains consistent.

#### Center of Mass at 2.0 m

![Velocity graph for 2.0m and 4 masses](plot_figures/E1/velocity_2_0.png)

Velocity response remains largely unaffected by this center of mass change.  

![Spring displacement graph for 2.0m and 4 masses](plot_figures/E1/spring_displacement_2_0.png)

The rearward shift of the center of mass further accentuates the weight distribution effect: rear springs show even higher displacement, and front springs show lower displacement.

#### Same Mass, Different center of mass

![Spring displacement graph for the same mass and 3 different CoM](plot_figures/E1/spring_displacement_same_mass.png)

By comparing the same mass with different center of mass positions, the impact on weight distribution becomes clear: a forward center of mass increases front spring displacement and reduces rear spring displacement, while a rearward center of mass has the opposite effect.

---

## 3. Variation of Step Amplitude

| Acceleration Step (m/s²) |
|---------------------------|
| 0.5                       |
| 1.0                       |
| 2.0                       |

![Velocity response for different acceleration steps](plot_figures/E1/acceleration_steps.png)

As the acceleration step increases, the vehicle reaches the target speed more quickly. Higher step amplitudes result in a faster rise in velocity, demonstrating the influence of input magnitude on system response.

![Spring displacement response for different acceleration steps](plot_figures/E1/acceleration_steps_spring.png)

The spring displacement response shows that during acceleration, higher step amplitudes produce slightly lower spring compression, while during deceleration, the springs experience more abrupt and higher compression. This reflects the increased dynamic load and nonlinearity in the system when larger acceleration commands are applied.

---

## 4. Variations of Integration Step

| Integration Step (s) |
|---------------------|
| 0.4                 |
| 0.8                 |
| 1.6                 |

![Integration step variation](plot_figures/E1/integration_steps.png)

Changing the integration step produced very similar results in this scenario, as the simulation involves a simple case of a vehicle moving in a straight line under constant acceleration.  

In more complex situations, increasing the integration step can introduce delays and numerical errors, since the model linearizations are updated less frequently. This can affect accuracy, stability, and the system's ability to respond to fast-changing dynamics.

# Exercise 2

For this exercise, I developed the script `control_scripts/curve_control.py`.  
The vehicle is commanded to accelerate for a given time, enter a curve, and then continue for a short period after completing the maneuver.  

The script allows variation of:  
- **Acceleration before the curve**  
- **Acceleration (or deceleration) during the curve**  
- **Curve aggressiveness** (steering profile)  
- **Final curve geometry** (final vehicle yaw)  

Steering is applied progressively: as the vehicle approaches the desired angle, the steering input is reduced. This produces smoother trajectories and highlights the vehicle’s physical response to different driving conditions.

---

## Parameter Variations

| Curve type | Degrees |
|------------|---------|
| Straight   | 0       |
| Gentle     | 30      |
| Medium     | 90      |
| Tight      | 180     |

The figure below shows the trajectories for all curve types:

![Cars trajectories](plot_figures/E2/position.png)

---

## Results

### Case 1 — Constant acceleration of 1 m/s²

![Velocity response for 1ms2 constant acceleration](plot_figures/E2/1ms_acceleration/velocity_change_0/velocity.png)  
![Spring displacement response for 1ms2 constant acceleration](plot_figures/E2/1ms_acceleration/velocity_change_0/spring_displacement.png)

At low acceleration, the vehicle’s motion remains relatively stable.  
However, in tighter curves, oscillations appear in the dynamics, probably because of delays in actuation.  

---

### Case 2 — 1 m/s² before the curve, 3 m/s² during the curve

![Velocity response for 1ms before and 3ms2 after](plot_figures/E2/1ms_acceleration/velocity_change_2/velocity.png)  
![Spring displacement response for 1ms before and 3ms2 after](plot_figures/E2/1ms_acceleration/velocity_change_2/spring_displacement.png)

Increasing acceleration inside the curve increases the applied forces.  
This produces stronger spring compression and improves the overall trajectory.

---

### Case 3 — Constant acceleration of 3 m/s²

![Velocity response for 3ms2 constant acceleration](plot_figures/E2/3ms_acceleration/velocity_change_0/velocity.png)  
![Spring displacement response for 3ms2 constant acceleration](plot_figures/E2/3ms_acceleration/velocity_change_0/spring_displacement.png)

At higher constant acceleration, the vehicle enters the curve with higher speed.  
The system response becomes more oscillatory compared to the previous example, even though both have the same acceleration step inside the curve.

---

### Case 4 — 3 m/s² before the curve, 5 m/s² during the curve

![Velocity response for 3ms before and 5ms2 after](plot_figures/E2/3ms_acceleration/velocity_change_2/velocity.png)  
![Spring displacement response for 3ms before and 5ms2 after](plot_figures/E2/3ms_acceleration/velocity_change_2/spring_displacement.png)

Now even though we are accelerating more during the curve, the acceleration step is too big and we start to see some oscilation again.

---

### Case 5 — 3 m/s² before the curve, -0.5 m/s² (deceleration) during the curve

![Velocity response for 3ms before and -0.5ms2 after](plot_figures/E2/3ms_acceleration/velocity_change_minus_3_5/velocity.png)  
![Spring displacement response for 3ms before and -0.5ms2 after](plot_figures/E2/3ms_acceleration/velocity_change_minus_3_5/spring_displacement.png)

Decelerating in the curve reduces the vehicle’s kinetic energy and lowers lateral acceleration.

# Exercise 3

To simulate different road conditions, the parameters `LMUX` and `LMUY` were modified. These represent the maximum available friction in the longitudinal and lateral directions, respectively.  

## Parameter Variations

| Condition    | LMUX/LMUY |
|--------------|-----------|
| Dry asphalt  | 0.90      |
| Wet asphalt  | 0.50      |
| Ice          | 0.10      |

---

## Results

### Case 1 — Acceleration step of 1 m/s²

![Position for 1ms2 constant acceleration](plot_figures/E3/1ms_acceleration/position.png)  
![Velocity response for 1ms2 constant acceleration](plot_figures/E3/1ms_acceleration/velocity.png)  
![Spring displacement response for 1ms2 constant acceleration](plot_figures/E3/1ms_acceleration/spring_displacement.png)  

At low acceleration, the influence of friction limits is minimal.  
The vehicle successfully follows the curves on all surfaces, since the required tire forces remain below the maximum friction available.  
Suspension displacement differences are small, as lateral load transfer is not yet extreme.

---

### Case 2 — Acceleration step of 3 m/s²

![Position for 3ms2 constant acceleration](plot_figures/E3/3ms_acceleration/position.png)  
![Velocity response for 3ms2 constant acceleration](plot_figures/E3/3ms_acceleration/velocity.png)  
![Spring displacement response for 3ms2 constant acceleration](plot_figures/E3/3ms_acceleration/spring_displacement.png)  

At this higher acceleration, friction limits become critical:  
- On **dry asphalt**, the vehicle completes the curve normally.  
- On **wet asphalt**, the reduced friction causes larger slip angles and a wider trajectory.  
- On **ice**, with extremely low friction (0.1), the vehicle struggles to generate enough lateral force, resulting in much slower curve negotiation and strong understeer.  

---

### Case 3 — Acceleration step of 5 m/s²

![Position for 5ms2 constant acceleration](plot_figures/E3/5ms_acceleration/position.png)  
![Velocity response for 5ms2 constant acceleration](plot_figures/E3/5ms_acceleration/velocity.png)  
![Spring displacement response for 5ms2 constant acceleration](plot_figures/E3/5ms_acceleration/spring_displacement.png)  

At very high acceleration, nonlinear effects are dominant:  
- On **dry asphalt**, the vehicle still manages the curve, though with higher lateral load transfer.  
- On **wet asphalt**, the trajectory widens significantly, as the tires saturate earlier.  
- On **ice**, the lack of grip makes the curve extremely wide — in fact, the turning radius becomes several times larger, showing that longitudinal demand has almost completely consumed the available friction.  
