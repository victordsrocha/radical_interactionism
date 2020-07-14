class Interface(object):

    def __init__(self, memory):
        self.map = 'pygame_simulation/map.txt'
        self.memory = memory

        self.ORIENTATION_UP = 0
        self.ORIENTATION_RIGHT = 1
        self.ORIENTATION_DOWN = 2
        self.ORIENTATION_LEFT = 3
        self.WIDTH = 6
        self.HEIGHT = 6
        self.m_x = 1
        self.m_y = 4
        self.m_o = 0
        self.m_agent = {'^', '>', 'v', '<'}

        self.m_board = [
            ['x', 'x', 'x', 'x', 'x', 'x'],
            ['x', ' ', ' ', ' ', 'x', 'x'],
            ['x', ' ', 'x', ' ', ' ', 'x'],
            ['x', ' ', 'x', 'x', ' ', 'x'],
            ['x', ' ', ' ', ' ', ' ', 'x'],
            ['x', 'x', 'x', 'x', 'x', 'x']
        ]

        # self.step_actions_list = step_actions_list

    def enact(self, intended_interaction, step_actions_list):
        """
        recebe somente interações primitivas
        esta função deve "tentar" executar a interação intencionada no ambiente
        em seguida deve retornar a interação realmente executada (enacted)
        esta pode ou não ser igual à intencionada
        """
        enacted_interaction = None

        act = intended_interaction.label[0]

        if act == '>':
            enacted_interaction = self.move()
        elif act == '^':
            enacted_interaction = self.left()
        elif act == 'v':
            enacted_interaction = self.right()
        elif act == '-':
            enacted_interaction = self.touch()
        elif act == '\\':
            enacted_interaction = self.touch_right()
        elif act == '/':
            enacted_interaction = self.touch_left()

        # print(enacted_interaction)
        step_actions_list.append((enacted_interaction.label, self.m_x, self.m_y, self.m_o))
        print(f'Posicao atual = {self.m_x},{self.m_y},{self.m_o}')
        return enacted_interaction

    def tile_content(self, x, y):
        return self.m_board[y][x]

    def right(self):
        self.m_o += 1
        if self.m_o > self.ORIENTATION_LEFT:
            self.m_o = self.ORIENTATION_UP
        return self.memory.add_or_get_primitive_interaction('vt', 0)

    def left(self):
        self.m_o -= 1
        if self.m_o < 0:
            self.m_o = self.ORIENTATION_LEFT
        return self.memory.add_or_get_primitive_interaction('^t', 0)

    def move(self):
        enacted_interaction = self.memory.add_or_get_primitive_interaction('>f', 0)

        if (self.m_o == self.ORIENTATION_UP) and (self.m_y > 0) and (
                self.tile_content(self.m_x, self.m_y - 1) == ' '):
            self.m_y -= 1
            enacted_interaction = self.memory.add_or_get_primitive_interaction('>t', 0)

        if (self.m_o == self.ORIENTATION_DOWN) and (self.m_y < self.HEIGHT) and (
                self.tile_content(self.m_x, self.m_y + 1) == ' '):
            self.m_y += 1
            enacted_interaction = self.memory.add_or_get_primitive_interaction('>t', 0)

        if (self.m_o == self.ORIENTATION_RIGHT) and (self.m_x < self.WIDTH) and (
                self.m_board[self.m_y][self.m_x + 1] == ' '):
            self.m_x += 1
            enacted_interaction = self.memory.add_or_get_primitive_interaction('>t', 0)

        if (self.m_o == self.ORIENTATION_LEFT) and (self.m_x > 0) and (self.m_board[self.m_y][self.m_x - 1] == ' '):
            self.m_x -= 1
            enacted_interaction = self.memory.add_or_get_primitive_interaction('>t', 0)

        return enacted_interaction

    def touch(self):
        """
        Touch the square forward.
        Succeeds if there is a wall, fails otherwise
        :return:
        """
        enacted_interaction = self.memory.add_or_get_primitive_interaction('-t', 0)

        if (((self.m_o == self.ORIENTATION_UP) and (self.m_y > 0) and (self.m_board[self.m_y - 1][self.m_x] == ' ')) or
                ((self.m_o == self.ORIENTATION_DOWN) and (self.m_y < self.HEIGHT) and (
                        self.m_board[self.m_y + 1][self.m_x] == ' ')) or
                ((self.m_o == self.ORIENTATION_RIGHT) and (self.m_x < self.WIDTH) and (
                        self.m_board[self.m_y][self.m_x + 1] == ' ')) or
                ((self.m_o == self.ORIENTATION_LEFT) and (self.m_x > 0) and (
                        self.m_board[self.m_y][self.m_x - 1] == ' '))):
            enacted_interaction = self.memory.add_or_get_primitive_interaction('-f', 0)

        return enacted_interaction

    def touch_right(self):
        """
        Touch the square to the right.
        Succeeds if there is a wall, fails otherwise.
        :return:
        """
        enacted_interaction = self.memory.add_or_get_primitive_interaction('\\t', 0)

        if (((self.m_o == self.ORIENTATION_UP) and (self.m_x > 0) and (self.m_board[self.m_y][self.m_x + 1] == ' ')) or
                ((self.m_o == self.ORIENTATION_DOWN) and (self.m_x < self.WIDTH) and (
                        self.m_board[self.m_y][self.m_x - 1] == ' ')) or
                ((self.m_o == self.ORIENTATION_RIGHT) and (self.m_y < self.HEIGHT) and (
                        self.m_board[self.m_y + 1][self.m_x] == ' ')) or
                ((self.m_o == self.ORIENTATION_LEFT) and (self.m_y > 0) and (
                        self.m_board[self.m_y - 1][self.m_x] == ' '))):
            enacted_interaction = self.memory.add_or_get_primitive_interaction('\\f', 0)

        return enacted_interaction

    def touch_left(self):

        enacted_interaction = self.memory.add_or_get_primitive_interaction('/t', 0)

        if (((self.m_o == self.ORIENTATION_UP) and (self.m_x > 0) and (self.m_board[self.m_y][self.m_x - 1] == ' ')) or
                ((self.m_o == self.ORIENTATION_DOWN) and (self.m_x < self.WIDTH) and (
                        self.m_board[self.m_y][self.m_x + 1] == ' ')) or
                ((self.m_o == self.ORIENTATION_RIGHT) and (self.m_y > 0) and (
                        self.m_board[self.m_y - 1][self.m_x] == ' ')) or
                ((self.m_o == self.ORIENTATION_LEFT) and (self.m_y < self.HEIGHT) and (
                        self.m_board[self.m_y + 1][self.m_x] == ' '))):
            enacted_interaction = self.memory.add_or_get_primitive_interaction('/f', 0)

        return enacted_interaction
