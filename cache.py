import random

class CacheBlock:
    def __init__(self):
        self.reset()

    def reset(self):
        self.valid = False
        self.tag = -1
        self.data = None
        self.timestamp = 0

    def update_block(self, tag, data, access_time):
        self.valid = True
        self.tag = tag
        self.data = data
        self.timestamp = access_time


class Cache:
    def __init__(self, num_blocks=32, line_size=16, assoc=2):
        self.num_blocks = num_blocks
        self.line_size = line_size
        self.assoc = assoc
        self.num_sets = num_blocks // assoc
        self.cache = self.initialize_cache()
        self.access_count = 0
        self.hit_count = 0
        self.miss_count = 0

    def initialize_cache(self):
        cache_structure = []
        for i in range(self.num_sets):
            set_blocks = [CacheBlock() for _ in range(self.assoc)]
            cache_structure.append(set_blocks)
        return cache_structure

    def reset_cache(self):
        self.cache = self.initialize_cache()
        self.access_count = 0
        self.hit_count = 0
        self.miss_count = 0

    def access_block(self, block_address):
        self.access_count += 1
        set_index, tag = self.calculate_index_tag(block_address)

        if self.check_hit(set_index, tag):
            return True

        self.handle_miss(set_index, tag, block_address)
        return False

    def calculate_index_tag(self, block_address):
        set_index = block_address % self.num_sets
        tag = block_address // self.num_sets
        return set_index, tag

    def check_hit(self, set_index, tag):
        for block in self.cache[set_index]:
            if block.valid and block.tag == tag:
                self.hit_count += 1
                block.timestamp = self.access_count
                self.debug_hit(set_index, tag)
                return True
        return False

    def handle_miss(self, set_index, tag, block_address):
        self.miss_count += 1
        lru_block = self.find_lru_block(set_index)
        self.replace_block(lru_block, tag, block_address)

    def find_lru_block(self, set_index):
        lru_block = self.cache[set_index][0]
        for block in self.cache[set_index]:
            if not block.valid:
                return block
            if block.timestamp < lru_block.timestamp:
                lru_block = block
        return lru_block

    def replace_block(self, lru_block, tag, block_address):
        new_data = f"Data for block {block_address}"
        lru_block.update_block(tag, new_data, self.access_count)
        self.debug_miss(tag, block_address, lru_block)

    def get_stats(self):
        hit_rate = self.hit_count / self.access_count if self.access_count != 0 else 0
        miss_rate = 1 - hit_rate
        avg_access_time = ((self.hit_count * 1) + (self.miss_count * 10)) / self.access_count
        return {
            "access_count": self.access_count,
            "hit_count": self.hit_count,
            "miss_count": self.miss_count,
            "hit_rate": hit_rate,
            "miss_rate": miss_rate,
            "avg_access_time": avg_access_time,
            "total_access_time": self.access_count * avg_access_time,
        }

    def debug_hit(self, set_index, tag):
        pass

    def debug_miss(self, tag, block_address, replaced_block):
        pass
