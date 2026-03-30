import cv2
import math
import random
import numpy as np

# ---------- COLORS ----------
COLORS = {
    "Cube": ((180,255,210),(120,200,170)),
    "Cuboid": ((170,240,210),(110,190,160)),
    "Sphere": ((220,235,255),(160,190,230)),
    "Triangle": ((230,210,255),(190,160,230)),
    "Cone": ((210,235,255),(150,190,230)),
    "Cylinder": ((200,235,255),(150,180,210)),
}

# ---------- INFO ----------
INFO = {
    "Cube": [
        "Regular hexahedron",
        "6 square faces",
        "12 equal edges",
        "8 vertices",
        "Volume = a^3",
        "Surface Area = 6a^2",
        "All angles are 90 deg"
    ],
    "Cuboid": [
        "Rectangular prism",
        "6 rectangular faces",
        "12 edges",
        "8 vertices",
        "Volume = lwh",
        "Surface Area = 2(lw+lh+wh)"
    ],
    "Sphere": [
        "Perfectly round solid",
        "No edges or vertices",
        "All points equidistant",
        "Volume = 4/3 pi r^3",
        "Surface Area = 4 pi r^2"
    ],
    "Cylinder": [
        "Two circular bases",
        "One curved surface",
        "No vertices",
        "Volume = pi r^2 h",
        "Surface Area = 2 pi r (h+r)"
    ],
    "Cone": [
        "One circular base",
        "One curved surface",
        "Single vertex",
        "Volume = 1/3 pi r^2 h",
        "Surface Area = pi r (l+r)"
    ],
    "Triangle": [
        "Tetrahedron",
        "4 triangular faces",
        "6 edges",
        "4 vertices"
    ]
}

def lerp(a, b, t):
    return a + (b - a) * t

class CubeSim:
    def __init__(self):
        self.angle_x = self.angle_y = self.angle_z = 0.0
        self.scale = 1.0
        self.spin = 0.0

        self.sx = self.sy = self.sz = 0.0
        self.sscale = 1.0

        self.size = 140

        self.shapes = ["Cube","Cuboid","Sphere","Triangle","Cone","Cylinder"]
        self.shape_id = 0
        self.current_shape_index = 0

        # info animation
        self.info_line = 0
        self.info_char = 0
        self.info_timer = 0
        self.last_shape = None

        self.clouds = {}
        self._init_clouds()

    # ---------- CLOUDS ----------
    def _init_clouds(self):
        self.clouds["Sphere"] = [self._rand_sphere() for _ in range(2600)]
        self.clouds["Cube"] = [self._rand_cube() for _ in range(1800)]
        self.clouds["Cuboid"] = [(random.uniform(-1.3,1.3),
                                  random.uniform(-0.8,0.8),
                                  random.uniform(-1,1)) for _ in range(1800)]
        self.clouds["Cylinder"] = [self._rand_cylinder() for _ in range(2200)]
        self.clouds["Cone"] = [self._rand_cone() for _ in range(2000)]
        self.clouds["Triangle"] = [self._rand_tetrahedron() for _ in range(600)]

    def _rand_cube(self):
        return (random.uniform(-1,1),random.uniform(-1,1),random.uniform(-1,1))

    def _rand_sphere(self):
        u,v = random.random()*2*math.pi, random.random()*math.pi
        return (math.cos(u)*math.sin(v), math.cos(v), math.sin(u)*math.sin(v))

    def _rand_cylinder(self):
        t = random.random()*2*math.pi
        r = math.sqrt(random.random())
        return (r*math.cos(t), random.uniform(-1,1), r*math.sin(t))

    def _rand_cone(self):
        y = random.random()
        r = (1-y)*math.sqrt(random.random())
        t = random.random()*2*math.pi
        return (r*math.cos(t), -1+2*y, r*math.sin(t))

    def _rand_tetrahedron(self):
        # Correct uniform sampling: sort 3 random values, use gaps as barycentric coords
        s, t, u = sorted([random.random(), random.random(), random.random()])
        a, b, c, d = s, t - s, u - t, 1 - u
        v0 = np.array((0, 1, 0))
        v1 = np.array((-1, -1, -1))
        v2 = np.array((1, -1, -1))
        v3 = np.array((0, -1, 1))
        return tuple(a*v0 + b*v1 + c*v2 + d*v3)

    # ---------- CONTROL ----------
    def next_shape(self):
        self.shape_id = (self.shape_id + 1) % len(self.shapes)
        self.current_shape_index = self.shape_id

    def update_spin(self, fist):
        self.spin = min(self.spin + 0.002, 0.04) if fist else self.spin * 0.9
        self.angle_z += self.spin

    # ---------- ROTATION ----------
    def _rotate(self, p):
        x,y,z = p
        cx,cy,cz = map(math.cos,(self.sx,self.sy,self.sz))
        sx,sy,sz = map(math.sin,(self.sx,self.sy,self.sz))

        y,z = y*cx - z*sx, y*sx + z*cx
        x,z = x*cy + z*sy, -x*sy + z*cy
        x,y = x*cz - y*sz, x*sz + y*cz
        return x,y,z

    # ---------- DRAW ----------
    def draw(self, frame):
        h,w,_ = frame.shape
        cx,cy = w//2,h//2

        self.sx = lerp(self.sx, self.angle_x, 0.12)
        self.sy = lerp(self.sy, self.angle_y, 0.12)
        self.sz = lerp(self.sz, self.angle_z, 0.12)
        self.sscale = lerp(self.sscale, self.scale, 0.15)

        shape = self.shapes[self.current_shape_index]
        col, gl = COLORS[shape]
        s = int(self.size * self.sscale)

        core = np.zeros_like(frame)
        glow = np.zeros_like(frame)

        for p in self.clouds[shape]:
            x,y,z = self._rotate(p)
            px,py = int(cx+x*s), int(cy+y*s)
            if 0<=px<w and 0<=py<h:
                cv2.circle(core,(px,py),1,col,-1)
                cv2.circle(glow,(px,py),4,gl,-1)

        self._draw_outline(shape, core, glow, cx, cy, s, col)

        glow = cv2.GaussianBlur(glow,(0,0),7)
        frame[:] = cv2.addWeighted(frame,1.0,glow,0.28,0)
        frame[:] = cv2.addWeighted(frame,1.0,core,1.0,0)

        self._draw_hud(frame, shape)

    # ---------- HUD ----------
    def _draw_hud(self, frame, shape):
        h,w,_ = frame.shape
        x = w - 240
        y = h//2 - 90

        if shape != self.last_shape:
            self.info_line = 0
            self.info_char = 0
            self.info_timer = 0
            self.last_shape = shape

        cv2.putText(frame, shape.upper(), (x,y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                    (220,240,255), 1, cv2.LINE_AA)

        lines = INFO.get(shape, [])
        fy = y + 24

        self.info_timer += 1
        if self.info_timer % 2 == 0:
            self.info_char += 1

        for i in range(self.info_line + 1):
            if i >= len(lines): break

            text = lines[i]
            if i == self.info_line:
                text = text[:self.info_char]
                if self.info_char >= len(lines[i]):
                    self.info_char = 0
                    self.info_line += 1

            cv2.circle(frame, (x-10, fy-4), 3, (180,220,255), -1)
            cv2.putText(frame, text, (x,fy),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.38,
                        (200,220,235), 1, cv2.LINE_AA)
            fy += 18

        # ---------- MINI WHITE GLOW GRAPH ----------
        gx = x
        gy = fy + 10
        gw = 120
        gh = 45

        graph_color = (245,245,245)
        graph_glow  = (180,180,180)

        values = [0.2, 0.45, 0.35, 0.7, 0.55]
        pts = []
        for i,v in enumerate(values):
            px = int(gx + i*(gw/(len(values)-1)))
            py = int(gy + gh - v*gh)
            pts.append((px,py))

        for i in range(len(pts)-1):
            cv2.line(frame, pts[i], pts[i+1], graph_glow, 3, cv2.LINE_AA)
        for i in range(len(pts)-1):
            cv2.line(frame, pts[i], pts[i+1], graph_color, 1, cv2.LINE_AA)

        cv2.rectangle(frame, (gx,gy), (gx+gw,gy+gh), graph_glow, 1)

    # ---------- OUTLINES ----------
    def _draw_outline(self, shape, core, glow, cx, cy, s, col):
        def proj(p):
            x,y,z = self._rotate(p)
            return int(cx+x*s), int(cy+y*s)

        if shape in ("Cube","Cuboid"):
            a = 1.3 if shape=="Cuboid" else 1
            pts=[(-a,-1,-1),(a,-1,-1),(a,1,-1),(-a,1,-1),
                 (-a,-1,1),(a,-1,1),(a,1,1),(-a,1,1)]
            P=[proj(p) for p in pts]
            edges=[(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
            for i,j in edges:
                cv2.line(glow,P[i],P[j],col,4,cv2.LINE_AA)
                cv2.line(core,P[i],P[j],col,2,cv2.LINE_AA)

        elif shape=="Triangle":
            pts=[(0,1,0),(-1,-1,-1),(1,-1,-1),(0,-1,1)]
            P=[proj(p) for p in pts]
            for i,j in [(0,1),(0,2),(0,3),(1,2),(2,3),(3,1)]:
                cv2.line(glow,P[i],P[j],col,4,cv2.LINE_AA)
                cv2.line(core,P[i],P[j],col,2,cv2.LINE_AA)

        elif shape=="Cylinder":
            for y in (-1,1):
                ring=[proj((math.cos(t),y,math.sin(t))) for t in np.linspace(0,2*math.pi,40)]
                cv2.polylines(glow,[np.array(ring)],True,col,4)
                cv2.polylines(core,[np.array(ring)],True,col,2)
            for x in (-1,1):
                a,b=proj((x,1,0)),proj((x,-1,0))
                cv2.line(glow,a,b,col,4,cv2.LINE_AA)
                cv2.line(core,a,b,col,2,cv2.LINE_AA)

        elif shape=="Cone":
            tip=proj((0,1,0))
            base=[proj((math.cos(t),-1,math.sin(t))) for t in np.linspace(0,2*math.pi,40)]
            cv2.polylines(glow,[np.array(base)],True,col,4)
            cv2.polylines(core,[np.array(base)],True,col,2)
            cv2.line(glow,tip,proj((0,-1,0)),col,4,cv2.LINE_AA)
            cv2.line(core,tip,proj((0,-1,0)),col,2,cv2.LINE_AA)
