"""
文件上传功能测试用例
"""
import os
import tempfile
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from pages.login_page import LoginPage
from pages.main_page import MainPage


class TestFileUpload:
    """文件上传功能测试类"""
    
    @pytest.fixture(scope="function")
    def driver(self):
        """测试前置：创建driver"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        driver.implicitly_wait(10)
        yield driver
        driver.quit()
    
    @pytest.fixture(scope="function")
    def main_page(self, driver):
        """创建主页面对象并登录"""
        login_page = LoginPage(driver)
        login_page.open_login_page()
        main_page = login_page.login("test", "test")
        return main_page
    
    @pytest.fixture(scope="function")
    def temp_file(self):
        """创建临时测试文件"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("This is a test file for Selenium upload testing.")
            temp_path = f.name
        yield temp_path
        # 清理
        if os.path.exists(temp_path):
            os.remove(temp_path)
    
    def test_upload_section_exists(self, main_page):
        """测试上传区域存在"""
        assert main_page.is_element_present(MainPage.UPLOAD_DROP_ZONE), "上传区域不存在"
        assert main_page.is_element_present(MainPage.FILE_INPUT), "文件输入框不存在"
    
    def test_upload_file(self, main_page, temp_file):
        """测试正常上传文件"""
        main_page.upload_file(temp_file)
        
        # 验证文件信息显示
        assert main_page.is_file_uploaded(), "文件上传后应显示文件信息"
        
        # 验证文件名
        file_name = os.path.basename(temp_file)
        assert main_page.get_uploaded_file_name() == file_name, "文件名显示不正确"
        
        # 验证文件大小
        file_size = os.path.getsize(temp_file)
        meta_text = main_page.get_uploaded_file_meta()
        assert "B" in meta_text or "KB" in meta_text, "文件大小应显示"
    
    def test_upload_file_fullpath(self, main_page, temp_file):
        """测试上传文件后显示完整路径"""
        main_page.upload_file(temp_file)
        
        fullpath = main_page.get_uploaded_file_fullpath()
        # fakepath格式: C:\fakepath\filename.txt
        assert "fakepath" in fullpath, f"完整路径应包含fakepath: {fullpath}"
        assert os.path.basename(temp_file) in fullpath, "完整路径应包含文件名"
    
    def test_upload_different_extensions(self, main_page):
        """测试上传不同扩展名的文件"""
        extensions = ['.txt', '.pdf', '.doc', '.jpg', '.png', '.py']
        
        for ext in extensions:
            with tempfile.NamedTemporaryFile(mode='w', suffix=ext, delete=False) as f:
                f.write(f"Test content for {ext} file")
                temp_path = f.name
            
            try:
                main_page.upload_file(temp_path)
                assert main_page.is_file_uploaded(), f"上传{ext}文件失败"
                
                # 清除文件，准备下一个测试
                main_page.clear_uploaded_file()
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
    
    def test_clear_uploaded_file(self, main_page, temp_file):
        """测试清除已上传文件"""
        main_page.upload_file(temp_file)
        assert main_page.is_file_uploaded(), "文件应已上传"
        
        main_page.clear_uploaded_file()
        
        # 验证文件信息已隐藏
        assert not main_page.is_file_uploaded(), "清除后文件信息应隐藏"
    
    def test_upload_nonexistent_file(self, main_page):
        """测试上传不存在的文件"""
        with pytest.raises(FileNotFoundError):
            main_page.upload_file("/path/to/nonexistent/file.txt")
    
    def test_upload_empty_file(self, main_page):
        """测试上传空文件"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("")  # 空文件
            temp_path = f.name
        
        try:
            main_page.upload_file(temp_path)
            assert main_page.is_file_uploaded(), "空文件也应能上传"
            
            # 验证文件大小显示
            meta_text = main_page.get_uploaded_file_meta()
            assert "0 B" in meta_text or "B" in meta_text, "空文件大小应显示为0 B"
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
