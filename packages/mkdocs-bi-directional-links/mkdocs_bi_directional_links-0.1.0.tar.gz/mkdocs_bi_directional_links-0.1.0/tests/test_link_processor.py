import unittest
from mkdocs_bi_directional_links.link_processor import LinkProcessor
from mkdocs_bi_directional_links.search_integration import SearchIntegration
from mkdocs.structure.pages import Page
from mkdocs.structure.files import File

class TestLinkProcessor(unittest.TestCase):
    def setUp(self):
        """
        初始化测试环境。
        """
        self.processor = LinkProcessor()
        self.search_integration = SearchIntegration()
        # 模拟 MkDocs 配置
        config = {"docs_dir": "tests/test_data", "plugins": {"search": {}}}
        self.search_integration.load_config(config)

        # 模拟文件列表
        files = [
            File("tests/test_data/page1.md", "tests/test_data", "tests/test_data", False),
            File("tests/test_data/subdir/page2.md", "tests/test_data", "tests/test_data", False),
            File("tests/test_data/image.png", "tests/test_data", "tests/test_data", False),
            File("tests/test_data/video.mp4", "tests/test_data", "tests/test_data", False),
            File("tests/test_data/audio.mp3", "tests/test_data", "tests/test_data", False)
        ]
        self.search_integration.load_files(files)

        # 模拟当前页面
        self.page = Page(
            title="Test Page",
            file=File("tests/test_data/page.md", "tests/test_data", "tests/test_data", False),
            config={}
        )
        self.page.markdown = ""  # 手动设置 markdown 内容

    def test_process_markdown(self):
        """
        测试双向链接处理模块。
        """
        markdown = "[[page1]]"
        result = self.processor.process_markdown(markdown, self.page, None, None, self.search_integration)
        self.assertIn('<a href="/tests/test_data/page1/">page1</a>', result)  # 确保生成正确的链接

    def test_process_markdown_with_text(self):
        """
        测试带自定义文本的双向链接。
        """
        markdown = "[[page1|第一页]]"
        result = self.processor.process_markdown(markdown, self.page, None, None, self.search_integration)
        self.assertIn('<a href="/tests/test_data/page1/">第一页</a>', result)  # 确保生成正确的链接

    def test_process_markdown_image(self):
        """
        测试图片链接。
        """
        markdown = "![[image.png]]"
        result = self.processor.process_markdown(markdown, self.page, None, None, self.search_integration)
        self.assertIn('<img src="/tests/test_data/image.png" alt="image.png">', result)  # 确保生成正确的图片标签

    def test_process_markdown_video(self):
        """
        测试视频链接。
        """
        markdown = "![[video.mp4]]"
        result = self.processor.process_markdown(markdown, self.page, None, None, self.search_integration)
        self.assertIn('<video controls><source src="/tests/test_data/video.mp4"></video>', result)  # 确保生成正确的视频标签

    def test_process_markdown_audio(self):
        """
        测试音频链接。
        """
        markdown = "![[audio.mp3]]"
        result = self.processor.process_markdown(markdown, self.page, None, None, self.search_integration)
        self.assertIn('<audio controls><source src="/tests/test_data/audio.mp3"></audio>', result)  # 确保生成正确的音频标签

    def test_process_markdown_file_not_found(self):
        """
        测试文件未找到时的处理逻辑。
        """
        markdown = "[[nonexistent.md]]"
        result = self.processor.process_markdown(markdown, self.page, None, None, self.search_integration)
        self.assertEqual(result, markdown)  # 确保返回原始文本