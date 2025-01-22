# C_healthy

C_healthy là thư viện Python để tính toán các chỉ số sức khỏe (BMI, BMR, TDEE) 

## Cách cài đặt
```bash
pip install C_healthy


## Cách sử dụng
```python
from HealthMetrics import calculate_bmi, calculate_bmr, calculate_tdee, recommend_diet

bmi = calculate_bmi(70, 1.75)
print("BMI:", bmi)
