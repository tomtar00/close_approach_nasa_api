from datetime import datetime
from math import pi
from tkinter import *
from numpy import cos, sin, sqrt
from util import api_utils as au
from gui.current import bodies_list as bl
import pandas as pd
from util import sys
from util import mathf

max_scale = 5
min_scale = .1
AU = 149597871
deg2rad = pi / 180.0

orbit_res = 30


class InfoPanel:

    def __init__(self, root, bg_color):
        self.frame = Frame(root, bg=bg_color, borderwidth=10)
        self.frame.pack(expand=True, fill=BOTH)

        self.bodies_df = pd.read_csv('./gui/current/bodies.csv')
        example_datetime = datetime(
            datetime.now().year, datetime.now().month, datetime.now().day)
        self.today_julian = sys.get_julian_datetime(example_datetime)

        # self.visual_data = []
        # for obj in bl.focus_bodies:
        #     key = bl.focus_bodies.get(obj).get('open_key')
        #     self.visual_data.append(au.get_json_from_url(
        #         f'https://api.le-systeme-solaire.net/rest/bodies/{key}'))

        # To create a label, which text may be changed we need to create StringVar object
        self.text = StringVar()
        self.text.set("Select close approach body")

        # Details
        details_frame = Frame(self.frame, bg=bg_color, height=130)
        details_frame.pack(fill=BOTH, pady=(0, 5))
        details_frame.pack_propagate(0)

        label = Label(details_frame, textvariable=self.text,
                      background=bg_color, foreground='white')
        label.pack()

        # Visualization
        self.visual_canvas = Canvas(self.frame, bg='black')
        self.visual_canvas.pack(fill=BOTH, expand=True, pady=(5, 0))

        self.visual_canvas.bind("<Configure>", self.check_size)
        self.scale = 1

        scaleup_btn = Button(self.visual_canvas, text='+',
                             command=self.increase_scale, width=3)
        scaleup_btn.pack(padx=5)
        scaleup_btn.place(x=10, y=10)
        scaledown_btn = Button(self.visual_canvas, text='-',
                               command=self.decrease_scale, width=3)
        scaledown_btn.pack(padx=5)
        scaledown_btn.place(x=50, y=10)
        self.scaleText = StringVar()
        self.scaleText.set(f'x{round(self.scale, 2)}')
        scale_label = Label(self.visual_canvas, textvariable=self.scaleText,
                            background='black', foreground='white')
        scale_label.pack(side=LEFT, padx=5)
        scale_label.place(x=90, y=13)

    def increase_scale(self):
        self.scale += .1
        if self.scale > max_scale:
            self.scale = max_scale
        self.scaleText.set(f'x{round(self.scale, 2)}')
        self.draw()

    def decrease_scale(self):
        self.scale -= .1
        if self.scale < min_scale:
            self.scale = min_scale
        self.scaleText.set(f'x{round(self.scale, 2)}')
        self.draw()

    def check_size(self, event):
        self.canvas_x = self.visual_canvas.winfo_width()
        self.canvas_y = self.visual_canvas.winfo_height()
        self.center_x, self.center_y = self.canvas_x / 2, self.canvas_y / 2
        self.offset_x = 0
        self.offset_y = 0
        self.draw()
        self.change_focus('Earth')

    def clear_canvas(self):
        self.visual_canvas.delete("all")

    def draw(self):
        self.clear_canvas()

        # Star
        self.draw_body(point=[0, 0], radius=10, color='yellow')

        # Planets
        # for body_data, body_name in zip(self.visual_data, bl.focus_bodies):
        #     clr = bl.focus_bodies.get(body_name).get('color')
        #     self.draw_body(point=self.body_space_position(body_data),
        #                radius=body_data['meanRadius'] / 1000, color=clr)

        self.bodies_coords = pd.DataFrame(columns=['Name', 'x', 'y'])
        for i, body_data in enumerate(self.bodies_df.iloc):

            clr = body_data['Color']

            # draw planet
            planet_pos = last_pos = self.body_space_position(body_data, self.today_julian)
            self.draw_body(point=last_pos, radius=body_data['Radius'] / 1000, color=clr)
            self.bodies_coords.loc[i] = [body_data['Name'], planet_pos[0], planet_pos[1]]

            # draw orbit
            days_per_point = body_data['per'] / orbit_res
            for i in range(orbit_res):       
                new_pos = self.body_space_position(body_data, self.today_julian - i * days_per_point)
                self.draw_line(last_pos, new_pos, clr)
                last_pos = new_pos
            self.draw_line(last_pos, planet_pos, clr)

        
        if bl.all_bodies_df is not None:
            for body_data in bl.all_bodies_df.iloc:

                # draw asteroid/comet
                body_data = pd.to_numeric(body_data, errors='coerce').round(15)
                #print(body_data)
                body_pos = last_pos = self.body_space_position(body_data, self.today_julian)
                self.draw_body(point=last_pos, radius=3, color='grey')

                # draw orbit
                days_per_point = body_data['per'] / orbit_res
                for i in range(orbit_res):
                    new_pos = self.body_space_position(body_data, self.today_julian - i * days_per_point)
                    self.draw_line(last_pos, new_pos, 'grey')
                    last_pos = new_pos
                    #print(last_pos)
                self.draw_line(last_pos, body_pos, 'grey')

    def draw_body(self, point, radius, color):
        _radius = radius * self.scale
        _point = [point[0] + self.offset_x, point[1] + self.offset_y]
        _point = [a * self.scale for a in _point]
        p1 = (self.center_x + _point[0] - _radius,
              self.center_y - _point[1] + _radius)
        p2 = (self.center_x + _point[0] + _radius,
              self.center_y - _point[1] - _radius)
        self.visual_canvas.create_oval(p1[0], p1[1], p2[0], p2[1], fill=color)

    def draw_line(self, point1, point2, color):
        _point1 = [point1[0] + self.offset_x, point1[1] + self.offset_y]
        _point2 = [point2[0] + self.offset_x, point2[1] + self.offset_y]
        _point1 = [a * self.scale for a in _point1]
        _point2 = [a * self.scale for a in _point2]
        p1 = (self.center_x + _point1[0], self.center_y - _point1[1])
        p2 = (self.center_x + _point2[0], self.center_y - _point2[1])
        self.visual_canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color)

    def body_space_position(self, obj_data, julian_date):
        # based on https://ssd.jpl.nasa.gov/planets/approx_pos.html

        T = (julian_date - 2451545) / 36525

        a = obj_data['a']               # semi-major axis (AU)
        e = obj_data['e']               # eccentricity                         
        I = obj_data['i']               # inclination to the ecliptic    
        O = obj_data['om']              # longitude of the ascending node
        

        if 'L' in obj_data:
            L = obj_data['L']           # mean longitude
            L += obj_data['L_sigma'] * T
        if 'W' in obj_data:
            W = obj_data['W']           # longitude of perihelion   
            W += obj_data['W_sigma'] * T

        a += obj_data['a_sigma'] * T
        e += obj_data['e_sigma'] * T
        I += obj_data['i_sigma'] * T 
        O += obj_data['om_sigma'] * T
        O = mathf.modulus_between_values(O, -180, 180)

        # b = obj_data['b']
        # c = obj_data['c']
        # s = obj_data['s']
        # f = obj_data['f']

        # argument of perihelion
        if 'w' in obj_data:
            w = obj_data['w']
        else:
            w = W - O
        w = mathf.modulus_between_values(w, -180, 180)

        # mean anomaly
        if 'ma' in obj_data:
            M = obj_data['ma']
        else:
            M = L - W #+ b * T**2 + c * cos(deg2rad*f*T) + s * sin(deg2rad*f*T)
        M = mathf.modulus_between_values(M, -180, 180)

        # eccentric anomaly
        E = M + e * sin(deg2rad*M) * (1.0 + e * cos(deg2rad*M))
        ee = e / deg2rad
        while True:
            dM = M - (E - ee*sin(deg2rad*E))
            dE = dM / (1 - e * cos(deg2rad*E))
            E += dE
            if (abs(dE) < 1e-6):
                break

        # if 'ma' in obj_data:
        #     print('asteroid', [a, e, I, O, w, M, E])
        # else:
        #     print(obj_data['Name'], [a, e, I, O, w, M, E])


        x1 = a * (cos(deg2rad*E) - e)
        y1 = a * sqrt(1 - e**2) * sin(deg2rad*E)

        cosw = cos(deg2rad*w)
        sinw = sin(deg2rad*w)
        cosO = cos(deg2rad*O)
        sinO = sin(deg2rad*O)
        cosI = cos(deg2rad*I)

        Xecl = (cosw*cosO - sinw*sinO*cosI)*x1 + \
            (-sinw*cosO - cosw*sinO*cosI)*y1
        Yecl = (cosw*sinO + sinw*cosO*cosI)*x1 + \
            (-sinw*sinO + cosw*cosO*cosI)*y1

        return Xecl * 100, Yecl * 100

    def change_focus(self, body_name):
        df = self.bodies_coords[self.bodies_coords['Name'] == body_name]
        self.offset_x = -float(df['x'])
        self.offset_y = -float(df['y'])
        self.draw()

    def supply_body_info(self, body_df_row):
        self.text.set(
            f"Name: {str(body_df_row['des'])}\nClosest approach: {str(body_df_row['cd'])}")
        self.draw()
