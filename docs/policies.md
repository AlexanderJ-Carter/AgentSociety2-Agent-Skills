# 项目治理 / Project Policies

本页汇总公开仓库的许可、贡献、安全和引用约定。源文件仍以仓库根目录为准。

## License

本仓库使用 MIT License。代码、文档和技能说明可以复制、修改、发布和再授权，但必须保留版权声明和许可文本。

第三方论文、书籍、模型名称、商标和引用资料仍归原权利人所有。`references/` 中的引用用于说明模型来源，不重新授权原始内容。

Source: `LICENSE`

## Contributing

欢迎贡献：

- 新技能和现有技能改进
- 理论依据、公式、变量范围和引用
- 确定性 baseline 脚本
- 文档、示例、站点和测试改进

提交前请运行：

```bash
python scripts/generate_skill_catalog.py
python -m unittest tests.test_skill_repository
python -m mkdocs build
```

Source: `CONTRIBUTING.md`

## Security

不要在公开 issue 中披露安全问题。安全报告应优先使用 GitHub private vulnerability reporting；如果仓库没有开启该功能，请通过维护者 GitHub 资料页或已有私有渠道联系。

不要提交：

- API keys、tokens、private keys、passwords
- 真实个人身份信息、位置轨迹、健康记录、财务记录或私密对话
- 未脱敏的真实 agent workspace dumps

Source: `SECURITY.md`

## Safety Boundary

这些技能用于社会仿真、agent 行为建模和可审查能力复用。心理、健康、经济、制度和媒介相关模型都是仿真近似，不是医疗、法律、金融、心理咨询或公共政策建议。

新增技能应写清楚模型边界，避免把简化公式包装成现实诊断或预测。

## Citation

如果在研究、论文、实验或项目报告中使用本仓库，请引用仓库或 `CITATION.cff`。

Source: `CITATION.cff`
