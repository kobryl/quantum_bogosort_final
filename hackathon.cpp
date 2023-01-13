// hackathon.cpp : Ten plik zawiera funkcję „main”. W nim rozpoczyna się i kończy wykonywanie programu.
//

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include <unordered_map>
#include <set>
#include <utility>

typedef std::pair<int, unsigned long long> PII;
typedef std::vector<PII> VPII;
typedef std::vector<VPII> VVPII;

void removeHeaderAndCommas(std::string path) {
    std::string outputPath = "data/processed_" + path;
    std::vector<std::string> outputLines;
    std::ofstream output(outputPath);
    std::ifstream input(path);
    std::string inputLine;
    input >> inputLine;
    while (getline(input, inputLine)) {
        for (int i = 0; i < inputLine.size(); i++)
            if (inputLine[i] == ' ')
                inputLine[i] = '_';
        for (int i = 0; i < inputLine.size(); i++)
            if (inputLine[i] == ',')
                inputLine[i] = ' ';
        outputLines.push_back(inputLine);
    }
    for (int i = 0; i < outputLines.size(); i++)
        output << outputLines[i] << "\n";
}

void processFiles() {
    removeHeaderAndCommas("gtfsgoogle/calendar_dates.txt");
    removeHeaderAndCommas("gtfsgoogle/trips.txt");
    removeHeaderAndCommas("gtfsgoogle/stop_times.txt");
}

struct BusStop {
    int stop_id;
    std::string stop_name;
    int stop_code;
    std::vector<int> trips;
};

struct BusStopSchedule {
    int day;
    int arrival, departure;
    int trip_id;
    int next_bus_stop_id;
};

struct vertex {
    bool visited;
    int arrival;
    int departure;
    int route_id;
    int parent;
    int id;
};

struct InfoProcessing {
    int route_id, arrival, departure, destination, stop_id, duration;
};

bool customCompare(const InfoProcessing& a, const InfoProcessing& b) {
    if (a.stop_id < b.stop_id)
        return true;
    else if (a.stop_id > b.stop_id)
        return false;
    else return a.arrival < b.arrival;
}

std::vector<vertex> vertices;
std::vector<std::vector<std::pair<int, int>>> edges;
std::vector<int> vertex_count;
std::unordered_map<int, int> short_to_long_id;
std::unordered_map<int, std::string> int_to_trip;
struct Day {
    std::vector<int> services_id;
    std::vector<std::string> trips_id;
};

class ShortestDistanceCalculator {
    std::vector<Day> days;
    std::unordered_map<int, int> service_days;
    std::unordered_map<std::string, int> trip_services;
    std::unordered_map<std::string, int> trip_to_int;
    std::unordered_map<int, BusStopSchedule> bus_stops;
    std::unordered_map<int, int> bus_stops_ids;

    int bus_stops_count = 0;
    int trip_id_count = 0;
    int searched_time = 0;
    int destination_bus_stop;
    std::vector<std::string> tripIds;

public:
    void processRoutes();
    void loadData();
    void findPath(int source);
    void setDestination(int destination);
    void setTime(int time);
};

void ShortestDistanceCalculator::setTime(int time) {
    searched_time = time;
}

int stringClockToInt(std::string& clock) {
    int result = 0;
    result += (clock[0] - '0') * 36000;
    result += (clock[1] - '0') * 3600;
    result += (clock[3] - '0') * 600;
    result += (clock[4] - '0') * 60;
    result += (clock[6] - '0') * 10;
    result += (clock[7] - '0') * 1;
    return result;
}

void ShortestDistanceCalculator::setDestination(int destination) {
    destination_bus_stop = bus_stops_ids[destination];
}

void ShortestDistanceCalculator::processRoutes() {
    std::ifstream dates("data/processed_calendar_dates.txt");
    std::vector<std::pair<int, int>> services_during_day;
    std::vector<std::pair<std::string, int>> trips;
    int service_id, day, exception_type;
    while (dates >> service_id >> day >> exception_type)
        services_during_day.push_back({ day, service_id });
    std::sort(services_during_day.begin(), services_during_day.end());
    for (int i = 0; i < services_during_day.size(); i++) {
        day = services_during_day[i].first;
        service_id = services_during_day[i].second;
        if (days.empty() || day != services_during_day[i - 1].first) {
            days.push_back(Day());
        }
        days.back().services_id.push_back(service_id);
        service_days[service_id] = day;
    }

    dates.close();
    std::ifstream trips_file("data/processed_trips.txt");
    int tmp;
    std::string tmp2, trip_id;
    while (trips_file >> tmp >> service_id >> trip_id >> tmp2 >> tmp >> tmp2 >> tmp) {
        trip_services[trip_id] = service_id;
    }

    std::ofstream processed_data;
    std::ifstream processed_stop_times("data/processed_stop_times.txt");
    std::ofstream processed_short_to_longs("data/short_to_long.txt");
    std::string arrival, departure;
    int last_day = -1;
    int stop_id, stop_on_route_count;
    while (processed_stop_times >> trip_id >> arrival >> departure >> stop_id >> stop_on_route_count >> tmp >> tmp) {
        service_id = trip_services[trip_id];
        day = service_days[service_id];
        if (trip_to_int.count(trip_id) == 0)
            trip_to_int[trip_id] = trip_id_count++;
        if (bus_stops_ids.count(stop_id) == 0) {
            bus_stops_ids[stop_id] = bus_stops_count;
            short_to_long_id[bus_stops_count] = stop_id;
            bus_stops_count++;
        }
        if (last_day != day) {
            processed_data.close();
            processed_data.open(std::to_string(day) + "data/processed_data.txt", std::ios::app);
        }
        processed_data << trip_to_int[trip_id] << " " << day << " " << stringClockToInt(arrival) << " "
            << stringClockToInt(departure) << " " << stop_id << " " << stop_on_route_count << "\n";
        last_day = day;
    }
    processed_data.close();
    processed_stop_times.close();

    std::ofstream trips_ids("data/trips_ids.txt");
    for (std::pair<std::string, int> element : trip_to_int) {
        trips_ids << element.second << " " << element.first << "\n";
    }

    processed_stop_times.open("data/20230113processed_data.txt");
    for (std::pair<int, int> element : short_to_long_id) {
        processed_short_to_longs << element.first << " " << element.second << "\n";
    }
    std::vector<InfoProcessing> info;
    int route_id, route_count, arr, dep;
    int last_stop_id, last_departure, last_arrival;
    while (processed_stop_times >> route_id >> day >> arr >> dep >> stop_id >> route_count) {
        if (route_count > 0) {
            int last_short_stop_id = bus_stops_ids[last_stop_id];
            int short_stop_id = bus_stops_ids[stop_id];
            info.push_back({ route_id, last_arrival, last_departure, short_stop_id, last_short_stop_id, arr - last_departure });
        }
        last_stop_id = stop_id;
        last_departure = dep;
        last_arrival = arr;
    }
    std::sort(info.begin(), info.end(), customCompare);
    processed_stop_times.close();
    processed_data.open("data/processed_dataInfo.txt");
    for (int i = 0; i < info.size(); i++) {
        processed_data << info[i].route_id << " " << info[i].arrival << " " << info[i].departure << " " << info[i].destination << " " << info[i].stop_id << " " << info[i].duration << "\n";
    }
    processed_data.close();
}

void ShortestDistanceCalculator::loadData() {
    int trip_id;
    int day, arrival, departure, stop_id, destination, duration;
    std::ifstream processed_data("data/processed_dataInfo.txt");
    int last_stop_id, last_departure, last_arrival;
    int max_id = 0;
    while (processed_data >> trip_id >> arrival >> departure >> destination >> stop_id >> duration) {
        int short_stop_id = stop_id;
        while (vertices.size() < short_stop_id * 30)
            vertices.push_back({ false, 0, 0, -1, -1, 0 });
        max_id = std::max(max_id, stop_id);
        max_id = std::max(max_id, destination);
        if (vertices.size() >= 30 * (short_stop_id + 1))
            continue;
        vertices.push_back({ false, arrival, departure, trip_id, -1, stop_id });
    }
    while (vertices.size() < max_id * 30 + 30)
        vertices.push_back({ false, 0, 0, -1, -1, 0 });
    processed_data.close();
    processed_data.open("data/processed_dataInfo.txt");
    while (processed_data >> trip_id >> arrival >> departure >> destination >> stop_id >> duration) {
        while (vertex_count.size() <= stop_id)
            vertex_count.push_back(0);
        while (edges.size() < max_id * 30 + 30)
            edges.push_back(std::vector<std::pair<int, int>>());

        if (vertex_count[stop_id] == 30)
            continue;
        for (int i = destination * 30; i < destination * 30 + 30; i++) {
            while (vertices.size() <= destination * 30 + 30)
                vertices.push_back({ false, 0, 0, -1, -1, 0 });
            if (departure + duration <= vertices[i].arrival || destination == destination_bus_stop) {
                int new_duration = vertices[i].arrival - departure;
                if (destination == destination_bus_stop) {
                    vertices[i].route_id = trip_id;
                    vertices[i].id = stop_id;
                    new_duration = duration;
                }
                edges[stop_id * 30 + vertex_count[stop_id]].push_back({ i, duration });
                if (vertices[i].route_id == -1) {
                    vertices[i].route_id = trip_id;
                    vertices[i].id = stop_id;
                }
            }
        }
        vertex_count[stop_id]++;
    }
    processed_data.close();

    std::ifstream trip_keys("data/trips_ids.txt");
    int trip_int;
    std::string trip_string_key;
    while (trip_keys >> trip_int >> trip_string_key) {
        int_to_trip[trip_int] = trip_string_key;
    }
    trip_keys.close();
    std::ifstream short_to_longs("data/short_to_long.txt");
    int short_id, long_id;
    while (short_to_longs >> short_id >> long_id) {
        short_to_long_id[short_id] = long_id;
        bus_stops_ids[long_id] = short_id;

    }
}

void dijkstras(int source_node, int dest_node, int node_count, std::vector<std::vector<std::pair<int, int>>>& graph) {

    const long long INF = 999999999999;
    std::vector<unsigned long long> dist(node_count, INF);
    std::set<PII> set_length_node;

    dist[source_node] = 0;
    set_length_node.insert(PII(0, source_node));

    while (!set_length_node.empty()) {

        PII top = *set_length_node.begin();
        set_length_node.erase(set_length_node.begin());

        int current_source_node = top.second;

        for (auto& it : graph[current_source_node]) {

            int adj_node = it.first;
            int length_to_adjnode = it.second;


            if (dist[adj_node] > length_to_adjnode + dist[current_source_node]) {
                if (dist[adj_node] != INF) {
                    set_length_node.erase(set_length_node.find(PII(dist[adj_node], adj_node)));
                }
                dist[adj_node] = length_to_adjnode + dist[current_source_node];
                vertices[adj_node].parent = current_source_node;
                set_length_node.insert(PII(dist[adj_node], adj_node));
            }
        }
    }
    long long best = INF;
    for (int i = dest_node * 30; i < dest_node * 30 + 30; i++) {
        if (dist[i] < best)
            best = dist[i];
    }
    std::vector<std::pair<int, int>> output;
    if (best == 0) {
        std::ofstream out("output");
        out << "";
        return;
    }
    for (int i = dest_node * 30; i < dest_node * 30 + 30; i++) {
        if (dist[i] == best) {
            i = vertices[i].parent;
            output.push_back({ dest_node, vertices[i].route_id });
            while (vertices[i].parent != -1) {
                output.push_back({ vertices[i].id, vertices[i].route_id });
                i = vertices[i].parent;
            }
            output.push_back({ vertices[i].id, vertices[i].route_id });
            break;
        }
    }
    reverse(output.begin(), output.end());
    std::ofstream found_path("result.txt");
    std::vector<bool> skip;
    for (int i = 0; i < output.size(); i++)
        skip.push_back(false);
    for (int i = 1; i < output.size() - 1; i++) {
        if (output[i - 1].second == output[i + 1].second)
            skip[i] = true;
    }

    for (int i = 0; i < output.size(); i++) {
        if ((skip[i] && i > 0 && !skip[i - 1]) || (i > 0 && !skip[i] && !skip[i - 1])) {
            found_path << int_to_trip[output[i].second] << " ";
        }
        if (!skip[i])
            found_path << short_to_long_id[output[i].first] << " ";
    }

}

void ShortestDistanceCalculator::findPath(int source) {
    vertices[source].arrival = searched_time;
    vertices[source].departure = searched_time;
    dijkstras(bus_stops_ids[source], destination_bus_stop, vertices.size(), edges);
}

void generateProcessedFiles() {
    processFiles();
    ShortestDistanceCalculator my_calculator;
    my_calculator.processRoutes();
}

int main() {
    //generateProcessedFiles();
    ShortestDistanceCalculator my_calculator;
    std::string time;
    int target, source;
    std::ifstream input("input.txt");
    input >> target >> source >> time;
    my_calculator.loadData();
    my_calculator.setDestination(target);
    my_calculator.setTime(stringClockToInt(time));
    my_calculator.findPath(source);
}