from typing import List
from app.schemas.tag import TagRead


class TagSize:
    @staticmethod
    async def calculate_tag_size(tags: List[TagRead]):
        # 计算每个标签的 posts 数量
        counts = [len(tag.posts) for tag in tags]

        # 找到最大值和最小值
        max_size = max(counts) if counts else 0
        min_size = min(counts) if counts else 0

        # 避免除以零错误
        if max_size == min_size:
            return [1.0] * len(counts)  # 如果所有标签的 posts 数量相同，返回统一值

        # 归一化处理
        normalized_counts = [
            (count - min_size) / (max_size - min_size) + 1 for count in counts
        ]

        return normalized_counts
