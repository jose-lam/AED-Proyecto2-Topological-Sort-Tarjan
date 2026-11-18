from manim import *
import json


class TopologicalSortTarjan(Scene):
    def construct(self):
        self.camera.background_color = "#0F111A"

        with open("traza.json", "r", encoding="utf-8") as f:
            datos = json.load(f)

        self.mostrar_portada()           # 0:00 – 0:10 (10.0 s)
        self.animar_dag(datos["caso_dag"])   # 0:10 – 1:12 (62.0 s: 22.0 s intro + 40.0 s recorrido)
        self.animar_ciclo(datos["caso_ciclo"]) # 1:12 – 1:30 (18.0 s)
        self.mostrar_cierre()            # 1:30 – 1:45 (15.0 s)

    def mostrar_portada(self):
        # Duración exacta: 1.2 + 1.2 + 6.6 + 1.0 = 10.0 s
        titulo = Text(
            "Topological Sort (Algoritmo de Tarjan)",
            font_size=40,
            weight=BOLD,
            color="#38BDF8"
        ).shift(UP * 1.45)

        subtitulo = Text(
            "Ordenamiento Topológico mediante DFS y Tiempos de Finalización",
            font_size=23,
            color="#E2E8F0"
        ).next_to(titulo, DOWN, buff=0.35)

        linea = Line(
            LEFT * 4.8, RIGHT * 4.8, color="#38BDF8", stroke_width=2
        ).next_to(subtitulo, DOWN, buff=0.4)

        integrantes = VGroup(
            Text("Integrantes:", font_size=22, weight=BOLD, color="#FACC15"),
            Text("• José Enrique Hilario Ruiz Lam", font_size=21, color="#F8FAFC"),
            Text("• Francesco Aroldo Ferrante Quino", font_size=21, color="#F8FAFC"),
            Text("• Osmar Armengol Vilchez Aguirre", font_size=21, color="#F8FAFC"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(linea, DOWN, buff=0.45)

        curso = Text(
            "CS2023 Algoritmos y Estructuras de Datos — UTEC (2026-2)",
            font_size=18,
            color="#94A3B8"
        ).to_edge(DOWN, buff=0.45)

        self.play(
            FadeIn(titulo, shift=UP * 0.3),
            FadeIn(subtitulo, shift=UP * 0.2),
            run_time=1.2
        )
        self.play(
            Create(linea),
            FadeIn(integrantes, shift=UP * 0.2),
            FadeIn(curso),
            run_time=1.2
        )
        self.wait(6.6)
        self.play(
            FadeOut(VGroup(titulo, subtitulo, linea, integrantes, curso)),
            run_time=1.0
        )

    def color_por_estado(self, estado):
        if estado == 0:
            return "#F8FAFC", "#0F111A"  # Blanco (No visitado)
        elif estado == 1:
            return "#FACC15", "#0F111A"  # Amarillo (En proceso)
        else:
            return "#22C55E", "#0F111A"  # Verde (Terminado)

    def animar_dag(self, caso):
        # Duración exacta:
        #   Intro conceptual (0:10 – 0:32): 1.0 + 2.0 + 19.0 = 22.0 s
        #   Recorrido paso a paso (0:32 – 1:12): 40.0 s
        header = Text(
            caso["titulo"], font_size=28, weight=BOLD, color="#38BDF8"
        ).to_edge(UP, buff=0.3)
        estado_txt = Text(
            "Grafo Dirigido Acíclico (DAG) de prerrequisitos universitarios",
            font_size=18,
            color="#CBD5E1"
        ).next_to(header, DOWN, buff=0.2)

        self.play(FadeIn(header), FadeIn(estado_txt), run_time=1.0)

        # Disposición por capas topológicas sin cruce de aristas:
        # 0:PROG1 -> 2:PROG2 -> {4:PROG3 -> 3:AED, 1:BD1} -> 5:BD2
        posiciones = {
            0: np.array([-5.8,  0.0,  0.0]),  # 0: PROG1
            2: np.array([-4.1,  0.0,  0.0]),  # 2: PROG2
            4: np.array([-2.3,  1.35, 0.0]),  # 4: PROG3
            1: np.array([-2.3, -1.35, 0.0]),  # 1: BD1
            3: np.array([-0.5,  1.35, 0.0]),  # 3: AED
            5: np.array([ 1.1,  0.0,  0.0]),  # 5: BD2
        }

        nodos_circ = {}
        nodos_lbl = {}
        tiempos_lbl = {}
        grupos_nodos = VGroup()

        for i in range(caso["n"]):
            pos = posiciones[i]
            fill_c, txt_c = self.color_por_estado(0)
            circ = Circle(
                radius=0.42,
                fill_color=fill_c,
                fill_opacity=1.0,
                stroke_color="#94A3B8",
                stroke_width=2.5
            ).move_to(pos)

            partes = caso["etiquetas"][i].split(": ")
            etq_corta = f"{partes[0]}\n{partes[1]}" if len(partes) > 1 else caso["etiquetas"][i]
            lbl = Text(etq_corta, font_size=15, weight=BOLD, color=txt_c).move_to(pos)

            t_lbl = Text("tin:- | tout:-", font_size=13, color="#94A3B8")
            t_lbl.next_to(circ, UP if pos[1] > 0 else DOWN, buff=0.14)

            nodos_circ[i] = circ
            nodos_lbl[i] = lbl
            tiempos_lbl[i] = t_lbl
            grupos_nodos.add(VGroup(circ, lbl, t_lbl))

        aristas_mob = {}
        grupo_aristas = VGroup()
        for u, v in caso["aristas"]:
            flecha = Arrow(
                posiciones[u],
                posiciones[v],
                buff=0.46,
                color="#64748B",
                stroke_width=3,
                max_tip_length_to_length_ratio=0.16
            )
            aristas_mob[(u, v)] = flecha
            grupo_aristas.add(flecha)

        panel_box = RoundedRectangle(
            corner_radius=0.15,
            width=4.2,
            height=5.1,
            stroke_color="#334155",
            fill_color="#1E293B",
            fill_opacity=0.65
        ).move_to([4.35, -0.25, 0])

        panel_titulo = Text(
            "Pila de Finalización (tout)",
            font_size=18,
            weight=BOLD,
            color="#FACC15"
        ).move_to([4.35, 1.95, 0])

        leyenda = VGroup(
            VGroup(Dot(color="#F8FAFC", radius=0.08), Text("0: No visitado", font_size=14, color="#CBD5E1")).arrange(RIGHT, buff=0.1),
            VGroup(Dot(color="#FACC15", radius=0.08), Text("1: En proceso", font_size=14, color="#CBD5E1")).arrange(RIGHT, buff=0.1),
            VGroup(Dot(color="#22C55E", radius=0.08), Text("2: Terminado", font_size=14, color="#CBD5E1")).arrange(RIGHT, buff=0.1),
        ).arrange(RIGHT, buff=0.35).move_to([-2.35, -3.25, 0])

        self.play(
            Create(grupo_aristas),
            FadeIn(grupos_nodos),
            FadeIn(panel_box),
            FadeIn(panel_titulo),
            FadeIn(leyenda),
            run_time=2.0
        )
        # Pausa para la introducción conceptual (0:13 – 0:32)
        self.wait(19.0)

        pila_items = []
        base_y = -2.15
        step_y = 0.68

        # Recorrido paso a paso (0:32 – 1:12 = 40.0 s exactos):
        # 6 iniciar_nodo * 1.40s = 8.40s
        # 5 explorar_arista * (0.80 + 0.40) = 6.00s
        # 1 arista_visitada * (0.90 + 0.50) = 1.40s
        # 6 finalizar_nodo * 2.10s = 12.60s
        # 1 resultado_final: 2.20s + 8.20s wait = 10.40s
        # FadeOut final: 1.20s  -> Total = 40.00s
        for ev in caso["eventos"]:
            tipo = ev["tipo"]
            nuevo_txt = Text(ev["mensaje"], font_size=18, color="#E2E8F0").next_to(header, DOWN, buff=0.2)

            if tipo == "iniciar_nodo":
                u = ev["u"]
                fill_c, txt_c = self.color_por_estado(1)
                nuevo_t = Text(
                    f"tin:{ev['tin']} | tout:-",
                    font_size=13,
                    weight=BOLD,
                    color="#FACC15"
                ).move_to(tiempos_lbl[u])

                self.play(
                    Transform(estado_txt, nuevo_txt),
                    nodos_circ[u].animate.set_fill(fill_c).set_stroke("#FACC15", width=3.5),
                    nodos_lbl[u].animate.set_color(txt_c),
                    Transform(tiempos_lbl[u], nuevo_t),
                    run_time=1.40
                )

            elif tipo == "explorar_arista":
                u, v = ev["u"], ev["v"]
                flecha = aristas_mob[(u, v)]
                self.play(
                    Transform(estado_txt, nuevo_txt),
                    flecha.animate.set_color("#38BDF8").set_stroke(width=4.5),
                    run_time=0.80
                )
                self.play(
                    flecha.animate.set_color("#94A3B8").set_stroke(width=3),
                    run_time=0.40
                )

            elif tipo == "arista_visitada":
                u, v = ev["u"], ev["v"]
                flecha = aristas_mob[(u, v)]
                self.play(
                    Transform(estado_txt, nuevo_txt),
                    flecha.animate.set_color("#22C55E").set_stroke(width=4.5),
                    run_time=0.90
                )
                self.play(
                    flecha.animate.set_color("#64748B").set_stroke(width=3),
                    run_time=0.50
                )

            elif tipo == "finalizar_nodo":
                u = ev["u"]
                fill_c, txt_c = self.color_por_estado(2)
                nuevo_t = Text(
                    f"tin:{ev['tin']} | tout:{ev['tout']}",
                    font_size=13,
                    weight=BOLD,
                    color="#22C55E"
                ).move_to(tiempos_lbl[u])

                idx = len(pila_items)
                target_pos = np.array([4.35, base_y + idx * step_y, 0])
                card = RoundedRectangle(
                    corner_radius=0.1,
                    width=3.65,
                    height=0.52,
                    fill_color="#22C55E",
                    fill_opacity=0.22,
                    stroke_color="#22C55E",
                    stroke_width=2
                )
                card_txt = Text(
                    f"{caso['etiquetas'][u]}   (tout = {ev['tout']})",
                    font_size=15,
                    weight=BOLD,
                    color="#F8FAFC"
                )
                item = VGroup(card, card_txt).move_to(posiciones[u]).scale(0.5)

                self.play(
                    Transform(estado_txt, nuevo_txt),
                    nodos_circ[u].animate.set_fill(fill_c).set_stroke("#22C55E", width=3.5),
                    nodos_lbl[u].animate.set_color(txt_c),
                    Transform(tiempos_lbl[u], nuevo_t),
                    item.animate.scale(2.0).move_to(target_pos),
                    run_time=2.10
                )
                pila_items.append(item)

            elif tipo == "resultado_final" and ev["es_dag"]:
                nuevo_panel_titulo = Text(
                    "Orden Topológico Final",
                    font_size=18,
                    weight=BOLD,
                    color="#38BDF8"
                ).move_to(panel_titulo)

                anims_reverso = []
                n_items = len(pila_items)
                for i, item in enumerate(pila_items):
                    rev_idx = n_items - 1 - i
                    nueva_pos = np.array([4.35, base_y + rev_idx * step_y, 0])
                    anims_reverso.append(item.animate.move_to(nueva_pos))
                    anims_reverso.append(
                        item[0].animate.set_stroke("#38BDF8").set_fill("#38BDF8", opacity=0.25)
                    )

                self.play(
                    Transform(estado_txt, nuevo_txt),
                    Transform(panel_titulo, nuevo_panel_titulo),
                    *anims_reverso,
                    run_time=2.20
                )
                self.wait(8.20)

        todo_dag = VGroup(
            header, estado_txt, grupo_aristas, grupos_nodos,
            panel_box, panel_titulo, leyenda, *pila_items
        )
        self.play(FadeOut(todo_dag), run_time=1.20)

    def animar_ciclo(self, caso):
        # Duración exacta (1:12 – 1:30):
        # 0.90 + 1.50 + 4*1.15 + 3*0.80 + (1.30 + 1.20 + 5.10) + 1.00 = 18.0 s
        header = Text(
            caso["titulo"], font_size=28, weight=BOLD, color="#F87171"
        ).to_edge(UP, buff=0.3)
        estado_txt = Text(
            "Evaluando dependencias con ciclo dirigido...",
            font_size=18,
            color="#CBD5E1"
        ).next_to(header, DOWN, buff=0.2)

        self.play(FadeIn(header), FadeIn(estado_txt), run_time=0.90)

        posiciones = {
            0: np.array([-4.3, 1.2, 0]),
            1: np.array([-0.8, 1.2, 0]),
            2: np.array([-0.8, -1.2, 0]),
            3: np.array([-4.3, -1.2, 0]),
        }

        nodos_circ = {}
        nodos_lbl = {}
        tiempos_lbl = {}
        grupos_nodos = VGroup()

        for i in range(caso["n"]):
            pos = posiciones[i]
            fill_c, txt_c = self.color_por_estado(0)
            circ = Circle(
                radius=0.42,
                fill_color=fill_c,
                fill_opacity=1.0,
                stroke_color="#94A3B8",
                stroke_width=2.5
            ).move_to(pos)
            lbl = Text(
                caso["etiquetas"][i].replace(": ", "\n"),
                font_size=15,
                weight=BOLD,
                color=txt_c
            ).move_to(pos)
            t_lbl = Text("tin:- | tout:-", font_size=14, color="#94A3B8")
            t_lbl.next_to(circ, UP if pos[1] > 0 else DOWN, buff=0.14)

            nodos_circ[i] = circ
            nodos_lbl[i] = lbl
            tiempos_lbl[i] = t_lbl
            grupos_nodos.add(VGroup(circ, lbl, t_lbl))

        aristas_mob = {}
        grupo_aristas = VGroup()
        for u, v in caso["aristas"]:
            flecha = Arrow(
                posiciones[u],
                posiciones[v],
                buff=0.46,
                color="#64748B",
                stroke_width=3,
                max_tip_length_to_length_ratio=0.15
            )
            aristas_mob[(u, v)] = flecha
            grupo_aristas.add(flecha)

        aviso_box = RoundedRectangle(
            corner_radius=0.15,
            width=4.8,
            height=3.4,
            stroke_color="#475569",
            fill_color="#1E293B",
            fill_opacity=0.75
        ).move_to([3.8, 0.0, 0])

        aviso_titulo = Text(
            "Monitor de Recursión DFS",
            font_size=19,
            weight=BOLD,
            color="#FACC15"
        ).move_to([3.8, 1.25, 0])

        aviso_cuerpo = Text(
            "Explorando nodos\nen estado 1 (amarillo)...",
            font_size=17,
            color="#E2E8F0",
            line_spacing=1.25
        ).move_to([3.8, -0.1, 0])

        self.play(
            Create(grupo_aristas),
            FadeIn(grupos_nodos),
            FadeIn(aviso_box),
            FadeIn(aviso_titulo),
            FadeIn(aviso_cuerpo),
            run_time=1.50
        )

        for ev in caso["eventos"]:
            tipo = ev["tipo"]
            nuevo_txt = Text(ev["mensaje"], font_size=18, color="#E2E8F0").next_to(header, DOWN, buff=0.2)

            if tipo == "iniciar_nodo":
                u = ev["u"]
                fill_c, txt_c = self.color_por_estado(1)
                nuevo_t = Text(
                    f"tin:{ev['tin']} | tout:-",
                    font_size=14,
                    weight=BOLD,
                    color="#FACC15"
                ).move_to(tiempos_lbl[u])

                self.play(
                    Transform(estado_txt, nuevo_txt),
                    nodos_circ[u].animate.set_fill(fill_c).set_stroke("#FACC15", width=3.5),
                    nodos_lbl[u].animate.set_color(txt_c),
                    Transform(tiempos_lbl[u], nuevo_t),
                    run_time=1.15
                )

            elif tipo == "explorar_arista":
                u, v = ev["u"], ev["v"]
                flecha = aristas_mob[(u, v)]
                self.play(
                    Transform(estado_txt, nuevo_txt),
                    flecha.animate.set_color("#38BDF8").set_stroke(width=4.5),
                    run_time=0.80
                )

            elif tipo == "ciclo_detectado":
                u, v = ev["u"], ev["v"]
                flecha_ciclo = aristas_mob[(u, v)]
                nuevo_aviso_t = Text(
                    "¡CICLO DIRIGIDO DETECTADO!",
                    font_size=19,
                    weight=BOLD,
                    color="#EF4444"
                ).move_to(aviso_titulo)

                nuevo_aviso_c = Text(
                    f"Arista ({u} → {v}) apunta a un\nnodo en estado == 1 (amarillo).\n\nOrden Topológico INVÁLIDO.",
                    font_size=16,
                    color="#FCA5A5",
                    line_spacing=1.25
                ).move_to(aviso_cuerpo)

                self.play(
                    Transform(estado_txt, nuevo_txt),
                    flecha_ciclo.animate.set_color("#EF4444").set_stroke(width=6),
                    nodos_circ[v].animate.set_stroke("#EF4444", width=5),
                    aviso_box.animate.set_stroke("#EF4444", width=3),
                    Transform(aviso_titulo, nuevo_aviso_t),
                    Transform(aviso_cuerpo, nuevo_aviso_c),
                    run_time=1.30
                )
                self.play(
                    Indicate(flecha_ciclo, color="#EF4444", scale_factor=1.12),
                    Indicate(nodos_circ[v], color="#EF4444"),
                    run_time=1.20
                )
                self.wait(5.10)

        todo_ciclo = VGroup(
            header, estado_txt, grupo_aristas, grupos_nodos,
            aviso_box, aviso_titulo, aviso_cuerpo
        )
        self.play(FadeOut(todo_ciclo), run_time=1.00)

    def mostrar_cierre(self):
        # Duración exacta (1:30 – 1:45): 1.00 + 1.50 + 11.30 + 1.20 = 15.0 s
        titulo = Text(
            "Análisis de Complejidad — Tarjan (DFS)",
            font_size=32,
            weight=BOLD,
            color="#38BDF8"
        ).to_edge(UP, buff=0.7)

        card_tiempo = RoundedRectangle(
            corner_radius=0.15,
            width=5.6,
            height=2.5,
            stroke_color="#22C55E",
            fill_color="#1E293B",
            fill_opacity=0.8
        ).shift(LEFT * 3.1 + UP * 0.2)
        t_head = Text("Complejidad Temporal", font_size=22, weight=BOLD, color="#22C55E").move_to(card_tiempo.get_top() + DOWN * 0.45)
        t_math = MathTex(r"\mathcal{O}(|V| + |E|)", font_size=40, color="#F8FAFC").move_to(card_tiempo.get_center() + DOWN * 0.05)
        t_desc = Text("Cada vértice y arista se visitan una vez", font_size=16, color="#CBD5E1").move_to(card_tiempo.get_bottom() + UP * 0.4)

        card_espacio = RoundedRectangle(
            corner_radius=0.15,
            width=5.6,
            height=2.5,
            stroke_color="#FACC15",
            fill_color="#1E293B",
            fill_opacity=0.8
        ).shift(RIGHT * 3.1 + UP * 0.2)
        e_head = Text("Complejidad Espacial", font_size=22, weight=BOLD, color="#FACC15").move_to(card_espacio.get_top() + DOWN * 0.45)
        e_math = MathTex(r"\mathcal{O}(|V|) \text{ aux. } / \ \mathcal{O}(|V| + |E|)", font_size=30, color="#F8FAFC").move_to(card_espacio.get_center() + DOWN * 0.05)
        e_desc = Text("Arreglos estado, tin, tout y pila DFS", font_size=16, color="#CBD5E1").move_to(card_espacio.get_bottom() + UP * 0.4)

        creditos = Text(
            "Equipo: [INTEGRANTE 1] • [INTEGRANTE 2] • [INTEGRANTE 3]  |  UTEC — CS2023",
            font_size=18,
            color="#94A3B8"
        ).to_edge(DOWN, buff=0.6)

        self.play(FadeIn(titulo, shift=DOWN * 0.2), run_time=1.00)
        self.play(
            FadeIn(VGroup(card_tiempo, t_head, t_math, t_desc), shift=UP * 0.2),
            FadeIn(VGroup(card_espacio, e_head, e_math, e_desc), shift=UP * 0.2),
            FadeIn(creditos),
            run_time=1.50
        )
        self.wait(11.30)
        self.play(
            FadeOut(VGroup(titulo, card_tiempo, t_head, t_math, t_desc, card_espacio, e_head, e_math, e_desc, creditos)),
            run_time=1.20
        )
