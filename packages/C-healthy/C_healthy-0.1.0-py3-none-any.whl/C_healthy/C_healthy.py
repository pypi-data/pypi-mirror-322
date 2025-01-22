# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def BMI(can_nang, chieu_cao):
    try:
        if(can_nang > 0 and chieu_cao > 0):
            return round(can_nang / (chieu_cao ** 2), 2)
        else:
            raise ValueError("""Vui lòng nhập theo mẫu BMI([Cân nặng (kg)], [Chiều cao (m)])""")    
    except Exception as e:
        raise ValueError(f"[Lỗi hàm {__name__}]: {e}")


def BMR(gioi_tinh ,can_nang, chieu_cao, tuoi):
    ktra_gioi_tinh(gioi_tinh)
    gioi_tinh_cho_phep = ["nam", "nu"]
    try:
        if(can_nang > 0 and chieu_cao > 0 and tuoi > 0) and gioi_tinh.lower() in gioi_tinh_cho_phep:
            chieu_cao = chieu_cao * 100
            if(gioi_tinh.lower() == gioi_tinh_cho_phep[1]):
                #BMR = 655 + (9,6 × trọng lượng tính bằng kg) + (1,8 × chiều cao tính bằng cm) – (4,7 × tuổi tính theo năm)
                return round((655 + (9.6 * can_nang) + (1.8 * chieu_cao) - (4.7 * tuoi)), 2)
            else:
                #Nam giới: BMR = 66 + (13,7 × trọng lượng tính bằng kg) + (5 × chiều cao tính bằng cm) – (6,8 × tuổi tính theo năm)
                return round((66 + (13.7 * can_nang) + (5 * chieu_cao) - (6.8 * tuoi)), 2) 
        else:
            raise ValueError("""Vui lòng nhập theo mẫu BMR([Giới tính (nam/nu)], [Cân nặng (kg)], [Chiều cao(m)], [Tuổi]""")
    except Exception as e:
        raise ValueError(f"[Lỗi hàm {__name__}]: {e}")
                    

def TDEE(gioi_tinh, can_nang, chieu_cao, tuoi, chi_so_R):
    try:
        ktra_gioi_tinh(gioi_tinh)
        he_so_van_dong = {
            1: 1.2,
            2: 1.375,
            3: 1.55,
            4: 1.725,
            5: 1.9
        }
        chi_so_bmr = BMR(gioi_tinh, can_nang, chieu_cao, tuoi)
        if(chi_so_R in he_so_van_dong):
            return round((chi_so_bmr * he_so_van_dong[chi_so_R]), 2)
        else:
            valid_keys = ", ".join(str(k) for k in he_so_van_dong.keys())
            raise ValueError(f"Chỉ số vận động không hợp lệ! Chọn một trong các giá trị: {valid_keys}")
    except Exception as e:
        raise ValueError(f"[Lỗi hàm {__name__}]: {e}")
        

def HDSD(Loai):
    try:
        if(Loai == "BMI"):
            noi_dung = (
                "Lệnh BMI: nhập theo cú pháp BMI([cân nặng] [chiều cao])",
                "Ví dụ: BMI(60, 1.75)"
            )
        elif(Loai == "BMR"):
            noi_dung = ( 
                "Lệnh BMR: nhập theo cú pháp BMR([giới tính] [cân nặng], [chiều cao], [tuổi])",
                "Ví dụ: BMR('nam', 60, 1.75, 18)"
            )   
        elif(Loai == "TDEE"):
            noi_dung = (
                """Lệnh TDEE: nhập theo cú pháp TDEE([giới tính], [cân nặng], [chiều cao], [tuổi], [chỉ số vận động]),
                Với chỉ số vận động gồm:
                1: Không vận động 
                2: Vận động nhẹ
                3: Vận động vừa
                4: Vận động nhiều
                5: Vận động rất nhiều
                Ví dụ: TDEE('nam', 60, 1.75, 18, 3)"""
            )
        else:
            raise ValueError("Loại không hợp lệ! Chọn giữa 'BMI', 'BMR', hoặc 'TDEE'")  
        return noi_dung 
    except Exception as e:
        raise ValueError(f"[Lỗi hàm {__name__}]: {e}")
        
def ktra_gioi_tinh(gioi_tinh):
    gioi_tinh_cho_phep = ["nam", "nu"]
    if gioi_tinh.lower() not in gioi_tinh_cho_phep:
        raise ValueError("Giới tính không hợp lệ! Chỉ được chọn 'nam' hoặc 'nu'")   
        