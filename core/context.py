import re
from typing import Any, List, Dict


class ContextGetter:
    @staticmethod
    def get_context(matches: List[Any], content: str,
                    name: str, rex='.+?') -> List[Dict[str, Any]]:
        ''' get context of matched items
        Args:
            matches: list of tuples (matched_string, start_index,
            end_index, line_number)
            content: the content to search in
            name: name of the regex pattern
            rex: regex pattern to find context, default is '.+?'
        Returns:
            list: A list of dictionaries containing matched items with context.
        '''
        items = []
        matches2: List[Any] = []
        # 保留行号信息
        for x in matches:
            if x[0] not in [m[0] for m in matches2]:
                matches2.append(x)
        for m in matches2:
            # 使用 re.escape 防止正则元字符导致语法错误
            context = re.findall('%s%s%s' % (rex, re.escape(m[0]), rex),
                                 content, re.IGNORECASE)
            item = {
                'matched': m[0],
                'name': name,
                'context': context,
                'multi_context': True if len(context) > 1 else False,
                'line': m[3]  # 新增行号
            }
            items.append(item)
        return items
