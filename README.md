# Emergency Vehicle Priority Routing System 🚦🚑

This repository contains the work for our project, developed as a collaboration between students in the Edge Computing (23CSE362) and Computational Intelligence courses. We designed this system to tackle the critical problem of emergency vehicle (EV) delays caused by traffic congestion in urban environments, especially relevant to the complex traffic conditions we often see in India.

## Our Core Idea

We aimed to build a system that's more than just reactive – we wanted something *predictive and adaptive*. Our solution is a hybrid approach that combines the strengths of our respective courses:

1.  *The Instant Edge Reflex:* Using Edge Computing principles, our system reacts immediately at the intersection. When an EV is detected, it instantly clears a path.
2.  *The Intelligent Fog Swarm:* Using Computational Intelligence concepts, our system coordinates across multiple intersections to find the best overall route and handle complex situations like multiple emergencies.

Our goal was to create something *fast, intelligent, and robust*.

## How We Designed It

Our system, "Guardian Flow," operates in distinct layers and stages:

1.  *Edge Detection & Action:*
    * At each intersection (in our simulation), we use an AI camera model (*YOLOv8*) to visually detect an approaching EV.
    * Simultaneously, a simulated Road-Side Unit (*RSU) reads a priority code (like "Code Black") which we imagine the driver sets via an On-Board Unit (OBU*).
    * Our Edge component immediately fuses this info and triggers the *"Green Corridor" model*: it stops conflicting traffic (RED lights) and opens the EV's entire lane (SOLID GREEN light).

2.  *Fog Coordination & Scheduling:*
    * The Edge layer alerts our *Fog Layer*, which contains a decentralized swarm of intelligent agents (one for each intersection).
    * These agents maintain a real-time map of traffic congestion.
    * The swarm performs *Task Scheduling* (our core challenge): it uses the priority codes to decide which EV goes first if multiple requests conflict.
    * It then calculates the optimal (least-congested) path using a pathfinding algorithm.
    * Finally, it coordinates a *"Green Wave"* by commanding the sequence of green lights along the chosen route.

## Our Implementation: A Virtual Prototype

To prove our concept, we built a virtual prototype:

* *The World:* We used *SUMO* to simulate a 5-junction city environment with traffic.
* *The Brain:* We wrote the control logic and swarm intelligence using *Python*.
* *The Connection:* We used the *TraCI* library to allow our Python script to interact with and control the SUMO simulation in real-time.

## The Core Challenge We Addressed

The central problem we focused on solving was *Priority Task Scheduling*. Our Fog Swarm is specifically designed to intelligently manage and de-conflict situations where multiple high-priority EVs might need the same intersection simultaneously, using the driver-set priority codes to make fair and efficient decisions.

## Running Our Simulation

*(You would add specific instructions here on how to set up and run your main.py script with SUMO)*

```bash

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/WzUeh8r0)
