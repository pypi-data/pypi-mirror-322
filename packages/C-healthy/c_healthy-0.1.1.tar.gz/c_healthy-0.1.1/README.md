# C_healthy

C_healthy là thư viện Python để tính toán các chỉ số sức khỏe (BMI, BMR, TDEE) 

## Cách cài đặt
```bash
pip install C_healthy


## Cách sử dụng
```python
from C_healthy import BMI, BMR, TDEE

bmi = BMI(70, 1.75)
bmr = BMR("nam", 60, 1.75, 18)
tdee = TDEE("nam", 60, 1.75, 18, 3)
print("BMI:", bmi)
print("BMR:", bmr)
print("TDEE:", tdee)
