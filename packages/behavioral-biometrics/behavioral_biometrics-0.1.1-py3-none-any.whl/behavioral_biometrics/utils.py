import numpy as np
from typing import List


def create_dummy_data(data: np.ndarray) -> List[np.ndarray]:
    dummy_data = []
    typing_frequency_email_avg = np.mean(data[:, 0])
    typing_frequency_password_avg = np.mean(data[:, 1])
    keypress_duration_email_avg = np.mean(data[:, 2])
    keypress_duration_password_avg = np.mean(data[:, 3])
    field_interaction_time_mail_avg = np.mean(data[:, 4])
    field_interaction_time_password_avg = np.mean(data[:, 5])
    login_submission_time_avg = np.mean(data[:, 6])
    mouse_movement_pattern_max = np.max(data[:, 7])
    mouse_or_tab_max = np.max(data[:, 8])

    for _ in range(20):
        dummy_entry = [
            typing_frequency_email_avg + np.random.randint(-10, 11),  # typing_frequency_email
            typing_frequency_password_avg + np.random.randint(-10, 11),  # typing_frequency_password
            keypress_duration_email_avg + np.random.randint(-15, 16),  # keypress_duration_email
            keypress_duration_password_avg + np.random.randint(-15, 16),  # keypress_duration_password
            field_interaction_time_mail_avg + np.random.uniform(-2, 2),  # field_interaction_time_mail
            field_interaction_time_password_avg + np.random.uniform(-2, 2),  # field_interaction_time_password
            login_submission_time_avg + np.random.uniform(-2, 2),  # login_submission_time
            mouse_movement_pattern_max,  # mouse_movement_pattern
            mouse_or_tab_max  # mouse_or_tab
        ]
        dummy_data.append(dummy_entry)

    return dummy_data
