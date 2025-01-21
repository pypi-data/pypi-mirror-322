#Definition of Sonar class

import numpy as np
import pandas as pd
import math

#dtype for '.sl2' files (144 bytes)
sl2_frame_dtype = np.dtype([
    ("first_byte", "<u4"),
    ("frame_version", "<u4"),
    ("unknown8", "<f4"),
    ("unknown12", "<f4"),
    ("unknown16", "<f4"),
    ("unknown20", "<f4"),
    ("unknown24", "<f4"),
    ("frame_size", "<u2"),
    ("prev_frame_size", "<u2"),
    ("survey_type", "<u2"),
    ("packet_size", "<u2"),
    ("id", "<u4"),
    ("min_range", "<f4"),
    ("max_range", "<f4"),
    ("unknown48", "<f4"),
    ("unknown52", "<u1"),
    ("frequency_type", "<u2"),
    ("unknown55", "<u1"),
    ("unknown56", "<f4"),
    ("hardware_time", "<u4"),
    ("water_depth", "<f4"),
    ("unknown68", "<f4"),
    ("unknown72", "<f4"),
    ("unknown76", "<f4"),
    ("unknown80", "<f4"),
    ("unknown84", "<f4"),
    ("unknown88", "<f4"),
    ("unknown92", "<f4"),
    ("unknown96", "<f4"),
    ("gps_speed", "<f4"),
    ("water_temperature", "<f4"),
    ("x", "<i4"),
    ("y", "<i4"),
    ("water_speed", "<f4"),
    ("gps_heading", "<f4"),
    ("gps_altitude", "<f4"),
    ("magnetic_heading", "<f4"),
    ("flags", "<u2"),
    ("unknown132", "<u2"),
    ("unknown136", "<f4"),
    ("seconds", "<u4")
])

#dtype for '.sl3' files (168 bytes)
sl3_frame_dtype = np.dtype([
    ("first_byte", "<u4"),
    ("frame_version", "<u4"),
    ("frame_size", "<u2"),
    ("prev_frame_size", "<u2"),
    ("survey_type", "<u2"),
    ("unknown14", "<i2"),
    ("id", "<u4"),
    ("min_range", "<f4"),
    ("max_range", "<f4"),
    ("unknown28", "<f4"),
    ("unknown32", "<f4"),
    ("unknown36", "<f4"),
    ("hardware_time", "<u4"),
    ("echo_size", "<u4"),
    ("water_depth", "<f4"),
    ("frequency_type", "<u2"),
    ("unknown54", "<f4"),
    ("unknown58", "<f4"),
    ("unknown62", "<i2"),
    ("unknown64", "<f4"),
    ("unknown68", "<f4"),
    ("unknown72", "<f4"),
    ("unknown76", "<f4"),
    ("unknown80", "<f4"),
    ("gps_speed", "<f4"),
    ("water_temperature", "<f4"),
    ("x", "<i4"),
    ("y", "<i4"),
    ("water_speed", "<f4"),
    ("gps_heading", "<f4"),
    ("gps_altitude", "<f4"),
    ("magnetic_heading", "<f4"),
    ("flags", "<u2"),
    ("unknown118", "<u2"),
    ("unknown120", "<u4"),
    ("seconds", "<u4"), #milliseconds
    ("prev_primary_offset", "<u4"),
    ("prev_secondary_offset", "<u4"),
    ("prev_downscan_offset", "<u4"),
    ("prev_left_sidescan_offset", "<u4"),
    ("prev_right_sidescan_offset", "<u4"),
    ("prev_sidescan_offset", "<u4"),
    ("unknown152", "<u4"),
    ("unknown156", "<u4"),
    ("unknown160", "<u4"),
    ("prev_3d_offseft", "<u4")
])

class Sonar:
    '''
    Class for reading and parsing the content of the Lowrance '.sl2' and '.sl3' file formats used to store sonar data.

    Arguments:
    clean = True - (True is default) - Perform basic data cleaning including dropping unknown columns and rows and observation where the water depth is 0.
    augment_coords = True - (False is default) - Perform coordinate augmentation as implemented in https://github.com/halmaia/SL3Reader.
    '''
    
    def __init__(self, path: str, clean: bool = True, augment_coords: bool = False):
        self.path = path
        self.file_header_size = 8
        self.extension = path.split(".")[-1]
        self.frame_header_size = 168 if "sl3" in self.extension else 144
        self.frame_dtype = sl3_frame_dtype if "sl3" in self.extension else sl2_frame_dtype

        self.supported_channels = ["primary", "secondary", "downscan", "sidescan"]
        self.valid_channels = []
        self.valid_channels_records = []
        
        self.survey_dict = {0: 'primary', 1: 'secondary', 2: 'downscan',
                            3: 'left_sidescan', 4: 'right_sidescan', 5: 'sidescan'}
        
        self.frequency_dict = {0: "200kHz", 1: "50kHz", 2: "83kHz",
                               3: "455kHz", 4: "800kHz", 5: "38kHz", 
                               6: "28kHz", 7: "130kHz_210kHz", 8: "90kHz_150kHz", 
                               9: "40kHz_60kHz", 10: "25kHz_45kHz"}
        
        self.vars_to_keep = ["id", "survey", "datetime",
                             "x", "y", "longitude", "latitude", 
                             "min_range", "max_range", "water_depth", 
                             "gps_speed", "gps_heading", "gps_altitude", 
                             "bottom_index", "frames"]
        
        self.augment_coords = augment_coords
        if augment_coords:
            self.vars_to_keep = self.vars_to_keep + ["longitude_augmented", "latitude_augmented"]

        self._read_bin()
        self._parse_header()
        self._decode()
        self._process()
        self._valid_channels()

        if augment_coords:
            self._coordinate_augmentation()

        if clean:
            self._select()
            self._drop_zero_depth()
            self._drop_unknown_channels()
            
        self._describe()

    def _read_bin(self):
        with open(self.path, "rb") as f:
            blob = f.read()
        self.header = blob[:self.file_header_size]
        self.buffer = blob[self.file_header_size:]
    
    def _parse_header(self):
        self.version, self.device_id, self.blocksize, self.reserved = np.frombuffer(self.header, dtype="int16")
        
    def _decode(self):
        position = 0
        frame_header_list = []
        frame_size_slice = slice(8, 10) if "sl3" in self.extension else slice(28, 30)

        while (position < len(self.buffer)):
            frame_head = self.buffer[position:(position+self.frame_header_size)]
            frame_size = int.from_bytes(frame_head[frame_size_slice], "little", signed = False)
            
            position += frame_size
            
            if(position < len(self.buffer)):
                frame_header_list.append(frame_head)
        
        self.df = pd.DataFrame(np.frombuffer(b''.join(frame_header_list), dtype=self.frame_dtype))
        self.df["first_byte_no_offset"] = self.df["first_byte"] - self.file_header_size
        self.df["frames"] = [np.frombuffer(self.buffer[(i+self.frame_header_size):(i+p)], dtype="uint8") for i, p in zip(self.df["first_byte_no_offset"], self.df["frame_size"])]        
        
    def _x2lon(self, x):
        return(x/6356752.3142*(180/math.pi))

    def _y2lat(self, y):
        return(((2*np.arctan(np.exp(y/6356752.3142)))-(math.pi/2))*(180/math.pi))
    
    def _bottom_index(self):
        frame_len = np.array([len(i) for i in self.df["frames"]])
        frame_bottom_index = ((frame_len/(self.df["max_range"]-self.df["min_range"]))*self.df["water_depth"]).astype("int32")
        return(frame_bottom_index)
    
    def _process(self):
        self.df[["water_depth", "min_range", "max_range", "gps_altitude"]] /= 3.2808399 #feet to meter
        self.df["gps_speed"] *=  0.5144 #knots to m/s
        self.df["survey"] = [self.survey_dict.get(i, "unknown") for i in self.df["survey_type"]]
        self.df["frequency"] = [self.frequency_dict.get(i, "unknown") for i in self.df["frequency_type"]]
        self.df["seconds"] /= 1000 #milliseconds to seconds
        hardware_time_start = self.df["hardware_time"][0]
        self.df["datetime"] = pd.to_datetime(hardware_time_start+self.df["seconds"], unit='s')
        self.df["bottom_index"] = self._bottom_index()
        self.frame_version = self.df["frame_version"].iloc[0]
        self.df["longitude"] = self._x2lon(self.df["x"])
        self.df["latitude"] = self._y2lat(self.df["y"])

    def _coordinate_augmentation(self):
        self.df['longitude_augmented'] = self.df['longitude']
        self.df['latitude_augmented'] = self.df['latitude']

        longitude0 = self.df.loc[0, 'longitude']
        latitude0 = self.df.loc[0, 'latitude']
        v0 = self.df.loc[0, 'gps_speed']
        t0 = self.df.loc[0, 'seconds']
        d0 = math.tau - self.df.loc[0, 'gps_heading'] + (math.pi / 2)
        lim = 1.2

        for i in range(1, len(self.df)):
            t1 = self.df.loc[i, 'seconds']
            v1 = self.df.loc[i, 'gps_speed']
            d1 = math.tau - self.df.loc[i, 'gps_heading'] + (math.pi / 2)

            dt = t1 - t0
            v_longitude0 = math.cos(d0) * v0
            v_latitude0 = math.sin(d0) * v0
            v_longitude1 = math.cos(d1) * v1
            v_latitude1 = math.sin(d1) * v1

            latitude0 += dt * 0.5 * (v_latitude0 + v_latitude1) * 180 / (math.pi * 6356752.3142)
            longitude0 += dt * 0.5 * (v_longitude0 + v_longitude1) * 180 / (math.pi * math.cos(math.radians(latitude0)) * 6356752.3142)

            d0, t0, v0 = d1, t1, v1

            if self.df.loc[i, 'survey_type'] in [0, 1]:
                dy = self.get_latitude_distance(latitude0, self.df.loc[i, 'latitude'])
                if abs(dy) > lim:
                    latitude0 = self.df.loc[i, 'latitude'] + math.copysign(math.degrees(lim / 6356752.3142), latitude0 - self.df.loc[i, 'latitude'])

                dx = self.get_longitude_distance(longitude0, self.df.loc[i, 'longitude'], latitude0)
                if abs(dx) > lim:
                    longitude0 = self.df.loc[i, 'longitude'] + math.copysign(math.degrees(lim / (6356752.3142 * math.cos(math.radians(latitude0)))), longitude0 - self.df.loc[i, 'longitude'])
            else:
                dy = self.get_latitude_distance(latitude0, self.df.loc[i, 'latitude'])
                if abs(dy) > 50:
                    latitude0 = self.df.loc[i, 'latitude']

                dx = self.get_longitude_distance(longitude0, self.df.loc[i, 'longitude'], latitude0)
                if abs(dx) > 50:
                    longitude0 = self.df.loc[i, 'longitude']

            self.df.loc[i, 'longitude_augmented'] = longitude0
            self.df.loc[i, 'latitude_augmented'] = latitude0

    def get_latitude_distance(self, lat1: float, lat2: float) -> float:
        return math.radians(abs(lat2 - lat1)) * 6356752.3142

    def get_longitude_distance(self, lon1: float, lon2: float, lat: float) -> float:
        return math.radians(abs(lon2 - lon1)) * (6356752.3142 * math.cos(math.radians(lat)))
        
    def _valid_channels(self):
        found_channels = set(self.df["survey"].tolist())
        self.valid_channels = [i for i in self.supported_channels if i in found_channels]

    def _select(self):
        self.df = self.df[self.vars_to_keep]
        
    def _describe(self):
        for i in self.valid_channels:
            data = self.df.query(f"survey == '{i}'")
            nrow = data.shape[0]
            self.valid_channels_records.append(nrow)
                
    def _drop_zero_depth(self):
        self.df = self.df[self.df["water_depth"] > 0]
        
    def _drop_unknown_channels(self):
        self.df = self.df[self.df["survey"].isin(self.valid_channels)]
        
    def __repr__(self):
        base_string = f"Summary of {self.extension.upper()} file:\n\n"
        
        for i, c in zip(self.valid_channels, self.valid_channels_records):
            base_string += f"- {i.title()} channel with {c} frames\n"

        datetime_start = self.df["datetime"].iloc[0]
        datetime_end = self.df["datetime"].iloc[-1]
        base_string += f"\nStart time: {datetime_start}\nEnd time: {datetime_end}\n"
        base_string += f"\nFile info: version {self.version}, device {self.device_id}, blocksize {self.blocksize}, frame version {self.frame_version}"
        
        return(base_string)
        
    def image(self, channel: str) -> np.ndarray:
        '''Extract the raw sonar image for a specific channel'''
        
        if channel not in self.valid_channels:
            raise ValueError("Wrong channel name or no data for that channel")
        
        return(np.stack(self.df.query(f"survey == '{channel}'")["frames"]))            
    
    def sidescan_xyz(self) -> pd.DataFrame:
        '''Extract georeferenced sidescan data as XYZ coordinates'''

        if "sidescan" not in self.valid_channels:
            raise ValueError("No sidescan data found")
        
        data = self.df.query(f"survey == 'sidescan'")
        dist = [np.linspace(start, stop, num = len(f)) for start, stop, f in zip(data["min_range"], 
                                                                                 data["max_range"], 
                                                                                 data["frames"])]
        dist_stack = np.stack(dist)
        
        sidescan_z = self.image("sidescan")            

        if self.augment_coords:
            sidescan_x = np.expand_dims(data["x_augmented"], axis=1) + dist_stack * np.cos(np.expand_dims(data["gps_heading"], axis=1))
            sidescan_y = np.expand_dims(data["y_augmented"], axis=1) - dist_stack * np.sin(np.expand_dims(data["gps_heading"], axis=1))

        else:
            sidescan_x = np.expand_dims(data["x"], axis=1) + dist_stack * np.cos(np.expand_dims(data["gps_heading"], axis=1))
            sidescan_y = np.expand_dims(data["y"], axis=1) - dist_stack * np.sin(np.expand_dims(data["gps_heading"], axis=1))
        
        sidescan_df = pd.DataFrame({"x": sidescan_x.ravel(),
                                    "y": sidescan_y.ravel(),
                                    "z": sidescan_z.ravel()})

        sidescan_df["longitude"] = self._x2lon(sidescan_df["x"])
        sidescan_df["latitude"] = self._y2lat(sidescan_df["y"])
        
        return(sidescan_df)
    
    def _interp_water(self, water, depth, out_len):
        x = np.linspace(0, depth, num=out_len)
        xp = np.linspace(0, depth, num=len(water))
        y = np.interp(x, xp, water)
        
        return(y)

    def water(self, channel: str, pixels: int) -> np.ndarray:
        '''Extract the water column part of the the raw sonar imagery for a specific channel.
        The water column part extends from the surface to water depth.
        Linear interpolation is performed for each sonar ping to create arrays of equal length of size "pixels"'''

        if channel not in self.valid_channels or channel == "sidescan":
            raise ValueError(f'Valid channels: {", ".join(self.valid_channels)}')
        
        data = self.df.query(f"survey == '{channel}'")
        frames_water = [f[0:b] for f, b in zip(data["frames"], data["bottom_index"])]
        frames_water_interp = [self._interp_water(f, d, pixels) for f, d in zip(frames_water, data["water_depth"])]
        
        return(np.stack(frames_water_interp))
    
    def bottom(self, channel: str) -> np.ndarray:
        '''Extract the bottom (sediment) part of the the raw sonar imagery for a specific channel.
        The bottom part extends from the water depth to the maximum range of the sonar.
        The length of the arrays are determined by the minimum length of all bottom pings for the survey'''
        
        if channel not in self.valid_channels or channel == "sidescan":
            raise ValueError(f'Valid channels: {", ".join(self.valid_channels)}')
        
        data = self.df.query(f"survey == '{channel}'")
        frames_bottom = [f[b:] for f, b in zip(data["frames"], data["bottom_index"])]
        min_len = min([len(f) for f in frames_bottom])
        frames_bottom_cut = [f[:min_len] for f in frames_bottom]
        
        return(np.stack(frames_bottom_cut))

    def bottom_intensity(self, channel: str) -> np.ndarray:
        '''Extract raw sonar intensity at the bottom'''
        
        if channel not in self.valid_channels or channel == "sidescan":
            raise ValueError(f'Valid channels: {", ".join(self.valid_channels)}')
        
        data = self.df.query(f"survey == '{channel}'")
        bottom_intensity = np.array([f[i] for f, i in zip(data["frames"], data["bottom_index"])])
                
        return(bottom_intensity)
