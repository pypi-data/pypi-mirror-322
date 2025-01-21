import pandas as pd
import pytest
from jerreda.cli import group_by_count

def test_group_count_by_free():
    input_data = group_by_count('자유')
    
    # 결과값이 존재하는지 검증
    assert input_data is not None

    # '자유' 키워드를 입력했을 때의 예상 결과
    data = {
         "president": ["박정희", "이승만", "노태우", "김대중", "문재인", 
                       "김영삼", "이명박", "전두환", "노무현", "박근혜", 
                       "최규하", "윤보선"],
         "count": [513, 438, 399, 305, 275, 
                   274, 262, 242, 230, 111, 
                   14, 1]
    }
    df = pd.DataFrame(data)
    expected_data = df.to_string(index=False)
    
    # 예상 결과와 일치하는지 검증
    assert input_data == expected_data, "\n'자유' 키워드는 예상 데이터와 일치하지 않습니다."

def test_group_count_by_demo():
    input_data = group_by_count('민주주의')

    # 결과값이 존재하는지 검증
    assert input_data is not None

    # '민주주의' 키워드를 입력했을 때의 예상 결과
    data = {
         "president": ["노태우", "김대중", "문재인", "노무현", "김영삼",
                       "이명박", "박정희", "전두환", "이승만", "박근혜",
                       "최규하", "윤보선"],
         "count": [402, 329, 237, 230, 203,
                   174, 163, 137, 116, 52,
                   7, 1]
    }
    df = pd.DataFrame(data)
    expected_data = df.to_string(index=False)

    # 예상 결과와 일치하는지 검증
    assert input_data == expected_data, "\n'민주주의' 키워드는 예상 데이터와 일치하지 않습니다."

def test_group_count_by_jerry():
    input_data = group_by_count('권오준')

    # 결과값이 존재하는지 검증
    # '권오준' 키워드가 들어간 데이터가 존재하지 않아야 함
    assert input_data is  None
