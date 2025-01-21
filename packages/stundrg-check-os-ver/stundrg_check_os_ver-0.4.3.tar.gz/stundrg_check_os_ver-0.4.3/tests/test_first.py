from stundrg_check_os_ver.osver import get_os_ver

def test_first():
    v = get_os_ver()
    assert v is not None
    assert v == "Ubuntu 24.04.1 LTS"
    # 빈 문자열이 아닌지
    assert v != ""
    # 문자열에 LTS가 포함 되었는지
    assert "LTS" in v
    # 문자열에 문자도 있고, 숫자도 있는지
    assert any(t.isalpha() for t in v)
    assert any(t.isdigit() for t in v)
    # .이 포함되어 있는지
    assert  "." in v
    # 길이가 적어도 얼마 이상인지 ............
    assert len(v) > 5
    # 기타 등등
