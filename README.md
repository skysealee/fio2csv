方便大家快速把多个fio标准输出结果转换为CSV以快速对比或制作可视化图表
用法 python fio2csv.py path
结果 扫描path中所有txt结尾的fio输出文件并生成csv
注意 暂无健壮性设计，读取到非标准fio输出文件会报错退出
