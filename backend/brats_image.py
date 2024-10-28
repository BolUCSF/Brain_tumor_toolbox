# backend/brats_image.py
import os, shutil
import numpy as np
import nibabel as nib
import requests

class brats_image_set:
    def __init__(self, path_json):
        if len(path_json['T1']) > 0:
            self.T1 = path_json['T1']  # T1 图像地址
        else:
            self.T1 = None
        if len(path_json['T1C']) > 0:
            self.T1C = path_json['T1C']  # T1C 图像地址
        else:
            self.T1C = None
        if len(path_json['T2']) > 0:
            self.T2 = path_json['T2']  # T2 图像地址
        else:
            self.T2 = None
        if len(path_json['FLAIR']) > 0:
            self.FLAIR = path_json['FLAIR']  # FLAIR 图像地址
        else:
            self.FLAIR = None
        self.brainmask_needed = None

    def registration_image(self, brainmask_needed=False):
        print("Registration image...")
        print(brainmask_needed)
        if self.T1 is None or self.T1C is None or self.T2 is None or self.FLAIR is None:
            raise ValueError("T1, T1C, T2, and FLAIR images are required.")
        self.root_dir = os.path.dirname(self.T1)
        self.working_dir = self.root_dir+'/working_dir'
        if not os.path.exists(self.working_dir):
            os.makedirs(self.working_dir)
        shutil.copy(self.T1, self.working_dir)
        shutil.copy(self.T1C, self.working_dir)
        shutil.copy(self.T2, self.working_dir)
        shutil.copy(self.FLAIR, self.working_dir)
        self.T1 = self.working_dir+'/'+os.path.basename(self.T1)
        self.T1C = self.working_dir+'/'+os.path.basename(self.T1C)
        self.T2 = self.working_dir+'/'+os.path.basename(self.T2)
        self.FLAIR = self.working_dir+'/'+os.path.basename(self.FLAIR)
        if brainmask_needed:
            yield("Generating brain mask...")
            self.brainmask_needed = True
            command = f'hd-bet -i {self.T1}'
            os.system(command)
            command = f'hd-bet -i {self.T1C}'
            os.system(command)
            command = f'hd-bet -i {self.T2}'
            os.system(command)
            command = f'hd-bet -i {self.FLAIR}'
            os.system(command)
            yield("Brain mask generated.")
            self.T1_bet = self.T1.replace('.nii.gz', '_bet.nii.gz')
            self.T1C_bet = self.T1C.replace('.nii.gz', '_bet.nii.gz')
            self.T2_bet = self.T2.replace('.nii.gz', '_bet.nii.gz')
            self.FLAIR_bet = self.FLAIR.replace('.nii.gz', '_bet.nii.gz')
        
        atlas_path = self.working_dir+'/atlas.nii.gz'
        if not os.path.exists(atlas_path):
            yield("Altas file does not exist. Downloading...")
            url = "https://ucsf.box.com/shared/static/yi6vjp2ciif82j1ui6b8htd1ovtw8hd4.gz"
            response = requests.get(url, stream=True)
            
            if response.status_code == 200:
                with open(atlas_path, 'wb') as file:
                    file.write(response.content)
                yield("Download complete.")
        
        if not brainmask_needed:
            T1_regi_path = self.T1.replace('.nii.gz','_regi.nii.gz')
            T1_regi_txt_path = self.T1.replace('.nii.gz','.txt')
            command = f'registration/rigid_reg.sh registration/reg_aladin {atlas_path} {self.T1} {T1_regi_path} {T1_regi_txt_path}'
            yield("Rigid registration of T1 image...")  
            os.system(command)

            T1C_regi_path = self.T1C.replace('.nii.gz','_regi.nii.gz')
            T1C_regi_txt_path = self.T1C.replace('.nii.gz','.txt')
            command = f'registration/rigid_reg.sh registration/reg_aladin {T1_regi_path} {self.T1C} {T1C_regi_path} {T1C_regi_txt_path}'
            yield("Rigid registration of T1C image...")
            os.system(command)

            T2_regi_path = self.T2.replace('.nii.gz','_regi.nii.gz')
            T2_regi_txt_path = self.T2.replace('.nii.gz','.txt')
            command = f'registration/rigid_reg.sh registration/reg_aladin {T1_regi_path} {self.T2} {T2_regi_path} {T2_regi_txt_path}'
            yield("Rigid registration of T2 image...")
            os.system(command)

            FLAIR_regi_path = self.FLAIR.replace('.nii.gz','_regi.nii.gz')
            FLAIR_regi_txt_path = self.FLAIR.replace('.nii.gz','.txt')
            command = f'registration/rigid_reg.sh registration/reg_aladin {T1_regi_path} {self.FLAIR} {FLAIR_regi_path} {FLAIR_regi_txt_path}'
            yield("Rigid registration of FLAIR image...")
            os.system(command)



            shutil.copy(T1_regi_path, self.root_dir)
            shutil.copy(T1C_regi_path, self.root_dir)
            shutil.copy(T2_regi_path, self.root_dir)
            shutil.copy(FLAIR_regi_path, self.root_dir)
            shutil.rmtree(self.working_dir)
            yield("Rigid registration completed.")
        else:
            T1_bet_regi_path = self.T1_bet.replace('.nii.gz','_regi.nii.gz')
            T1_bet_regi_txt_path = self.T1_bet.replace('.nii.gz','.txt')
            T1_regi_path = self.T1.replace('.nii.gz','_regi.nii.gz')
            command = f'registration/rigid_reg.sh registration/reg_aladin {atlas_path} {self.T1_bet} {T1_bet_regi_path} {T1_bet_regi_txt_path}'
            yield("Rigid registration of T1_bet image...")
            os.system(command)
            command = f'registration/transform.sh registration/reg_resample {atlas_path} {self.T1} {T1_regi_path} {T1_bet_regi_txt_path} 4'
            yield("Transforming T1 image...")
            os.system(command)

            T1C_bet_regi_path = self.T1C_bet.replace('.nii.gz','_regi.nii.gz')
            T1C_bet_regi_txt_path = self.T1C_bet.replace('.nii.gz','.txt')
            T1C_regi_path = self.T1C.replace('.nii.gz','_regi.nii.gz')
            command = f'registration/rigid_reg.sh registration/reg_aladin {atlas_path} {self.T1C_bet} {T1C_bet_regi_path} {T1C_bet_regi_txt_path}'
            yield("Rigid registration of T1C_bet image...")
            os.system(command)
            command = f'registration/transform.sh registration/reg_resample {atlas_path} {self.T1C} {T1C_regi_path} {T1C_bet_regi_txt_path} 4'
            yield("Transforming T1C image...")
            os.system(command)

            T2_bet_regi_path = self.T2_bet.replace('.nii.gz','_regi.nii.gz')
            T2_bet_regi_txt_path = self.T2_bet.replace('.nii.gz','.txt')
            T2_regi_path = self.T2.replace('.nii.gz','_regi.nii.gz')
            command = f'registration/rigid_reg.sh registration/reg_aladin {atlas_path} {self.T2_bet} {T2_bet_regi_path} {T2_bet_regi_txt_path}'
            yield("Rigid registration of T2_bet image...")
            os.system(command)
            command = f'registration/transform.sh registration/reg_resample {atlas_path} {self.T2} {T2_regi_path} {T2_bet_regi_txt_path} 4'
            yield("Transforming T2 image...")
            os.system(command)

            FLAIR_bet_regi_path = self.FLAIR_bet.replace('.nii.gz','_regi.nii.gz')
            FLAIR_bet_regi_txt_path = self.FLAIR_bet.replace('.nii.gz','.txt')
            FLAIR_regi_path = self.FLAIR.replace('.nii.gz','_regi.nii.gz')
            command = f'registration/rigid_reg.sh registration/reg_aladin {atlas_path} {self.FLAIR_bet} {FLAIR_bet_regi_path} {FLAIR_bet_regi_txt_path}'
            yield("Rigid registration of FLAIR_bet image...")
            os.system(command)
            command = f'registration/transform.sh registration/reg_resample {atlas_path} {self.FLAIR} {FLAIR_regi_path} {FLAIR_bet_regi_txt_path} 4'
            yield("Transforming FLAIR image...")
            os.system(command)

            shutil.copy(T1_regi_path, self.root_dir)
            shutil.copy(T1C_regi_path, self.root_dir)
            shutil.copy(T2_regi_path, self.root_dir)
            shutil.copy(FLAIR_regi_path, self.root_dir)
            shutil.copy(T1_bet_regi_path, self.root_dir)
            shutil.copy(T1C_bet_regi_path, self.root_dir)
            shutil.copy(T2_bet_regi_path, self.root_dir)
            shutil.copy(FLAIR_bet_regi_path, self.root_dir)
            shutil.rmtree(self.working_dir)
            yield("Rigid registration completed.")
            
    # 你可以在这里添加其他方法

