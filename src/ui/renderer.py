import pygame
import math

class Renderer:
    def __init__(self, screen, camera_offset=(0, 0)):
        self.screen = screen
        self.camera_x = camera_offset[0]
        self.camera_y = camera_offset[1]
        self.font = pygame.font.SysFont("arial", 20)
        self.ui_font = pygame.font.SysFont("arial", 20)
        self.small_font = pygame.font.SysFont("arial", 16)
        self.title_font = pygame.font.SysFont("arial", 72, bold=True)
        self.menu_font = pygame.font.SysFont("arial", 32)
        self.end_turn_rect = pygame.Rect(20, 20, 160, 50)
        self.new_game_rect = pygame.Rect(0, 0, 300, 60)
        self.load_game_rect = pygame.Rect(0, 0, 300, 60)
        self.info_rect = pygame.Rect(0, 0, 300, 60)

    def clear(self):
        self.screen.fill((30, 30, 40))

    def render_main_menu(self):
        self.clear()
        screen_center = self.screen.get_rect().center
        title_surf = self.title_font.render("Node Conquest", True, (255, 230, 120))
        title_rect = title_surf.get_rect(center=(screen_center[0], screen_center[1] - 200))
        self.screen.blit(title_surf, title_rect)
        buttons = [
            (self.new_game_rect, "Novo Jogo", -50),
            (self.load_game_rect, "Carregar Jogo", 30),
            (self.info_rect, "Tutorial", 110)
        ]
        for rect, text, offset_y in buttons:
            rect.center = (screen_center[0], screen_center[1] + offset_y)
            mouse_pos = pygame.mouse.get_pos()
            color = (100, 100, 130) if rect.collidepoint(mouse_pos) else (70, 70, 90)
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 2, border_radius=10)
            btn_surf = self.menu_font.render(text, True, (255, 255, 255))
            btn_rect = btn_surf.get_rect(center=rect.center)
            self.screen.blit(btn_surf, btn_rect)

    def _get_hex_geometry(self, node):
        x, y = node.get_screen_coords()
        cx = x + node.width / 2 + self.camera_x
        cy = y + node.height / 2 + self.camera_y
        radius = node.height / 2
        w_half = radius * (math.sqrt(3) / 2)
        h_half = radius
        points = [
            (cx, cy - h_half),
            (cx + w_half, cy - h_half * 0.5),
            (cx + w_half, cy + h_half * 0.5),
            (cx, cy + h_half),
            (cx - w_half, cy + h_half * 0.5),
            (cx - w_half, cy - h_half * 0.5)
        ]
        return points, cx, cy

    def render_graph(self, graph, preview_path=None, current_actor=None):
        for node in graph.nodes.values():
            self.draw_hex(node)
        if preview_path and current_actor:
            self.draw_preview_path(preview_path, current_actor)

    def render_actors(self, actors):
        for actor in actors:
            _, cx, cy = self._get_hex_geometry(actor.current_node)
            pygame.draw.circle(self.screen, (255, 255, 255), (int(cx), int(cy)), 16)
            pygame.draw.circle(self.screen, actor.color, (int(cx), int(cy)), 12)

    def render_ui(self, actors, current_actor):
        pygame.draw.rect(self.screen, (70, 70, 90), self.end_turn_rect, border_radius=8)
        button_text = self.font.render("End Turn", True, (255, 255, 255))
        self.screen.blit(button_text, (45, 33))
        start_y = 130
        for i, actor in enumerate(actors):
            y = start_y + (i * 90)
            card_rect = pygame.Rect(20, y, 180, 75)
            bg_color = (120, 105, 40) if actor == current_actor else (55, 55, 70)
            pygame.draw.rect(self.screen, bg_color, card_rect, border_radius=10)
            name_text = self.font.render(actor.name, True, (255, 255, 255))
            self.screen.blit(name_text, (card_rect.x + 30, card_rect.y + 8))
            points_text = self.small_font.render(f"Points: {actor.points} | Moves: {actor.moves_left}/{actor.max_moves}", True, (220, 220, 220))
            self.screen.blit(points_text, (card_rect.x + 30, card_rect.y + 36))

    def draw_hex(self, node):
        points, cx, cy = self._get_hex_geometry(node)
        pygame.draw.polygon(self.screen, node.color, points)
        pygame.draw.polygon(self.screen, (40, 40, 40), points, 2)
        if node.move_cost > 0:
            text = self.font.render(str(node.move_cost), True, (0, 0, 0))
            self.screen.blit(text, text.get_rect(center=(cx, cy)))

    def draw_preview_path(self, path, actor):
        sim_moves = actor.moves_left
        sim_paid = actor.has_used_paid_move
        for node in path:
            can_reach = False
            if node.owner == actor:
                if not sim_paid:
                    can_reach = True
            else:
                if sim_moves >= node.move_cost:
                    sim_moves -= node.move_cost
                    sim_paid = True
                    can_reach = True
                else:
                    can_reach = False
                    sim_paid = True
            
            color = (255, 255, 0) if can_reach else (255, 0, 0)
            points, _, _ = self._get_hex_geometry(node)
            pygame.draw.polygon(self.screen, color, points, 4)

    def get_node_at_pos(self, graph, pos):
        mx, my = pos
        closest_node = None
        closest_dist = float("inf")
        for node in graph.nodes.values():
            _, cx, cy = self._get_hex_geometry(node)
            dist = (cx - mx)**2 + (cy - my)**2
            if dist < closest_dist:
                closest_dist = dist
                closest_node = node
        if closest_node and closest_dist < (closest_node.height / 2)**2:
            return closest_node
        return None