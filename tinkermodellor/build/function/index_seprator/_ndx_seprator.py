from typing import List

def parse_ndx(ndx: str) -> List[int]:
    result = []
    parts = ndx.split(',')
    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            result.extend(range(start, end+1))
        else:
            result.append(int(part))
    return result