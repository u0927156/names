import pandas as pd
import jellyfish


def convert_number_to_rate(df):

    return df.div(df.sum(axis=0), axis=1)


def add_sound_columns(df: pd.DataFrame) -> pd.DataFrame:
    df["metaphone"] = [jellyfish.metaphone(name) for name in df.index]
    df["soundex"] = [jellyfish.soundex(name) for name in df.index]
    df["nysiis"] = [jellyfish.nysiis(name) for name in df.index]
    df["match_rating_codex"] = [jellyfish.match_rating_codex(name) for name in df.index]
    return df
