from trafilatura import fetch_url, extract


def load_url(url):
    """URL에서 채용 공고 Text 추출"""
    downloaded = fetch_url(url)
    result = extract(downloaded, output_format="markdown", with_metadata=True)
    print(result)
    return(result)
