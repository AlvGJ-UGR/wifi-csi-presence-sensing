# 01 — Maxwell's Equations and Electromagnetic Wave Propagation

> **Theory Series**  
> WiFi CSI Presence Sensing  
> Chapter 1 — Electromagnetic Foundations

---

# 1. Why start with Maxwell?

Every wireless communication system—whether WiFi, Bluetooth, 5G, radar or satellite communications—is ultimately governed by **Maxwell's Equations**.

Although this project analyses **Channel State Information (CSI)** produced by WiFi devices, CSI is nothing more than a measurement of how an **electromagnetic wave** has propagated through the environment.

Therefore, understanding CSI requires first understanding the physics of electromagnetic fields.

The complete causal chain is

```
Maxwell's Equations
        ↓
Electromagnetic Waves
        ↓
Propagation
        ↓
Multipath
        ↓
Wireless Channel
        ↓
OFDM Channel Estimation
        ↓
Channel State Information (CSI)
        ↓
Presence Detection
```

Nothing in this project exists outside this chain.

---

# 2. Electric and Magnetic Fields

An electromagnetic wave consists of two coupled vector fields.

## Electric Field

The electric field

\[
\mathbf{E}(\mathbf{r},t)
\]

represents the force experienced by a unit positive charge.

Its SI unit is

\[
V/m
\]

It describes how electric charges interact.

---

## Magnetic Field

The magnetic field

\[
\mathbf{H}(\mathbf{r},t)
\]

describes magnetic forces produced by moving charges.

Its SI unit is

\[
A/m
\]

---

These two fields cannot exist independently during wave propagation.

A changing electric field creates a magnetic field.

A changing magnetic field creates an electric field.

This mutual interaction allows electromagnetic waves to propagate through space.

---

# 3. Maxwell's Equations

In differential form, Maxwell's equations are

## Gauss's Law

\[
\nabla\cdot\mathbf E
=
\frac{\rho}{\varepsilon}
\]

Electric charges generate electric fields.

---

## Gauss's Law for Magnetism

\[
\nabla\cdot\mathbf B
=
0
\]

Magnetic monopoles do not exist.

Magnetic field lines always form closed loops.

---

## Faraday's Law

\[
\nabla\times\mathbf E
=
-
\frac{\partial\mathbf B}{\partial t}
\]

A changing magnetic field produces an electric field.

This principle is the basis of generators and transformers.

---

## Ampère-Maxwell Law

\[
\nabla\times\mathbf H
=
\mathbf J
+
\frac{\partial\mathbf D}{\partial t}
\]

A changing electric field generates a magnetic field.

Without Maxwell's displacement current term,

\[
\frac{\partial\mathbf D}{\partial t},
\]

electromagnetic waves could not exist.

---

# 4. Constitutive Relations

Inside a material,

\[
\mathbf D
=
\varepsilon\mathbf E
\]

\[
\mathbf B
=
\mu\mathbf H
\]

where

- ε is the permittivity
- μ is the permeability

These two parameters determine how fast electromagnetic waves travel inside the medium.

---

# 5. Wave Equation

Combining Maxwell's equations produces the electromagnetic wave equation.

For the electric field,

\[
\nabla^2\mathbf E
-
\mu\varepsilon
\frac{\partial^2\mathbf E}{\partial t^2}
=
0
\]

Similarly,

\[
\nabla^2\mathbf H
-
\mu\varepsilon
\frac{\partial^2\mathbf H}{\partial t^2}
=
0
\]

These equations describe every radio signal used in modern telecommunications.

---

# 6. Speed of Propagation

The propagation velocity is

\[
v
=
\frac1{\sqrt{\mu\varepsilon}}
\]

In vacuum,

\[
v=c
=
299\,792\,458\ m/s
\]

Inside walls, furniture or other materials,

\[
v<c
\]

because

\[
\varepsilon_r>1
\]

This is one reason why walls affect WiFi propagation.

---

# 7. Plane Waves

A monochromatic plane wave travelling along the x-axis can be written as

\[
E(x,t)
=
E_0
\cos(kx-\omega t)
\]

where

- \(E_0\) is the amplitude
- \(k\) is the wave number
- \(\omega\) is the angular frequency

Alternatively,

\[
E(x,t)
=
E_0
e^{j(kx-\omega t)}
\]

using complex notation.

Complex exponentials greatly simplify communication system analysis.

Only the real part represents the physical field.

---

# 8. Wavelength

The wavelength is

\[
\lambda
=
\frac{c}{f}
\]

For WiFi at

\[
2.4\ GHz
\]

\[
\lambda
=
\frac{3\times10^8}
{2.4\times10^9}
\approx
0.125\ m
\]

approximately

**12.5 cm**.

This number appears constantly throughout RF engineering.

---

# 9. Polarisation

Electromagnetic waves have polarisation.

Typical antenna polarisations include

- Vertical
- Horizontal
- Circular

Maximum received power occurs when transmitter and receiver share the same polarisation.

Polarisation mismatch reduces received power.

---

# 10. Electromagnetic Energy

The instantaneous power flow is described by the **Poynting Vector**

\[
\mathbf S
=
\mathbf E
\times
\mathbf H
\]

Its direction indicates the direction of energy propagation.

Its magnitude represents power density

\[
W/m^2
\]

---

# 11. Electromagnetic Interaction with Objects

When an electromagnetic wave encounters an obstacle, four phenomena occur simultaneously.

## Reflection

Part of the energy bounces off the surface.

Examples

- walls
- windows
- metal objects

---

## Refraction

Part of the wave changes direction after entering another material.

---

## Diffraction

The wave bends around edges and corners.

---

## Scattering

Rough surfaces redistribute energy into multiple directions.

Examples

- people
- furniture
- trees
- clothing

---

# 12. Human Body as a Scatterer

The human body contains mostly water.

At

\[
2.4\ GHz
\]

water strongly interacts with electromagnetic fields.

A person therefore

- absorbs energy,
- reflects energy,
- scatters energy.

Consequently,

the wireless channel changes.

Importantly,

the ESP32 never "detects a person".

It measures only the consequences of that person's interaction with the electromagnetic field.

---

# 13. From Physics to Telecommunications

Suppose an antenna transmits

\[
E_t
\]

The receiver never observes only

\[
E_t.
\]

Instead,

it receives

\[
E_r
=
\sum_{i=1}^{N}
a_i
e^{-j2\pi f\tau_i}
\]

where

- each path has amplitude

\[
a_i
\]

- each path has delay

\[
\tau_i
\]

This equation introduces the concept of **multipath propagation**.

It is the mathematical bridge between Maxwell's equations and wireless communication theory.

The next chapter studies this equation in detail.

---

# 14. Relation to This Project

Everything measured by CSI originates here.

A moving person changes

- reflection coefficients,
- propagation delays,
- scattering,
- attenuation,
- phase.

Those changes modify the wireless channel.

Later,

the WiFi receiver estimates that channel using OFDM pilots.

The estimated channel becomes

**Channel State Information (CSI).**

Therefore,

the project does **not** measure people.

It measures the electromagnetic consequences of people interacting with the environment.

---

# Key Takeaways

- Maxwell's equations govern every wireless communication system.
- WiFi signals are electromagnetic waves.
- Electromagnetic waves interact continuously with the environment.
- Reflection, diffraction and scattering create multiple propagation paths.
- Human bodies modify these propagation paths.
- These modifications alter the wireless channel.
- CSI is an estimate of that channel.

---

# What's Next?

The next chapter introduces the mathematical model of the wireless channel itself.

We will derive

\[
h(t,\tau)
\]

the **time-varying impulse response**,

and show how multipath propagation transforms a simple transmitted signal into the complex wireless channel observed by the ESP32.

**Next chapter**

> **02_Wireless_Channel.md**
