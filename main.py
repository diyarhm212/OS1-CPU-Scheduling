def read_processes(filename):
    processes = []

    with open(filename, "r") as file:
        for line in file:
            parts = line.split()

            if len(parts) == 4:
                name = parts[0]
                arrival = int(parts[1])
                burst = int(parts[2])
                priority = int(parts[3])

                process = {
                    "name": name,
                    "arrival": arrival,
                    "burst": burst,
                    "priority": priority
                }

                processes.append(process)

    return processes

def fcfs(processes):
    ready = sorted(
        enumerate(processes),
        key=lambda item: (item[1]["arrival"], item[0])
    )

    time = 0
    timeline = []

    for index, process in ready:
        if time < process["arrival"]:
            time = process["arrival"]

        start = time
        end = start + process["burst"]

        timeline.append({
            "name": process["name"],
            "start": start,
            "end": end
        })

        time = end

    return timeline


def priority_scheduling(processes):
        remaining = list(enumerate(processes))
        timeline = []
        time = 0

        while remaining:
            available = [
                item for item in remaining
                if item[1]["arrival"] <= time
            ]

            if not available:
                time = min(item[1]["arrival"] for item in remaining)
                continue

            selected = min(
                available,
                key=lambda item: (
                    item[1]["priority"],
                    item[1]["arrival"],
                    item[0]
                )
            )

            index, process = selected
            start = time
            end = start + process["burst"]

            timeline.append({
                "name": process["name"],
                "start": start,
                "end": end
            })

            time = end
            remaining.remove(selected)

        return timeline

def calculate_metrics(processes, timeline):
    results = []

    for process in processes:
        name = process["name"]

        item = next(
            step for step in timeline
            if step["name"] == name
        )

        start = item["start"]
        finish = item["end"]

        turnaround = finish - process["arrival"]
        waiting = turnaround - process["burst"]
        response = start - process["arrival"]

        results.append({
            "name": name,
            "waiting": waiting,
            "turnaround": turnaround,
            "response": response
        })

    return results

def show_gantt(timeline):
    print("\nGANTT CHART")
    print("=" * 50)

    segments = []
    current_time = 0

    for item in timeline:
        if item["start"] > current_time:
            segments.append({
                "name": "IDLE",
                "start": current_time,
                "end": item["start"]
            })

        segments.append(item)
        current_time = item["end"]

    for item in segments:
        print("+-------", end="")
    print("+")

    for item in segments:
        print(f"| {item['name']:^5} ", end="")
    print("|")

    for item in segments:
        print("+-------", end="")
    print("+")

    print(f"{segments[0]['start']:<7}", end="")

    for item in segments:
        print(f"{item['end']:<8}", end="")

    print("\n")

def show_results(processes, timeline, algorithm_name):
    results = calculate_metrics(processes, timeline)

    print("\n", algorithm_name)
    print("=" * 65)
    print(f"{'Process':<12}{'Waiting':<12}{'Turnaround':<15}{'Response':<12}")

    for result in results:
        print(
            f"{result['name']:<12}"
            f"{result['waiting']:<12}"
            f"{result['turnaround']:<15}"
            f"{result['response']:<12}"
        )

    avg_waiting = sum(r["waiting"] for r in results) / len(results)
    avg_turnaround = sum(r["turnaround"] for r in results) / len(results)
    avg_response = sum(r["response"] for r in results) / len(results)

    print("-" * 65)
    print(f"Average Waiting Time: {avg_waiting:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround:.2f}")
    print(f"Average Response Time: {avg_response:.2f}")

    show_gantt(timeline)


def main():
    processes = read_processes("input.txt")

    if not processes:
        print("No processes found!")
        return

    fcfs_result = fcfs(processes)
    priority_result = priority_scheduling(processes)

    show_results(processes, fcfs_result, "FCFS")
    show_results(processes, priority_result, "Priority")

    print("\nCOMPARISON")
    print("=" * 40)

    fcfs_avg = sum(r["waiting"] for r in calculate_metrics(processes, fcfs_result)) / len(processes)
    priority_avg = sum(r["waiting"] for r in calculate_metrics(processes, priority_result)) / len(processes)

    print(f"FCFS Average Waiting Time: {fcfs_avg:.2f}")
    print(f"Priority Average Waiting Time: {priority_avg:.2f}")

    if fcfs_avg < priority_avg:
        print("FCFS is better in average waiting time.")
    elif priority_avg < fcfs_avg:
        print("Priority is better in average waiting time.")
    else:
        print("Both algorithms have equal average waiting time.")


if __name__ == "__main__":
    main()