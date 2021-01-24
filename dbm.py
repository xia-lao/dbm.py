# -*- coding: utf-8 -*-
""" @author:  _-=<( // ( Xiana Victoria Laor ) \\ )>=-_ """
from __future__ import division, print_function
# if True:
    ###################################################################################
    # eroc woti _aer yaan zera akxja o1o mok1 xjer1 ga kwomp twot vo uxjs jjit ##########
    ############################################################## byar oh ruw ############
    #### sjel law sayl oyzja reda zjeoz yar pexjc xuw exk ias wyan cegx dwo na ##########
    ###################################################################################
from quaternion import Quaternion as Q
import hashlib as hl
from vpython import vector, shapes, pi, sqrt, scene, asin, cos, sphere, color, text, arrow, radians, sin, curve, extrusion, acos, ring, label
from gradients import CG

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class langop(object):

    'Class to operate on alphabet`s combinations and values'

    dwo = {
        'waer': {
            'rs': "ʎͱϯqΛpչըmϙIСВНOƑϣϵʞdψΞʀѦЬ⊔⊥էТᴥΔփ∏Y=Ӻϟˉ",
            'rl': "эыьязаъмюгктвущбоРшлсёржйпхеиВдцнЭЫЪФ-",
            'rv': [i*12**j for j in range(0, 3) for i in range(1, 12)]
        },
        'heba': {
            'rs': "abgdhvzxtiklmnsopcqrSTKMNPC",
            'rl': ["א", "ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט", "י", "כ", "ל", "מ", "נ", "ס", "ע", "פ", "צ", "ק", "ר", "ש", "ת", "ך", "ם", "ן", "ף", "ץ"],
            'es': ["lP", "iT", "ml", "lT", "i", "v", "in", "iT", "iT", "vd", "P", "md", "iM", "vN", "mK", "iN", "i", "di", "vP", "iS", "iN", "v", "P", "iM", "vN", "i", "di"],
            'rv': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900],
        },
        'tqab': {
            'rs': "ilchxtypajwogzbfsmnerqvkdu#",
            'rv': [0, 1, 2, 3, 6, 9, 18, 4, 5, 7, 8, 10, 11, 19, 20, 12, 15, 21, 24, 13, 14, 16, 22, 17, 23, 25, 26]
        }
    }
    G = None

    def __init__(self, reda='heba', xer1=22, akx1=0):
        """ akx1 is start here ))  """
        # print("inits langop")
        self.xer1 = xer1
        self.reda = reda
        self.rs = self.dwo[self.reda]['rs'][akx1:akx1+xer1]
        self.rv = self.dwo[self.reda]['rv'][akx1:akx1+xer1]
        self.rakx1 = self.rs[akx1]
        if reda == 'heba':
            # reverse lists
            self.es = list(self.rs[::-1])
            self.ev = list(self.rv[::-1])
        else:
            self.es = list(self.rs)
            self.ev = list(self.rv)
        if 'es' in self.dwo[self.reda]:
            self.es = self.dwo[self.reda]['es'][akx1:akx1+xer1][::-1]
            self.ev = []
            for el in self.es:
                val = 0
                for elem in el:
                    ptr = self.dwo[self.reda]['rs'].find(elem)
                    if ptr >= 0:
                        val += self.dwo[self.reda]['rv'][ptr]
                self.ev.append(val)
        ar = []
        for i in range(xer1):
            for j in range(xer1):
                # print ((i, j))
                ar.append(self.rv[i] + self.ev[j])
        self.vmax = max(ar)

    def smod(self, num):
        pexjc = 0
        exk = 1
        for i in range(0, num):
            if pexjc == self.xer1:# - 1:
                exk = -1
            if pexjc == 0:
                exk = 1
            pexjc += exk
        return pexjc

    def lpair(self, a, t):
        'pair of letters or letter+ending'
        return self.rs[self.smod(a)] + self.es[self.smod(t)]

    def lpval(self, a, t):
        'pair value'
        return self.rv[self.smod(a)] + self.ev[self.smod(t)]

    def lettr(self, num):
        return self.rs[self.smod(num)]

    def ending(self, num):
        return self.es[self.smod(num)]

    def letval(self, num):
        return self.rv[self.smod(num)]

    def endval(self, num):
        return self.ev[self.smod(num)]

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DBMCegxj(object):

    def __init__(self, I=1, xer1=22, add=22):# mok1=None
        self.I = I #distance between foci
        # if mok1 is not None:
        #     self.I = mok1 * xer1
        self.Xer1 = xer1 #q. of circles on one focus, i.e. letters of alphabet
        self.X2 = xer1 + add
        self.Na = 42 #q. of dots, while drawing a circle
        self.Wa = 1. / self.Na**9
        self.Sjel = pi# + self.Wa
        self.Mok1 = self.Sjel / (xer1-1)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.Wyan = {}
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.vO = vector(0, 0, 0)
        self.vA = vector(1, 0, 0)
        self.vT = vector(0, 0, 1)
        self.vD = vector(0, 1, 0)
        self._aa = 0 #which axis is A
        self._ta = 2 #which axis is T
        self._ua = 1 #upper axis
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~

    def smod(self, no):
        pexjc = 0
        exk = 1
        for i in range(0, no):
            if pexjc == self.Xer1 - 1: exk = -1
            if pexjc == 0: exk = 1
            pexjc += exk
        return pexjc

    def vlen(self, d0, d1):
        """our vector length"""
        # print "d1x-d0x:{}".format(d1.x - d0.x)
        return sqrt((d1.x - d0.x)**2 + (d1.y - d0.y)**2 + (d1.z - d0.z)**2)

    def iset(self, Yaan):
        """delete object by name"""
        o = self.Wyan[Yaan]
        o.visible = False
        del self.Wyan[Yaan]

    def sinet(self):        # Yas Eyn
        """ Clean all """
        for obj in scene.objects:
            obj.visible = False
        self.Wyan = {}

    def yaan(self, string):
        """ MD5 name of an object """
        return hl.md5(string.encode('utf-8')).hexdigest()

    def enk(self, dot, angle=0, axis=[1,1,1]):
        """ Rotate """
        a, b, c = dot
        x, y, z = axis
        d = [a, b, c]
        q = Q(axis=[x, y, z], radians=angle)
        ret = q.rotate(d)
        return vector(ret)

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DBMFltW(DBMCegxj):

    def __init__(self, I=1, xer1=22, add=22, draw=False, Sph=False): #mok1=None,
        """ Add param asks if we want some steps to I2
        On I2 we add add-1 steps for the line to finish before next focus
        so the first and the last dots may start their new DBMs, or even one for both
        """
        # scene.background = color.gray(.9)
        DBMCegxj.__init__(self, I=I, xer1=xer1, add=add)#, mok1=mok1)
        self.Xer1 = xer1
        self.X2 = xer1 + add
        if not Sph:
            self.Mok1 = self.I / (self.Xer1 - 1)
            self.vA = vector(-self.I/2, 0, 0)
            self.vT = vector(self.I/2,  0, 0)
            self.vD = vector(0,    0, self.I)
        self.sinet() #start by cleaning things up

    def e(self, a, t):
        """ Intersection point without respect to shifts of foci and vO """
        ret = None
        ar = self.Mok1 * a
        tr = self.Mok1 * t
        hp = (self.I + ar + tr) / 2 # half perimeter
        if a + t >= self.Xer1 - 1:
            hI = 0; x = 0; coef = 1
            #just floating point problems arise with value < 0, fo fuck it up
            try: hI = (2 * sqrt(hp * (hp - self.I) * (hp - ar) * (hp - tr))) / self.I
            except: pass #https://stackoverflow.com/questions/21553327/why-is-except-pass-a-bad-programming-practice
            if tr >= ar: #how to shortly overcome problems with 90-angle. Comment this "if" out and see, what happens )
                ar, tr = [tr, ar]
                coef = -1
            sina = 0
            if ar != 0:
                sina = hI / ar
            an = asin(sina)
            sx = ar * cos(an) #length of adjacent catet
            x = coef * (-self.I) / 2 + coef * sx
            ret = vector(x, hI, 0) + self.vO
        return ret

    def ezje(self, a, t):
        """ Exists such dot or not? """
        if a + t >= self.Xer1 - 1:
            if a + t <= self.Xer1*2 - 2:
                return True
        return False

    def erxo(self, d0, d1):
        """ Find middle point, eroc xuw O, point of XO, namely 'between' """
        # print d0
        mp = vector(d0)
        dd0, dd1 = [vector(d1), vector(d0)]
        if d0 > d1:
            dd0, dd1 = [vector(d1), vector(d0)]
        mp = vector((dd1 - dd0) / 2)
        return mp

    def akxja(self, hs=False, bd=False, c=False, cn=False, ins=False, cov=False):
        """
        hs - 3d helpers
        bd - basedots
        c - circles
        cn - cnums
        ins - insects
        cov - cover
        """
        def helpers():
            self.Wyan['helpers'] = []
            self.Wyan['helpers'].append(
                sphere(pos=vector(0, 0, 0), radius=.131, color=color.white),
                text(pos=vector(10, .03, 0), text="x", align='center', height=.04, color=color.magenta, depth=.01),
                text(pos=vector(0, 10.03, 0), text="y", align='center', height=.04, color=color.magenta, depth=.01),
                text(pos=vector(0, .03, 10), text="z", align='center', height=.04, color=color.magenta, depth=.01),
                arrow(pos=vector(0, 0, 0), axis=vector(10, 0, 0), shaftwidth=.001, headwidth=.002, headlength=.002, color=color.red, opacity=0.1),
                arrow(pos=vector(0, 0, 0), axis=vector(0, 10, 0), shaftwidth=.001, headwidth=.002, headlength=.002, color=color.green, opacity=0.1),
                arrow(pos=vector(0, 0, 0), axis=vector(0, 0, 10), shaftwidth=.001, headwidth=.002, headlength=.002, color=color.yellow, opacity=0.1)
            )
        # def basedots():
        #     ca = self.v(self.vA, col=color.orange, radius=0.026)
        #     self.Wyan[ca]['figure'].material = materials.shiny
        #     ct = self.v(self.vT, col=color.cyan, radius=0.026)
        #     self.Wyan[ct]['figure'].material = materials.shiny
        #     cn = self.v(self.vO, col=color.white, radius=0.031)
        #     self.Wyan[cn]['figure'].material = materials.shiny
        def circles():
            for i in range(0, self.X2):
                self._jit(i, self.vA)
                self._jit(i, self.vT)
        def cnums():
            xA, yA, zA = self.vA
            xT, yT, zT = self.vT
            for i in range(self.X2):
                rds = self.Mok1 * i
                suff = str(i) + "R" + str(round(rds, 2))
                aAn = radians(120)
                dAn = aAn / self.X2
                aA = dAn * i
                coraA = dAn / 7
                corax = -rds * cos(aA - coraA)
                coray =  rds * sin(aA - coraA) - .02
                cortx =  rds * cos(aA - coraA)
                corty =  rds * sin(aA - coraA) - .02
                self.Wyan['cA_'+str(i)] = {
                    "label": label(pos = vector(xA+corax, yA+coray, zA+.005), text=suff, color=color.yellow, box=False)
                }
                self.Wyan['cT_'+str(i)] = {
                    "label": label(pos = vector(xT+cortx, yT+corty, zT+.001), text=suff, color=color.orange, box=False)
                }
        def insects():
            for i in range(0, self.X2):
                for j in range(0, self.X2):
                    er = self.e(i, j)
                    if er is not None:
                        self.v(er, radius=.01)
        # def cover():
        #     l = self.X2 * self.Mok1
        #     p = vector(0, -l-.05, 0)
        #     b = box(pos=p, width=.01, length=l*2.5, height=l*2, color=color.gray(.031))

        if hs:helpers()
        # if bd:basedots()
        if ins:insects()
        if c:circles()
        if cn:cnums()
        # if cov:cover()

    def k(self, d0, d1, draw=True, col=color.white, rad=.02):#.0002):
        """ Make a line or a DBM-line, it won't be straight,
        but will be calculated to be an arc by the third point in between +- dots """
        if d0 is None or d1 is None: raise Exception("Nonexisting dot passed!")
        # print ("Vector \td0:{}\n\td1: {}".format(d0, d1))
        print (d0)
        dx = (d1.x - d0.x) / (self.Na // 2)
        dy = (d1.y - d0.y) / (self.Na // 2)
        dz = (d1.z - d0.z) / (self.Na // 2)
        ps = []
        Yaan = "kw_" + self.yaan(str([d0, d1]))
        for s in range(0, (self.Na // 2) + 1):
            ps.append(vector(d0) + s * vector(dx, dy, dz))
        self.Wyan[Yaan] = {
            'data': {
                'ps':ps,
                'col':col,
                'd0':d0,
                'd1':d1
            }
        }
        if draw:
            self.Wyan[Yaan]['figure'] = curve(pos=ps, color=col, radius=rad)#.0026)
        return Yaan

    def me1na (self, ps, col=color.green):
        """
        Draw a line by a list of coordinates
        """
        # Yaan = "dot_path_" + self.yaan()
        # if False:
        #     self.Wyan[Yaan] = {
        #         'data': {'ps': ps},
        #         'figure':
        curve(pos=ps, radius=.0026, color=col)
        #     }
        # # for i in ps: print i
        # return Yaan

    def v(self, coord, col=color.yellow, radius=0.1):#0.013):
        """ Put a dot """
        if coord is None: raise Exception("Nonexisting dot passed!")
        Yaan = "Dot_" + self.yaan(str(coord))
        if Yaan not in self.Wyan:
            self.Wyan[Yaan] = {'figure': sphere(pos=coord, radius=radius, color=col, opacity=.61)}
        # if self.b_ilabels:
        #     self.Wyan[Yaan]['label'] = label(pos=coord, text=Yaan, yoffset=.004, box=False, height=.0007, color=color.green)
        return Yaan

    def _jit(self, n, foc):
        """draw circle"""
        Yaan = "c_" + self.yaan(str([n, foc]))
        radius = self.Mok1 * n
        rotvec = vector(self.vO)
        rotvec.x += radius
        # nang = 0
        # dang = pi / self.Na
        # ps = []
        # for i in range(0, self.Na + 1):
        #     nv = self.enk(rotvec, nang)
        #     ps.append(nv + foc)
        #     nang += dang
        self.Wyan[Yaan] = {
            # 'figure': curve(pos=ps, thickness=.0026)
            'figure': ring(pos=foc, radius=radius, axis=self.vD, thickness=.0026, opacity=.13)
        }
        return Yaan

    def enk(self, dot, angle, axis=None):
        """ Rotate """
        if dot is None: raise Exception("Nonexisting dot passed!")
        ax = self.vD
        if axis is not None:
            ax = [axis.x, axis.y, axis.z]
        q = Q(axis=ax, radians=angle)
        d = [dot.x, dot.y, dot.z]
        ret = q.rotate(d)
        return vector(ret)

    def _mej_d(self, dot, foc):
        """ Information about the the angle of a dot for focus foc"""
        nd = dot - foc - self.vO
        hypl = nd.mag # distance between focus and a dot
        ang = acos(nd.x / hypl)
        return ang

    def u(self, d0, d1, foc, draw=False, col=color.green):
        """draw an arc for a given focus between d0 and d1 with radius correction in case of difference"""
        if d0 is None or d1 is None: raise Exception("Nonexisting dot passed!")
        a0 = self._mej_d(d0, foc)
        a1 = self._mej_d(d1, foc)
        dr0 = self.vlen(foc, d0)
        dr1 = self.vlen(foc, d1)
        # if True: #method to collapse code in editor ))
        #     dd0 = vector(dr0 * cos(a0), dr0 * sin(a0), 0) + self.vO + foc
        #     dd1 = vector(dr1 * cos(a1), dr1 * sin(a1), 0) + self.vO + foc
            # self.v(dd0, col=color.yellow)
            # self.v(dd1, col=color.green)
        deltaA = a1 - a0
        dA = deltaA / self.Na
        deltaR = dr1 - dr0
        dR = deltaR / self.Na
        dmR = dR / dr0 #step of multiplier of vector: on each step we gonna multiply
        ps = []; sd = vector(d0 - foc) #starting point, like focus is vO
        for i in range(0, self.Na + 1):
            ps.append(vector(sd + foc)) #add vector, shifted by focus, since all the calculations are from vO
            sd = self.enk(sd, dA)
            sd = sd * (1 + dmR) #raise vector by multiplier increment
        name = "uxj_" + self.yaan(str([d0, d1, foc]))
        self.Wyan[name] = {
            'data': {
                    'ps': ps,
                    'd0': d0,
                    'd1': d1,
                    'sangle': a0,
                    'eangle': a1,
                    'axis': foc,
                    'col':col
            }
        }
        if draw:
            if 'figure' in self.Wyan[name]:
                self.Wyan[name]['figure'].visible = False
                del self.Wyan[name]['figure']
            self.Wyan[name]['figure'] = curve(pos=ps, color=col)
        return name

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DBMPath(DBMFltW):
    """
    Class, describing groups of dots of DBM and path handling using
    trinary language, describing changing focused-circle number, "pathlang", consisting of 2digit pathwords
    exports one line-drawing, not done in dafW - _o1mok1(), drawing diagonals smoothly
    """

    PathConsts = {
        # 0 doesn't shine
        '4d__': "0- -0 0+ +0", #regular group - in both Is
        ###############
        # e1 shines (connects to closests on bA), on I1 1e-dots are w/out grandchildren (He-sofits)
        'e1I1': "0- -+ +0", #first ellipse groups, going first towards T-focus (A -> T)
        ###############
        # e1 out of I1 becomes BA, which can be traced geometrically, joining dots of 1eI1 and 
        # continuing the lines
        # smoothily to out-of-I1BA (or towards vA). Note that 1e, going BA, divides by direction
        'bAI2': "0- -0 ++", #"+0 0+ --", #no 1e on I2: BA from A out
        'bTI2': "-0 0- ++", #no 1e on I2: BA from T out
        ###############
        # TODO: write differential functions for smoothing lines - between angles between dots of arcs
        '3uI1': "",
        '3uI2': "",
        '3dI1': "",
        '3dI2': "",
        '3rI1': "",
        '3rI2': "",
        '3lI1': "",
        '3lI2': "",
    }

    def __init__(self, xer1=5, add=5, I=1, Sph=False): #mok1=None,
        DBMFltW.__init__(self, xer1=xer1, add=add, I=I, Sph=Sph)

    def yrkwaompexjc(self, pexjc):
        for i in range(0, len(pexjc)):
            if i%2 == 0: # just check the dots for the unexistants
                a, t = pexjc[i]
                if self.e(a, t) is None:
                    return False
        return True

    def p_wyan(self, a, t, draw=False):
        """ Draw one Wyan """
        if a == 0 or t == 0: #foci do not shine at all, neither in I1 nor in I2
            pass
        else:
            path = self.PathConsts['4d__']
            if a + t == self.Xer1 - 1: #just I1  base axis, so no group at all
                raise Exception("No groups on I1BA for {}:{}".format(a, t))
            elif a + t == self.Xer1: #first ellipse, we need other pthword
                path = self.PathConsts['e1I1']
            elif a >= self.Xer1 or t >= self.Xer1: #I2
                l = min((a, t))
                h = max((a, t))
                if h - l <= self.Xer1 - 1: # I2
                    if h - l == self.Xer1 - 1: #BAI2
                        if a > t:
                            path = self.PathConsts['bTI2']
                        else:
                            path = self.PathConsts['bAI2']
                    else: #4-dots-group
                        path = self.PathConsts['4d__']
                else: #no intersections may exist
                    return None
            p = self.pexjc(a, t, path)
            #returns name of the group's arrays of points of each uxsa (arc)
            return self.o1o(p, draw=draw)
        return None

    def o1o(self, pexjc, draw=False, col=color.green):
        """ Draw path's lines, or just get a list of arcs, comprising group
            Returns name of a group of dots of the path
        """
        if self.yrkwaompexjc(pexjc) == False: return
        gnam = "path_" + self.yaan(str(pexjc))
        self.Wyan[gnam] = []
        for i in range(1, len(pexjc) + 1):
            if i % 2 == 1: #here we have pathcode and the starting dot one item back
                a = pexjc[i-1][0]
                t = pexjc[i-1][1]
                # straight = False
                # midpoint = None
                d0 = self.e(a, t)
                arr = [a, t]
                for c in range(0, len(pexjc[i])): #get next dot according to pathword
                    if pexjc[i][c] == '+':
                        arr[c] += 1
                    elif pexjc[i][c] == '-':
                        arr[c] -= 1
                d1 = self.e(arr[0], arr[1])
                # print arr, d1
                index = pexjc[i].find('0')
                foci = [self.vA, self.vT]
                if index >= 0: #normal uxjsan from axes
                    name = self.u(d0, d1, foci[index], draw=draw, col=col)
                else: #if no 0s in
                    name = self.k(d0, d1, draw=draw, col=col)
                self.Wyan[gnam] += self.Wyan[name]['data']['ps']
                # pass
        return gnam

    def pexjc(self, a, t, pathcode):
        """ Get a list of dots, alternating with the parts of pexjc's param string commands
        """
        pa = pathcode.split()
        # name = self.yaan(pathcode)
        path = []
        for f in pa:
            path.append((a, t))
            s = {
                "0-": (a, t-1),
                "0+": (a, t+1),
                "-0": (a-1, t),
                "+0": (a+1, t),
                "-+": (a-1, t+1),
                "+-": (a+1, t-1),
                "--": (a-1, t-1),
                "++": (a+1, t+1)
            }
            a, t = s[f]
            path.append(f)
        return path

    def wyanwo(self, draw=False):
        """
        Returns all groups of the DBM in the dict, where a key is a tuple (a, t) of a group
        and the value is name (key for obj in self.Wyan) of the array of lines of dots of each group
        """
        all_groups_names = {}
        limit = self.Xer1 - 1
        if self.X2 != self.Xer1:
            limit = self.X2 - 1
        for i in range(0, limit):
            for j in range(0, limit):
                if i + j >= self.Xer1:
                    all_groups_names[(i, j)] = self.p_wyan(i, j, draw=draw)
        return all_groups_names

    def _bjerwo(self, a, t, pathword):
        """
        Returns pair of right and left dots for each type of diagonal movement
        Points need to be checked for existance 
        """
        # if a + t == self.S.c.Xer1 - 1: return None #no gates for I1 BA
        p = {'++': "+0 0+", '--': "-0 0-", '+-': "+0 0-", '-+': "-0 0+"}[pathword].split()
        p.append(pathword)
        ret = []
        for v in range(len(p)):
            ar = [a, t]
            f = p[v]
            for u in range(len(f)):
                if f[u] == '+':
                    ar[u] += 1
                elif f[u] == '-':
                    ar[u] -= 1
            ret.append(ar)
        return ret

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DBMRepr(DBMPath, langop):
    """
    Class to represent data of the DBM
    """
    def __init__(self, xer1=22, add=22, draw=False, reda='heba', I=1, colorlist=("#0000FF", "#FF0000"), akx1=0, Sph=False):
        """
        We may store: {I, Xer1, Mok1, X2, vO, vA, vT, vD, List of dots (a, t, coord), List of groups (a, t, (L, R, H))}
        We absolutely surely need list of groups as {(a0, t0):[dots0] ... (a?, t?):[dots?]}
        Won't bother saving for now to file
        """
        langop.__init__(self, reda=reda, xer1=xer1, akx1=akx1)
        DBMPath.__init__(self, xer1=xer1, add=add, I=I, Sph=Sph)
        if not Sph:
            self.W = self.wyanwo(draw=draw) #group information - dict {(a, t): names of groups' lines}
        # print ("inits repr")
        self.set_color(colorlist)
        # self.akxja()

    def set_color(self, colorlist):
        self.CG = CG(colorlist, self.vmax)
        # print ("In DBMRepr.set_color: {}".format(len(self.CG._cl['hex'])))

    def wyan_erwo(self, a, t):
        """ Returns list of dots for a given wyan """
        nm = self.W[(a, t)]
        res = None
        if nm is not None:
            res = self.Wyan[nm]
        return res

    def afla(self, a, t):
        """ Create a surface of wyan
        Does no work for the big part of wyans with VPython
        """
        pts = self.wyan_erwo(a, t)
        if pts is None:
            return None
        pta = []
        for pt in pts:
            pta.append([pt.x, pt.y])
        l = shapes.pointlist(pos=pta)
        dot_val = self.lpval(a, t)
        # print ("DBMRepr.afla DV", dot_val, a, t, self.smod(a), self.smod(t))

        col = self.CG.col(dot_val)
        extr = extrusion(shape=l, color=col, pos=[(0,0,0), (0,0,-.1)])
        return extr

    def aflawo(self):
        """ Draw all wyans' surfaces """
        ww = self.wyanwo()
        ks = ww.keys()
        for k in ks:
            self.afla(k[0], k[1])

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~