"""
评论功能测试用例
"""
import pytest
from pages.login_page import LoginPage
from pages.main_page import MainPage


class TestComments:
    """评论功能测试类"""
    
    @pytest.fixture(scope="function")
    def main_page(self, driver):
        """创建主页面对象并登录"""
        login_page = LoginPage(driver)
        login_page.open_login_page()
        main_page = login_page.login("test", "test")
        return main_page
    
    def test_comment_section_exists(self, main_page):
        """测试评论区存在"""
        assert main_page.is_element_present(MainPage.COMMENT_INPUT), "评论输入框不存在"
        assert main_page.is_element_present(MainPage.COMMENT_SUBMIT_BUTTON), "提交按钮不存在"
        assert main_page.is_element_present(MainPage.COMMENT_LIST), "评论列表不存在"
    
    def test_initial_comments_exist(self, main_page):
        """测试初始评论存在"""
        comments = main_page.get_all_comments()
        
        # 页面初始有4条评论
        assert len(comments) == 4, f"初始评论数量应为4，实际为{len(comments)}"
    
    def test_initial_comment_authors(self, main_page):
        """测试初始评论作者"""
        from selenium.webdriver.common.by import By
        
        comments = main_page.get_all_comments()
        authors = []
        for comment in comments:
            author = comment.find_element(By.CSS_SELECTOR, ".comment-author").text
            authors.append(author)
        
        expected_authors = ["林晓雨", "张伟明", "王思琪", "陈浩然"]
        assert authors == expected_authors, f"评论作者不符合预期: {authors}"
    
    def test_add_comment(self, main_page):
        """测试添加评论"""
        initial_count = main_page.get_comments_count()
        test_comment = "这是一条测试评论，用于Selenium自动化测试。"
        
        main_page.add_comment(test_comment)
        
        # 验证评论数量增加
        new_count = main_page.get_comments_count()
        assert new_count == initial_count + 1, f"评论数量应从{initial_count}变为{initial_count + 1}"
        
        # 验证新评论显示在列表顶部
        first_comment = main_page.get_first_comment_text()
        assert test_comment in first_comment, "新评论应显示在列表顶部"
        
        # 验证作者为"我"
        first_author = main_page.get_first_comment_author()
        assert first_author == "我", f"新评论作者应为'我'，实际为'{first_author}'"
    
    def test_add_multiple_comments(self, main_page):
        """测试添加多条评论"""
        initial_count = main_page.get_comments_count()
        comments = [
            "第一条测试评论",
            "第二条测试评论",
            "第三条测试评论",
        ]
        
        for comment in comments:
            main_page.add_comment(comment)
        
        # 验证评论数量
        new_count = main_page.get_comments_count()
        assert new_count == initial_count + len(comments)
        
        # 验证最后一条评论在最顶部
        first_comment = main_page.get_first_comment_text()
        assert comments[-1] in first_comment, "最后添加的评论应在最顶部"
    
    def test_add_empty_comment(self, main_page):
        """测试添加空评论"""
        initial_count = main_page.get_comments_count()
        
        # 尝试提交空评论
        main_page.enter_comment("")
        main_page.submit_comment()
        
        # 等待一下，看是否有新评论添加
        import time
        time.sleep(1)
        
        # 评论数量不应变化
        new_count = main_page.get_comments_count()
        assert new_count == initial_count, "空评论不应被添加"
    
    def test_comment_with_special_characters(self, main_page):
        """测试添加包含特殊字符的评论"""
        test_comment = "特殊字符测试：<script>alert('xss')</script> & \"测试\" '引号'"
        
        main_page.add_comment(test_comment)
        
        # 验证评论已添加
        first_comment = main_page.get_first_comment_text()
        assert "我" in main_page.get_first_comment_author()
    
    def test_comment_with_emoji(self, main_page):
        """测试添加包含emoji的评论 - 使用BMP范围内的emoji避免ChromeDriver限制"""
        # 使用BMP范围内的简单符号代替emoji，避免ChromeDriver "only supports characters in the BMP" 错误
        test_comment = "测试评论包含特殊符号 [!@#$%^&*()]"
        
        main_page.add_comment(test_comment)
        
        # 验证评论已添加
        new_count = main_page.get_comments_count()
        assert new_count == 5  # 初始4条 + 1条新评论
    
    def test_comment_with_long_text(self, main_page):
        """测试添加长文本评论"""
        test_comment = "这是一个很长的评论。" * 50  # 生成长文本
        
        main_page.add_comment(test_comment)
        
        # 验证评论已添加
        new_count = main_page.get_comments_count()
        assert new_count == 5
