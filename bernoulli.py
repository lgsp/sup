from manim import *
import manim
from math import e, pi
import math
from PIL import Image

def disp_sub(self, lang):
    if lang.lower() == "en":
        written, phon = "Subscribe", "/səbˈskraɪb/"
        sub_pic = SVGMobject("/Users/digitalnomad/Documents/pics/svg/subscribe.svg")
        sub_scale = 0.8 
    elif lang.lower() == "fr":
        written, phon = "Abonnez-vous", "/abɔne vu/"
        sub_pic = ImageMobject("/Users/digitalnomad/Documents/pics/png/sabonner.png")
        sub_scale = 0.45
    elif lang.lower() == "ru":
        written, phon = "Подпишитесь", "/pɐd'piʂitʲɪsʲ/"

    sub = Paragraph(written, phon, line_spacing=0.5)
    self.play(GrowFromCenter(sub))
    self.wait(.5)
    self.play(FadeOut(sub))
    self.add(sub_pic.scale(sub_scale))
    self.wait(.5)

    
def disp_full_part_full(self, full, part, images, lang, full_scale=1):
    self.play(Write(full.scale(full_scale), run_time = 5))
    self.wait(.5)
    self.play(FadeOut(full))

    for img in images:
        pic = ImageMobject(img)
        self.add(pic.scale(0.25))
        self.wait(.5)
        self.remove(pic)
        
    self.play(Write(part.scale(full_scale), run_time = 3))
    self.wait(.5)
        
    self.play(ReplacementTransform(part, full), run_time=3)
    self.wait(.5)
    self.play(FadeOut(full))
    
    disp_sub(self, lang)


    
def inbox_msg(*inboxes, font_size):
    msg_text = ""
    for inbox in inboxes:
        msg_text += r"\mbox{" + f"{inbox}" + r"} \\"
    msg = MathTex(
        msg_text,
        tex_template=TexFontTemplates.french_cursive,
        font_size=font_size
    )
    return msg



def get_regular_polygon(n_gon):
    angle = (360 / n_gon) * DEGREES
    poly_n_gon = RegularPolygon(
        n = n_gon,
        start_angle = angle,
        color = RED
    )
    return poly_n_gon    



def replace_and_write(self, old, new, pos_ref, duration, **lines_and_scales):
    to_be_continued = False
    m, n = len(old), len(new)
    min_mn = m
    keys = lines_and_scales.keys()
    
    if m < n:
        to_be_continued = True
        min_mn = m
    elif m > n:
        self.play(*[FadeOut(old[i]) for i in range(n, m)])
        to_be_continued = False
        min_mn = n
    else: min_mn = m
    
    if lines_and_scales == {}:
        self.play(
            ReplacementTransform(
                old[0], new[0].next_to(pos_ref, 3 * DOWN)
            ),
            *[
                ReplacementTransform(
                    old[i],
                    new[i].next_to(new[i-1], DOWN)
                ) for i in range(1, min_mn)
            ]
        )
        if to_be_continued:
            self.play(
                *[
                    Write(new[i].next_to(new[i-1], DOWN)
                          ) for i in range(min_mn, n)
                ]
            )
    else:
        self.play(
            *[
                ReplacementTransform(
                old[0],
                new[0].scale(
                    lines_and_scales['0']
                ).next_to(pos_ref, 3 * DOWN)
                ) for i in range(1) if '0' in keys
              ],
            *[
                ReplacementTransform(
                old[0],
                new[0].next_to(pos_ref, 3 * DOWN)
                ) for i in range(1) if '0' not in keys
              ],
            *[
                ReplacementTransform(
                    old[i],
                    new[i].scale(
                        lines_and_scales[str(i)]
                    ).next_to(new[i - 1], DOWN)
                ) for i in range(1, min_mn) if str(i) in keys
            ],
            *[
                ReplacementTransform(
                    old[i],
                    new[i].next_to(new[i-1], DOWN)
                ) for i in range(1, min_mn) if str(i) not in keys
            ],
        )
        if to_be_continued:
            self.play(
                *[
                    Write(
                        new[i].scale(
                            lines_and_scales[str(i)]).next_to(
                                new[i - 1], DOWN)
                    ) for i in range(min_mn, n) if str(i) in keys
                ],
                *[
                    Write(
                        new[i].next_to(new[i - 1], DOWN)
                    ) for i in range(min_mn, n) if not str(i) in keys
                ],
            )
    
    self.wait(duration)


    
    
def cursive_msg(phrase, sep, font_size=40):
    inboxes = phrase.split(sep)
    msg = inbox_msg(*inboxes, font_size=font_size)
    return msg



def targets_to_write(text, ref, size=1, direction=DOWN):
    #text = [Text(t) for t in text if isinstance(t, str)]
    n = len(text)
    # Create a list of target objects
    targets = [text[0].next_to(ref, size * direction)]
    targets += [
        text[i].next_to(
            text[i - 1],
            size * direction
        ) for i in range(1, n)
    ]
    return text

def disp_calculations(self, previous_mobj, calcs, next2obj, direction):
            """
            This function replace previous_mobj with calcs next2obj
            
            previous_mobj: mobj to replace
            calcs: calculations to display
            next2obj: obj nearby to display
            direction: direction from next2obj
            """
            if previous_mobj:
                self.play(
                    ReplacementTransform(
                        previous_mobj,
                        calcs[0].next_to(next2obj, direction)
                    )
                )
            else:
                self.play(
                    Write(calcs[0].next_to(next2obj, direction))
                )
            self.wait(2)
            for i in range(len(calcs) - 1):
                self.play(
                    ReplacementTransform(
                        calcs[i],
                        calcs[i+1].next_to(next2obj, direction)
                    )
                )
                self.wait(2)

def disp_tex_list(self, previous_mobj, tex_list, next2obj, direction):
            """
            This function replace previous_mobj with tex_list next2obj
            
            previous_mobj: mobj to replace
            tex_list: list with Tex mobjs to display
            next2obj: obj nearby to display
            direction: direction from next2obj
            """
            if previous_mobj:
                self.play(
                    ReplacementTransform(
                        previous_mobj,
                        tex_list[0].next_to(next2obj, direction)
                    )
                )
            else:
                self.play(
                    Write(tex_list[0].next_to(next2obj, direction))
                )
            self.wait(2)
            for i in range(len(tex_list) - 1):
                self.play(
                    Write(
                        tex_list[i+1].next_to(tex_list[i], direction)
                    )
                )
                self.wait(2)
                
##################################################
# 
##################################################

# Pile ou Face
class Part1HT(Scene):
    def construct(self):
        msg1 = "Loi de Bernoulli (partie 1)"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        intro = [
            r"Imaginez que vous lancez une pièce de monnaie parfaitement équilibrée",
            r"alors vous avez une chance sur deux qu'elle tombe sur pile",
            r"et une chance sur deux qu'elle tombe sur face."
        ]

        intro_tex = [Tex(i).scale(0.85) for i in intro]
        introVGroup = VGroup(*intro_tex)
        
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=intro_tex,
            next2obj=title1,
            direction=DOWN
        )

        # s = "Lancer"
        # p = "Pile"
        # f = "Face"
        # graph = Graph(
        #     [s, prob, prob, p, f],
        #     [(s, p), (s, f)],
        #     layout="tree",
        #     layout_config={"root_vertex": s},
        #     labels=True
        # ).scale(0.75)
        # self.play(Write(graph.next_to(intro_tex[-1], DOWN)))
        # self.wait()

        ax = Axes().add_coordinates()

        # Origine
        o = Dot(ax.coords_to_point(2, 2))
        
        # Pile
        p = Dot(ax.coords_to_point(6, 4))
        p_lab = Tex(r"Pile").next_to(p, RIGHT)
        
        op = Line(o, p)
        p_p = MathTex(r"\dfrac{1}{2}").next_to(op, UP)
        
        # Face
        f = Dot(ax.coords_to_point(6, 0))
        f_lab = Tex(r"Face").next_to(f, RIGHT)
        
        of = Line(o, f)
        of_p = MathTex(r"\dfrac{1}{2}").next_to(of, DOWN)

        tree = VGroup(o, p, p_lab, op, p_p, f, f_lab, of, of_p)
        self.play(
            Write(tree.scale(0.75).next_to(intro_tex[-1], DOWN))
        )
        self.wait()

        codage = [
            r"Améliorons la représentation en utilisant une variable aléatoire",
            r"qu'on notera \(X\) et on va coder \(X = 1\) pour obtenir pile",
            r"et \(X = 0\) pour obtenir face. Ainsi on obtient le nouvel arbre"
        ]
        codage_tex = [Tex(c).scale(0.85) for c in codage]
        codageVGroup = VGroup(*codage_tex)
        
        disp_tex_list(self, 
            previous_mobj=introVGroup,
            tex_list=codage_tex,
            next2obj=title1,
            direction=DOWN
        )

        ax = Axes().add_coordinates()

        # Origine
        o = Dot(ax.coords_to_point(2, 2))
        
        # Pile
        p = Dot(ax.coords_to_point(6, 4))
        p_lab = Tex(r"X = 1").next_to(p, RIGHT)
        
        op = Line(o, p)
        p_p = MathTex(r"\dfrac{1}{2}").next_to(op, UP)
        
        # Face
        f = Dot(ax.coords_to_point(6, 0))
        f_lab = Tex(r"X = 0").next_to(f, RIGHT)
        
        of = Line(o, f)
        of_p = MathTex(r"\dfrac{1}{2}").next_to(of, DOWN)

        tree2 = VGroup(o, p, p_lab, op, p_p, f, f_lab, of, of_p)
        self.play(
            ReplacementTransform(
                tree,
                tree2.scale(0.75).next_to(codage_tex[-1], DOWN)
            )
        )
        self.wait()

        tableau = [
            r"En fait, on peut même remplacer l'arbre par un tableau",
            r"une ligne pour les valeurs de \(X\) et une ligne pour les probabilités"
        ]
        tableau_tex = [Tex(t).scale(0.85) for t in tableau]
        tableauVGroup = VGroup(*tableau_tex)
        
        disp_tex_list(self, 
            previous_mobj=codageVGroup,
            tex_list=tableau_tex,
            next2obj=title1,
            direction=DOWN
        )

        x_vals = [0, 1]
        y_vals = [r"\dfrac{1}{2}", r"\dfrac{1}{2}"]
        t0 = MathTable(
            [x_vals, y_vals],
            row_labels=[MathTex(r"X = k"), MathTex(r"P(X = k)")],
            h_buff=1,
        )

        self.play(
            ReplacementTransform(tree2, t0.next_to(tableau_tex[-1], DOWN))
        )
        self.wait()

        tableau2 = [
            r"Toute situation binaire peut être modélisée par une loi de Bernoulli",
            r"gagner ou ne pas gagner, réussir ou échouer une épreuve de Benoulli",
            r"avec une probabilité \(p\)"
        ]
        tableau2_tex = [Tex(t).scale(0.85) for t in tableau2]
        tableau2VGroup = VGroup(*tableau2_tex)
        
        disp_tex_list(self, 
            previous_mobj=tableauVGroup,
            tex_list=tableau2_tex,
            next2obj=title1,
            direction=DOWN
        )

        x_vals = [0, 1]
        y_vals = [r"1 - p", r"p"]
        t1 = MathTable(
            [x_vals, y_vals],
            row_labels=[MathTex(r"X = k"), MathTex(r"P(X = k)")],
            h_buff=1,
        )

        self.play(
            ReplacementTransform(t0, t1.next_to(tableau2_tex[-1], DOWN))
        )
        self.wait()

        expectation = [
            r"D'où l'espérance, \(E(X) = 0\times P(X = 0) + 1\times P(X = 1)\)",
            r"Ainsi \(E(X) = P(X = 1)\)",
            r"\(E(X) = p\)"
        ]
        expectation_tex = [Tex(t).scale(0.85) for t in expectation]
        expectationVGroup = VGroup(*expectation_tex)
        
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=expectation_tex,
            next2obj=t1,
            direction=DOWN
        )

        self.play(
            Indicate(expectation_tex[-1], color=RED),
        )
        self.wait()

        self.play(
            Circumscribe(expectation_tex[-1], color=RED),
        )
        self.wait()


        
        disp_sub(self, lang="fr")

# Part 2        
class Part2HT(Scene):
    def construct(self):
        msg1 = "Loi de Bernoulli (partie 2)"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        konig = [
            r"Rappelons la définition de la variance.",
            r"\(V(X) = E[(X - E[X])^2]\)",
            r"\(V(X) = E[X^2 - 2XE(X) + E(X)^2]\)",
            r"Par linéarité de l'espérance : \(V(X) = E[X^2] - 2E(X)E(X) + E(X)^2\)",
            r"D'où la formule de König-Huygens : \(V(X) = E(X^2) - E(X)^2\)"
        ]

        konig_tex = [Tex(i).scale(0.85) for i in konig]
        konigVGroup = VGroup(*konig_tex)
        
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=konig_tex,
            next2obj=title1,
            direction=DOWN
        )




        x_vals = [0, 1]
        y_vals = [r"1 - p", r"p"]
        t1 = MathTable(
            [x_vals, y_vals],
            row_labels=[MathTex(r"X^2 = k^2"), MathTex(r"P(X = k)")],
            h_buff=1,
        )

        self.play(
            ReplacementTransform(konigVGroup, t1.next_to(title1, DOWN))
        )
        self.wait()

        expectation = [
            r"D'où l'espérance, \(E(X^2) = 0\times P(X = 0) + 1\times P(X = 1)\)",
            r"Ainsi \(E(X^2) = P(X = 1)\)",
            r"C'est-à-dire \(E(X^2) = p\)"
        ]
        expectation_tex = [Tex(t).scale(0.85) for t in expectation]
        expectationVGroup = VGroup(*expectation_tex)
        
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=expectation_tex,
            next2obj=t1,
            direction=DOWN
        )



        var = [
            r"Appliquons la formule de Konig-Huygens :",
            r"\(V(X) = E(X^2) - E(X)^2\)",
            r"\(V(X) = p - p^2\)",
            r"\(V(X) = p(1 - p)\)"
        ]

        var_tex = [Tex(t).scale(0.85) for t in var]
        varVGroup = VGroup(*var_tex)
        disp_tex_list(self, 
            previous_mobj=expectationVGroup,
            tex_list=var_tex,
            next2obj=t1,
            direction=DOWN
        )

        self.play(
            Indicate(var_tex[-1], color=RED),
        )
        self.wait()

        self.play(
            Circumscribe(var_tex[-1], color=RED),
        )
        self.wait()

        
        disp_sub(self, lang="fr")


# Part 3        
class Part3HT(Scene):
    def construct(self):
        msg1 = "Loi de Bernoulli (partie 3)"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        summary = [
            r"Pour résumer, on dit qu'une variable aléatoire \(X\)",
            r"suit une loi de Bernoulli de paramètre \(p\)",
            r"si \(X\) prend deux valeurs qu'on code généralement",
            r"0 pour l'échec et 1 pour le succès.",
            r"Ainsi pour \(x\in\{0 ; 1\}\) on a :",
            r"\(P(X = x) = p^x(1 - p)^{1 - x}\)",
            r"\(E(X) = p\)",
            r"\(V(X) = p(1 - p)\)"
        ]

        summary_tex = [Tex(i).scale(0.85) for i in summary]
        summaryVGroup = VGroup(*summary_tex)
        
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=summary_tex,
            next2obj=title1,
            direction=DOWN
        )

        self.play(
            Indicate(summary_tex[-3], color=RED),
            Indicate(summary_tex[-2], color=RED),
            Indicate(summary_tex[-1], color=RED),
        )
        self.wait()

        self.play(
            Circumscribe(summary_tex[-3], color=RED),
            Circumscribe(summary_tex[-2], color=RED),
            Circumscribe(summary_tex[-1], color=RED),
        )
        self.wait()

        
        disp_sub(self, lang="fr")
