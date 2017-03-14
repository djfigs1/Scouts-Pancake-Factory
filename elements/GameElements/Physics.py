def Gravity(accel, prevPos, prevVol, deltaT):
    vel = accel * deltaT + prevVol
    pos = 0.5 * accel * (deltaT ** 2) + vel*deltaT + prevPos
    return (vel, pos)