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

![Velocity graph for 1.6m and 4 masses](plot_figures/velocity_1_6.png)

From the velocity graph, we can clearly see the effect of changing the vehicle mass: heavier vehicles take longer to accelerate **and** also take longer to decelerate.  

![Spring displacement graph for 1.6m and 4 masses](plot_figures/spring_displacement_1_6.png)

In the spring displacement graph, the curve shapes are very similar across all weights; the main difference is the magnitude of displacement. Heavier vehicles put more strain on the springs, and due to their slower deceleration, the stopping force is observed later in the heavier vehicles.

#### Center of Mass at 1.8 m

![Velocity graph for 1.8m and 4 masses](plot_figures/velocity_1_8.png)

The same observations apply: changing the center of mass has minimal effect on velocity response.  

![Spring displacement graph for 1.8m and 4 masses](plot_figures/spring_displacement_1_8.png)

With the center of mass shifted slightly rearward, we notice a redistribution of suspension load: rear springs experience higher displacement, while front springs experience slightly less. The overall curve shape remains consistent.

#### Center of Mass at 2.0 m

![Velocity graph for 2.0m and 4 masses](plot_figures/velocity_2_0.png)

Velocity response remains largely unaffected by this center of mass change.  

![Spring displacement graph for 2.0m and 4 masses](plot_figures/spring_displacement_2_0.png)

The rearward shift of the center of mass further accentuates the weight distribution effect: rear springs show even higher displacement, and front springs show lower displacement.

#### Same Mass, Different center of mass

![Spring displacement graph for the same mass and 3 different CoM](plot_figures/spring_displacement_same_mass.png)

By comparing the same mass with different center of mass positions, the impact on weight distribution becomes clear: a forward center of mass increases front spring displacement and reduces rear spring displacement, while a rearward center of mass has the opposite effect.

---

## 3. Variation of Step Amplitude

| Acceleration Step (m/s²) |
|---------------------------|
| 0.5                       |
| 1.0                       |
| 2.0                       |

![Velocity response for different acceleration steps](plot_figures/acceleration_steps.png)

As the acceleration step increases, the vehicle reaches the target speed more quickly. Higher step amplitudes result in a faster rise in velocity, demonstrating the influence of input magnitude on system response.

![Spring displacement response for different acceleration steps](plot_figures/acceleration_steps_spring.png)

The spring displacement response shows that during acceleration, higher step amplitudes produce slightly lower spring compression, while during deceleration, the springs experience more abrupt and higher compression. This reflects the increased dynamic load and nonlinearity in the system when larger acceleration commands are applied.

---

## 4. Variations of Integration Step

| Integration Step (s) |
|---------------------|
| 0.4                 |
| 0.8                 |
| 1.6                 |

![Integration step variation](plot_figures/integration_steps.png)

Changing the integration step produced very similar results in this scenario, as the simulation involves a simple case of a vehicle moving in a straight line under constant acceleration.  

In more complex situations, increasing the integration step can introduce delays and numerical errors, since the model linearizations are updated less frequently. This can affect accuracy, stability, and the system's ability to respond to fast-changing dynamics.
