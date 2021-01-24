# -*- coding: utf-8 -*-
""" @author:  _-=<( // ( Xiana Victoria Laor ) \\ )>=-_ """

from __future__ import division, print_function
from vpython import * #fabs, color, vector, points, sqrt, radians, sin, cos, sphere, text, arrow, curve, label, acos, norm
from numpy import linspace
from dbm import DBMRepr
from quaternion import Quaternion as Q
#from baseconvert import base
import cmath as cm
from gradients import CG, hex_to_RGB

if True:
    #######################################################################################
    import inspect
    def caller_name(skip=2):
        """Get a name of a caller in the format module.class.method

        `skip` specifies how many levels of stack to skip while getting caller
        name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.

        An empty string is returned if skipped levels exceed stack height
        """
        stack = inspect.stack()
        start = 0 + skip
        if len(stack) < start + 1:
            return ''
        parentframe = stack[start][0]

        name = []
        module = inspect.getmodule(parentframe)
        # `modname` can be None when frame is executed directly in console
        # TODO(techtonik): consider using __main__
        if module:
            name.append(module.__name__)
        # detect classname
        if 'self' in parentframe.f_locals:
            # I don't know any way to detect call from the object method
            # XXX: there seems to be no way to detect static method call - it will
            #      be just a function call
            name.append(parentframe.f_locals['self'].__class__.__name__)
        codename = parentframe.f_code.co_name
        if codename != '<module>':  # top level usually
            name.append( codename ) # function or a method

        ## Avoid circular refs and frame leaks
        #  https://docs.python.org/2.7/library/inspect.html#the-interpreter-stack
        del parentframe, stack

        return ".".join(name)

    def print_caller_name(stack_size=3):
        def wrapper(fn):
            def inner(*args, **kwargs):
                import inspect
                stack = inspect.stack()

                # https://stackoverflow.com/questions/2654113/python-how-to-get-the-callers-method-name-in-the-called-method
                # modules = [(index, inspect.getmodule(stack[index][0])) for index in reversed(range(1, stack_size))]
                #(This will raise an IndexError if the requeted stack depth is greater than the actual. Solution: )
                modules = [(index, inspect.getmodule(stack[index][0])) for index in reversed(range(1, min(stack_size, len(inspect.stack()))))]
                module_name_lengths = [len(module.__name__)
                                    for _, module in modules]

                s = '{index:>5} : {module:^%i} : {name}' % (max(module_name_lengths) + 4)
                callers = ['',
                        s.format(index='level', module='module', name='name'),
                        '-' * 50]

                for index, module in modules:
                    callers.append(s.format(index=index,
                                            module=module.__name__,
                                            name=stack[index][3]))

                callers.append(s.format(index=0,
                                        module=fn.__module__,
                                        name=fn.__name__))
                callers.append('')
                print('\n'.join(callers))

                fn(*args, **kwargs)
            return inner
        return wrapper
          #######################################################################################


class compfn(DBMRepr):
    def __init__(self, er=7.1e-9, xer1=22, add=22,
                 draw=False, reda='heba', I=1,
                 colorlist=("#0000FF", "#FF0000", "#FFFFFF"), akx1=0):

        DBMRepr.__init__(self, xer1=xer1, add=add,
                         draw=draw, reda=reda, I=I,
                         colorlist=colorlist, akx1=akx1)
        self.er = er
        self.intersection = self.e
        self.dot = self.v
        self.line = self.k
        self.curve = self.me1na
        self.arc = self.u

    def equals_within_error(self, a, b):
        if fabs(b - a) < self.er:
            return True
        return False

    def close_to_whole(self, a):
        if fabs(a - int(a)) < self.er:
            return True
        return False

    def points(self, ps, col=color.blue, rad=.1, draw_lines=False, axis=2, sparse=12):
        if draw_lines:
            n=0
            for p in ps:
                if n % sparse == 0:
                    self.k(
                            vector(0, 0, p[axis]),
                            vector(p),
                            draw=True
                        )
                n = n+1

        return points(pos=ps, color=col, radius=rad)

    def wave_coords(self):
        _PERIOD = 3 #wave length coefficient
        _RANGE = 13 #quantity of loops
        _RRUN = 4 #within how many loops the radius changes from min to max or backwards
        _SHEER_FACTOR = .5
        _CIRCLE = 360. #number of degrees in a loop
        _RADIUS = 2 #just the radius of a wave
        _ZSHIFT = .005
        # sheer polarization is governed by the radius of ellipse at the given point
        # всё есть здесь: https://ru.wikipedia.org/wiki/Эллипс
        # r = (_BHA * _LHA) / sqrt(_LHA**2 * cos(radians(BHA_Point_angle))**2 + _BHA**2 * sin(radians(BHA_Point_angle))**2)
        #or:  excentricity = sqrt(1 - _LHA**2 / _BHA**2)
        # r = _LHA / sqrt(1 - excentricity**2 * cos(BHA_Point_angle)**2)
        _ELLIPSE = 1 #0: ellipse, 1: ellipse + z-running r-shift, 2: z-running r-shift
        _BHA = _RADIUS
        _LHA = _RADIUS / 2
        _EANGLE = 30. #angle of the _BHA inclination
        _ROTEAN = False #rotate _EANGLE by the _CIRCLE/_RANGE part for each iteration. Experimental, has explicable rips

        res = []
        rfactor = -1
        # zfactor = -1
        sfactor = lambda r: (r / _SHEER_FACTOR) / _CIRCLE #sheer factor
        r = _RADIUS
        bha = _BHA
        lha = _LHA
        rng = int(_CIRCLE * _RANGE)
        elrad = lambda b, l, phi: (b * l) / sqrt(l**2 * cos(radians(phi))**2 + b**2 * sin(radians(phi))**2)

        for angle in range(rng):

            aa = angle % _CIRCLE

            BHA_Point_angle = aa - _EANGLE

            if _ROTEAN: #EXPERIMENTAL!
                if aa == 0:
                    _EANGLE = _EANGLE + (_CIRCLE / _RANGE)

            if _ELLIPSE == 0: #try elliptical polarization
                r = elrad(_BHA, _LHA, BHA_Point_angle)

            elif _ELLIPSE == 1: #try'em both
                if angle % (_CIRCLE * _RRUN) == 0:
                    rfactor = -rfactor
                bha = bha + rfactor * sfactor(_BHA)
                lha = lha + rfactor * sfactor(_LHA)
                r = elrad(bha, lha, BHA_Point_angle)

            elif _ELLIPSE == 2: #try just changing radius for several cycles, TODO: may be joined to the elliptical polarization
                if angle % (_CIRCLE * _RRUN) == 0:
                    rfactor = -rfactor
                r = r + rfactor * sfactor(_RADIUS)
            else:
                pass #static radius

            c0 = r * cm.exp( ( -1j ) * radians(aa) )

            time = _PERIOD / 360 * angle

            p0 = vector(c0.real, c0.imag, time) #
            res.append(p0)

        return res

    def grid(self, step=.1, quantity=10, thickness=.0026, col=color.gray(.56)):
        # llen = step*(quantity-1)
        arr = []
        coef = 1./255
        for i in range(quantity):
            for j in range(quantity):
                for k in range(quantity):
                    arr.append(vector(step*i*coef, step*j*coef, step*k*coef))
                    col = map(lambda x: x *round(255 / quantity), arr[-1])
                    print ((i, j, k), col)
                # self.line(vector(0, step*i, step*j), vector(llen, step*i, step*j), draw=true, col=col, rad=thickness)
                # self.line(vector(step*i, 0, step*j), vector(step*i, llen, step*j), draw=true, col=col, rad=thickness)
                # self.line(vector(step*i, step*j, 0), vector(step*i, step*j, llen), draw=true, col=col, rad=thickness)
                    self.points(arr[-1], col=col, rad=.1)

    def show_colors(self):
        arr = []
        for i in range(len(self.CG._cl['hex'])):
            val = hex_to_RGB(self.CG._cl['hex'][i])
            valO=val
            for j in range(len(val)):
                val[j] = (1/255) * val[j]
            arr.append(vector(val))
            print (valO, arr[-1])
        self.points(arr, col=color.red, rad=.2)

    # cf = compfn(xer1=22, add=0)
    # cf.akxja(hs=True)#, ins=True, c=True, cn=True)
    # cf.points(cf.wave_coords(), draw_lines=True, sparse=6)


    # cg = CG(("#0000FF", "#FF0000", "#FFFFFF"), 835)
    # clh = cg._cl['hex']

    # cf.aflawo()

    # cf.grid()
    # cf.show_colors()
#######################################################################################

class DBMSph(DBMRepr):

    def __init__(self, I=1., xer1=22):
        # scene.background = color.gray(.9)
        # add=0 is always so for Spherical DBM
        DBMRepr.__init__(self, xer1=xer1, add=0, I=I, Sph=True)

    def akxja(self, helpers=True, h_only=False):
        """
        Initialize graphics
        """
        self.sinet()
        if helpers:
            self.Wyan['helpers'] = []
            self.Wyan['helpers'].append([
                sphere(pos=vector(0, 0, 0), radius=.031, color=color.black),
                text(pos=vector(1, .03, 0), text="x", align='center', height=.04, color=color.magenta, depth=.01),
                text(pos=vector(0, 1.03, 0), text="y", align='center', height=.04, color=color.magenta, depth=.01),
                text(pos=vector(0, .03, 1), text="z", align='center', height=.04, color=color.magenta, depth=.01),
                arrow(pos=vector(0, 0, 0), axis=vector(1, 0, 0), shaftwidth=.001, headwidth=.002, headlength=.002, color=color.red, opacity=0.2),
                arrow(pos=vector(0, 0, 0), axis=vector(0, 1, 0), shaftwidth=.001, headwidth=.002, headlength=.002, color=color.green, opacity=0.2),
                arrow(pos=vector(0, 0, 0), axis=vector(0, 0, 1), shaftwidth=.001, headwidth=.002, headlength=.002, color=color.blue, opacity=0.2)])
        if not h_only:
            for i in range(0, self.X2):
                # rate(5)
                # print("\t==> ",
                self._xjeof(i, z=0, col=color.blue)
                # print("\t==> ",
                self._xjeof(i, z=1, col=color.red)
                #_________________________________
                # for i in range(0, self.Xer1):
                #     for j in range(0, self.Xer1):
                #         if i + j >= self.Xer1:
                #             rate(10)
                #             print("||| A{}T{}".format(i, j))
                #             d0 = self._eroc(i, j)
                #             print("||| d0 = {}".format(d0))
                #             self._1aer(d0)
                """
                Odd
                0 > 0:4
                1 > 1:3, 1:5 | 1:4
                2 > 2:2, 2:6 | 2:5, 2:3 | 2:4
                3 > 3:1, 3:7 | 3:6, 3:2 | 3:5, 3:3 | 3:4
                Even
                2:0:1
                
                """
                # _________________________________
        # OR
        # self._xjeof(4, z=0, col=color.blue)
        # self._xjeof(4, z=1, col=color.red)
        # self._xjeof(3, z=0, col=color.blue)
        # self._xjeof(5, z=1, col=color.red)

    def _kwomp(self, d0, d1, col=color.red):
        """
        Make a line
        """
        dx = (d1[0] - d0[0]) / (self.Na // 2)
        dy = (d1[1] - d0[1]) / (self.Na // 2)
        dz = (d1[2] - d0[2]) / (self.Na // 2)
        ps = []
        name = "kw_" + self.yaan(str([d0, d1]))
        for s in range(0, (self.Na // 2) + 1):
            ps.append(vector(d0) + s * vector([dx, dy, dz]))
        self.Wyan[name] = {
            'figure': curve(pos=ps, radius=.0026, color=col),
        }
        return name

    def _dwo_jjit(self, n):
        """
        Information about the path (circle)
        Odd: middle is (xer1-1)/2
        Evn: middles are (xer1-1)/2; (xer1+1)/2
        """
        # xym = (self.Xer1 - 1) / 2  # xy-mirror XD
        # oldn = n
        # if oldn > xym:
        #     n = self.Xer1 - oldn

        ang = 0
        if isinstance(n, int):
            # print("dwo_jjit, n passed as int")
            ang = self.Mok1 * n
        elif isinstance(n, float):
            # print("dwo_jjit, n passed as float")
            ang = n
        shift = self.I * cos(ang)
        radius = self.I * sin(ang)
        if radius == 0.:
            radius = self.Wa
        return [radius, shift]

    def _eroc(self, a, t, sign=1):
        """
        Intersection point
        """
        ajr, ajs = self._dwo_jjit(a)
        tjr, tjs = self._dwo_jjit(t)
        arise = 0
        if ajr > self.Wa:
            cAng = tjs / ajr
            # print ("<{}:{}, {}>\n\tA Radius: {}, Sjift:{}, \n\tT Radius:{}, Shift:{}, \n\t Cosine of TShift/ARad:{}".format(a, t, sign, ajr*10, ajs*10, tjr*10, tjs*10, cAng))
            # self.k( vector(ajs, 0,   0),   vector(ajs, 0, tjs) , rad=.002)
            # self.k( vector(ajs, ajr, tjs), vector(ajs, 0, tjs) , rad=.002, col=color.yellow)
            angle = acos(cAng)
            arise = sign * ajr * sin(angle)
        self.k(vector(0, 0, 0), vector(ajs, arise, tjs), rad=.005, col=color.magenta)
        return vector(ajs, arise, tjs)

    def _enk1(self, dot, angle=0, axis=[1,1,1]):
        if False:
            """ Rotate - module independent version  (Copyleft)
            AND DOESN'T WORK (((
            """
            axis = [angle, axis[0], axis[1], axis[2]]
            dot = [0, dot[0], dot[1], dot[2]]
            def conj(q):
                print ("\t in CONJ q: {}".format(q))
                return [q[0], -q[1], -q[2], -q[3]]
            def mult(p, q):
                print ("\t in MULT \n\t  p: {}, \n\t  q: {}".format(p, q))
                w, x, y, z = [0, q[0], q[1], q[2]]
                a, b, c, d = p
                return [
                    a*w - b*x - c*y - d*z,
                    a*x + b*w - c*z + d*y,
                    a*y + b*z + c*w - d*x,
                    a*z - b*y + c*x + d*w
                ]
            print ("- In ENK axis: {}\n\n".format(axis))
            return mult(axis, mult(dot, conj(axis)))

    def _enk(self, dot, angle=0, axis=[1,1,1]):
        """ Rotate """
        q = Q(axis=[axis.x, axis.y, axis.z], radians=angle)
        d = [dot.x, dot.y, dot.z]
        ret = q.rotate(d)
        return vector(ret[0], ret[1], ret[2])

    def _uxjsa(self, d0, d1, draw=True, col=color.green):
        name = "Ar_" + self.yaan(str([d0, d1]))
        axis = d0.cross(d1)
        coef = 1
        if d0[self._aa] == d1[self._aa]: #case of rotation about x axis
            axis = self.vA
            d01 = vector(0, d0[1], d0[2])
            d11 = vector(0, d1[1], d1[2])
            dsc = d01.dot(norm(d11)) / d01.mag
            if d01[self._ua] < d11[self._ua]:
                coef = -1
        elif d0[self._ta] == d1[self._ta]: #case of rotation about z axis
            axis = self.vT
            d01 = vector(d0[0], d0[1], 0)
            d11 = vector(d1[0], d1[1], 0)
            dsc = d01.dot(norm(d11)) / d01.mag
            if d01[self._ua] > d11[self._ua]:
                coef = -1
        else:    #case of rotation about vO (center)
            # cos of angle is scalar projection of d0 on d1 over hypotenuse(magnitude of d0 (== 1.))
            dsc = d0.dot(norm(d1)) / d0.mag
            dsa = acos(dsc)
            da = dsa / self.Na
            ps = []

        for i in range(0, self.Na+1):
            ps.append(self._enk(d0, angle=coef*da*i, axis=axis))
        self.Wyan[name] = {
            'data': {
                    # 'ps': ps,
                    'd0': d0,
                    'd1': d1,
                    'axis': axis
                    # 'angle': dsa,
                    # 'col':col
            }
        }
        # print ("Data of Uxjsa:{}".format(self.Wyan[name]))
        if draw:
            if 'figure' in self.Wyan[name]:
                self.Wyan[name]['figure'].visible = False
                del self.Wyan[name]['figure']
        self.Wyan[name]['figure'] = curve(pos=ps, radius=.0026, color=col)
        return name

    def _1aer(self, coord=None, a=None, t=None, col=color.white, radius=0.031):
        """
        Put a dot
        """
        Yaan = None
        if coord is None:
            if a is None:
                return
            else:
                coord = self._eroc(a, t)
                Yaan = "Dot_" + str([a, t])
        else:
            Yaan = "Dot_" + self.yaan(str(coord))
        if Yaan not in self.Wyan:
            self.Wyan[Yaan] = {'figure': sphere(pos=coord, radius=radius, color=col)}
        # if self.b_ilabels:
        # if coord is None:
        #     self.Wyan[Yaan]['label'] = label(pos=coord, text=Yaan, yoffset=.004, box=False, height=.0007, color=color.green)

    def _xjeof(self, n, z=1, col=color.green):
        """
        Draw a circle
        if n is float, will draw the float radius, not just by number of circle,
        so the func may be used to draw at any AT-plane-angle

        LU in _dwo_jjit
        """
        radius, shift = self._dwo_jjit(n)
        axis = self.vA
        axs = self._aa
        coef = 1
        if z == 1:
            axis = self.vT
            axs = self._ta
            coef = -1
        pref = "A"
        if z == 1:
            pref = "Z"
        name = pref + str([n, z])

        # print("Circle {} of {} with radius {} and offset {}".format(n, pref, radius, shift))

        # pos = list(axis.astuple())
        pos = [axis.x, axis.y, axis.z]
        pos[axs] = shift
        pos[self._ua] = radius
        pos = vector(pos[0], pos[1], pos[2])

        # print("""{}: \n\tAxis: {}, \n\tAxisIndex: {}, \n\tDirection: {}, \n\tRadius:{}, \n\tShift: {}, \n\tPosition of start: {}""".format(name, axis, axs, coef, radius, shift, pos))
        ps = []        # points of the circle
        Jjit = (pi * 2) + self.Wa
        for an in linspace(0, Jjit, self.Na):
            ps.append(self._enk(pos, angle=coef * an, axis=axis))
        self.Wyan[name] = {
            'data': {
                'ps': ps,
                'n': n,
                'z': z,
                'axis': axis,
                'axs': axs,
                'col':col
            },
            'figure': curve(pos=ps, radius=.0026, color=col, axis=axis, name=name),
            'label': label(pos=ps[self.Xer1 - self.Xer1 // 3], text=name, height=.007, box=False, color=col)
        }
        return name

# #%%

scene.resizable = True
scene.align = 'right'
d = DBMSph(xer1=8)
d.akxja()

# d0 = d._eroc(5, 5)
# d._1aer(coord=d0)
# print (d0)