import unittest
from mkdocs_bi_directional_links.search_integration import SearchIntegration
from mkdocs.structure.files import File

class TestSearchIntegration(unittest.TestCase):
    def setUp(self):
        """
        初始化测试环境。
        """
        self.search_integration = SearchIntegration()
        # 模拟 MkDocs 配置
        config = {"docs_dir": "tests/test_data", "plugins": {"search": {}}}
        self.search_integration.load_config(config)

        # 模拟文件列表
        self.files = [
            File("tests/test_data/page1.md", "tests/test_data", "tests/test_data", False),
            File("tests/test_data/subdir/page2.md", "tests/test_data", "tests/test_data", False),
            File("tests/test_data/image.png", "tests/test_data", "tests/test_data", False),
            File("tests/test_data/video.mp4", "tests/test_data", "tests/test_data", False),
            File("tests/test_data/audio.mp3", "tests/test_data", "tests/test_data", False)
        ]

        self.search_integration.load_files(self.files)

    def test_find_file(self):
        """
        测试 Search 插件的文件查找功能。
        """
        # 模拟查找文件
        from_file = "tests/test_data/page.md"
        file_ref = "page1.md"
        result = self.search_integration.find_file(from_file, file_ref)
        self.assertIsNotNone(result)  # 确保找到文件
        self.assertEqual(result, "tests/test_data/page1.md")  # 确保路径正确

    def test_find_file_not_found(self):
        """
        测试文件未找到时的处理逻辑。
        """
        # 模拟查找不存在的文件
        from_file = "tests/test_data/page.md"
        file_ref = "nonexistent.md"
        result = self.search_integration.find_file(from_file, file_ref)
        self.assertIsNone(result)  # 确保返回 None

    def test_find_file_with_subdir(self):
        """
        测试子目录中的文件查找。
        """
        # 模拟查找子目录中的文件
        from_file = "tests/test_data/page.md"
        file_ref = "subdir/page2.md"
        result = self.search_integration.find_file(from_file, file_ref)
        self.assertIsNotNone(result)  # 确保找到文件
        self.assertEqual(result, "tests/test_data/subdir/page2.md")  # 确保路径正确

    def test_cache_output(self):
        """
        测试输出缓存功能。
        """
        # 模拟查找文件并缓存结果
        from_file = "tests/test_data/page.md"
        file_ref = "page1.md"
        result = self.search_integration.find_file(from_file, file_ref)
        self.assertIsNotNone(result)  # 确保找到文件
        self.assertEqual(result, "tests/test_data/page1.md")  # 确保路径正确

        # 调用 print_cache 方法输出缓存内容
        cache_output = self.search_integration.file_cache
        self.assertIn("page1.md", cache_output)  # 确保缓存中包含查找的文件
