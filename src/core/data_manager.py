import json
import os
from core.graph import Graph

class DataManager:
    def __init__(self, map_dir="maps"):
        self.map_dir = map_dir
        if not os.path.exists(self.map_dir):
            os.makedirs(self.map_dir)

    def save_game(self, filename, graph, actors, current_idx):
        map_data = {
            "cols": graph.cols,
            "rows": graph.rows,
            "tile_width": graph.tile_width,
            "tile_height": graph.tile_height,
            "current_idx": current_idx,
            "nodes": [],
            "actors": []
        }
        for coords, node in graph.nodes.items():
            node_info = {
                "x": node.grid_x,
                "y": node.grid_y,
                "weight": node.weight,
                "owner_name": node.owner.name if node.owner else None
            }
            map_data["nodes"].append(node_info)
        for actor in actors:
            map_data["actors"].append({
                "name": actor.name,
                "color": actor.color,
                "is_ai": actor.is_ai,
                "node_x": actor.current_node.grid_x if actor.current_node else 0,
                "node_y": actor.current_node.grid_y if actor.current_node else 0,
                "points": actor.points,
                "moves_left": actor.moves_left,
                "has_used_paid_move": actor.has_used_paid_move
            })
        filepath = os.path.join(self.map_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(map_data, f, indent=4)

    def load_game(self, filename):
        filepath = os.path.join(self.map_dir, filename)
        if not os.path.exists(filepath):
            return None, None, None, None
        with open(filepath, 'r') as f:
            data = json.load(f)
        new_graph = Graph(data["cols"], data["rows"], data["tile_width"], data["tile_height"])
        return new_graph, data.get("actors", []), data.get("current_idx", 0), data["nodes"]

    def list_maps(self):
        return [f for f in os.listdir(self.map_dir) if f.endswith('.json')]