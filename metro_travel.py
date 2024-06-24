import tkinter as tk
import heapq
import networkx as nx
import matplotlib.pyplot as plt

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
        flights =
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



class MetroTravelGUI:
    def __init__(self, master, destinos_file, vuelos_file):
        self.master = master
        master.title("Metro Travel")

        self.metro_travel = MetroTravel(destinos_file, vuelos_file)

        # Crear widgets
        self.label_origen = tk.Label(master, text="Aeropuerto de origen:")
        self.entry_origen = tk.Entry(master)
        self.label_destino = tk.Label(master, text="Aeropuerto de destino:")
        self.entry_destino = tk.Entry(master)
        self.label_visa = tk.Label(master, text="¿Tiene visa?:")
        self.var_visa = tk.StringVar()
        self.radio_visa_si = tk.Radiobutton(master, text="Sí", variable=self.var_visa, value="si")
        self.radio_visa_no = tk.Radiobutton(master, text="No", variable=self.var_visa, value="no")
        self.label_optimizar = tk.Label(master, text="Optimizar por:")
        self.var_optimizar = tk.StringVar()
        self.radio_optimizar_cost = tk.Radiobutton(master, text="Costo", variable=self.var_optimizar, value="cost")
        self.radio_optimizar_stops = tk.Radiobutton(master, text="Escalas", variable=self.var_optimizar, value="stops")
        self.button_buscar = tk.Button(master, text="Buscar ruta", command=self.find_route)
        self.text_resultado = tk.Text(master, height=5, width=50)

        # Posicionar widgets
        self.label_origen.grid(row=0, column=0)
        self.entry_origen.grid(row=0, column=1)
        self.label_destino.grid(row=1, column=0)
        self.entry_destino.grid(row=1, column=1)
        self.label_visa.grid(row=2, column=0)
        self.radio_visa_si.grid(row=2, column=1)
        self.radio_visa_no.grid(row=2, column=2)
        self.label_optimizar.grid(row=3, column=0)
        self.radio_optimizar_cost.grid(row=3, column=1)
        self.radio_optimizar_stops.grid(row=3, column=2)
        self.button_buscar.grid(row=4, column=0, columnspan=3)
        self.text_resultado.grid(row=5, column=0, columnspan=3)

    def find_route(self):
        origen = self.entry_origen.get().strip().upper()
        destino = self.entry_destino.get().strip().upper()
        tiene_visa = self.var_visa.get().strip().lower() == 'si'
        optimizar_por = self.var_optimizar.get().strip().lower()

        resultado = self.metro_travel.get_route(origen, destino, tiene_visa, optimizar_por)

        self.text_resultado.delete("1.0", tk.END)
        self.text_resultado.insert(tk.END, str(resultado))

        if isinstance(resultado, tuple):
            costo, ruta = resultado
            self.visualize_route(origen, destino, ruta)
        else:
            self.clear_plot()

    def visualize_route(self, origen, destino, ruta):
        G = nx.Graph()
        for airport in self.metro_travel.airports:
            G.add_node(airport)
        for (o, d), _ in self.metro_travel.flights.items():
            G.add_edge(o, d)

        pos = nx.spring_layout(G)
        plt.figure(figsize=(8, 6))
        nx.draw_networkx_nodes(G, pos, node_color='lightblue')
        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_labels(G, pos)

        ruta_edges = [(ruta[i], ruta[i+1]) for i in range(len(ruta)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=ruta_edges, edge_color='red', width=2)

        plt.title(f"Ruta de {origen} a {destino}")
        plt.show()

    def clear_plot(self):
        plt.figure(figsize=(8, 6))
        plt.clf()
        plt.close()

if __name__ == "__main__":
    destinos_file = 'destinos.txt'
    vuelos_file = 'vuelos.txt'

    root = tk.Tk()
    metro_travel_gui = MetroTravelGUI(root, destinos_file, vuelos_file)
    root.mainloop()