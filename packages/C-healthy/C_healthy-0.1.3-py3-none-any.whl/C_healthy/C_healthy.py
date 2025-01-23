# -*- coding: utf-8 -*-
# !py 
# using Vietnamese 
# NTC++ coding this file 
# ------------------------------------------------------------------------------------------------------------------------------------------- #
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# BMI (chỉ số khối cơ thể)
def BMI(can_nang, chieu_cao):
    try:
        if(can_nang > 0 and chieu_cao > 0):
            return round(can_nang / (chieu_cao ** 2), 2)
        else:
            return "Invalid input"   
    except Exception as e:
        raise ValueError(f"[{e}]")

# BMR (Tỷ lệ chuyển hóa cơ bản)
def BMR(gioi_tinh ,can_nang, chieu_cao, tuoi):
    if(not ktra_gioi_tinh(gioi_tinh)):
        return("Gioi tinh cho phep: ['nam', 'nu']\nVui long nhap lai cu phap")
    try:
        if(can_nang > 0 and chieu_cao > 0 and tuoi > 0):
            chieu_cao = chieu_cao * 100
            if(gioi_tinh.lower() == "nu"):
                #BMR = 655 + (9,6 × trọng lượng tính bằng kg) + (1,8 × chiều cao tính bằng cm) – (4,7 × tuổi tính theo năm)
                return round((655 + (9.6 * can_nang) + (1.8 * chieu_cao) - (4.7 * tuoi)), 2)
            else:
                #Nam giới: BMR = 66 + (13,7 × trọng lượng tính bằng kg) + (5 × chiều cao tính bằng cm) – (6,8 × tuổi tính theo năm)
                return round((66 + (13.7 * can_nang) + (5 * chieu_cao) - (6.8 * tuoi)), 2) 
        else:
            return "Invalid input"
    except Exception as e:
        raise ValueError(f"[{e}]")
                    
# TDEE (năng lượng tiêu thụ hàng ngày)
def TDEE(gioi_tinh, can_nang, chieu_cao, tuoi, chi_so_R):
    try:
        if(not ktra_gioi_tinh(gioi_tinh)):
            return("Gioi tinh cho phep: ['nam', 'nu']\nVui long nhap lai cu phap")
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
            raise ValueError(f"Chi so van dong khong hop le! Chon 1 trong cac gia tri: {valid_keys}")
    except Exception as e:
        raise ValueError(f"[{e}]")
        
# HƯỚNG DẪN SỬ DỤNG
# HƯỚNG DẪN SỬ DỤNG
def HDSD(Loai):
    try:
        if(Loai.upper() == "BMI"):
            noi_dung = (
                """Lenh BMI: nhap theo cu phap BMI([can nang] [chieu cao]),
                Vi du: BMI(60, 1.75)"""
            )
        elif(Loai.upper() == "BMR"):
            noi_dung = ( 
                """Lenh BMR: nhap theo cu phap BMR([gioi tinh] [can nang], [chieu cao], [tuoi]),
                Vi du: BMR('nam', 60, 1.75, 18)"""
            )   
        elif(Loai.upper() == "TDEE"):
            noi_dung = (
                """Lenh TDEE: nhap theo cu phap TDEE([gioi tinh], [can nang], [chieu cao], [tuoi], [chi so van dong]),
                Voi chi so van dong gom:
                1: Khong van dong 
                2: Van dong nhe
                3: Van dong vua
                4: Van dong nhieu
                5: Van dong rat nhieu
                Vi du: TDEE('nam', 60, 1.75, 18, 3)"""
            )
        elif(Loai.upper() == "WHR"):
            noi_dung = (
                """Lenh WHR: nhap theo cu phap WHR([gioi tinh], [vong eo], [vong hong]),
                Vi du: WHR('nu', 70, 80)"""
            )
        elif(Loai.upper() == "LBM"):
            noi_dung = (
                """Lenh LBM: nhap theo cu phap LBM([gioi tinh], [can nang], [chieu cao]),
                Vi du: LBM('nam', 60, 1.75)"""
            )
        elif(Loai.upper() == "BFP"):
            noi_dung = (
                """Lenh BFP: nhap theo cu phap BFP([gioi tinh], [can nang], [chieu cao], [tuoi]),
                Vi du: BFP('nam', 60, 1.75, 18)"""
            )
        elif(Loai.upper() == "NW"):
            noi_dung = (
                """Lenh NW: nhap theo cu phap NW([can nang]),
                Vi du: NW(60)"""
            )
        elif(Loai.upper() == "IBW"):
            noi_dung = (
                """Lenh IBW: nhap theo cu phap IBW([gioi tinh], [chieu cao]),
                Vi du: IBW('nam', 1.75)"""
            )
        elif(Loai.upper() == "MA"):
            noi_dung = (
                """Lenh MA: nhap theo cu phap MA([gioi tinh], [can nang], [chieu cao], [tuoi]),
                Vi du: MA('nam', 70, 1.75, 18)"""
            )
        elif(Loai.upper() == "ALL"):
            noi_dung = (
                "Lenh BMI: nhap theo cu phap BMI([can nang] [chieu cao])",
                "Vi du: BMI(60, 1.75)",
                "Lenh BMR: nhap theo cu phap BMR([gioi tinh] [can nang], [chieu cao], [tuoi])",
                "Vi du: BMR('nam', 60, 1.75, 18)",
                """Lenh TDEE: nhap theo cu phap TDEE([gioi tinh], [can nang], [chieu cao], [tuoi], [chi so van dong]),
                Voi chi so van dong gom:
                1: Khong van dong 
                2: Van dong nhe
                3: Van dong vua
                4: Van dong nhieu
                5: Van dong rat nhieu
                Vi du: TDEE('nam', 60, 1.75, 18, 3)""",
                """Lenh WHR: nhap theo cu phap WHR([gioi tinh], [vong eo], [vong hong]),
                Vi du: WHR('nu', 70, 80)""",
                """Lenh LBM: nhap theo cu phap LBM([gioi tinh], [can nang], [chieu cao]),
                Vi du: LBM('nam', 60, 1.75)""",
                """Lenh BFP: nhap theo cu phap BFP([gioi tinh], [can nang], [chieu cao], [tuoi]),
                Vi du: BFP('nam', 60, 1.75, 18)""",
                """Lenh NW: nhap theo cu phap NW([can nang]),
                Vi du: NW(60)""",
                """Lenh IBW: nhap theo cu phap IBW([gioi tinh], [chieu cao]),
                Vi du: IBW('nam', 1.75)""",
                """Lenh MA: nhap theo cu phap MA([gioi tinh], [can nang], [chieu cao], [tuoi]),
                Vi du: MA('nam', 70, 1.75, 18)"""
            )    
        else:
            return "Invalid input" 
        return noi_dung 
    except Exception as e:
        raise ValueError(f"[{e}]")


# KIỂM TRA GIỚI TÍNH         
def ktra_gioi_tinh(gioi_tinh):
    gioi_tinh_cho_phep = ["nam", "nu"]
    if gioi_tinh.lower() not in gioi_tinh_cho_phep:
        return False
    else: 
        return True      
    
# WHR (tỷ lệ vòng eo/hông)    
def WHR(gioi_tinh, vong_eo, vong_hong):
    try:
        if(not ktra_gioi_tinh(gioi_tinh)):
            return("Gioi tinh cho phep: ['nam', 'nu']\nVui long nhap lai cu phap")
        if(vong_eo <= 0 or vong_hong <= 0):
            return "Invalid input"
        return round((vong_eo / vong_hong), 2)
    except Exception as e:
        raise ValueError(f"[{e}]") 

# LBM (khối lượng cơ thể không mỡ)
def LBM(gioi_tinh, can_nang, chieu_cao):
    try:
        if(not ktra_gioi_tinh(gioi_tinh)):
            return("Gioi tinh cho phep: ['nam', 'nu']\nVui long nhap lai cu phap")
        chieu_cao = chieu_cao * 100    
        if(gioi_tinh.lower() == "nam"):
            lbm = round(((0.32810 * can_nang) + (0.33929 * chieu_cao) - 29.5336), 2)
        else:
            lbm = round(((0.29569 * can_nang) + (0.41813 * chieu_cao) - 43.2933), 2) 
        return lbm    
    except Exception as e:
        raise ValueError(f"[{e}]")

# BFP (Phần trăm mỡ cơ thể)
def BFP(gioi_tinh, can_nang, chieu_cao, tuoi):
    try:
        if(not ktra_gioi_tinh(gioi_tinh)):
            return("Gioi tinh cho phep: ['nam', 'nu']\nVui long nhap lai cu phap")
        bmi = BMI(can_nang, chieu_cao) 
        if(gioi_tinh.lower() == "nam"):
            bfp = round((1.20 * bmi) + (0.23 * tuoi) - 16.2, 2)
        else:
            bfp = round((1.20 * bmi) + (0.23 * tuoi) - 5.4, 2)
        return bfp
    except Exception as e:
        raise ValueError(f"[{e}]")

# Need water (lượng nước cần thiết mỗi ngày tính theo lít)
def NW(can_nang):
    try:
        luong_nuoc = round(can_nang * 0.033, 2)
        return luong_nuoc
    except Exception as e:
        raise ValueError(f"[{e}]")

# IBW (cân nặng lý tưởng dựa trên chiều cao)
def IBW(gioi_tinh, chieu_cao):
    try:
        if(not ktra_gioi_tinh(gioi_tinh)):
            return("Gioi tinh cho phep: ['nam', 'nu']\nVui long nhap lai cu phap")
        chieu_cao = chieu_cao * 100
        if(gioi_tinh.lower() == "nam"):
            ibw = round(50 + 2.3 * (chieu_cao - 152.4) / 2.54, 2)
        else:
            ibw = round(45.5 + 2.3 * (chieu_cao - 152.4) / 2.54, 2)
        return ibw
    except Exception as e:
        raise ValueError(f"[{e}]")

# MA (Metabolic age (tuổi sinh học))
def MA(gioi_tinh, can_nang, chieu_cao, tuoi):
    try:
        if(not ktra_gioi_tinh(gioi_tinh)):
            return("Gioi tinh cho phep: ['nam', 'nu']\nVui long nhap lai cu phap")
        bmr = BMR(gioi_tinh, can_nang, chieu_cao, tuoi)
        bmr_tb_nam = {
            (18, 30): 1900,
            (31, 50): 1800,
            (51, 70): 1700,
            (71, 150): 1600
        }
        bmr_tb_nu = {
            (18, 30): 1500,
            (31, 50): 1400,
            (51, 70): 1300,
            (71, 150): 1200
        }
        bang_bmr = bmr_tb_nam if gioi_tinh.lower() == "nam" else bmr_tb_nu
        bmr_tb = None
        for gioi_han_tuoi, tb_bmr in bang_bmr.items():
            if(gioi_han_tuoi[0] <= tuoi <= gioi_han_tuoi[1]):
                bmr_tb = tb_bmr
                break
        if bmr_tb is None:
            return(f"Tuoi '{tuoi}' khong duoc ho tro !") 
        he_so_dieu_chinh = (bmr - bmr_tb) / 100  
        ma = int(round(tuoi - he_so_dieu_chinh))  
        return ma
    except Exception as e:
        raise ValueError(f"[{e}]")


"""print(WHR("nam", -1, -100))  # Output: WHR: 0.85 - Nguy cơ thấp.
print(WHR("nu", 70, 80))    # Output: WHR: 0.88 - Nguy cơ cao.
print(WHR("nu", 60, 75))    # Output: WHR: 0.8 - Nguy cơ trung bình.
print(HDSD("mn"))
print(BMI(1, -1))
print(TDEE("nam", 67, 1.7, 18, 3))
print(LBM("nam", 60, 1.7))
print(BFP("nam", 60, 1.7, 18))
print(MA("nam", 70, 1.7, 18))"""

# ------------------------------------------------------ Copyright by NTC++ 22/01/2025 ------------------------------------------------------ #