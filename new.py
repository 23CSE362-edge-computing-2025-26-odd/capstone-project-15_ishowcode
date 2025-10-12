import random
import time
import math

# ------------------ INTERSECTION AGENT ------------------
class IntersectionAgent:
    def __init__(self, id, neighbors):
        self.id = id
        self.neighbors = neighbors  # connected intersections
        self.local_traffic = random.randint(10, 100)
        self.travel_time = {n: random.randint(2, 8) for n in neighbors}
        self.pheromone = {n: 1.0 for n in neighbors}  # initial pheromone level
    
    def process_local_data(self):
        # Simulate real-time traffic variation
        change = random.randint(-10, 10)
        self.local_traffic = max(5, min(100, self.local_traffic + change))
        return self.local_traffic
    
    def share_with_neighbors(self, network):
        for n in self.neighbors:
            network[n].receive_neighbor_data(self.id, self.local_traffic)
    
    def receive_neighbor_data(self, nid, traffic):
        # Update pheromone (low traffic → higher pheromone)
        self.pheromone[nid] = max(0.1, 1 / (traffic + 1))
    
    def send_to_central(self):
        return {
            "id": self.id,
            "traffic": self.local_traffic,
            "travel_time": self.travel_time
        }
    
    def apply_global_guidance(self, adjustment):
        for n in self.pheromone:
            self.pheromone[n] = max(0.1, self.pheromone[n] + adjustment)
    
    def __repr__(self):
        return f"Agent({self.id})"

# ------------------ CENTRAL CONTROLLER ------------------
class CentralController:
    def __init__(self):
        self.global_data = {}
        self.history = []
    
    def receive_data(self, data_list):
        self.global_data = {d["id"]: d["traffic"] for d in data_list}
        self.history.append(self.global_data)
    
    def analyze_patterns(self):
        avg = sum(self.global_data.values()) / len(self.global_data)
        print(f"\n[Central Node] Global average congestion: {avg:.2f}")
        return avg
    
    def send_guidance(self, agents, avg):
        for a in agents:
            if a.local_traffic > avg:
                a.apply_global_guidance(-0.1)
            else:
                a.apply_global_guidance(0.1)
    
    def find_best_dynamic_route(self, start, end, network):
        visited = set([start])
        current = start
        route = [current]
        total_cost = 0

        while current != end:
            neighbors = network[current].neighbors
            choices = [n for n in neighbors if n not in visited]
            if not choices:
                break

            # Combine pheromone, traffic, and travel time
            probs = []
            for n in choices:
                pher = network[current].pheromone[n]
                traffic = network[n].local_traffic
                ttime = network[current].travel_time[n]
                # Weighted fitness score: pheromone vs congestion vs time
                score = pher / ((traffic + 1) * (ttime + 0.1))
                probs.append(score)

            total = sum(probs)
            probs = [p / total for p in probs]
            next_node = random.choices(choices, weights=probs, k=1)[0]

            total_cost += network[next_node].local_traffic + network[current].travel_time[next_node]
            visited.add(next_node)
            route.append(next_node)
            current = next_node

        return route, total_cost

# ------------------ SIMULATION LOOP ------------------
if __name__ == "__main__":
    network = {
        1: IntersectionAgent(1, [2, 3]),
        2: IntersectionAgent(2, [1, 3, 4]),
        3: IntersectionAgent(3, [1, 2, 4]),
        4: IntersectionAgent(4, [2, 3, 5]),
        5: IntersectionAgent(5, [4])
    }

    central = CentralController()
    start, end = 1, 5

    print("🚑 Starting Real-Time Fog Network Simulation...\n")
    for t in range(1, 6):  # simulate 5 time intervals
        print(f"\n⏱️ Time step {t} ---------------------------")
        
        # Local sensing & neighbor coordination
        for agent in network.values():
            agent.process_local_data()
            agent.share_with_neighbors(network)

        # Fog → Central communication
        all_data = [a.send_to_central() for a in network.values()]
        central.receive_data(all_data)

        # Central learning and feedback
        avg_congestion = central.analyze_patterns()
        central.send_guidance(list(network.values()), avg_congestion)

        # Central computes best current route
        route, cost = central.find_best_dynamic_route(start, end, network)
        print(f"🚦 Best route at t={t}: {route} | Cost: {cost:.2f}")

        # (Optional delay for realism)
        time.sleep(1)

    print("\n✅ Simulation complete.")
