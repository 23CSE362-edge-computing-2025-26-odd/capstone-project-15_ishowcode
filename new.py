# import random
# import time
# import math

# # ------------------ INTERSECTION AGENT ------------------
# class IntersectionAgent:
#     def __init__(self, id, neighbors):
#         self.id = id
#         self.neighbors = neighbors  # connected intersections
#         self.local_traffic = random.randint(10, 100)
#         self.travel_time = {n: random.randint(2, 8) for n in neighbors}
#         self.pheromone = {n: 1.0 for n in neighbors}  # initial pheromone level
    
#     def process_local_data(self):
#         # Simulate real-time traffic variation
#         change = random.randint(-10, 10)
#         self.local_traffic = max(5, min(100, self.local_traffic + change))
#         return self.local_traffic
    
#     def share_with_neighbors(self, network):
#         for n in self.neighbors:
#             network[n].receive_neighbor_data(self.id, self.local_traffic)
    
#     def receive_neighbor_data(self, nid, traffic):
#         # Update pheromone (low traffic → higher pheromone)
#         self.pheromone[nid] = max(0.1, 1 / (traffic + 1))
    
#     def send_to_central(self):
#         return {
#             "id": self.id,
#             "traffic": self.local_traffic,
#             "travel_time": self.travel_time
#         }
    
#     def apply_global_guidance(self, adjustment):
#         for n in self.pheromone:
#             self.pheromone[n] = max(0.1, self.pheromone[n] + adjustment)
    
#     def __repr__(self):
#         return f"Agent({self.id})"

# # ------------------ CENTRAL CONTROLLER ------------------
# class CentralController:
#     def __init__(self):
#         self.global_data = {}
#         self.history = []
    
#     def receive_data(self, data_list):
#         self.global_data = {d["id"]: d["traffic"] for d in data_list}
#         self.history.append(self.global_data)
    
#     def analyze_patterns(self):
#         avg = sum(self.global_data.values()) / len(self.global_data)
#         print(f"\n[Central Node] Global average congestion: {avg:.2f}")
#         return avg
    
#     def send_guidance(self, agents, avg):
#         for a in agents:
#             if a.local_traffic > avg:
#                 a.apply_global_guidance(-0.1)
#             else:
#                 a.apply_global_guidance(0.1)
    
#     def find_best_dynamic_route(self, start, end, network):
#         visited = set([start])
#         current = start
#         route = [current]
#         total_cost = 0

#         while current != end:
#             neighbors = network[current].neighbors
#             choices = [n for n in neighbors if n not in visited]
#             if not choices:
#                 break

#             # Combine pheromone, traffic, and travel time
#             probs = []
#             for n in choices:
#                 pher = network[current].pheromone[n]
#                 traffic = network[n].local_traffic
#                 ttime = network[current].travel_time[n]
#                 # Weighted fitness score: pheromone vs congestion vs time
#                 score = pher / ((traffic + 1) * (ttime + 0.1))
#                 probs.append(score)

#             total = sum(probs)
#             probs = [p / total for p in probs]
#             next_node = random.choices(choices, weights=probs, k=1)[0]

#             total_cost += network[next_node].local_traffic + network[current].travel_time[next_node]
#             visited.add(next_node)
#             route.append(next_node)
#             current = next_node

#         return route, total_cost

# # ------------------ SIMULATION LOOP ------------------
# if __name__ == "__main__":
#     network = {
#         1: IntersectionAgent(1, [2, 3]),
#         2: IntersectionAgent(2, [1, 3, 4]),
#         3: IntersectionAgent(3, [1, 2, 4]),
#         4: IntersectionAgent(4, [2, 3, 5]),
#         5: IntersectionAgent(5, [4])
#     }

#     central = CentralController()
#     start, end = 1, 5

#     print("🚑 Starting Real-Time Fog Network Simulation...\n")
#     for t in range(1, 6):  # simulate 5 time intervals
#         print(f"\n⏱️ Time step {t} ---------------------------")
        
#         # Local sensing & neighbor coordination
#         for agent in network.values():
#             agent.process_local_data()
#             agent.share_with_neighbors(network)

#         # Fog → Central communication
#         all_data = [a.send_to_central() for a in network.values()]
#         central.receive_data(all_data)

#         # Central learning and feedback
#         avg_congestion = central.analyze_patterns()
#         central.send_guidance(list(network.values()), avg_congestion)

#         # Central computes best current route
#         route, cost = central.find_best_dynamic_route(start, end, network)
#         print(f"🚦 Best route at t={t}: {route} | Cost: {cost:.2f}")

#         # (Optional delay for realism)
#         time.sleep(1)

#     print("\n✅ Simulation complete.")


# import random
# import matplotlib.pyplot as plt

# # ------------------ INTERSECTION AGENT ------------------
# class IntersectionAgent:
#     def __init__(self, id, neighbors):
#         self.id = id
#         self.neighbors = neighbors
#         self.local_traffic = random.randint(10, 100)
#         self.travel_time = {n: random.randint(2, 8) for n in neighbors}
#         self.pheromone = {n: 1.0 for n in neighbors}
#         self.emergency_present = False

#     def process_local_data(self):
#         change = random.randint(-10, 10)
#         self.local_traffic = max(5, min(100, self.local_traffic + change))
#         self.emergency_present = random.random() < 0.1
#         return self.local_traffic, self.emergency_present

#     def share_with_neighbors(self, network):
#         for n in self.neighbors:
#             network[n].receive_neighbor_data(self.id, self.local_traffic, self.emergency_present)

#     def receive_neighbor_data(self, nid, traffic, emergency):
#         base_pheromone = max(0.1, 1 / (traffic + 1))
#         if emergency:
#             base_pheromone *= 2
#         self.pheromone[nid] = base_pheromone

#     def send_to_central(self):
#         return {
#             "id": self.id,
#             "traffic": self.local_traffic,
#             "emergency": self.emergency_present,
#             "travel_time": self.travel_time.copy()
#         }

#     def apply_global_guidance(self, adjustment):
#         for n in self.pheromone:
#             self.pheromone[n] = max(0.1, self.pheromone[n] + adjustment)

# # ------------------ CENTRAL SERVER ------------------
# class CentralController:
#     def __init__(self):
#         self.global_data = {}
#         self.history = []

#     def receive_data(self, data_list):
#         self.global_data = {d["id"]: {"traffic": d["traffic"], "emergency": d["emergency"]} for d in data_list}
#         self.history.append(self.global_data.copy())

#     def analyze_patterns(self):
#         avg = sum(d["traffic"] for d in self.global_data.values()) / len(self.global_data)
#         return avg

#     def send_guidance(self, agents):
#         avg_traffic = self.analyze_patterns()
#         for a in agents:
#             if a.local_traffic > avg_traffic:
#                 a.apply_global_guidance(-0.1)
#             else:
#                 a.apply_global_guidance(0.1)

# # ------------------ DYNAMIC ROUTING ------------------
# def find_best_route(start, end, network, alpha=1.0, beta=2.0):
#     visited = set([start])
#     current = start
#     route = [current]
#     total_cost = 0

#     while current != end:
#         neighbors = network[current].neighbors
#         choices = [n for n in neighbors if n not in visited]
#         if not choices:
#             break

#         scores = []
#         for n in choices:
#             pher = network[current].pheromone[n] ** alpha
#             traffic = network[n].local_traffic + 1
#             ttime = network[current].travel_time[n] + 0.1
#             score = pher / (traffic ** beta * ttime)
#             if network[n].emergency_present:
#                 score *= 5
#             scores.append(score)

#         total = sum(scores)
#         probs = [s / total for s in scores]
#         next_node = random.choices(choices, weights=probs, k=1)[0]

#         total_cost += network[next_node].local_traffic + network[current].travel_time[next_node]
#         visited.add(next_node)
#         route.append(next_node)
#         current = next_node

#     return route, total_cost

# # ------------------ SIMULATION ------------------
# if __name__ == "__main__":
#     network = {
#         1: IntersectionAgent(1, [2, 3]),
#         2: IntersectionAgent(2, [1, 3, 4]),
#         3: IntersectionAgent(3, [1, 2, 4]),
#         4: IntersectionAgent(4, [2, 3, 5]),
#         5: IntersectionAgent(5, [4])
#     }

#     central = CentralController()
#     start, end = 1, 5
#     results = []

#     for t in range(1, 11):
#         # Edge/Fog updates
#         for agent in network.values():
#             agent.process_local_data()
#             agent.share_with_neighbors(network)

#         # Fog → Cloud communication
#         all_data = [a.send_to_central() for a in network.values()]
#         central.receive_data(all_data)

#         # Cloud guidance
#         central.send_guidance(list(network.values()))

#         # Compute best route
#         route, cost = find_best_route(start, end, network)
#         avg_traffic = central.analyze_patterns()

#         # Save timestep results
#         pheromone_snapshot = {a.id: a.pheromone.copy() for a in network.values()}
#         results.append({
#             "time": t,
#             "avg_traffic": avg_traffic,
#             "best_route": route,
#             "route_cost": cost,
#             "pheromones": pheromone_snapshot
#         })

#         # Print real-time results
#         print(f"Timestep {t}: Best Route={route}, Cost={cost:.2f}, Avg Traffic={avg_traffic:.2f}")

#     # ------------------ VISUALIZATION ------------------
#     # Plot Best Route Cost over Time
#     plt.figure(figsize=(10,5))
#     plt.plot([r["time"] for r in results], [r["route_cost"] for r in results], marker='o')
#     plt.title("Best Route Cost Over Time")
#     plt.xlabel("Timestep")
#     plt.ylabel("Route Cost")
#     plt.grid(True)
#     plt.show()

#     # Plot Pheromone Evolution for Each Node
#     plt.figure(figsize=(12,6))
#     for node in network:
#         for neighbor in network[node].neighbors:
#             pher_vals = [r["pheromones"][node][neighbor] for r in results]
#             plt.plot([r["time"] for r in results], pher_vals, marker='o', label=f"Pheromone {node}->{neighbor}")
#     plt.title("Pheromone Evolution Over Time")
#     plt.xlabel("Timestep")
#     plt.ylabel("Pheromone Value")
#     plt.legend()
#     plt.grid(True)
#     plt.show()

import random
import matplotlib.pyplot as plt

# ------------------ INTERSECTION AGENT (FOG NODE) ------------------
class IntersectionAgent:
    def __init__(self, id, neighbors):
        self.id = id
        self.neighbors = neighbors
        self.local_traffic = random.randint(10, 100)
        self.travel_time = {n: random.randint(2, 8) for n in neighbors}
        self.pheromone = {n: 1.0 for n in neighbors}
        self.emergency_present = False
        self.green_signal = False

    def process_local_data(self):
        # Random traffic variation
        self.local_traffic = max(5, min(100, self.local_traffic + random.randint(-10, 10)))
        # Random emergency vehicle presence
        self.emergency_present = random.random() < 0.1
        return self.local_traffic, self.emergency_present

    def share_with_neighbors(self, network):
        for n in self.neighbors:
            network[n].receive_neighbor_data(self.id, self.local_traffic, self.emergency_present)

    def receive_neighbor_data(self, nid, traffic, emergency):
        base_pheromone = max(0.1, 1 / (traffic + 1))
        if emergency:
            base_pheromone *= 3  # Prioritize emergency
        self.pheromone[nid] = base_pheromone

    def update_signal(self, incoming_route):
        # Turn green if emergency is approaching
        self.green_signal = self.emergency_present or (incoming_route and incoming_route[0] == self.id)

    def send_to_central(self):
        return {
            "id": self.id,
            "traffic": self.local_traffic,
            "emergency": self.emergency_present,
            "travel_time": self.travel_time.copy()
        }

    def apply_global_guidance(self, adjustment):
        for n in self.pheromone:
            self.pheromone[n] = max(0.1, self.pheromone[n] + adjustment)

# ------------------ CENTRAL SERVER ------------------
class CentralController:
    def __init__(self):
        self.global_data = {}
        self.history = []

    def receive_data(self, data_list):
        self.global_data = {d["id"]: {"traffic": d["traffic"], "emergency": d["emergency"]} for d in data_list}
        self.history.append(self.global_data.copy())

    def analyze_patterns(self):
        avg = sum(d["traffic"] for d in self.global_data.values()) / len(self.global_data)
        return avg

    def send_guidance(self, agents):
        avg_traffic = self.analyze_patterns()
        for a in agents:
            if a.local_traffic > avg_traffic:
                a.apply_global_guidance(-0.1)
            else:
                a.apply_global_guidance(0.1)

# ------------------ DYNAMIC ROUTING WITH ACO ------------------
def find_best_route(start, end, network, alpha=1.0, beta=2.0):
    visited = set([start])
    current = start
    route = [current]
    total_cost = 0

    while current != end:
        neighbors = network[current].neighbors
        choices = [n for n in neighbors if n not in visited]
        if not choices:
            break

        scores = []
        for n in choices:
            pher = network[current].pheromone[n] ** alpha
            traffic = network[n].local_traffic + 1
            ttime = network[current].travel_time[n] + 0.1
            score = pher / (traffic ** beta * ttime)
            if network[n].emergency_present:
                score *= 5
            scores.append(score)

        total = sum(scores)
        probs = [s / total for s in scores]
        next_node = random.choices(choices, weights=probs, k=1)[0]

        total_cost += network[next_node].local_traffic + network[current].travel_time[next_node]
        visited.add(next_node)
        route.append(next_node)
        current = next_node

    return route, total_cost

# ------------------ SIMULATION ------------------
if __name__ == "__main__":
    # Define intersections and neighbors
    network = {
        1: IntersectionAgent(1, [2, 3]),
        2: IntersectionAgent(2, [1, 3, 4]),
        3: IntersectionAgent(3, [1, 2, 4]),
        4: IntersectionAgent(4, [2, 3, 5]),
        5: IntersectionAgent(5, [4])
    }

    central = CentralController()
    start, end = 1, 5
    results = []

    for t in range(1, 11):
        # Edge/Fog updates
        for agent in network.values():
            agent.process_local_data()
            agent.share_with_neighbors(network)

        # Fog nodes decide signal state (green wave)
        route, _ = find_best_route(start, end, network)
        for agent in network.values():
            agent.update_signal(route)

        # Fog → Central communication
        all_data = [a.send_to_central() for a in network.values()]
        central.receive_data(all_data)

        # Central guidance
        central.send_guidance(list(network.values()))

        # Compute best route with ACO
        route, cost = find_best_route(start, end, network)
        avg_traffic = central.analyze_patterns()

        # Save timestep results
        pheromone_snapshot = {a.id: a.pheromone.copy() for a in network.values()}
        results.append({
            "time": t,
            "avg_traffic": avg_traffic,
            "best_route": route,
            "route_cost": cost,
            "pheromones": pheromone_snapshot
        })

        # Print results
        print(f"Timestep {t}: Best Route={route}, Cost={cost:.2f}, Avg Traffic={avg_traffic:.2f}")

    # ------------------ VISUALIZATION ------------------
    # Best Route Cost
    plt.figure(figsize=(10,5))
    plt.plot([r["time"] for r in results], [r["route_cost"] for r in results], marker='o')
    plt.title("Best Route Cost Over Time")
    plt.xlabel("Timestep")
    plt.ylabel("Route Cost")
    plt.grid(True)
    plt.show()

    # Pheromone Evolution
    plt.figure(figsize=(12,6))
    for node in network:
        for neighbor in network[node].neighbors:
            pher_vals = [r["pheromones"][node][neighbor] for r in results]
            plt.plot([r["time"] for r in results], pher_vals, marker='o', label=f"Pheromone {node}->{neighbor}")
    plt.title("Pheromone Evolution Over Time")
    plt.xlabel("Timestep")
    plt.ylabel("Pheromone Value")
    plt.legend()
    plt.grid(True)
    plt.show()

