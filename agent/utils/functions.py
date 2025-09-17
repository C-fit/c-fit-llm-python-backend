from trafilatura import fetch_url, extract


def merge_dict(existing: dict, new: dict) -> dict:
    """states.py의 기존값 유지를 위한 리듀서"""
    if existing is None:
        return new
    return {**existing, **new}


def get_job_description(url):
    """URL에서 채용 공고 Text 추출"""
    downloaded = fetch_url(url)
    result = extract(downloaded, output_format="markdown", with_metadata=True)
    return(result)