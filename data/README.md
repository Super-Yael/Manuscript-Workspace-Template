# 数据获取与准备

- raw/：原始输入。当前 example.csv 是手工构造的 12 条虚构数据，可以随模板公开。
- dictionary.csv：字段、类型、单位、取值范围、缺失规则及含义。
- prepare.R：读取、校验和整理输入；输出 derived/measurements.csv。
- derived/：可重新生成的数据，不手动修改，不默认提交。

运行 make data。输入路径与分组在 config/project.R 中设置；更换输入路径时同步更新 Makefile 中的文件依赖。

示例拒绝空表、重复/空样本编号、缺失值、非数值或非有限结局、未知/缺失组别和不足两个样本的组。真实研究应按方案改写校验和缺失处理，而非沿用示例规则。

使用真实数据时先记录来源、获取日期、许可、原始校验和及数据版本，并按实际权限调整 Git 忽略规则和 submission/package.R 的打包白名单。make clean 永不删除 raw/。
