import arcade
import random
import time
import statistics
import pygame

# Define a largura e altura da tela
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

# Inicializa o pygame para tocar sons
pygame.mixer.init()
# Carrega um som de bip para ser reproduzido durante o jogo
beep_sound = pygame.mixer.Sound("stop-13692.mp3")

# Classe para representar a posição de um círculo
class Position:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.radius = 70  # Define o raio padrão dos círculos

# Classe para o círculo vermelho
class RedCircle:
    def __init__(self):
        self.center = Position()
        # Define uma posição aleatória para o círculo, respeitando os limites da tela
        self.center.x = random.randint(80, SCREEN_WIDTH - 80)
        self.center.y = random.randint(80, SCREEN_HEIGHT - 80)
        self.alive = True
        self.direction = 'up'  # Direção associada ao círculo vermelho

    def draw(self):
        # Desenha o círculo vermelho na tela
        arcade.draw_circle_filled(self.center.x, self.center.y, self.center.radius, arcade.color.RED)

# Classe para o círculo azul
class BlueCircle:
    def __init__(self):
        self.center = Position()
        self.center.x = random.randint(80, SCREEN_WIDTH - 80)
        self.center.y = random.randint(80, SCREEN_HEIGHT - 80)
        self.alive = True
        self.direction = 'down'  # Direção associada ao círculo azul

    def draw(self):
        # Desenha o círculo azul na tela
        arcade.draw_circle_filled(self.center.x, self.center.y, self.center.radius, arcade.color.BLUE)

# Classe para o círculo amarelo
class YellowCircle:
    def __init__(self):
        self.center = Position()
        self.center.x = random.randint(80, SCREEN_WIDTH - 80)
        self.center.y = random.randint(80, SCREEN_HEIGHT - 80)
        self.alive = True
        self.direction = 'left'  # Direção associada ao círculo amarelo

    def draw(self):
        # Desenha o círculo amarelo na tela
        arcade.draw_circle_filled(self.center.x, self.center.y, self.center.radius, arcade.color.YELLOW)

# Classe para o círculo verde
class GreenCircle:
    def __init__(self):
        self.center = Position()
        self.center.x = random.randint(80, SCREEN_WIDTH - 80)
        self.center.y = random.randint(80, SCREEN_HEIGHT - 80)
        self.alive = True
        self.direction = 'right'  # Direção associada ao círculo verde

    def draw(self):
        # Desenha o círculo verde na tela
        arcade.draw_circle_filled(self.center.x, self.center.y, self.center.radius, arcade.color.GREEN)

# Classe principal do jogo de reação
class ReactionGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.pressed_keys = set()  # Conjunto para rastrear teclas pressionadas
        self.input_direction = ''  # Armazena a direção de entrada do jogador
        self.correct_guesses = 0  # Contador de acertos
        self.attempts = 0  # Contador de tentativas
        self.current_circles = []  # Lista de círculos atuais na tela
        self.red_circle = RedCircle()  # Instância do círculo vermelho
        arcade.set_background_color(arcade.color.WHITE)  # Define a cor de fundo
        self.reaction_times = []  # Lista para armazenar os tempos de reação
        self.game_started = False  # Indica se o jogo começou

    def update(self, delta_time):
        # Chance aleatória de adicionar um novo círculo
        self.random_chance = random.randint(1, 100)
        if self.random_chance == 1 and len(self.current_circles) == 0 and self.attempts < 10:
            self.add_random_circle()  # Adiciona um círculo aleatório

    def on_draw(self):
        arcade.start_render()  # Inicia o processo de desenho
        if not self.game_started:  # Se o jogo não começou, desenha a tela inicial
            self.draw_start_screen()
        else:
            self.draw_score()  # Desenha o placar

            if self.attempts < 10:  # Enquanto houver tentativas disponíveis
                for circle in self.current_circles:
                    circle.draw()  # Desenha os círculos atuais
            else:
                self.draw_results()  # Desenha os resultados finais

    def draw_start_screen(self):
        # Desenha a tela inicial com instruções
        arcade.draw_text("Pressione ENTER para começar", start_x=SCREEN_WIDTH / 2, start_y=SCREEN_HEIGHT / 2 + 100,
                         font_size=40, color=arcade.color.BLACK, bold=True, anchor_x="center")
        arcade.draw_text("Controles:", start_x=SCREEN_WIDTH / 2, start_y=SCREEN_HEIGHT / 2 + 30, font_size=30,
                         color=arcade.color.BLACK, anchor_x="center")
        arcade.draw_text("Cima (↑) - Vermelho", start_x=SCREEN_WIDTH / 2, start_y=SCREEN_HEIGHT / 2, font_size=25,
                         color=arcade.color.BLACK, anchor_x="center")
        arcade.draw_text("Baixo (↓) - Azul", start_x=SCREEN_WIDTH / 2, start_y=SCREEN_HEIGHT / 2 - 30, font_size=25,
                         color=arcade.color.BLACK, anchor_x="center")
        arcade.draw_text("Esquerda (←) - Amarelo", start_x=SCREEN_WIDTH / 2, start_y=SCREEN_HEIGHT / 2 - 60,
                         font_size=25, color=arcade.color.BLACK, anchor_x="center")
        arcade.draw_text("Direita (→) - Verde", start_x=SCREEN_WIDTH / 2, start_y=SCREEN_HEIGHT / 2 - 90, font_size=25,
                         color=arcade.color.BLACK, anchor_x="center")
        arcade.draw_text("Pressione ESPAÇO para resetar", start_x=SCREEN_WIDTH / 2, start_y=SCREEN_HEIGHT / 2 - 150,
                         font_size=25, color=arcade.color.BLACK, anchor_x="center")

    def draw_results(self):
        # Mensagem exibida ao final do teste
        arcade.draw_text("Fim de Teste", start_x=SCREEN_WIDTH / 2, start_y=SCREEN_HEIGHT / 2 + 100, font_size=60,
                         color=arcade.color.BLACK, bold=True, anchor_x="center")

        start_y = SCREEN_HEIGHT / 2 - 20
        distancia_horizontal = 300  # Espaço horizontal entre os textos
        arcade.draw_text("Tempos", start_x=SCREEN_WIDTH / 2 - distancia_horizontal, start_y=start_y, font_size=30,
                         color=arcade.color.BLACK, anchor_x="center")
        arcade.draw_text(f"Acertos: {self.correct_guesses}", start_x=SCREEN_WIDTH / 2, start_y=start_y, font_size=30,
                         color=arcade.color.BLACK, anchor_x="center")

        # Calcula e exibe a média dos tempos de reação
        media = statistics.mean(self.reaction_times) if self.reaction_times else 0  # Previne divisão por zero
        arcade.draw_text(f"Média: {media:.2f}ms", start_x=SCREEN_WIDTH / 2 + distancia_horizontal, start_y=start_y,
                         font_size=30, color=arcade.color.BLACK, anchor_x="center")

        # Exibe os tempos de reação individuais
        start_y_tempo = SCREEN_HEIGHT / 2 - 60
        for reaction_time in self.reaction_times:
            arcade.draw_text(f"{reaction_time}ms", start_x=SCREEN_WIDTH / 2 - distancia_horizontal, start_y=start_y_tempo,
                             font_size=25, color=arcade.color.BLACK, anchor_x="center")
            start_y_tempo -= 30

    def draw_score(self):
        # Desenha o placar de tentativas na tela
        score_text = "Tentativas: {}".format(self.attempts)
        start_x = SCREEN_WIDTH - 280  # Alinha à direita
        start_y = SCREEN_HEIGHT - 50

        # Desenha o texto do placar
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=30, color=arcade.color.BLACK,
                         font_name="game_font")  # Substitua 'game_font' pelo nome do arquivo da sua fonte

    def add_random_circle(self):
        # Adiciona um círculo de cor aleatória à tela
        color_choice = random.randint(1, 4)
        circle = None
        if color_choice == 1:
            circle = RedCircle()
        elif color_choice == 2:
            circle = BlueCircle()
        elif color_choice == 3:
            circle = YellowCircle()
        elif color_choice == 4:
            circle = GreenCircle()

        self.current_circles.append(circle)  # Adiciona o círculo à lista
        self.start_time = int(round(time.time() * 1000))

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:  # Inicia o jogo quando a tecla ENTER é pressionada
            self.game_started = True
            self.attempts = 0  # Reseta as tentativas
            self.correct_guesses = 0  # Reseta os acertos
            self.reaction_times = []  # Reseta os tempos de reação
            self.current_circles.clear()  # Limpa os círculos atuais
            self.add_random_circle()  # Adiciona um círculo aleatório

        if key == arcade.key.SPACE:  # Reinicia o jogo quando a tecla SPACE é pressionada
            self.game_started = False  # Para a contagem
            self.current_circles.clear()  # Limpa os círculos atuais

        # Verifica se a tecla pressionada corresponde à direção correta
        if self.game_started and len(self.current_circles) > 0:
            if key == arcade.key.UP and isinstance(self.current_circles[0], RedCircle):
                self.correct_guesses += 1  # Aumenta o contador de acertos
                self.current_circles.pop(0)  # Remove o círculo que foi acertado
                self.attempts += 1  # Aumenta o contador de tentativas
                self.play_beep()  # Toca o som de acerto
                self.record_reaction_time()  # Registra o tempo de reação
                self.add_random_circle()  # Adiciona um novo círculo aleatório

            elif key == arcade.key.DOWN and isinstance(self.current_circles[0], BlueCircle):
                self.correct_guesses += 1
                self.current_circles.pop(0)
                self.attempts += 1
                self.play_beep()
                self.record_reaction_time()
                self.add_random_circle()

            elif key == arcade.key.LEFT and isinstance(self.current_circles[0], YellowCircle):
                self.correct_guesses += 1
                self.current_circles.pop(0)
                self.attempts += 1
                self.play_beep()
                self.record_reaction_time()
                self.add_random_circle()

            elif key == arcade.key.RIGHT and isinstance(self.current_circles[0], GreenCircle):
                self.correct_guesses += 1
                self.current_circles.pop(0)
                self.attempts += 1
                self.play_beep()
                self.record_reaction_time()
                self.add_random_circle()

            else:
                # Se o jogador errar a cor, apenas incrementa as tentativas
                self.attempts += 1

    def play_beep(self):
        beep_sound.play()  # Toca o som de bip quando uma cor é acertada

    def record_reaction_time(self):
        reaction_time = int(round(time.time() * 1000)) - self.start_time  # Calcula o tempo de reação
        self.reaction_times.append(reaction_time)  # Adiciona o tempo de reação à lista

def main():
    # Inicia a aplicação
    game = ReactionGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()  # Executa o jogo

if __name__ == "__main__":
    main()  # Chama a função principal
