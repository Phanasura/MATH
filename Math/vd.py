import math

# Góc 30 độ trong radian
angle_radian = math.radians(30)

# Tính giá trị tan(30 độ)
tan_30_degree = math.tan(angle_radian)

# Tính giá trị của biểu thức
result = round(((3/4) + tan_30_degree) / (1 - (3/4) * tan_30_degree), 2)

print("Kết quả của biểu thức:", result)
