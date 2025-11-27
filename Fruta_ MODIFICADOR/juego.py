import pygame
import time
from jugador import Jugador
from fruta import Fruta
from obstaculo import Obstaculo

# ================================
# PANTALLA DE NIVELES
# ================================
class PantallaNiveles:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        try:
            self.fondo = pygame.image.load("assets/niveles/pantalla_fondo_niveles.png").convert()
            self.fondo = pygame.transform.scale(self.fondo, (800, 600))
        except:
            self.fondo = None

        try:
            self.fuente_titulo = pygame.font.Font("assets/fuente/letra_titulo.ttf", 70)
        except:
            self.fuente_titulo = pygame.font.Font(None, 70)
        self.fuente_titulo.set_bold(True)

        self.fuente_botones = pygame.font.Font(None, 40)

        try:
            self.boton_atras_img = pygame.image.load("assets/boton/boton_atras.png").convert_alpha()
            self.boton_atras_img = pygame.transform.scale(self.boton_atras_img, (150, 60))
        except:
            self.boton_atras_img = pygame.Surface((150, 60))
            self.boton_atras_img.fill((200, 50, 50))

        self.boton_atras_rect = self.boton_atras_img.get_rect(center=(100, 550))

        posiciones = [(200, 180), (400, 180), (600, 180), (300, 350), (500, 350)]
        self.niveles_rects = []
        for pos in posiciones:
            rect = pygame.Rect(0, 0, 150, 120)
            rect.center = pos
            self.niveles_rects.append(rect)

        # iconos por nivel (colocar assets/niveles/icono_nivel_1.png ... _5.png)
        self.iconos_niveles = []
        for i in range(1, 6):
            ruta = f"assets/niveles/icono_nivel_{i}.png"
            try:
                icono = pygame.image.load(ruta).convert_alpha()
                icono = pygame.transform.scale(icono, (80, 80))
            except:
                icono = pygame.Surface((80, 80))
                icono.fill((150, 150, 150))
            self.iconos_niveles.append(icono)

    def ejecutar(self):
        ejecutando = True
        while ejecutando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # volver
                    if self.boton_atras_rect.collidepoint(event.pos):
                        return "atras"
                    # seleccionar nivel
                    for i, rect in enumerate(self.niveles_rects):
                        if rect.collidepoint(event.pos):
                            return f"nivel_{i+1}"

            if self.fondo:
                self.pantalla.blit(self.fondo, (0, 0))
            else:
                self.pantalla.fill((220, 220, 250))

            titulo = self.fuente_titulo.render("NIVELES", True, (0, 0, 0))
            self.pantalla.blit(titulo, titulo.get_rect(center=(400, 70)))

            for i, rect in enumerate(self.niveles_rects):
                pygame.draw.rect(self.pantalla, (180, 180, 180), rect, border_radius=12)
                icono = self.iconos_niveles[i]
                icono_rect = icono.get_rect(center=(rect.centerx, rect.centery - 10))
                self.pantalla.blit(icono, icono_rect)
                numero = self.fuente_botones.render(f"Nivel {i+1}", True, (0, 0, 0))
                self.pantalla.blit(numero, numero.get_rect(center=(rect.centerx, rect.centery + 50)))

            self.pantalla.blit(self.boton_atras_img, self.boton_atras_rect)
            pygame.display.update()

# ================================
# PANTALLA DE INICIO
# ================================
class PantallaInicio:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        try:
            self.fondo = pygame.image.load("assets/fondo_inicio/fondo_juego_inicio.png").convert()
            self.fondo = pygame.transform.scale(self.fondo, (800, 600))
        except:
            self.fondo = None

        try:
            self.boton_img = pygame.image.load("assets/boton/boton_jugar_.png").convert_alpha()
            self.boton_img = pygame.transform.scale(self.boton_img, (200, 80))
        except:
            self.boton_img = pygame.Surface((200, 80))
            self.boton_img.fill((180, 180, 180))
        self.boton_rect = self.boton_img.get_rect(center=(400, 380))

        try:
            self.boton_niveles = pygame.image.load("assets/boton/boton_niveles_.png").convert_alpha()
            self.boton_niveles = pygame.transform.scale(self.boton_niveles, (200, 80))
        except:
            self.boton_niveles = pygame.Surface((200, 80))
            self.boton_niveles.fill((150, 150, 255))
        self.boton_niveles_rect = self.boton_niveles.get_rect(center=(400, 480))

        try:
            self.fuente = pygame.font.Font("assets/fuente/letra_titulo.ttf", 85)
        except:
            self.fuente = pygame.font.Font(None, 85)
        self.fuente.set_bold(True)

    def dibujar_texto_con_sombra(self, texto, x, y):
        sombra = self.fuente.render(texto, True, (0, 0, 0))
        self.pantalla.blit(sombra, sombra.get_rect(center=(x + 4, y + 4)))
        texto_real = self.fuente.render(texto, True, (150, 0, 150))
        self.pantalla.blit(texto_real, texto_real.get_rect(center=(x, y)))

    def ejecutar(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton_rect.collidepoint(event.pos):
                        return "primer_nivel"
                    if self.boton_niveles_rect.collidepoint(event.pos):
                        return "niveles"
            if self.fondo:
                self.pantalla.blit(self.fondo, (0, 0))
            else:
                self.pantalla.fill((220, 250, 220))
            self.dibujar_texto_con_sombra("FRUTAMANIA", 400, 230)
            self.pantalla.blit(self.boton_img, self.boton_rect)
            self.pantalla.blit(self.boton_niveles, self.boton_niveles_rect)
            pygame.display.update()

# ==========================================
# SISTEMA DE NIVELES Y JUEGO
# ==========================================
class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("FrutaManía 🍎")
        self.reloj = pygame.time.Clock()

        # iconos para botones pausa/inicio (colocar en assets/iconos/)
        try:
            self.icono_pausa = pygame.image.load("assets/iconos/pausa_icon.png").convert_alpha()
            self.icono_pausa = pygame.transform.scale(self.icono_pausa, (40, 40))
        except:
            self.icono_pausa = pygame.Surface((40, 40))
            self.icono_pausa.fill((255, 200, 0))
        try:
            self.icono_inicio = pygame.image.load("assets/iconos/inicio_icon.png").convert_alpha()
            self.icono_inicio = pygame.transform.scale(self.icono_inicio, (40, 40))
        except:
            self.icono_inicio = pygame.Surface((40, 40))
            self.icono_inicio.fill((255, 50, 50))

    def iniciar(self):
        while True:
            pantalla_inicio = PantallaInicio(self.pantalla)
            accion = pantalla_inicio.ejecutar()

            if accion == "niveles":
                pantalla_niveles = PantallaNiveles(self.pantalla)
                volver = pantalla_niveles.ejecutar()
                if volver == "atras":
                    continue
                # si eligió un nivel directamente:
                if volver and volver.startswith("nivel_"):
                    n = int(volver.split("_")[1])
                    self.jugar_niveles(desde_nivel=n)
            elif accion == "primer_nivel":
                self.jugar_niveles(desde_nivel=1)

    def jugar_niveles(self, desde_nivel=1):
        for nivel in range(desde_nivel, 6):
            resultado = self.jugar_partida(nivel)
            if resultado == "perdio" or resultado == "salio":
                return
        print("🎉 ¡GANASTE TODOS LOS NIVELES!")

    # --------------------------
    # JUEGO DE CADA NIVEL
    # --------------------------
    def jugar_partida(self, numero_nivel):
        # CREAR ENTIDADES COMUNES
        jugador = Jugador(400, 300)
        fruta = Fruta()
        obstaculo = Obstaculo()

        # VEHÍCULOS/ENTIDADES ESPECIALES POR NIVEL
        # LEVEL SPECIFIC ASSETS (rutas sugeridas - coloca archivos en assets/)
        bg_ruta = f"assets/niveles/level{numero_nivel}_bg.png"        # fondo por nivel
        hielo_ruta = f"assets/niveles/hielo_{numero_nivel}.png"       # solo si usas sprite
        bomba_ruta = f"assets/niveles/bomba_{numero_nivel}.png"
        sorpresa_ruta = f"assets/niveles/sorpresa_{numero_nivel}.png"

        # cargar fondo específico del nivel (si existe)
        try:
            fondo_n = pygame.image.load(bg_ruta).convert()
            fondo_n = pygame.transform.scale(fondo_n, (800, 600))
        except:
            fondo_n = None

        # Preparaciones por nivel
        puntaje = 0
        objetivo = 5            # 5 frutas por defecto (puedes cambiar)
        vidas = 3

        # HUD (misma fuente del inicio)
        try:
            fuente_hud = pygame.font.Font("assets/fuente/letra_titulo.ttf", 30)
        except:
            fuente_hud = pygame.font.Font(None, 30)
        fuente_hud.set_bold(True)

        def dibujar_texto_bonito(texto, x, y):
            sombra = fuente_hud.render(texto, True, (0, 0, 0))
            self.pantalla.blit(sombra, (x + 2, y + 2))
            render = fuente_hud.render(texto, True, (255, 255, 255))
            self.pantalla.blit(render, (x, y))

        # botones pausa / inicio (iconos ya cargados en __init__)
        boton_pausa = pygame.Rect(700, 10, 80, 40)
        boton_inicio = pygame.Rect(700, 60, 80, 40)

        # Datos para comportamientos por nivel
        hielos = []     # rects de hielo (nivel 2 y 4)
        bombas = []     # rects de bombas (nivel 3)
        paredes = []    # rects del laberinto (nivel 3)
        sorpresa_rect = None  # el objeto sorpresa (nivel 4)
        puerta_rect = None    # nivel 5 puerta final
        # Inicialización de imágenes de Nivel 5 para evitar errores de ámbito
        tigre_img = None
        tigre_congelado_img = None
        puerta_img = None

        tigres = []
        tigres_congelados = []

        # --- configurar cada nivel ---
        if numero_nivel == 1:
            # nivel 1: fruta + un tigre enemigo (obstaculo ya existe)
            pass

        elif numero_nivel == 2:
            # nivel 2: placas de hielo en áreas (si tocan, restan 1 vida y reducen movimiento temporalmente)
            # ejemplo: generar 4 placas de hielo
            hielos = [pygame.Rect(150, 250, 120, 80), pygame.Rect(500, 120, 120, 80),
                      pygame.Rect(300, 420, 120, 80)]
        elif numero_nivel == 3:
            # nivel 3: laberinto + bombas
            # Ejemplo de paredes (rects) — adáptalas al diseño real
            paredes = [
                pygame.Rect(100, 100, 600, 20), pygame.Rect(100, 100, 20, 400),
                pygame.Rect(100, 480, 600, 20), pygame.Rect(680, 100, 20, 400),
                pygame.Rect(250, 180, 300, 20), pygame.Rect(250, 260, 20, 160),
                pygame.Rect(530, 260, 20, 160), pygame.Rect(350, 320, 150, 20)
            ]
            # bombas
            bombas = [pygame.Rect(420, 200, 30, 30), pygame.Rect(300, 360, 30, 30)]
            # colocar la fruta meta como "manzana" en una posición escondida por ejemplo:
            fruta.x, fruta.y = 150, 140

        elif numero_nivel == 4:
            # nivel 4: bloque de hielo que congela (zona) y sorpresa que restaura velocidad
            hielo_zona = pygame.Rect(350, 250, 120, 120)
            hielos = [hielo_zona]
            # sorpresa (objeto recup.)
            sorpresa_rect = pygame.Rect(650, 480, 32, 32)

        elif numero_nivel == 5:
            # nivel 5: varios tigres y puerta final
            for i in range(4):  # crea 4 tigres como Obstaculo
                t = Obstaculo()
                tigres.append(t)
            # puerta salida
            puerta_rect = pygame.Rect(380, 20, 90, 120)
            # Note: cargar imágenes para tigre y puerta abajo

        # cargar imágenes específicas (si existen)
        try:
            icon_bomba = pygame.image.load(bomba_ruta).convert_alpha()
            icon_bomba = pygame.transform.scale(icon_bomba, (30, 30))
        except:
            icon_bomba = None

        try:
            icon_sorpresa = pygame.image.load(sorpresa_ruta).convert_alpha()
            icon_sorpresa = pygame.transform.scale(icon_sorpresa, (32, 32))
        except:
            icon_sorpresa = None

        # si nivel 5: cargar tigre y puerta (rutas sugeridas)
        if numero_nivel == 5:
            try:
                tigre_img = pygame.image.load("assets/nivel5/tigre.png").convert_alpha()
                tigre_img = pygame.transform.scale(tigre_img, (70, 70))
            except:
                tigre_img = None
            try:
                tigre_congelado_img = pygame.image.load("assets/nivel5/tigre_congelado.png").convert_alpha()
                tigre_congelado_img = pygame.transform.scale(tigre_congelado_img, (70, 70))
            except:
                tigre_congelado_img = None
            try:
                puerta_img = pygame.image.load("assets/nivel5/puerta_salida.png").convert_alpha()
                puerta_img = pygame.transform.scale(puerta_img, (90, 120))
            except:
                puerta_img = None
        
        # Eliminada la línea 'else: tigre_img = tigre_congelado_img = puerta_img = None'
        # ya que las variables se inicializaron a None al principio de la función.


        # Tiempo de congelado en segundos
        congelado_duracion = 3.0

        # estado de velocidad (para nivel 4)
        velocidad_reducida = False
        velocidad_reducida_until = 0

        ejecutando = True
        while ejecutando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "salio"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # chequeo botones
                    if boton_pausa.collidepoint(event.pos):
                        self.pausar_juego()
                    if boton_inicio.collidepoint(event.pos):
                        return "salio"
                if event.type == pygame.KEYDOWN:
                    # nivel 5: presionar espacio congela tigres (agregar timestamp)
                    if numero_nivel == 5 and event.key == pygame.K_SPACE:
                        # Añade el timestamp actual para congelar a los tigres
                        tigres_congelados.append(time.time())

            # GUARDAR POSICIÓN PREVIA (para colisiones/ajustes)
            prev_x, prev_y = jugador.x, jugador.y

            teclas = pygame.key.get_pressed()
            jugador.mover(teclas)

            # movimiento efectivo (dx,dy) para poder "reducir" movimiento en hielo
            dx = jugador.x - prev_x
            dy = jugador.y - prev_y

            jugador_rect = pygame.Rect(jugador.x, jugador.y, 60, 60)
            fruta_rect = pygame.Rect(fruta.x, fruta.y, 40, 40)
            obstaculo_rect = pygame.Rect(obstaculo.x, obstaculo.y, 70, 70)

            # --- comportamiento común para niveles 1-4 (fruta + obstáculo perseguidor) ---
            if numero_nivel in (1, 2, 3, 4):
                # nivel 3: laberinto => si choca con pared, volver atrás (evita atravesar paredes)
                if numero_nivel == 3 and paredes:
                    collided_wall = False
                    for pared in paredes:
                        if jugador_rect.colliderect(pared):
                            collided_wall = True
                            break
                    if collided_wall:
                        # revertir movimiento
                        jugador.x = prev_x
                        jugador.y = prev_y
                        jugador_rect = pygame.Rect(jugador.x, jugador.y, 60, 60)

                # nivel 2: hielo que resta vida y reduce movimiento temporalmente
                if numero_nivel == 2 and hielos:
                    for hielo in hielos:
                        if jugador_rect.colliderect(hielo):
                            # daño al tocar hielo
                            vidas -= 1
                            # retroceso pequeño
                            jugador.x = prev_x
                            jugador.y = prev_y
                            jugador_rect = pygame.Rect(jugador.x, jugador.y, 60, 60)
                            # si vidas <=0 -> pierde
                            if vidas <= 0:
                                return "perdio"

                # nivel 4: zona de hielo que reduce movimiento (congelamiento parcial)
                if numero_nivel == 4 and hielos:
                    on_hielo = False
                    for hielo in hielos:
                        if jugador_rect.colliderect(hielo):
                            on_hielo = True
                            break
                    if on_hielo:
                        # reducir movimiento: hacemos que la posición sea la mitad del desplazamiento
                        jugador.x = int(prev_x + dx * 0.4)
                        jugador.y = int(prev_y + dy * 0.4)
                        jugador_rect = pygame.Rect(jugador.x, jugador.y, 60, 60)

                # nivel 4: recoger sorpresa para restaurar velocidad (si existe)
                if numero_nivel == 4 and sorpresa_rect:
                    if jugador_rect.colliderect(sorpresa_rect):
                        velocidad_reducida = False
                        velocidad_reducida_until = 0
                        # "recoger" sorpresa: moverlo fuera
                        sorpresa_rect.x = -1000

                # colisiones fruta / obstáculo
                if jugador_rect.colliderect(fruta_rect):
                    puntaje += 1
                    fruta = Fruta()
                    if puntaje >= objetivo:
                        return "ok"

                if jugador_rect.colliderect(obstaculo_rect):
                    vidas -= 1
                    obstaculo = Obstaculo()
                    if vidas <= 0:
                        return "perdio"
                # obstaculo persigue
                obstaculo.seguir_jugador(jugador.x, jugador.y)

                # nivel 3: bombas => daño instantáneo
                if numero_nivel == 3 and bombas:
                    for b in bombas:
                        if jugador_rect.colliderect(b):
                            vidas -= 1
                            # mover jugador a inicio del laberinto
                            jugador.x, jugador.y = 400, 520
                            if vidas <= 0:
                                return "perdio"

            # --- nivel 5: múltiples tigres ---
            if numero_nivel == 5:
                # colisión con puerta (salida)
                if puerta_rect and jugador_rect.colliderect(puerta_rect):
                    return "ok"

                # tigres: colisiones y movimiento
                for tigre in tigres:
                    t_rect = pygame.Rect(tigre.x, tigre.y, 70, 70)
                    # si tocó tigre
                    if jugador_rect.colliderect(t_rect):
                        vidas -= 1
                        # respawn leve
                        jugador.x, jugador.y = 400, 520
                        if vidas <= 0:
                            return "perdio"
                    # comprobar si tigre está congelado (algún timestamp dentro de ventana)
                    congelado_flag = False
                    # Limpiamos los timestamps viejos para que no ralentice el juego
                    tigres_congelados = [t0 for t0 in tigres_congelados if time.time() - t0 < congelado_duracion]
                    for t0 in tigres_congelados:
                        if time.time() - t0 < congelado_duracion:
                            congelado_flag = True
                            break
                    if not congelado_flag:
                        tigre.seguir_jugador(jugador.x, jugador.y)

            # DIBUJADO
            if fondo_n:
                self.pantalla.blit(fondo_n, (0, 0))
            else:
                self.pantalla.fill((200, 255, 200))

            # dibujar elementos por nivel
            if numero_nivel in (1, 2, 3, 4):
                # fruta y obstaculo visibles
                fruta.dibujar(self.pantalla)
                obstaculo.dibujar(self.pantalla)

            # dibujar paredes (laberinto)
            if numero_nivel == 3 and paredes:
                for pared in paredes:
                    pygame.draw.rect(self.pantalla, (80, 80, 80), pared)

            # dibujar bombas
            if numero_nivel == 3 and bombas:
                for b in bombas:
                    if icon_bomba:
                        self.pantalla.blit(icon_bomba, b)
                    else:
                        pygame.draw.rect(self.pantalla, (200, 50, 50), b)

            # dibujar hielo zonas
            if numero_nivel in (2, 4) and hielos:
                for hielo in hielos:
                    # si tienes sprite de hielo, podrías blitearlo; aquí rect
                    pygame.draw.rect(self.pantalla, (200, 230, 255), hielo, border_radius=6)

            # dibujar sorpresa (nivel 4)
            if numero_nivel == 4 and sorpresa_rect and sorpresa_rect.x > 0:
                if icon_sorpresa:
                    self.pantalla.blit(icon_sorpresa, sorpresa_rect)
                else:
                    pygame.draw.rect(self.pantalla, (255, 215, 0), sorpresa_rect)

            # dibujar jugador/obstaculos
            jugador.dibujar(self.pantalla)
            if numero_nivel in (1, 2, 3, 4):
                # obstaculo (tigre de 1, etc.)
                obstaculo.dibujar(self.pantalla)

            # dibujar puerta y tigres (nivel 5)
            if numero_nivel == 5:
                # puerta (solo si existe la rect)
                if puerta_rect:
                    if puerta_img:
                        self.pantalla.blit(puerta_img, puerta_rect)
                    else:
                        pygame.draw.rect(self.pantalla, (200, 0, 200), puerta_rect)

                # DIBUJAR TIGRES
                for tigre in tigres:
                    t_rect = pygame.Rect(tigre.x, tigre.y, 70, 70)

                    # Verificar si este tigre está congelado
                    frozen = False
                    for t0 in tigres_congelados:
                        if time.time() - t0 < congelado_duracion:
                            frozen = True
                            break

                    # Dibujar tigre (normal o congelado)
                    # HECHO: Corregido el error de lógica/indentación
                    if frozen and tigre_congelado_img:
                        self.pantalla.blit(tigre_congelado_img, t_rect)
                    elif tigre_img:
                        self.pantalla.blit(tigre_img, t_rect)
                    else:
                        # Fallback draw
                        pygame.draw.rect(self.pantalla, (255, 150, 0), t_rect)

            # HUD bonito (misma fuente)
            dibujar_texto_bonito(f"Nivel {numero_nivel}", 10, 10)
            dibujar_texto_bonito(f"Vidas: {vidas}", 10, 45)
            if numero_nivel < 5:
                dibujar_texto_bonito(f"Frutas: {puntaje}/{objetivo}", 10, 80)
            else:
                 # Mostrar tiempo de congelamiento en Nivel 5
                tiempo_restante = max(0, congelado_duracion - (time.time() - (tigres_congelados[-1] if tigres_congelados else 0)))
                dibujar_texto_bonito(f"Congelamiento: {tiempo_restante:.1f}s", 10, 80)
                dibujar_texto_bonito("Presiona [ESPACIO] para congelar", 10, 115)


            # BOTONES con iconos
            pygame.draw.rect(self.pantalla, (255, 255, 255), boton_pausa, border_radius=6)
            self.pantalla.blit(self.icono_pausa, (710, 10))
            pygame.draw.rect(self.pantalla, (255, 255, 255), boton_inicio, border_radius=6)
            self.pantalla.blit(self.icono_inicio, (710, 60))

            pygame.display.update()
            self.reloj.tick(30)

    # ======================
    # MODO PAUSA
    # ======================
    def pausar_juego(self):
        try:
            fuente = pygame.font.Font("assets/fuente/letra_titulo.ttf", 40)
        except:
            fuente = pygame.font.Font(None, 40)

        en_pausa = True
        aviso = fuente.render("PAUSADO - presiona P para continuar", True, (255, 255, 255))
        fondo_aviso = pygame.Surface((600, 40))
        fondo_aviso.fill((0, 0, 0))
        while en_pausa:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        en_pausa = False
            # mostrar overlay
            overlay = pygame.Surface(self.pantalla.get_size(), flags=pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            self.pantalla.blit(overlay, (0, 0))
            self.pantalla.blit(fondo_aviso, ((800-600)//2, 280))
            self.pantalla.blit(aviso, aviso.get_rect(center=(400, 300)))
            pygame.display.update()
            self.reloj.tick(30)
