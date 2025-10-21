def interpolated_consumption(profile, minutes, standby):
    keys = sorted(profile)
    if not keys:
        return standby
    if minutes <= keys[0]:
        return profile[keys[0]]
    elif minutes >= keys[-1]:
        return profile[keys[-1]]
    else:
        for i in range(len(keys) - 1):
            t1, t2 = keys[i], keys[i + 1]
            if t1 <= minutes < t2:
                c1, c2 = profile[t1], profile[t2]
                factor = (minutes - t1) / (t2 - t1)
                return c1 + (c2 - c1) * factor
    return profile[keys[0]]

# Profiles: keys are minutes from start; values are Watts; "standby" is the idle draw.
consumption_profiles = {
    "Fridge": {
        "standby": 23, # on the left the value of the minutes, on the right the value of the power consumed
        "profile": {
            0: 74.7,
            16: 70.6,
            33: 70.6,
            49: 99.7,
            65: 99.7,
            81: 99.7,
            98: 74.8,
            114: 24.0,
            130: 24.0,
            146: 90.1,
            163: 90.1,
            179: 82.9
        }
    },

    "Washing_Machine": {
        "standby": 0,
        "profile": {
            0: 3.0,
            13: 687.6,
            26: 2094.3,
            39: 102.9,
            52: 100.3,
            65: 108.3,
            78: 138.7,
            91: 255.0
        }
    },

    "Oven": {
        "standby": 0,
        "profile": {
            0: 942.8,
            3: 995.3,
            6: 916.6,
            9: 947.7
        }
    },

    "Computer": {
        "standby": 103.5,
        "profile": {
            0: 90.4,
            13: 90.9,
            26: 52.1,
            65: 73.5,
            78: 106.5,
            101: 111.5,
            114: 108.7,
            127: 103.2,
            150: 100.9,
            173: 102.7,
            196: 103.8,
            205: 105.3,
            218: 104.6,
            231: 103.1,
            245: 103.5  # return to standby
        }
    },

    "Dishwasher": {
        "standby": 0,
        "profile": {
            0: 67.1,
            13: 1716.1,
            26: 151.2,
            39: 66.5,
            52: 1966.7,
            65: 7.8,
            78: 4.6
        }
    },

    "Coffee_Machine": {
        "standby": 0,
        "profile": {
            0: 1200.0,
            1: 700.0,
            2: 200.0
        }
    }
}


def consumption_step(profile: dict, minutes: float, standby: float, repeat: bool = False, start_from_standby: bool = True) -> float:

    if not profile:
        return standby
    keys = sorted(profile)
    duration = keys[-1]

    t = minutes % duration if repeat and duration > 0 else minutes

    if t < keys[0]:
        return profile[keys[0]]

    last_key = keys[0]
    for k in keys:
        if t < k:
            return profile[last_key]
        last_key = k
    return profile[keys[-1]] if repeat else profile[keys[-1]]

def get_device_consumption(device_name, device_type, current_timestamp, active_cycles, device_state=1):
    if device_state == 0:
        return 0.0

    profile = consumption_profiles.get(device_type)
    if not profile:
        return 0.0

    standby = profile["standby"]
    prof_det = profile["profile"]

    # Which device types should loop their profile (e.g., fridge cycles) versus run once.
    repeat_by_type = {
        "Fridge": True,
        "Washing_Machine": False,
        "Dishwasher": False,
        "Coffee_Machine": False,
        "Oven": False,
        "Computer": False
    }

    repeat = repeat_by_type.get(device_type, False)

    if device_name in active_cycles:
        start_time, _type = active_cycles[device_name]
        elapsed_min = (current_timestamp - start_time).total_seconds() / 60.0
        return consumption_step(prof_det, elapsed_min, standby, repeat=repeat, start_from_standby=True)
    else:
        # device turned on but cycle not recorded: start immediately from t=0 (no standby)
        keys = sorted(prof_det)
        return prof_det[keys[0]] if keys else standby
