import heapq

class MetroTravel:
    def __init__(self, destinos_file, vuelos_file):
        self.airports = self.load_airports(destinos_file)
        self.flights = self.load_flights(vuelos_file)
        self.adj_list = self.create_adjacency_list()
    
    def load_airports(self, file_path):
        airports = {}
        with open(file_path, 'r') as file:
            for line in file:
                code, name, visa = line.strip().split(',')
                airports[code] = (name, visa.lower() == 'si')
        return airports
    
    def load_flights(self, file_path):
        flights = {}
        with open(file_path, 'r') as file:
            for line in file:
                origin, destination, price = line.strip().split(',')
                price = float(price)
                flights[(origin, destination)] = price
                flights[(destination, origin)] = price
        return flights

    def create_adjacency_list(self):
        adj_list = {airport: [] for airport in self.airports}
        for (origin, destination), price in self.flights.items():
            adj_list[origin].append((destination, price))
        return adj_list

    def find_cheapest_route(self, start, end, has_visa):
        if not has_visa and self.airports[start][1]:
            return "No puedes empezar en un destino que requiere visa sin tenerla."
        
        pq = [(0, start, [])]  # (cost, node, path)
        visited = set()
        
        while pq:
            cost, node, path = heapq.heappop(pq)
            if node in visited:
                continue
            visited.add(node)
            path = path + [node]
            
            if node == end:
                return cost, path
            
            for neighbor, price in self.adj_list[node]:
                if has_visa or not self.airports[neighbor][1]:
                    heapq.heappush(pq, (cost + price, neighbor, path))
        
        return "No hay ruta disponible."

    def find_shortest_route(self, start, end, has_visa):
        if not has_visa and self.airports[start][1]:
            return "No puedes empezar en un destino que requiere visa sin tenerla."
        
        pq = [(0, start, [])]  # (stops, node, path)
        visited = set()
        
        while pq:
            stops, node, path = heapq.heappop(pq)
            if node in visited:
                continue
            visited.add(node)
            path = path + [node]
            
            if node == end:
                return stops, path
            
            for neighbor, _ in self.adj_list[node]:
                if has_visa or not self.airports[neighbor][1]:
                    heapq.heappush(pq, (stops + 1, neighbor, path))
        
        return "No hay ruta disponible."

    def get_route(self, start, end, has_visa, optimize_for):
        if optimize_for == 'cost':
            return self.find_cheapest_route(start, end, has_visa)
        elif optimize_for == 'stops':
            return self.find_shortest_route(start, end, has_visa)
        else:
            return "Opción no válida. Elija 'cost' o 'stops'."

# Ejemplo de uso
if __name__ == "__main__":
    destinos_file = 'destinos.txt'
    vuelos_file = 'vuelos.txt'
    
    metro_travel = MetroTravel(destinos_file, vuelos_file)
    
    origen = input("Ingrese el código del aeropuerto de origen: ").strip().upper()
    destino = input("Ingrese el código del aeropuerto de destino: ").strip().upper()
    tiene_visa = input("¿El pasajero tiene visa? (si/no): ").strip().lower() == 'si'
    optimizar_por = input("¿Desea optimizar por costo o escalas? (cost/stops): ").strip().lower()
    
    resultado = metro_travel.get_route(origen, destino, tiene_visa, optimizar_por)
    print("Resultado:", resultado)
