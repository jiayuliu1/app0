class Material:
    def __init__(self, name, alias, drug_property, part, produce, area, effects, taboo, img=''):
        self.name = name  # 药材名
        self.alias = alias  # 别名
        self.drug_property = drug_property  # 药性
        self.part = part  # 入药部分
        self.produce = produce  # 药材使用方法
        self.area = area  # 产地分布
        self.effects = effects  # 功效
        self.taboo = taboo  # 禁忌
        self.img = img

