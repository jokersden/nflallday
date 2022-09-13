from datetime import datetime

def get_weekends(df_preseason):
    return df_preseason[
        df_preseason.date.isin(
            [
                datetime(2022, 8, 4),
                datetime(2022, 8, 5),
                datetime(2022, 8, 6),
                datetime(2022, 8, 7),
                datetime(2022, 8, 11),
                datetime(2022, 8, 12),
                datetime(2022, 8, 13),
                datetime(2022, 8, 14),
                datetime(2022, 8, 18),
                datetime(2022, 8, 19),
                datetime(2022, 8, 20),
                datetime(2022, 8, 21),
                datetime(2022, 8, 22),
                datetime(2022, 8, 25),
                datetime(2022, 8, 26),
                datetime(2022, 8, 27),
                datetime(2022, 8, 28),
            ]
        )
    ]

def get_non_weekends(df_preseason):
    return df_preseason[
        ~df_preseason.date.isin(
            [
                datetime(2022, 8, 4),
                datetime(2022, 8, 5),
                datetime(2022, 8, 6),
                datetime(2022, 8, 7),
                datetime(2022, 8, 11),
                datetime(2022, 8, 12),
                datetime(2022, 8, 13),
                datetime(2022, 8, 14),
                datetime(2022, 8, 18),
                datetime(2022, 8, 19),
                datetime(2022, 8, 20),
                datetime(2022, 8, 21),
                datetime(2022, 8, 22),
                datetime(2022, 8, 25),
                datetime(2022, 8, 26),
                datetime(2022, 8, 27),
                datetime(2022, 8, 28),
            ]
        )
    ]