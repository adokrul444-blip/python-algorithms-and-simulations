def convert_time(time_str):
    if (time_str == ""):
        return -1
    parts = time_str.split(":")
    if (len(parts) != 3):
        return -1
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = int(parts[2])
    return hours * 3600 + minutes * 60 + seconds

def seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours}:{minutes:02d}:{seconds:02d}"

def seconds_to_pace(seconds):
    total_seconds = int(seconds)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def load_data(file_path):
    directory = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(",")

            bib = int(parts[0])
            name = parts[1]
            raw_gender = parts[3].strip()
            gender = "M" if raw_gender in ["Muži", "Muzi", "MuĹľi"] else "F"

            splits = {}
            split_keys = ["5", "10", "15", "20", "21", "26", "31", "36", "41"]

            for i in range(9):
                if parts[4 + i] != "":
                    splits[split_keys[i]] = convert_time(parts[4 + i])

            gun_time = convert_time(parts[13])
            net_time = convert_time(parts[14])

            runner = {
                "bib": bib,
                "name": name,
                "gender": gender,
                "splits": splits,
                "gun_time": gun_time,
                "net_time": net_time
            }

            directory.append(runner)

    return directory


def find_fastest(all_results, category, n=100):
    runners_in_category = []
    for runner in all_results:
        if runner["gender"] == category and runner["net_time"] != -1:
            runners_in_category.append(runner)
    runners_in_category.sort(key=lambda x: x["net_time"])
    return [runner["name"] for runner in runners_in_category[:n]]


def get_position(all_results, station, bib):
    target_runner = None
    for runner in all_results:
        if runner["bib"] == bib:
            target_runner = runner
            break
    if target_runner is None:
        return -1
    if station not in target_runner["splits"]:
        return -1
    target_category = target_runner["gender"]
    target_time = target_runner["splits"][station]
    position = 1

    for runner in all_results:
        if runner["gender"] == target_category and station in runner["splits"] and runner["splits"][station] < target_time:            position += 1

    return position


def save_results(all_results, category, station):
    filtered_runners = []
    for runner in all_results:
        if runner["gender"] == category and station in runner["splits"]:
            filtered_runners.append(runner)
    filtered_runners.sort(key=lambda x: x["splits"][station])
    with open(f"results_{category}_{station}K.csv", "w") as file:
        for i, runner in enumerate(filtered_runners, start=1):
            file.write(f"{i},{runner['bib']},{runner['name']},{seconds_to_hms(runner['splits'][station])}\n")
    return None


def get_gender_results(all_results, category):
    category_runners = []
    finishers = []

    for runner in all_results:
        if runner["gender"] == category:
            category_runners.append(runner)
            if runner["net_time"] != -1:
                finishers.append(runner)

    finishers.sort(key=lambda x: x["net_time"])

    winner = finishers[0]["name"]
    best_time = seconds_to_hms(finishers[0]["net_time"])
    average_time = seconds_to_hms(sum([runner["net_time"] for runner in finishers]) // len(finishers))
    worst_time = seconds_to_hms(finishers[-1]["net_time"])
    dnf = len(category_runners) - len(finishers)

    return {"Winner": winner, "Best": best_time, "Average": average_time, "Worst": worst_time, "DNF": dnf}


def find_most_consistent(all_results, category=None):
    best_name = ""
    best_deviation = None
    best_pace = 0.0

    for runner in all_results:
        if runner["gun_time"] != -1:
            if category is None or runner["gender"] == category:
                sorted_splits = sorted(runner["splits"].items(), key=lambda x: int(x[0]))
                paces = []
                prev_distance = 0
                prev_time = 0
                for distance, time in sorted_splits:
                    distance = float(distance)
                    pace = (time - prev_time) / (distance - prev_distance)
                    paces.append(pace)
                    prev_distance = distance
                    prev_time = time

                if prev_distance < 42.195:
                    pace = (runner["gun_time"] - prev_time) / (42.195 - prev_distance)
                    paces.append(pace)

                if len(paces) > 0:
                    avg_pace = runner["gun_time"] / 42.195
                    deviation = sum(abs(p - avg_pace) for p in paces) / len(paces)

                    if best_deviation is None or deviation < best_deviation:
                        best_name = runner["name"]
                        best_deviation = deviation
                        best_pace = avg_pace

    return (best_name, best_deviation, best_pace)


def get_target_pace_for_position(all_results, pos, category=None):
    finishers = []
    for runner in all_results:
        if runner["gun_time"] != -1:
            if category is None or runner["gender"] == category:
                finishers.append(runner)
    finishers.sort(key=lambda x: x["gun_time"])
    if pos > len(finishers):
        return ""
    target_runner = finishers[pos - 1]
    target_time = target_runner["gun_time"] - 1
    pace = target_time / 42.195
    return seconds_to_pace(pace)


def calculate_target_pace(section, section_time, target_time):
    section_time = convert_time(section_time)
    target_time = convert_time(target_time)
    remaining_distance = 42.195 - section
    remaining_time = target_time - section_time

    if remaining_time <= 0 or remaining_distance <= 0:
        return None

    pace = remaining_time / remaining_distance  
    if pace < 180:
        return None
    return seconds_to_pace(pace)


def find_slowest_starter(all_results):
    max_diff = -1
    slowest_runner = ""
    for runner in all_results:
        if runner["gun_time"] != -1 and runner["net_time"] != -1:
            diff = runner["gun_time"] - runner["net_time"]
            if diff > max_diff:
                max_diff = diff
                slowest_runner = runner["name"]
    return (slowest_runner, max_diff)


def calculate_split(all_results, bib):
    target_runner = None
    for runner in all_results:
        if runner["bib"] == bib:
            target_runner = runner
            break

    if target_runner is None:
        return ""
    if target_runner["gun_time"] == -1:
        return ""

    target_category = target_runner["gender"]
    winner_time = None

    for runner in all_results:
        if runner["gender"] == target_category and runner["gun_time"] != -1:
            if winner_time is None or runner["gun_time"] < winner_time:
                winner_time = runner["gun_time"]

    diff = target_runner["gun_time"] - winner_time

    if diff >= 3600:
        return seconds_to_hms(diff)
    else:
        minutes = diff // 60
        seconds = diff % 60
        return f"{minutes}:{seconds:02d}"


if __name__ == '__main__':
    print("Marathon Data Analytics module loaded. Use load_data('results.csv') to process race telemetry.")