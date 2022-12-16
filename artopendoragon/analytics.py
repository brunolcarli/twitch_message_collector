import pandas as pd


def get_messages_dataframe(queryset):
    columns = [
        'id',
        'message_datetime',
        'message',
        'username',
        'message_sentiment',
        'message_offense_level'
    ]
    return pd.DataFrame(queryset.values_list(), columns=columns)


def get_messages_count_rank(queryset, limit=10, reverse=False):
    df = get_messages_dataframe(queryset)
    df = df.groupby('username').count().message.sort_values(ascending=reverse).head(limit)
    return list(df.items())


def get_messages_average_polarities(queryset):
    df = get_messages_dataframe(queryset)
    df['positive'] = (df.message_sentiment > 0).astype(int)
    df['negative'] = (df.message_sentiment < 0).astype(int)
    df['neutral'] = (df.message_sentiment == 0).astype(int)
    return dict((df[['positive', 'negative', 'neutral']].mean() * 100).round(2))
