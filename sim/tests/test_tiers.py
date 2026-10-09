"""Unit tests for the tier cache: eviction order, cascading, promotion and reuse-aware admission."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from simulate import Tiers  # noqa: E402


def test_lru_cascades_down_and_drops_at_the_bottom():
    t = Tiers({"hbm": 2, "dram": 1, "ssd": 0, "hdd": 0}, ["hbm", "dram"], False)
    for h in (1, 2, 3):
        t.touch(h)
    assert t.lookup(1) == "dram" and t.lookup(2) == "hbm" and t.lookup(3) == "hbm"
    t.touch(4)                       # 2 falls to dram, pushing 1 out entirely
    assert t.lookup(1) is None and t.lookup(2) == "dram" and t.dropped == 1


def test_hit_is_promoted_back_to_gpu_memory():
    t = Tiers({"hbm": 1, "dram": 2, "ssd": 0, "hdd": 0}, ["hbm", "dram"], False)
    t.touch(1); t.touch(2)
    assert t.lookup(1) == "dram"
    t.touch(1)
    assert t.lookup(1) == "hbm" and t.lookup(2) == "dram"


def test_each_block_lives_in_one_tier_only():
    t = Tiers({"hbm": 2, "dram": 2, "ssd": 2, "hdd": 2}, ["hbm", "dram", "ssd", "hdd"], False)
    for h in [1, 2, 3, 4, 5, 1, 6, 2, 7, 8]:
        t.touch(h)
    held = [h for tier in t.lru.values() for h in tier]
    assert len(held) == len(set(held)) == len(t.where)


def test_reuse_aware_admission_keeps_one_off_blocks_off_disk():
    t = Tiers({"hbm": 1, "dram": 1, "ssd": 5, "hdd": 0}, ["hbm", "dram", "ssd"], True)
    t.touch(1); t.touch(2); t.touch(3)   # 1 was used once, so it is dropped instead of written to SSD
    assert t.lookup(1) is None and t.writes["ssd"] == 0
    t.touch(2); t.touch(4); t.touch(5)   # 2 was reused, so it may go to SSD
    assert t.lookup(2) == "ssd" and t.writes["ssd"] == 1
