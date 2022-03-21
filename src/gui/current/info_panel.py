from datetime import datetime
from math import pi
from tkinter import *
from numpy import cos, sin, sqrt, linspace
from gui.current import bodies_list as bl
import pandas as pd
from util import sys
from util import mathf

max_scale_main = 3
min_scale_main = .1
zoom_diff_main = .1

max_scale_zoom = 100
min_scale_zoom = 20
zoom_diff_zoom = 10

AU = 149597871
deg2rad = pi / 180.0

orbit_res = 50

class InfoPanel:

    def __init__(self, root, bg_color):
        self.frame = Frame(root, bg=bg_color, borderwidth=10)
        self.frame.pack(expand=True, fill=BOTH)

        self.bodies_df = pd.read_csv('./gui/current/bodies.csv')
        self.target_julian = self.current_julian_date()

        # To create a label, which text may be changed we need to create StringVar object
        self.text = StringVar()
        self.text.set("Select close approach body")

        # ==== Details
        details_frame = Frame(self.frame, bg=bg_color, height=130)
        details_frame.pack(fill=BOTH, pady=(0, 5))
        details_frame.pack_propagate(0)

        label = Label(details_frame, textvariable=self.text,
                      background=bg_color, foreground='white')
        label.pack()

        # ==== Visualization
        self.bodies_coords = pd.DataFrame(columns=['Name', 'x', 'y'])
        self.zoom_mode = False
        self.focus_planet_name = ''
        self.focus_body_name = ''
        self.visual_canvas = Canvas(self.frame, bg='black')
        self.visual_canvas.pack(fill=BOTH, expand=True, pady=(5, 0))

        self.visual_canvas.bind("<Configure>", self.check_size)
        self.scale = 1

        # Scale GUI
        scale_label = Label(self.visual_canvas, text='Scale:',
                            background='black', foreground='white')
        scale_label.pack(side=LEFT, padx=5)
        scale_label.place(x=10, y=13)
        scaleup_btn = Button(self.visual_canvas, text='+',
                             command=self.increase_scale, width=3)
        scaleup_btn.pack(padx=5)
        scaleup_btn.place(x=50, y=10)
        scaledown_btn = Button(self.visual_canvas, text='-',
                               command=self.decrease_scale, width=3)
        scaledown_btn.pack(padx=5)
        scaledown_btn.place(x=90, y=10)
        self.scaleText = StringVar()
        self.scaleText.set(f'x{round(self.scale, 2)}')
        scale_value = Label(self.visual_canvas, textvariable=self.scaleText,
                            background='black', foreground='white')
        scale_value.pack(side=LEFT, padx=5)
        scale_value.place(x=130, y=13)

        # Time GUI
        date_label = Label(self.visual_canvas, text='Date:',
                            background='black', foreground='white')
        date_label.pack(side=LEFT, padx=5)
        date_label.place(x=10, y=43)
        previousday_btn = Button(self.visual_canvas, text='<',
                             command=self.previous_day, width=3)
        previousday_btn.pack(padx=5)
        previousday_btn.place(x=50, y=40)
        nextday_btn = Button(self.visual_canvas, text='>',
                               command=self.next_day, width=3)
        nextday_btn.pack(padx=5)
        nextday_btn.place(x=90, y=40)
        nextday_btn = Button(self.visual_canvas, text='reset',
                               command=self.reset_date, width=5)
        nextday_btn.pack(padx=5)
        nextday_btn.place(x=130, y=40)
        self.dateText = StringVar()
        self.dateText.set(f'{sys.get_gregorian_datetime(self.target_julian)}')
        date_value = Label(self.visual_canvas, textvariable=self.dateText,
                            background='black', foreground='white')
        date_value.pack(side=LEFT, padx=5)
        date_value.place(x=185, y=43)

    def increase_scale(self):
        self.scale += (zoom_diff_main if self.zoom_mode == False else zoom_diff_zoom)

        if self.scale > max_scale_main and self.zoom_mode == False:
            self.zoom_mode = True
            self.scale = min_scale_zoom
        if self.scale > max_scale_zoom:
            self.scale = max_scale_zoom

        self.scaleText.set(f'x{round(self.scale, 2)}')
        self.draw()

    def decrease_scale(self):
        self.scale -= (zoom_diff_main if self.zoom_mode == False else zoom_diff_zoom)

        if self.scale < min_scale_zoom and self.zoom_mode == True:
            self.zoom_mode = False
            self.scale = max_scale_main
        if self.scale < min_scale_main:
            self.scale = min_scale_main

        self.scaleText.set(f'x{round(self.scale, 2)}')
        self.draw()

    def next_day(self):
        self.target_julian += 1
        self.dateText.set(f'{sys.get_gregorian_datetime(self.target_julian)}')
        self.draw()
        self.change_focus(self.focus_planet_name)

    def previous_day(self):
        self.target_julian -= 1
        self.dateText.set(f'{sys.get_gregorian_datetime(self.target_julian)}')
        self.draw()
        self.change_focus(self.focus_planet_name)

    def reset_date(self):
        self.target_julian = self.current_julian_date()
        self.dateText.set(f'{sys.get_gregorian_datetime(self.target_julian)}')
        self.draw()
        self.change_focus(self.focus_planet_name)

    def current_julian_date(self):
        return sys.get_julian_datetime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

    def check_size(self, event):
        self.canvas_x = self.visual_canvas.winfo_width()
        self.canvas_y = self.visual_canvas.winfo_height()
        self.center_x, self.center_y = self.canvas_x / 2, self.canvas_y / 2
        self.offset_x = 0
        self.offset_y = 0
        self.draw()
        self.change_focus(self.focus_planet_name)

    def clear_canvas(self):
        self.visual_canvas.delete("all")

    def draw(self):
        self.clear_canvas()

        # Star
        self.draw_body(point=[0, 0], radius=10, color='yellow')

        # Planets
        for i, body_data in enumerate(self.bodies_df.iloc):

            if self.zoom_mode == True and self.focus_planet_name != body_data['Name']:
                continue

            clr = body_data['Color']

            # draw planet
            planet_pos = last_pos = self.planet_space_position(body_data, self.target_julian)
            self.draw_body(point=planet_pos, radius=body_data['Radius'] / 1000, color=clr)
            self.bodies_coords.loc[i] = [body_data['Name'], planet_pos[0], planet_pos[1]]

            # draw orbit
            days_per_point = body_data['per'] / orbit_res
            for i in range(orbit_res):       
                new_pos = self.planet_space_position(body_data, self.target_julian - i * days_per_point)
                self.draw_line(last_pos, new_pos, clr)
                last_pos = new_pos
            self.draw_line(last_pos, planet_pos, clr)

        # Asteroids / Comets
        if bl.all_bodies_df is not None:
            focus_bodies_df = bl.all_bodies_df[bl.all_bodies_df['body'] == self.focus_planet_name]
            for body_data in focus_bodies_df.iloc:
               
                body_name = str(body_data['des'])
                clr = 'grey' if self.focus_body_name != body_name else 'white'
                body_data = pd.to_numeric(body_data, errors='coerce')

                # move mean anomaly forward in time to get current value (add mean motion for each day difference)
                body_mean_anomaly = body_data['ma'] + (self.target_julian - body_data['epoch']) * body_data['n']
                # draw asteroid/comet
                body_pos = self.body_space_position(body_data, body_mean_anomaly)
                self.draw_body(point=body_pos, radius=3, color=clr)

                # draw orbit
                if self.zoom_mode == True or self.focus_body_name == body_name:
                    first_pos = last_pos = self.body_space_position(body_data, body_mean_anomaly)
                    bins = linspace(body_mean_anomaly, body_mean_anomaly + 360, orbit_res)
                    angles = mathf.sigmoid(bins * deg2rad - pi - (body_mean_anomaly * deg2rad), 2) * 360
                    for i in range(1, orbit_res):
                        new_pos = self.body_space_position(body_data, angles[i] + body_mean_anomaly)
                        self.draw_line(last_pos, new_pos, clr)
                        last_pos = new_pos
                    self.draw_line(last_pos, first_pos, clr)

    def draw_body(self, point, radius, color):
        _radius = radius * (self.scale if self.zoom_mode == False else max_scale_main)
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

    def planet_space_position(self, obj_data, julian_date):
        # based on https://ssd.jpl.nasa.gov/planets/approx_pos.html

        T = (julian_date - 2451545) / 36525

        a = obj_data['a']               # semi-major axis (AU)
        e = obj_data['e']               # eccentricity                         
        I = obj_data['i']               # inclination to the ecliptic    
        O = obj_data['om']              # longitude of the ascending node   
        L = obj_data['L']               # mean longitude          
        W = obj_data['W']               # longitude of perihelion       

        a += obj_data['a_rate'] * T
        e += obj_data['e_rate'] * T
        I += obj_data['i_rate'] * T 
        O += obj_data['om_rate'] * T
        L += obj_data['L_rate'] * T
        W += obj_data['W_rate'] * T

        # b = obj_data['b']
        # c = obj_data['c']
        # s = obj_data['s']
        # f = obj_data['f']

        # argument of perihelion
        w = W - O

        # mean anomaly
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

    def body_space_position(self, obj_data, point_angle=-1):
        # based on https://ssd.jpl.nasa.gov/planets/approx_pos.html

        a = obj_data['a']               # semi-major axis (AU)
        e = obj_data['e']               # eccentricity                         
        I = obj_data['i']               # inclination to the ecliptic    
        O = obj_data['om']              # longitude of the ascending node   

        # argument of perihelion
        w = obj_data['w']

        # mean anomaly
        if point_angle >= 0:
            M = point_angle
        else:
            M = obj_data['ma']
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
        self.focus_planet_name = body_name
        df = self.bodies_coords[self.bodies_coords['Name'] == body_name]
        if len(df.index) > 0:
            self.offset_x = -float(df['x'])
            self.offset_y = -float(df['y'])
            self.draw()

    def supply_body_info(self, body_df_row):
        self.focus_body_name = str(body_df_row['des'])
        self.text.set(
            f"Name: {str(body_df_row['des'])}\
            \nClosest approach: {str(body_df_row['cd'])}\
            \nDistance: {str(float(body_df_row['dist']) * AU / 1000000)} mln km")
        self.draw()
