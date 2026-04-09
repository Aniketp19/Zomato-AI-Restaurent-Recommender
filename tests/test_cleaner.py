import pandas as pd

from src.data.cleaner import DataCleaner


def test_data_cleaner_normalizes_core_fields() -> None:
    raw = pd.DataFrame(
        [
            {
                "id": 1,
                "name": " Pasta House ",
                "city": "new delhi",
                "cuisines": "Italian, Continental",
                "average_cost_for_two": "1,200",
                "rating": "4.3",
            }
        ]
    )
    cleaned = DataCleaner().clean(raw)

    assert len(cleaned) == 1
    assert cleaned.iloc[0]["name"] == "Pasta House"
    assert cleaned.iloc[0]["city"] == "New Delhi"
    assert cleaned.iloc[0]["budget_bucket"] == "medium"
