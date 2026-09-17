from streamlit_app.services.dataset import load_dataset, profile_dataset


def test_csv_profile_reports_shape_duplicates_and_missing_values():
    frame = load_dataset("telemetry.csv", b"temperature,humidity\n5,90\n5,\n5,90\n")
    profile = profile_dataset(frame)

    assert profile["rows"] == 3
    assert profile["columns"] == 2
    assert profile["duplicates"] == 1
    assert profile["missing"] == {"humidity": 1}