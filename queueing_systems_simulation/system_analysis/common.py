import typing as tp

import numpy as np

def count_state_probabilities(customers_arrival_and_departure: np.array, states_count: int,
                              simulation_start_time: float, simulation_finish_time: float) -> np.array:
    customers_events: tp.List[tp.Tuple[float, int]] = []
    for customer_no in range(len(customers_arrival_and_departure)):
        customer_arrival, customer_departure = customers_arrival_and_departure[customer_no]

        customers_events.append((customer_arrival, 1))
        customers_events.append((customer_departure, 0))

    state_total_durations: np.array = np.zeros(states_count)

    current_state = 0
    last_event_time = simulation_start_time
    for event_time, event_type in sorted(customers_events):
        state_total_durations[current_state] += event_time - last_event_time
        if event_type == 1:
            current_state += 1
        elif event_type == 0:
            current_state -= 1
        last_event_time = event_time

    return state_total_durations / (simulation_finish_time - simulation_start_time)

def compute_theoretical_probabilities(arrival_rates: np.array, departure_rates: np.array) -> np.array:
    arrival_rates_over_departure_rates = arrival_rates / departure_rates
    arrival_rates_over_departure_rates_cumprod = np.cumprod(arrival_rates_over_departure_rates)

    state_probabilities = np.zeros(arrival_rates.size + 1)
    probability_state_0 = 1 / (np.sum(arrival_rates_over_departure_rates_cumprod) + 1)
    state_probabilities[0] = probability_state_0
    state_probabilities[1:] = probability_state_0 * arrival_rates_over_departure_rates_cumprod
    return state_probabilities
