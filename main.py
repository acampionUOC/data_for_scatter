from bs4 import BeautifulSoup
import pandas as pd


def create_dataset_from_html(html_file):
    # soup from html
    with open(html_file) as fp:
        soup = BeautifulSoup(fp, "html.parser")

    # create output struct
    data = dict()
    # get fields as span in defined class
    for f in ['acceleration', 'topspeed', 'erange_real', 'efficiency', 'fastcharge_speed hidden', 'model', 'battery']:
        data[f] = [x.text.split(' ')[0] for x in soup.find_all("span", class_=f)]

    # get fields as title-wrap
    tw = soup.find_all("div", class_="title-wrap")
    data['car_link'] = [x.h2.a['href'] for x in tw]
    data['car_oem'] = [x.h2.a.span.text for x in tw]
    data['market_segment'] = [x.text for x in soup.find_all("span", title='Market Segment')]

    # to DataFrame
    df = pd.DataFrame(data)

    # transformation to numeric
    for c in ['acceleration', 'topspeed', 'erange_real', 'efficiency',
              'fastcharge_speed hidden', 'battery']:
        df[c] = pd.to_numeric(df[c])

    # drop nan
    df = df.dropna()
    return df


html_file = r"dataset\Compare electric vehicles - EV Database.html"
out_dataset = r'dataset\EV_database.csv'

# create dataset
df = create_dataset_from_html(html_file)

# save to file
df.to_csv(out_dataset, index=False)
