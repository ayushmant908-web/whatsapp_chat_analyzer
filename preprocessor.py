import re
import pandas as pd

def preprocess_txt(data):

    # Clean hidden characters
    data = data.replace("\u202f", " ").replace("\u200e", "").replace("\xa0", " ")

    # WhatsApp date-time pattern
    pattern = r'\[?\d{1,2}/\d{1,2}/\d{2,4}[,\]]?\s*\d{1,2}:\d{2}(?:\s?(?:AM|PM|am|pm))?\]? - '

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    if len(messages) == 0:
        return pd.DataFrame()

    df = pd.DataFrame({"raw_message": messages, "raw_date": dates})

    df["raw_date"] = df["raw_date"].str.replace(" - ", "", regex=False)
    df["date"] = pd.to_datetime(df["raw_date"], errors="coerce", dayfirst=True)

    users = []
    msgs = []

    for msg in df["raw_message"]:
        msg = msg.strip()

        # Extract username
        entry = re.split(r"([^:–—\-]+)[\:–—\-]\s", msg, maxsplit=1)

        if len(entry) > 2:
            users.append(entry[1].strip())      # user extracted
            msgs.append(entry[2].strip())       # message extracted
        else:
            users.append("group_notification")
            msgs.append(msg)

    df["user"] = users
    df["message"] = msgs

    df.drop(columns=["raw_message", "raw_date"], inplace=True)

    # Additional columns
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month_name()
    df["day"] = df["date"].dt.day
    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute

    return df




