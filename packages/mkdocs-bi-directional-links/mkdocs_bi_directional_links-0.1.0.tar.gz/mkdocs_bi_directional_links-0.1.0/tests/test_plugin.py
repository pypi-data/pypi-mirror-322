import unittest
from mkdocs_bi_directional_links.plugin import BiDirectionalLinksPlugin

class TestPlugin(unittest.TestCase):
    def test_plugin_initialization(self):
        """
        测试插件初始化。
        """
        plugin = BiDirectionalLinksPlugin()
        self.assertFalse(plugin.debug)  # 确保调试模式默认关闭

    def test_on_config_with_debug(self):
        """
        测试插件配置加载（启用调试模式）。
        """
        plugin = BiDirectionalLinksPlugin()
        config = {
            "docs_dir": "docs",
            "plugins": {
                "bi_directional_links": {
                    "debug": True  # 启用调试模式
                }
            }
        }
        plugin.on_config(config)
        self.assertTrue(plugin.debug)  # 确保调试模式已启用

    def test_on_config_without_debug(self):
        """
        测试插件配置加载（未启用调试模式）。
        """
        plugin = BiDirectionalLinksPlugin()
        config = {
            "docs_dir": "docs",
            "plugins": {
                "bi_directional_links": {
                    "debug": False  # 未启用调试模式
                }
            }
        }
        plugin.on_config(config)
        self.assertFalse(plugin.debug)  # 确保调试模式未启用