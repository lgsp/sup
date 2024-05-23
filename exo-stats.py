from manim import *
import manim
from math import e, pi
import math
from PIL import Image

def disp_sub(self, lang):
    if lang.lower() == "en":
        written, phon = "Subscribe", "/səbˈskraɪb/"
        sub_pic = SVGMobject("/Users/dn/Documents/pics/svg/subscribe.svg")
        sub_scale = 0.8 
    elif lang.lower() == "fr":
        written, phon = "Abonnez-vous", "/abɔne vu/"
        sub_pic = ImageMobject("/Users/dn/Documents/pics/png/sabonner.png")
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

# Statistiques avec min = Q1
class MinQ1(Scene):
    def construct(self):
        msg1 = "Statistiques descriptives"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        intro = [
            r"Soit la série 2, 2, 3, 3, 3, 4, 4, 4, 4",
            r"dont la densité \(f\) est définie par :",
            r"\(f(x, y) = \dfrac{12}{5}x(2 - x - y)\quad \forall (x, y)\in[0 ; 1]^2\)"
        ]

        intro_tex = [Tex(i).scale(0.85) for i in intro]
        introVGroup = VGroup(*intro_tex)
        
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=intro_tex,
            next2obj=title1,
            direction=DOWN
        )
        
        q1_txt = [
            r"1. Vérifiez que \(f(x, y)\) est bien une fonction de densité",
        ]
        q1 = [Tex(t).scale(0.85) for t in q1_txt]

        q1VGroup = VGroup(*q1)
        
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=q1,
            next2obj=intro_tex[-1],
            direction=DOWN
        )
        
        rep1_txt_part1 = [
            r"Pour vérifiez que \(f\) est bien une fonction de densité",
            r"il faut calculer son intégrale sur \(\mathbb{R}^2\)",
            r"et montrer qu'elle vaut 1."
        ]
        
        rep1 = [Tex(t).scale(0.85) for t in rep1_txt_part1]
        rep1VGroup = VGroup(*rep1)
        
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=rep1,
            next2obj=q1[-1],
            direction=DOWN
        )


        rep1_txt_part2 = [
            r"\(I = \int\int_{(x, y)\in[0 ; 1]^2}\dfrac{12}{5}x(2-x-y)dxdy\)",
            r"Intégrons par rapport à \(y\) puis par rapport à \(x\) :",
            r"\(I = \dfrac{12}{5}\int_{0}^{1}\left[2xy-x^2y-\dfrac{xy^2}{2}\right]_0^1dx\)",
            r"\(I = \dfrac{12}{5}\int_{0}^{1}(2x-x^2-\dfrac{x}{2})dx\)",
            r"\(I = \dfrac{12}{5}\left[x^2-\dfrac{x^3}{3}-\dfrac{x^2}{4}\right]_0^1\)",
            r"\(I = \dfrac{12}{5}\left(1-\dfrac{1}{3}-\dfrac{1}{4}\right)\)",
            r"\(I = \dfrac{12}{5}\times\dfrac{5}{12}\)",
            r"\(I = 1\)"
        ]

        rep1_calc = [Tex(t).scale(0.85) for t in rep1_txt_part2]
        
        disp_calculations(self, 
            previous_mobj=rep1VGroup,
            calcs=rep1_calc,
            next2obj=q1[-1],
            direction=DOWN
        )
        
        box = SurroundingRectangle(rep1_calc[-1])
        self.play(Write(box))
        self.wait()

# Exo 1 Question 2
class Exo1Question2(Scene):
    def construct(self):
        msg1 = "Couple de variables aléatoires"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        intro = [
            r"Soit \((X, Y)\) un couple de variables aléatoires continues,",
            r"dont la densité \(f\) est définie par :",
            r"\(f(x,y) = \dfrac{12}{5}x(2-x-y)\quad\forall (x,y)\in[0;1]^2\)"
        ]

        intro_tex = [Tex(i).scale(0.85) for i in intro]
        introVGroup = VGroup(*intro_tex)
        
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=intro_tex,
            next2obj=title1,
            direction=DOWN
        )
        
        q2_txt = [
            r"2. Déterminez les densités marginales des variables aléatoires \(X\) et \(Y\).",
        ]
        q2 = [Tex(t).scale(0.85) for t in q2_txt]

        q2VGroup = VGroup(*q2)
        
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=q2,
            next2obj=intro_tex[-1],
            direction=DOWN
        )
        
        rep2_txt_part1 = [
            r"Pour déterminer la densité marginale de \(X\)",
            r"il faut calculer l'intégrale de la densité jointe",
            r"par rapport à \(y\) en sans donner de valeur à \(x\).",
            r"Pour celle de \(Y\) c'est l'inverse."
        ]
        
        rep2 = [Tex(t).scale(0.85) for t in rep2_txt_part1]
        rep2VGroup = VGroup(*rep2)
        
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=rep2,
            next2obj=q2[-1],
            direction=DOWN
        )

        f_x = Title("Calcul de la densité marginale de \(X\)")
        self.play(
            ReplacementTransform(title1, f_x)
        )
        
        rep2_txt_part2 = [
            r"\(f_X(x) = \int_{y\in[0 ; 1]}\dfrac{12}{5}x(2-x-y)dy\)",
            r"\(f_X(x) = \dfrac{12}{5}\left[2xy-x^2y-\dfrac{xy^2}{2}\right]_0^1\)",
            r"\(f_X(x) = \dfrac{12}{5}\left(2x-x^2-\dfrac{x}{2}\right)\)",
            r"\(f_X(x) = \dfrac{12}{5}\left(\dfrac{3x}{2}-x^2\right)\)",
        ]

        rep2_calc = [Tex(t).scale(0.85) for t in rep2_txt_part2]
        
        disp_calculations(self, 
            previous_mobj=rep2VGroup,
            calcs=rep2_calc,
            next2obj=q2[-1],
            direction=DOWN
        )
        
        box = SurroundingRectangle(rep2_calc[-1])
        f_x_res = VGroup(rep2_calc[-1], box)
        self.play(Write(f_x_res))
        self.wait()

        f_y = Title("Calcul de la densité marginale de \(Y\)")
        self.play(
            f_x_res.animate.shift(4 * LEFT),
            ReplacementTransform(f_x, f_y)
        )
        
        rep2_txt_part3 = [
            r"\(f_Y(y) = \int_{x\in[0 ; 1]}\dfrac{12}{5}x(2-x-y)dx\)",
            r"\(f_Y(y) = \dfrac{12}{5}\left[x^2-\dfrac{x^3}{3}-\dfrac{x^2y}{2}\right]_0^1\)",
            r"\(f_Y(y) = \dfrac{12}{5}\left(1-\dfrac{1}{3}-\dfrac{y}{2}\right)\)",
            r"\(f_Y(y) = \dfrac{12}{5}\left(\dfrac{2}{3}-\dfrac{y}{2}\right)\)",
        ]

        rep2_calc2 = [Tex(t).scale(0.85) for t in rep2_txt_part3]
        
        disp_calculations(self, 
            previous_mobj=None,
            calcs=rep2_calc2,
            next2obj=rep2_calc[-1],
            direction=DOWN
        )
        
        box = SurroundingRectangle(rep2_calc2[-1])
        f_y_res = VGroup(rep2_calc2[-1], box)
        self.play(
            Write(f_y_res),
            f_y_res.animate.shift(4 * RIGHT)
        )
        self.wait()

        ax = Axes(
            x_range=[0, 1, 5],
            y_range=[0, 1.5, 5],
            x_length=5,
            y_length=5
        )

        curve_1 = ax.plot(lambda x: 2.4*(1.5*x - x**2), color=RED)
        curve_2 = ax.plot(lambda x: 2.4*(2/3 - x/2), color=GREEN)
        ax_and_curves = VGroup(ax, curve_1, curve_2)
        
        label_1 = ax.get_graph_label(
            curve_1,
            "f_X",
            x_val=0.5,
            direction=0.25 * UP
        )
        label_2 = ax.get_graph_label(
            curve_2,
            "f_Y",
            x_val=0.5,
            direction=2.25 * DOWN
        )
        labels = VGroup(label_1, label_2)
        
        intro_qVGroup = VGroup(introVGroup, q2VGroup)
        
        self.play(
            f_x_res.animate.shift(DOWN).scale(0.75),
            f_y_res.animate.shift(4 * RIGHT).scale(0.75),
            ReplacementTransform(
                intro_qVGroup,
                ax_and_curves.next_to(f_y, DOWN).scale(0.75)
            ),
            Write(labels)
        )
        self.wait()

# Exo 1 Question 3        
class Exo1Question3(Scene):
    def construct(self):
        msg1 = "Couple de variables aléatoires"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        intro = [
            r"Soit \((X, Y)\) un couple de variables aléatoires continues,",
            r"dont la densité \(f\) est définie par :",
            r"\(f(x,y) = \dfrac{12}{5}x(2-x-y)\quad\forall (x,y)\in[0;1]^2\)"
        ]

        intro_tex = [Tex(i).scale(0.85) for i in intro]
        introVGroup = VGroup(*intro_tex)
        
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=intro_tex,
            next2obj=title1,
            direction=DOWN
        )
        
        q3_txt = [
            r"3. Les variables aléatoires \(X\) et \(Y\) ",
            r"sont-elles indépendantes ?",
        ]
        q3 = [Tex(t).scale(0.85) for t in q3_txt]

        q3VGroup = VGroup(*q3)
        
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=q3,
            next2obj=intro_tex[-1],
            direction=DOWN
        )
        
        rep3_txt_part1 = [
            r"Pour déterminer si des variables aléatoires",
            r"sont indépendantes on peut utiliser la relation",
            r"\(f_{X, Y}(x, y) = f_X(x)f_Y(y) \iff E(XY) = E(X)E(Y)\)",
        ]
        
        rep3 = [Tex(t).scale(0.85) for t in rep3_txt_part1]
        rep3VGroup = VGroup(*rep3)
        
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=rep3,
            next2obj=q3[-1],
            direction=DOWN
        )

        e_x = Title("Calcul de l'espérance de \(X\)")
        self.play(
            ReplacementTransform(title1, e_x)
        )
        
        rep3_txt_part2 = [
            r"\(E(X) = \int_{[0,1]}xf_X(x)dx\)",
            r"\(E(X) = \dfrac{12}{5}\left[\dfrac{1}{2}x^3-\dfrac{x^4}{4}\right]_0^1\)",
            r"\(E(X) = \dfrac{12}{5}\left(\dfrac{1}{2} - \dfrac{1}{4}\right)\)",
            r"\(E(X) = \dfrac{12}{5}\times\dfrac{1}{4}\)",
            r"\(E(X) = \dfrac{3}{5}\)",
        ]

        rep3_calc = [Tex(t).scale(0.85) for t in rep3_txt_part2]
        
        disp_calculations(self, 
            previous_mobj=rep3VGroup,
            calcs=rep3_calc,
            next2obj=q3[-1],
            direction=DOWN
        )
        
        box = SurroundingRectangle(rep3_calc[-1])
        e_x_res = VGroup(rep3_calc[-1], box)
        self.play(
            Write(box),
            e_x_res.animate.shift(4 * LEFT)
        )
        self.wait()

        
        e_y = Title("Calcul de l'espérance de \(Y\)")
        self.play(
            ReplacementTransform(e_x, e_y)
        )
        
        rep3_txt_part3 = [
            r"\(E(Y) = \int_{[0,1]}yf_Y(y)dy\)",
            r"\(E(Y) = \dfrac{12}{5}\left[\dfrac{1}{3}y^2-\dfrac{y^3}{6}\right]_0^1\)",
            r"\(E(Y) = \dfrac{12}{5}\left(\dfrac{1}{3} - \dfrac{1}{6}\right)\)",
            r"\(E(Y) = \dfrac{12}{5}\times\dfrac{1}{6}\)",
            r"\(E(Y) = \dfrac{2}{5}\)",
        ]

        rep3_calc2 = [Tex(t).scale(0.85) for t in rep3_txt_part3]
        
        disp_calculations(self, 
            previous_mobj=rep3VGroup,
            calcs=rep3_calc2,
            next2obj=q3[-1],
            direction=DOWN
        )
        
        box = SurroundingRectangle(rep3_calc2[-1])
        e_y_res = VGroup(rep3_calc2[-1], box)
        self.play(
            Write(box),
            e_y_res.animate.shift(4 * RIGHT)
        )
        self.wait()

        
        e_xy = Title("Calcul de l'espérance de \(XY\)")
        self.play(
            ReplacementTransform(e_y, e_xy)
        )
        
        rep3_txt_part4 = [
            r"\(E(XY) = \int\int_{[0;1]^2}xyf_{X,Y}(x, y)dxdy\)",
            r"\(E(XY) = \dfrac{12}{5}\int\int_{[0;1]^2}x^2y(2 - x - y)dxdy\)",
            r"\(E(XY) = \dfrac{12}{5}\int_{[0;1]}\left[x^2y^2 - \dfrac{1}{2}x^3y^2 - \dfrac{1}{3}x^2y^3\right]_0^1dx\)",
            r"\(E(XY) = \dfrac{12}{5}\int_{[0;1]}\left(x^2 - \dfrac{1}{2}x^3 - \dfrac{1}{3}x^2\right)dx\)",
            r"\(E(XY) = \dfrac{12}{5}\left[\dfrac{1}{3}x^3 - \dfrac{1}{8}x^4 - \dfrac{1}{9}x^3\right]_0^1\)",
            r"\(E(XY) = \dfrac{12}{5}\left(\dfrac{1}{3} - \dfrac{1}{8} - \dfrac{1}{9}\right)\)",
            r"\(E(XY) = \dfrac{12}{5}\times\dfrac{7}{36}\)",
            r"\(E(XY) = \dfrac{7}{15}\)",
        ]

        rep3_calc3 = [Tex(t).scale(0.85) for t in rep3_txt_part4]
        full_introVGroup = VGroup(introVGroup, q3VGroup)
        
        disp_calculations(self, 
            previous_mobj=full_introVGroup,
            calcs=rep3_calc3,
            next2obj=e_xy,
            direction=DOWN
        )
        
        box = SurroundingRectangle(rep3_calc3[-1])
        e_xy_res = VGroup(rep3_calc3[-1], box)
        self.play(
            Write(box),
        )
        self.wait()

        conclusion = [
            r"Puisque \(E(XY) \neq E(X)E(Y)\)",
            r"Les variables ne sont pas indépendantes"
        ]
        
        conclusion_tex = [Tex(t).scale(0.85) for t in conclusion]
        conclusionVGroup = VGroup(*conclusion_tex)
        
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=conclusionVGroup,
            next2obj=e_xy_res,
            direction=DOWN
        )


# Bonus covariance et indépendance        
class Bonus(Scene):
    def construct(self):
        msg1 = "Covariance et indépendance"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        intro = [
            r"Soit \((X, Y)\) un couple de variables aléatoires indépendantes,",
            r"telles que \(Y\{-1;1\}\) avec \(P(Y = -1) = \dfrac{1}{2} = P(Y = 1)\) :",
            r"Ainsi \(E(Y) = 0\). Soit \(Z = XY\) donc \(Z\) dépend de \(X\)."
        ]

        intro_tex = [Tex(i).scale(0.85) for i in intro]
        introVGroup = VGroup(*intro_tex)
        
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=intro_tex,
            next2obj=title1,
            direction=DOWN
        )
        
        q3_txt = [
            r"Calculons la covariance entre \(X\) et \(Z\) :",
            r"\(Cov(X, Z) = E(XZ) - E(X)E(Z)\)",
            r"\(Cov(X, Z) = E(X^2Y) - E(X)E(XY)\)",
            r"Par indépendance de \(X\) et \(Y\) on a \(E(XY) = E(X)E(Y)\)",
            r"\(Cov(X, Z) = E(X^2)E(Y) - E(X)^2E(Y)\)",
            r"\(Cov(X, Z) = E(Y)(E(X^2) - E(X)^2)\)",
            r"\(Cov(X, Z) = 0\) car \(E(Y) = 0\).",
        ]
        q3 = [Tex(t).scale(0.85) for t in q3_txt]

        q3VGroup = VGroup(*q3)
        
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=q3,
            next2obj=intro_tex[-1],
            direction=DOWN
        )
        
        rep3_txt_part1 = [
            r"Ainsi on a montré que \(Cov(X, Z) = 0\) alors que \(X\) et \(Z\) sont dépendantes.",
            r"L'implication est donc à sens unique : ",
            r"\(X\) et \(Y\) indépendantes implique \(Cov(X, Y) = 0\)",
            r"Mais la réciproque est fausse."
        ]
        
        rep3 = [Tex(t).scale(0.85) for t in rep3_txt_part1]
        rep3VGroup = VGroup(*rep3)
        
        disp_tex_list(self, 
            previous_mobj=q3VGroup,
            tex_list=rep3,
            next2obj=intro_tex[-1],
            direction=DOWN
        )
        
