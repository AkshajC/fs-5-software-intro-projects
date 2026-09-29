**Goal:** Build a simplified car physics engine. The car will have six parts: throttle, brake, drag, steering, traction, and motor. Follow the instructions and use given equations for each part. 



**Part One: Throttle**
When the driver presses the accelerator pedal, a sensor sends a signal to the car’s powertrain, which sends current to the motor, which in turn rotates the wheels to accelerate the car. 

The driver input is normalized between 0.0 and 1.0, zero meaning no acceleration, one meaning full throttle. Simulate the driver pressing the pedal from 0.0 to 1.0 over 7 seconds, then holding the pedal at 1.0 for 15 seconds. At each time step, calculate acceleration by using the following formulas. 

Multiply driver input by the maximum motor torque to get command torque (rotational force needed from the motor). 
Force at the wheels = (command torque * gear ratio) / radius of the wheels.
To find acceleration, use the formula Force = mass * acceleration. 

Assume a maximum motor torque of 180 Nm, mass of the car to be 300 kg (with driver), gear ratio to be 3:1, and wheel radius to be 0.216 meters. Template provided.



**Part Two: Traction**
Traction is the friction between tires and road. When the driver turns the steering wheel, the direction the tires are pointing and the direction the car is moving is different. This difference is called the slip angle, as the tire rubber deforms to change direction it produces cornering force which pushes the car into a turn. 

The car has a forward velocity(how fast it is moving in the direction the car is pointed), but since the tire can not perfectly follow the steering wheel, some of the car’s motion slides perpendicular to the direction it is pointing. That is called lateral velocity. Lateral acceleration is how quickly lateral velocity is building up.

Simulate the driver turning the steering angle from zero degrees ( tires pointing straight) to five degrees over 3 seconds, then holding the steering wheel for 7 seconds. At each time step, calculate slip angle, lateral force, lateral acceleration, and lateral velocity using the following formulas. 

Slip angle = steer angle - (lateral velocity/forward speed). 

Lateral force =  cornering stiffness * slip angle

Lateral acceleration = lateral force/mass

Lateral velocity = lateral velocity(previous) + (lateral acceleration * timestep)

Assume forward speed of 15 m/s, cornering stiffness to be 36000 N/rad, mass of the car to be 300 kg. Initialize lateral velocity at 0 m/s. Make sure to convert degrees to radians in your calculations. 



**Part Three: Drag**
Drag is the air resistance that pushes against the car when it is moving (accelerating or de-accelerating). Cross sectional area and the drag coefficient of a car affects how much drag force the car experiences. 

Cross sectional area is how much space the car takes from the front (how much air it needs to push out of the way). A drag coefficient is a number that tells us how aerodynamic the car is ( lower drag coefficient means that the car is more aerodynamic).

From 0 m/s accelerate the car at 5 m/s^2 for 10 seconds. At each time step calculate drag, total acceleration, and update velocity.

Drag = 0.5 * Cross sectional area *  drag coefficient * air density * velocity^2. 

Net acceleration = acceleration - (drag/mass)

 Velocity =  velocity + (net acceleration * timestep).

After 10 seconds, stop accelerating completely, let drag slow the car down until a complete stop. At each time step, calculate drag, net acceleration, and update velocity. Stop the simulation once velocity drops to 0.1 m/s (drag gets smaller as the car slows down, never actually becomes zero, so just stop at this point).

Use an air density of 1.2 kg/m^3. Assume cross sectional area to be 1.2 meters^2, drag coefficient to be 0.7, and mass to be 300 kgs. 



**Part Four: Motor Model**
As a motor spins faster (to make the car go faster), it generates resistance to its own current called back-EMF. Back- EMF limits how much torque the motor can deliver. Because of this phenomena, cars have a top speed and can't just keep accelerating forever. 

Simulate the driver pressing the acceleration pedal from 0.0 to 1.0 over three seconds, then hold it at full throttle for 20 seconds. At each time step calculate propulsion force, acceleration, and velocity. 

Propulsion force = maximum propulsion force * throttle input * (1 - (v/vmax)). 

Force = Mass * acceleration

Velocity = velocity + (acceleration * timestep)

Take maximum propulsion force of 2000 N, let vmax be 27 m/s, let mass be 300 kg. 

Hint: Use driver input and time-step loop structure from part one, no need to calculate torque/force at wheels though.



**Part Five: Braking**
Simulate the braking force generated if the car was to cruise at 25 m/s (dont model acceleration, just start it from here) then after two seconds, applies full braking force until the car comes to a stop. The driver input is normalized between 0.0 (no braking input) and 1.0 (max braking input). At each time step, calculate braking force, acceleration, and update velocity. 

Braking force = driver input * maximum braking capacity
Acceleration = - (braking force/mass)
Velocity = velocity + (acceleration * timestep)

Take the maximum braking capacity as 1850 N. Take mass as 300 kgs. Make sure to stop the sim once velocity reaches zero: the car should not move backwards if velocity becomes negative. 
Hint: driver input for the first two seconds is 0.0, then it's 1.0 for the rest of the time.


**Part Six: Unsimplify**
Choose one part (or more) and research how to make it more realistic/accurate. More info given in person
