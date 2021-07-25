import os
import control as ct
import numpy as np
import control.matlab as cm
from matplotlib import pyplot as plt
spacer = " ---------------------- "


def question1(Gpr, plot=True):
    print(spacer+"Question 1"+spacer)
    # 1. POLES AND ZEROS
    poles = ct.pole(Gpr)
    zeros = ct.zero(Gpr)
    print("\t Poles of the system are {}, and zeroes are {}".format(poles, zeros))

    # 2. PZ MAP
    H = 1
    OLTF = Gpr*H

    plt.figure("Q1 - PZ map")
    ct.pzmap(OLTF)

    if plot:
        plt.show
    # 3. STABILITY
    stable = True
    for pole in poles:
        if(pole > 0):
            stable = False

    temp = "unstable"
    if(stable):
        temp = "stable"
    print("\t Since {} are the poles, the system is {}".format(poles, temp))

    # 4. STEP RESPONSE
    t, c = ct.step_response(OLTF)
    end_value = c[c.size-1]

    print("\t The end value of the OL step_response is {}".format(end_value))

    plt.figure("Q1 - Step response")
    plt.plot(t, c)

    # plot asymptote
    x_coordinates = [t[0], t[t.size-1]]
    y_coordinates = [end_value, end_value]
    plt.plot(x_coordinates, y_coordinates)

    if plot:
        plt.show()

    return OLTF


def question2(OLTF, plot=True):
    print(spacer+"Question 2"+spacer)
    # 1. BODE PLOT
    plt.figure("Q2 - Bode plot")
    ct.bode_plot(OLTF, dB=True, margins=True)
    if plot:
        plt.show()

    # 2. GAIN
    gainHz = ct.stability_margins(OLTF)
    gaindB = ct.mag2db(gainHz)

    print("\t The maximum gain in Hz is {} and in dB is {}".format(gainHz, gaindB))

    return (gainHz, gaindB)


def question3(OLTF, gainHz, plot=True):
    print(spacer+"Question 3"+spacer)

    Kp = gainHz[0]
    print("\t Kp is {}".format(Kp))

    OLTF = OLTF*Kp

    plt.figure("Q3 - Nyquist plot")
    ct.nyquist_plot(OLTF, plot=True)
    if plot:
        plt.show()

    return OLTF


def pi_pid(OLTF, q, plot=True):
    # SETTLING & RISE
    CLTF = ct.feedback(OLTF)
    var = cm.stepinfo(CLTF)
    print(var)

    plt.figure("Q{} - Bode plot".format(q))
    ct.bode_plot(CLTF, dB=True, margins=True)
    t, c = ct.step_response(CLTF)
    plt.figure("Q{} - Step responce question".format(q))
    plt.plot(t, c)
    if plot:
        plt.show()


def question4(Gpr, H=1, plot=True):
    print(spacer+"Question 4"+spacer)

    # PI REGULATOR
    Kp = 43.3
    Ti = 5
    Gc = (Kp*(1+(Ti*s)))/(Ti*s)
    print(Gc)

    # NEW OLTF
    OLTF = Gpr*Gc*H

    pi_pid(OLTF, 4, plot)


def question5(Gpr, H=1, plot=True):
    print(spacer+"Question 5"+spacer)
    # PID REGULATOR
    Kp = 5
    Td = 60
    Ti = 30
    Gc = Kp*(1 + (1/Ti*s) + Td*s)
    print(Gc)

    # NEW OLTF
    OLTF = Gpr*Gc*H
    pi_pid(OLTF, 5, plot)


if __name__ == "__main__":
    s = ct.tf('s')
    plotting = False

    # Q1
    Gpr = 1/((s+0.3)*(s+3)*(s+6))
    OLTF = question1(Gpr, plot=plotting)

    # Q2
    (gainHz, gaindB) = question2(OLTF, plot=plotting)

    # Q3
    OLTF = question3(OLTF, gainHz, plot=plotting)

    # Q4
    question4(Gpr, plot=plotting)

    # Q5
    question5(Gpr, plot=plotting)

    # Plotting
    if not plotting:
        plt.show()
