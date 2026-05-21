class Player:
    def __init__(self, name, start_node=None, color=(255, 50, 50), is_ai=False):
        self.name = name

        self.current_node = start_node

        self.color = color

        self.is_ai = is_ai

        self.path = []

        self.move_timer = 0
        self.base_move_delay = 8

        self.max_moves = 3
        self.moves_left = 3

        self.points = 0

        self.ai_timer = 0

        self.has_used_paid_move = False

    def set_path(self, path):
        self.path = path
        self.move_timer = 0

    def reset_moves(self):
        self.moves_left = self.max_moves

        self.path = []

        self.ai_timer = 30

        self.has_used_paid_move = False

    def can_traverse(self, node):
        if node.owner == self:
            return not self.has_used_paid_move

        return self.moves_left >= node.move_cost

    def update(self):
        if not self.path:
            return True

        next_node = self.path[0]

        if not self.can_traverse(next_node):
            self.path = []
            return True

        self.move_timer += 1

        target_delay = self.base_move_delay

        if next_node.owner != self:
            target_delay *= next_node.move_cost

        if self.move_timer >= target_delay:
            self.move_timer = 0

            self.current_node = self.path.pop(0)

            if self.current_node.owner != self:
                self.moves_left -= self.current_node.move_cost
                self.has_used_paid_move = True

            self.current_node.capture(self)

            if not self.path:
                return True

        return False

    def ai_think(self, graph, pathfinder):
        if self.moves_left <= 0 and self.has_used_paid_move:
            return False

        if self.ai_timer > 0:
            self.ai_timer -= 1
            return True

        best_path = None

        best_value = -1

        for node in graph.nodes.values():
            if node.owner is not None:
                continue

            path = pathfinder.get_path(
                self.current_node,
                node,
                self
            )

            if not path:
                continue

            simulated_moves = self.moves_left
            simulated_paid_move = self.has_used_paid_move

            valid = True

            for step in path:
                if step.owner == self:
                    if simulated_paid_move:
                        valid = False
                        break
                else:
                    if simulated_moves < step.move_cost:
                        valid = False
                        break

                    simulated_moves -= step.move_cost
                    simulated_paid_move = True

            if not valid:
                continue

            distance = len(path)

            value = step.move_cost / (distance + 1)

            if value > best_value:
                best_value = value
                best_path = path

        if best_path:
            self.set_path(best_path)
            return True

        self.moves_left = 0

        return False