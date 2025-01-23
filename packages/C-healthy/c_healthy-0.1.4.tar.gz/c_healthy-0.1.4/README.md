# C_healthy

C_healthy là thư viện Python để tính toán các chỉ số sức khỏe (BMI, BMR, TDEE) 

## Cách cài đặt
```bash
pip install C_healthy

## Cách sử dụng
```python
from C_healthy import BMI, BMR, TDEE, WHR, LBM, BFP, NW, IBW, MA

bmi = BMI(70, 1.75)
bmr = BMR("nam", 60, 1.75, 18)
tdee = TDEE("nam", 60, 1.75, 18, 3)
lbm = LBM("nam", 70, 1.75) 
bfp = BFP("nam", 70, 1.75, 20)
ibw = IBW("nam", 1.75)
whr = WHR("nam", 85, 95)
nw = NW(60)
ma = MA("nam", 70, 1.7, 18)
print("BMI:", bmi)
print("BMR:", bmr)
print("TDEE:", tdee)
print("LBM:", lbm)
print("BFP:", bfp)
print("WHR:", whr)
print("IBW:", ibw)
print("NW:", nw)
print("MA:", ma)