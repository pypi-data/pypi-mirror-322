# translator.py

class Translator:
    def __init__(self, language="English"):
        self.language = language
        self.translations = {
            # 软件标题
            "Water-flooding Method for Urban 3D-morphology": {
                "English": "Water-flooding Method for Urban 3D-morphology", "Chinese": "“地形-漫水”城市复杂空间演化模拟分析系统"},

            # 按钮名称
            "Step1:Create 2D Plot": {"English": "Step1:Create 2D Plot", "Chinese": "步骤1：创建2D图"},
            "Step2:Create 3D Plot": {"English": "Step2:Create 3D Plot", "Chinese": "步骤2：创建3D图"},
            "Step3:Water-flooding Simulation": {"English": "Step3:Water-flooding Simulation", "Chinese": "步骤3：淹水模拟"},

            # 滑块名称
            "① Number of Points": {"English": "① Number of Points", "Chinese": "① 点的数量"},
            "② Noise Ratio": {"English": "② Noise Ratio", "Chinese": "② 噪声比例"},
            "③ Number of Clusters": {"English": "③ Number of Clusters", "Chinese": "③ 聚类数量"},
            "④ Cluster Standard Deviation": {"English": "④ Cluster Standard Deviation", "Chinese": "④ 聚类标准差"},
            "⑤ Minimum Distance": {"English": "⑤ Minimum Distance", "Chinese": "⑤ 最小距离"},
            "⑥ Water Level": {"English": "⑥ Water Level", "Chinese": "⑥ 水位"},
            "⑦ X Slice": {"English": "⑦ X Slice", "Chinese": "⑦ X切片"},
            "⑧ Y Slice": {"English": "⑧ Y Slice", "Chinese": "⑧ Y切片"},

            # 其他常用文本
            "Language": {"English": "Language", "Chinese": "语言"},
        }

    def translate(self, element_name):
        # 获取当前语言的翻译
        return self.translations.get(element_name, {}).get(self.language, element_name)

    def set_language(self, language):
        self.language = language
