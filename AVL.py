import pygame
from pygame.locals import *

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1
        # Positions will be assigned dynamically
        self.x = 0
        self.y = 0

class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def right_rotate(self, y):
        x = y.left
        T3 = x.right
        x.right = y
        y.left = T3
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x

    def left_rotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, root, key):
        if not root:
            return Node(key)
        elif key < root.key:
            root.left = self._insert(root.left, key)
        elif key > root.key:
            root.right = self._insert(root.right, key)
        else:
            return root  # No duplicates

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # Left Left Case
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)

        # Right Right Case
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)

        # Left Right Case
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Left Case
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, root, key):
        if not root:
            return root

        if key < root.key:
            root.left = self._delete(root.left, key)
        elif key > root.key:
            root.right = self._delete(root.right, key)
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            min_val = self._min_value_node(root.right).key
            root.key = min_val
            root.right = self._delete(root.right, min_val)

        if not root:
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # Left Left Case
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)

        # Left Right Case
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Right Case
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)

        # Right Left Case
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

class AVLVisualizer:
    def __init__(self, tree):
        self.tree = tree
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("AVL Tree Visualization")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)
        self.input_box = pygame.Rect(10, 10, 140, 32)
        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('gray15')
        self.color = self.color_passive
        self.active = False
        self.text = ''
        self.mode = 'insert'  # 'insert' or 'delete'

    def assign_positions(self, node, x, y, spacing):
        if not node:
            return
        node.x = x
        node.y = y
        if node.left:
            self.assign_positions(node.left, x - spacing, y + 80, spacing // 2)
        if node.right:
            self.assign_positions(node.right, x + spacing, y + 80, spacing // 2)

    def draw_tree(self, node):
        if not node:
            return
        # Draw node
        pygame.draw.circle(self.screen, (255, 255, 255), (node.x, node.y), 20)
        text = self.font.render(str(node.key), True, (0, 0, 0))
        self.screen.blit(text, (node.x - 10, node.y - 10))
        # Draw edges
        if node.left:
            pygame.draw.line(self.screen, (255, 0, 0), (node.x, node.y), (node.left.x, node.left.y))
            self.draw_tree(node.left)
        if node.right:
            pygame.draw.line(self.screen, (255, 0, 0), (node.x, node.y), (node.right.x, node.right.y))
            self.draw_tree(node.right)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == MOUSEBUTTONDOWN:
                    if self.input_box.collidepoint(event.pos):
                        self.active = True
                        self.color = self.color_active
                    else:
                        self.active = False
                        self.color = self.color_passive
                if event.type == KEYDOWN:
                    if event.key == K_i:
                        self.mode = 'insert'
                    elif event.key == K_d:
                        self.mode = 'delete'
                    if self.active:
                        if event.key == K_RETURN:
                            try:
                                val = int(self.text)
                                if self.mode == 'insert':
                                    self.tree.insert(val)
                                elif self.mode == 'delete':
                                    self.tree.delete(val)
                            except ValueError:
                                pass
                            self.text = ''
                        elif event.key == K_BACKSPACE:
                            self.text = self.text[:-1]
                        else:
                            self.text += event.unicode

            self.screen.fill((0, 0, 0))
            # Draw input box
            pygame.draw.rect(self.screen, self.color, self.input_box, 2)
            txt_surface = self.font.render(self.text, True, (255, 255, 255))
            self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
            # Draw mode and instructions
            mode_text = self.font.render(f"Mode: {self.mode} (Press I/D to change)", True, (255, 255, 255))
            self.screen.blit(mode_text, (160, 10))
            instr_text = self.font.render("Enter number and press Return", True, (255, 255, 255))
            self.screen.blit(instr_text, (10, 50))
            # Draw tree
            if self.tree.root:
                self.assign_positions(self.tree.root, 640, 100, 320)
                self.draw_tree(self.tree.root)
            pygame.display.flip()
            self.clock.tick(30)
        pygame.quit()

if __name__ == "__main__":
    avl_tree = AVLTree()
    visualizer = AVLVisualizer(avl_tree)
    visualizer.run()