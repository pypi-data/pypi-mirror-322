# -*- coding: utf-8 -*-

import pytest
from hiedwinlan import say_hello

def test_say_hello():
    """测试 say_hello 函数是否返回正确的字符串"""
    # 准备预期结果
    expected = "Hello World"
    
    # 调用测试函数
    result = say_hello()
    
    # 验证结果
    assert result == expected
    assert isinstance(result, str)

def test_say_hello_type():
    """测试 say_hello 函数返回值类型"""
    result = say_hello()
    assert isinstance(result, str)

def test_say_hello_not_empty():
    """测试 say_hello 函数返回值不为空"""
    result = say_hello()
    assert result.strip() != "" 