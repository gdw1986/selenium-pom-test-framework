"""
评论功能测试用例
"""
import pytest
import time
from pages.login_page import LoginPage
from pages.main_page import MainPage
from config.settings import LOGIN_USERNAME, LOGIN_PASSWORD


class TestComment:
    """评论功能测试类"""
    
    @pytest.fixture(scope="function")
    def main_page(self, driver):
        """创建主页面对象（已登录状态）"""
        login_page = LoginPage(driver)
        login_page.open_login_page()
        main_page = login_page.login(LOGIN_USERNAME, LOGIN_PASSWORD)
        return main_page
    
    def test_new_comment_appears_at_top(self, main_page):
        """测试新添加的评论显示在最上方"""
        # 记录添加评论前的第一条评论内容
        original_first_comment = main_page.get_first_comment_text()
        
        # 添加一条新评论
        new_comment_text = f"这是一条测试评论，创建于 {time.strftime('%H:%M:%S')}"
        main_page.add_comment(new_comment_text)
        
        # 验证新评论显示在最上方
        updated_first_comment = main_page.get_first_comment_text()
        assert updated_first_comment == new_comment_text, \
            f"新评论应该显示在最上方。期望: '{new_comment_text}', 实际: '{updated_first_comment}'"
        
        # 验证原来的第一条评论变成了第二条
        all_comments = main_page.get_all_comment_texts()
        assert len(all_comments) >= 2, "评论列表应该至少有2条评论"
        assert all_comments[1] == original_first_comment, \
            f"原来的第一条评论应该变成第二条。期望: '{original_first_comment}', 实际: '{all_comments[1]}'"
    
    def test_add_multiple_comments_order(self, main_page):
        """测试添加多条评论的顺序"""
        # 添加3条评论
        comments_to_add = [
            "第一条测试评论",
            "第二条测试评论", 
            "第三条测试评论"
        ]
        
        for comment in comments_to_add:
            main_page.add_comment(comment)
        
        # 获取所有评论
        all_comments = main_page.get_all_comment_texts()
        
        # 验证最新的3条评论是按倒序排列的（最新的在最上面）
        # 取前3条进行验证
        recent_comments = all_comments[:3]
        expected_order = list(reversed(comments_to_add))
        
        assert recent_comments == expected_order, \
            f"评论顺序不正确。期望: {expected_order}, 实际: {recent_comments}"
    
    def test_comment_submission_success_toast(self, main_page):
        """测试评论提交成功后显示toast提示"""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.common.by import By
        
        main_page.enter_comment("测试toast提示")
        main_page.submit_comment()
        
        # 等待toast显示（toast在提交后很快显示）
        try:
            WebDriverWait(main_page.driver, 2).until(
                lambda d: "show" in d.find_element(By.ID, "comment-toast").get_attribute("class")
            )
            toast_visible = True
        except:
            toast_visible = False
        
        assert toast_visible, "评论提交后应该显示成功toast提示"
    
    def test_comment_author_is_current_user(self, main_page):
        """测试新评论的作者显示为当前用户"""
        main_page.add_comment("测试作者显示")
        
        # 验证新评论的作者是"我"
        first_author = main_page.get_first_comment_author()
        assert first_author == "我", f"新评论的作者应该显示为'我'，实际显示为: '{first_author}'"
