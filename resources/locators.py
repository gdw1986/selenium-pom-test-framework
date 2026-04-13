# -*- coding: utf-8 -*-
"""Locator 统一加载库 - 供 Robot Framework 调用"""
import json
import os
from robot.api import logger

LOCATORS_DIR = os.path.join(os.path.dirname(__file__), "..", "locators")
_cache = {}


def _load_locators():
    """懒加载所有 locator JSON 文件"""
    if _cache:
        return _cache

    locators_dir = os.path.abspath(LOCATORS_DIR)
    for filename in os.listdir(locators_dir):
        if filename.endswith(".json"):
            page_name = filename[:-5]  # 去掉 .json
            filepath = os.path.join(locators_dir, filename)
            with open(filepath, encoding="utf-8") as f:
                _cache[page_name] = json.load(f)

    logger.info(f"Loaded locators: {list(_cache.keys())}")
    return _cache


def get_locator(page: str, key: str) -> str:
    """获取指定 page 和 key 的 locator 值

    Usage in RF:
        ${selector}=    Get Locator    main    alert_button
        Click           ${selector}
    """
    locators = _load_locators()
    if page not in locators:
        raise ValueError(f"Unknown locator page: {page}. Available: {list(locators.keys())}")
    if key not in locators[page]:
        raise ValueError(f"Unknown locator key '{key}' in page '{page}'. "
                         f"Available: {list(locators[page].keys())}")
    return locators[page][key]


def get_locator_dict(page: str) -> dict:
    """获取指定页面的所有 locator

    Usage in RF:
        &{locs}=    Get Locator Dict    main
        Click       ${locs.alert_button}
    """
    locators = _load_locators()
    if page not in locators:
        raise ValueError(f"Unknown locator page: {page}. Available: {list(locators.keys())}")
    return locators[page]


# Robot Framework 关键字
class LocatorKeywords:
    """暴露给 Robot Framework 的关键字"""

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def get_locator(self, page: str, key: str) -> str:
        """获取单个 locator 值"""
        return get_locator(page, key)

    def get_locator_dict(self, page: str) -> dict:
        """获取页面所有 locator 作为字典"""
        return get_locator_dict(page)

    def reload_locators(self):
        """强制重新加载 locator 缓存"""
        global _cache
        _cache.clear()
        _load_locators()
