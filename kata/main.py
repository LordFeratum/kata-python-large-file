import codecs

from urllib.request import urlopen

from settings import settings


def download_csv(url, encoding='utf-8'):
    def _iter(response):
        line = response.readline()
        while line:
            yield line
            line = response.readline()

    response = urlopen(url)
    return codecs.iterdecode(_iter(response), encoding)


def process_csv(iterdata):
    total_rows = 0
    for row, datum in enumerate(iterdata):
        total_rows = row

    return {
        'total_rows': total_rows,
        'average_tip_amount': 0
    }


def main():
    url = settings['amazon']['url']
    csv = download_csv(url)
    result = process_csv(csv)
    print(result)


if __name__ == '__main__':
    main()
