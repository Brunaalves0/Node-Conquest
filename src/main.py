import pygame
import random
import math
from core.graph import Graph
from core.player import Player
from core.territory import TerritoryManager
from core.data_manager import DataManager
from ui.renderer import Renderer
from algorithms.a_star import AStar

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("Node Conquest")
    clock = pygame.time.Clock()
    
    renderer = Renderer(screen)
    data_manager = DataManager()
    
    state = "MENU"
    game_map = None
    actors = []
    current_idx = 0
    pathfinder = None
    territory_manager = None
    preview_path = []
    
    is_dragging = False
    last_mouse_pos = (0, 0)

    def center_camera(cols, rows):
        renderer.zoom = 1.0
        map_pixel_width = cols * 64 * (math.sqrt(3) / 2)
        map_pixel_height = rows * 64 * 0.75
        screen_w, screen_h = screen.get_size()
        renderer.camera_x = (screen_w / 2) - (map_pixel_width / 2)
        renderer.camera_y = (screen_h / 2) - (map_pixel_height / 2)

    def next_turn(idx):
        new_idx = (idx + 1) % len(actors)
        actors[new_idx].reset_moves()
        territory_manager.update()
        return new_idx

    def start_new_game(cols, rows):
        nonlocal game_map, actors, current_idx, pathfinder, territory_manager, state
        game_map = Graph(cols, rows, 64, 64)
        
        spawn_safe = {
            (0,0), (1,0), (0,1),
            (cols-1,0), (cols-2,0), (cols-1,1),
            (0,rows-1), (1,rows-1), (0,rows-2),
            (cols-1,rows-1), (cols-2,rows-1), (cols-1,rows-2)
        }
        
        for node in game_map.nodes.values():
            if (node.grid_x, node.grid_y) in spawn_safe:
                node.set_weight(1)
            else:
                node.set_weight(random.randint(1, 3))
        
        pathfinder = AStar(game_map)
        actors = [
            Player("Jogador", game_map.get_node(0, 0), color=(100, 200, 255)),
            Player("AI 1", game_map.get_node(cols-1, 0), color=(255, 100, 100), is_ai=True),
            Player("AI 2", game_map.get_node(0, rows-1), color=(100, 255, 100), is_ai=True),
            Player("AI 3", game_map.get_node(cols-1, rows-1), color=(200, 100, 255), is_ai=True)
        ]
        
        for actor in actors:
            actor.current_node.capture(actor)
            actor.points = 0
            
        territory_manager = TerritoryManager(game_map, actors)
        current_idx = 0
        center_camera(cols, rows)
        state = "GAME"

    def load_game_action():
        nonlocal game_map, actors, current_idx, pathfinder, territory_manager, state
        new_graph, actors_data, c_idx, nodes_data = data_manager.load_game("savegame.json")
        if new_graph is None:
            return
        
        new_actors = []
        actor_lookup = {}
        for adata in actors_data:
            actor = Player(adata["name"], None, tuple(adata["color"]), adata["is_ai"])
            actor.points = adata["points"]
            actor.moves_left = adata["moves_left"]
            actor.has_used_paid_move = adata["has_used_paid_move"]
            new_actors.append(actor)
            actor_lookup[actor.name] = actor
            
        for node_data in nodes_data:
            x, y = node_data["x"], node_data["y"]
            weight = node_data["weight"]
            owner_name = node_data.get("owner_name")
            node = new_graph.get_node(x, y)
            if node:
                node.set_weight(weight)
                if owner_name in actor_lookup:
                    node.owner = actor_lookup[owner_name]
                    node.color = actor_lookup[owner_name].color
                    node.move_cost = 0

        for adata in actors_data:
            actor = actor_lookup[adata["name"]]
            actor.current_node = new_graph.get_node(adata["node_x"], adata["node_y"])

        game_map = new_graph
        actors = new_actors
        current_idx = c_idx
        pathfinder = AStar(game_map)
        territory_manager = TerritoryManager(game_map, actors)
        center_camera(game_map.cols, game_map.rows)
        state = "GAME"

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            
            if state == "MENU":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if renderer.new_game_rect.collidepoint(event.pos):
                        state = "SIZE_SELECT"
                    elif renderer.load_game_rect.collidepoint(event.pos):
                        load_game_action()
                    elif renderer.info_rect.collidepoint(event.pos):
                        state = "INFO"
                        
            elif state == "SIZE_SELECT":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if renderer.btn_small.collidepoint(event.pos):
                        start_new_game(10, 10)
                    elif renderer.btn_med.collidepoint(event.pos):
                        start_new_game(15, 15)
                    elif renderer.btn_large.collidepoint(event.pos):
                        start_new_game(25, 25)
                    elif renderer.btn_back.collidepoint(event.pos):
                        state = "MENU"
            
            elif state == "GAME":
                current_actor = actors[current_idx]
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = "MENU"
                    elif event.key == pygame.K_s:
                        data_manager.save_game("savegame.json", game_map, actors, current_idx)
                
                # Pan map logic
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: # Right click
                    is_dragging = True
                    last_mouse_pos = event.pos
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                    is_dragging = False
                elif event.type == pygame.MOUSEMOTION and is_dragging:
                    dx = event.pos[0] - last_mouse_pos[0]
                    dy = event.pos[1] - last_mouse_pos[1]
                    renderer.camera_x += dx
                    renderer.camera_y += dy
                    last_mouse_pos = event.pos
                
                # Zoom logic
                if event.type == pygame.MOUSEWHEEL:
                    old_zoom = renderer.zoom
                    renderer.zoom += event.y * 0.1
                    renderer.zoom = max(0.3, min(renderer.zoom, 3.0))
                    
                    # Zoom towards mouse cursor
                    mx, my = pygame.mouse.get_pos()
                    world_x = (mx - renderer.camera_x) / old_zoom
                    world_y = (my - renderer.camera_y) / old_zoom
                    
                    renderer.camera_x = mx - (world_x * renderer.zoom)
                    renderer.camera_y = my - (world_y * renderer.zoom)

                if not current_actor.is_ai:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if renderer.end_turn_rect.collidepoint(event.pos):
                            current_idx = next_turn(current_idx)
                        else:
                            target = renderer.get_node_at_pos(game_map, event.pos)
                            if target and not current_actor.path:
                                path = pathfinder.get_path(current_actor.current_node, target, current_actor)
                                if path: current_actor.set_path(path)

            elif state == "GAME_OVER" or state == "INFO":
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    state = "MENU"

        if state == "MENU":
            renderer.render_main_menu()
        elif state == "SIZE_SELECT":
            renderer.render_size_select()
        elif state == "GAME":
            if all(node.owner is not None for node in game_map.nodes.values()):
                state = "GAME_OVER"
            else:
                current_actor = actors[current_idx]
                if not current_actor.is_ai and not current_actor.path:
                    hover = renderer.get_node_at_pos(game_map, mouse_pos)
                    preview_path = pathfinder.get_path(current_actor.current_node, hover, current_actor) if hover else []
                
                is_idle = current_actor.update()
                if current_actor.is_ai and is_idle:
                    if current_actor.moves_left > 0:
                        if not current_actor.ai_think(game_map, pathfinder):
                            current_idx = next_turn(current_idx)
                    else:
                        current_idx = next_turn(current_idx)

                renderer.clear()
                renderer.render_graph(game_map, preview_path, current_actor)
                renderer.render_actors(actors)
                renderer.render_ui(actors, current_actor)
        elif state == "GAME_OVER":
            renderer.render_game_over(actors)
        elif state == "INFO":
            renderer.clear()
            overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
            overlay.fill((30, 30, 30, 230))
            screen.blit(overlay, (0, 0))
            
            instructions = [
                ("COMO JOGAR", (255, 215, 0), 50),
                ("Conquiste o máximo de nós para ganhar pontos", (255, 255, 255), 150),
                ("Você tem 3 pontos de movimento por turno", (255, 255, 255), 200),
                ("Cada nó possui um custo (1, 2 ou 3) para entrar nele", (255, 255, 255), 250),
                ("Você pode se movimentar entre os nós da sua cor sem custo,", (255, 255, 255), 300),
                ("   mas somente se você ainda não tiver se movimentado", (255, 255, 255), 325),
                ("Se você isolar uma área que não foi capturada por outros jogadores,", (255, 255, 255), 375),
                ("      todo aquele território se torna seu automaticamente", (255, 255, 255), 400),
                ("Use o Botão Direito do Mouse para mover a câmera e a Roda do Mouse para dar zoom", (255, 215, 0), 475),
                ("Aperte 'S' durante o jogo para salvar seu progresso", (100, 200, 255), 525),
                ("Clique em qualquer lugar para voltar", (150, 150, 150), 625)
            ]
            
            for text, color, y_pos in instructions:
                font = renderer.menu_font if "COMO" in text else renderer.ui_font
                txt_surf = font.render(text, True, color)
                rect = txt_surf.get_rect(center=(640, y_pos))
                screen.blit(txt_surf, rect)

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()