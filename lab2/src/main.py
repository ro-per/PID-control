import os
import control as ct
import numpy as nps
import control.matlab as cm
import pandas as pd
import math
from matplotlib import pyplot as plt
spacer = " ---------------------- "

# Vraag 1: polen nullen diagram, eindwaarde stapantwoord


def question1(Gpr, OLTF, plot=True):
    print(spacer+"Question 1"+spacer)
    # 1. POLES AND ZEROS
    poles = ct.pole(Gpr)
    zeros = ct.zero(Gpr)
    print("\t Poles of the system are {}, and zeroes are {}".format(poles, zeros))
    # 2. PZ MAP
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
    t, c = ct.step_response(OLTF, T=10000)
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

# Vraag 2: Ontwerp een P regelaar door Kp te zoeken mbv een poolbaan. Verifieer dmv Nyquist criterium


def question2(OLTF, plot=True):
    print(spacer+"Question 2"+spacer)
    # 1. ROOT LOCUS
    plt.figure("Q2 - Root locus")
    ct.root_locus(OLTF)

    # 2. GAIN
    gainHz = ct.stability_margins(OLTF)

    print("\t The maximum gain in Hz is {}".format(gainHz))

    # 2. Nyquist Original
    plt.figure("Q2 - Nyquist Original VS. Regulated")
    plt.subplot(1, 2, 1)
    ct.nyquist_plot(OLTF)

    # 3. P regulator design
    Kp = 3  # Must be larger than 2
    OLTF = Gpr*Kp*H

    # 4. Nyquist Regulated
    plt.subplot(1, 2, 2)
    ct.nyquist_plot(OLTF)

    if plot:
        plt.show()

    return OLTF

# Vraag 3: Ontwerp een P en PI regelaar die CL stapantwoord naar 1 laten eindigen


def cltf_feedback(OLTF):
    CLTF = ct.feedback(OLTF)
    t, c = ct.step_response(CLTF, T=30)
    end_value = c[c.size-1]
    print("\t The end value is {}".format(end_value))
    return (CLTF, t, c)


def p_regulator(Gpr, Kp):
    Gc = Kp
    OLTF = Gpr*Gc*H
    return cltf_feedback(OLTF)


def pi_regulator(Gpr, Kp, Ti):
    Gc = (Kp*(1+(Ti*s)))/(Ti*s)
    OLTF = Gpr*Gc*H
    return cltf_feedback(OLTF)


def question3(Gpr, H, plot=True):
    print(spacer+"Question 3"+spacer)
    plt.figure("Q3 - Design of P- and PI- regulator")

    # P regelaar
    # Kp=3
    (CLTF_P, t, c) = p_regulator(Gpr, 3)
    plt.subplot(2, 2, 1)
    plt.plot(t, c, color="orange")
    # Kp=30
    (CLTF_P, t, c) = p_regulator(Gpr, 30)
    plt.subplot(2, 2, 2)
    plt.plot(t, c, color="red")

    if plot:
        plt.show()

    # PI regelaar
    # Kp=3 Ti=-1
    (CLTF_PI, t, c) = pi_regulator(Gpr, 3, -1)
    plt.subplot(2, 2, 3)
    plt.plot(t, c, color="green")
    # Kp=30 Ti=-1
    (CLTF_PI, t, c) = pi_regulator(Gpr, 30, -1)
    plt.subplot(2, 2, 4)
    plt.plot(t, c, color="blue")

    if plot:
        plt.show()

    return (CLTF_P, CLTF_PI)

 # Vraag 4: Vergelijk de regelaars van hierboven op rise, settling tijden en doorschot. Bereken ook de bandbreedte


def question4(CLTF_P, CLTF_PI, plot=True):
    print(spacer+"Question 4"+spacer)
    # STEP RESPONSES
    plt.figure("Q4 P / PI - Step response")
    t, c = ct.step_response(CLTF_P)
    plt.plot(t, c, color="red")
    t, c = ct.step_response(CLTF_PI)
    plt.plot(t, c, color="blue")
    # STEPINFO
    cltf_p_stepinfo = cm.stepinfo(CLTF_P)
    cltf_pi_stepinfo = cm.stepinfo(CLTF_PI)
    df1 = pd.DataFrame.from_dict(cltf_p_stepinfo, orient='index')
    df2 = pd.DataFrame.from_dict(cltf_pi_stepinfo, orient='index')
    df = pd.concat([df1.T, df2.T], keys=["P regulator", "PI Regulator"])
    print(df)
    df.to_excel("q4.xlsx")

    # BODE PLOT
    plt.figure("Q4 P / PI - Bode")
    plt.subplot(2, 1, 1)
    (mag, phase, omega) = ct.bode_plot(CLTF_P, color="red")
    df1 = pd.DataFrame.from_records((ct.mag2db(mag), phase, omega))
    df1.to_excel("bb1.xlsx")

    plt.subplot(2, 1, 2)
    (mag, phase, omega) = ct.bode_plot(CLTF_PI, color="blue")
    df1 = pd.DataFrame.from_records((ct.mag2db(mag), phase, omega))
    df1.to_excel("bb2.xlsx")

    if plot:
        plt.show()


if __name__ == "__main__":
    s = ct.tf('s')
    plotting = False

    Gpr = (s+0.5)/((s+1)*(s-1))
    H = 1  # ideale sensor
    OLTF = Gpr*H

    # Q1
    OLTF_1 = question1(Gpr, OLTF, plot=plotting)

    # Q2
    OLTF_2 = question2(OLTF, plot=plotting)

    # Q3
    (CLTF_3_P, CLTF_3_PI) = question3(Gpr, H, plot=plotting)

    # Q4
    question4(CLTF_3_P, CLTF_3_PI, plot=plotting)

    # Plotting
    if not plotting:
        plt.show()
