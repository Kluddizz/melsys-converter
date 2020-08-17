import pandas as pd

def get_melsys_entry(df, alarm_number):
    entry = df.loc[df['ALARM_PV_NAME'] == alarm_number]

    if entry.empty:
        return None
    else:
        return entry.iloc[0]

if __name__ == "__main__":
    # Read old melsys file, which contains information about if the alarm is enabled
    melsys_data = pd.read_csv(r'melsysback.csv', sep=';', encoding="ISO-8859-1", error_bad_lines=False)

    # Read new aip file, where the information above should be applied
    aip_data = pd.read_excel('aip.xlsx', sheet_name='Meldungen', encoding='utf-8')

    for i, row in aip_data.iterrows():
        alarm_number = row[0]
        entry = get_melsys_entry(melsys_data, alarm_number)

        if entry is not None:
            alarm_enabled = entry[5]
            daily_alarm = entry[8] == "Tagesalarme"

            if daily_alarm and alarm_enabled:
                row[27] = "AIP_TAG"
            elif alarm_enabled:
                row[27] = "AIP"

    aip_data.to_csv('mapped.csv', index=False, sep=';')
