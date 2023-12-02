# M5 - Pong (Part 2)

This project implements a 2-player pong game that uses gesture recognition to control the player's movement.

## Comparing M4 vs. M5 Gestures

In M4, player 1's movement is determined by `ay`, the y-axis value taken from the Arduino IMU, for gesture control. 

$\text{M4 Player 1 movement}=\begin{cases}
  \text{up} & ay>0.5 \\
  \text{down} & ay<0.5 \\
  \text{stop} & \text{otherwise}
\end{cases}$

Player 2's movement is determined by holding down the "up" and "down" keys on the computer.

$\text{M4 Player 2 movement}=\begin{cases}
  \text{up} & \text{UP key pressed} \\
  \text{down} & \text{DOWN key pressed} \\
  \text{stop} & \text{otherwise}
\end{cases}$

### M5
In M5, player 1's movement is determined by the IMU gyroscope data. Right-left movement is determined by examining the `gx` values jumping from >700 to <-600 over a 170ms period. Up-down movement is determined by examining the `gy` values jumping from >300 to <-400 over a 170s period. These constant values were determined through careful experimentation.

$\text{M5 Player 1 movement}=\begin{cases}
  \text{up} & \text{right-left wrist movement} \\
  \text{down} & \text{up-down wrist movement} \\
  \text{stop} & \text{otherwise}
\end{cases}$

Player 2's movement is determined by the `az` accelerometer values.

$\text{M5 Player 2 movement}=\begin{cases}
  \text{up} & az>0.5 \\
  \text{down} & az < 0.5 \\
  \text{stop} & \text{otherwise}
\end{cases}$

### Metrics of Success
* intuitive gestures: should be similar to natural human movement for "up", "down", and "stop"
* play-ability: user is able to use the gesture control with little errors within 1 game 
* easily detectible by IMU: few false-positives (moving when we don't intend to) and false-negatives (not moving when we intend to)

### Experiment Results
M4's gesture control is intuitive since the resting position of the Arduino is already in the "stop" motion. Flipping the Arduino up and down to change the `ax` value is also intuitive because they match with the motion of the player's sprite in-game. These controls have easy play-ability and detectability by the IMU since the Arduino sends continuous HTTP POST messages when `ax` is within the given threshold for "up" or "down".

M5's player 1 gesture control is less intuitive for moving "up" and "down" since these movements are not similar to any human gestures for those movements. This gesture control is also less play-able because one individual movement right-left or up-down only sends one HTTP POST message which makes player movement much slower. This is also less detectible by the IMU as there are many false-negatives, perhaps due to un-optimal threshold and delay values between samples.

M5's player 2 gesture control is also less intuitive for movement since the resting position of the Arduino corresponds to "up" as `az` < 0.5. This results in a bit of a learning curve to understand the gesture control. However, this is equally as play-able and detectible as M4's gesture control.

### Conclusion
In conclusion, M4's gesture control surpasses both M5 player 1 and M5 player 2 in all the metrics of success.