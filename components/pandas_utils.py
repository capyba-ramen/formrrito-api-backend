import io

import pandas as pd


def convert_df_to_excel(df: pd.DataFrame):
    with io.BytesIO() as output:
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        data = output.getvalue()
    return data
