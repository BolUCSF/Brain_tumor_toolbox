## Brain tumor toolbox
Preprocess any Brain MRI image with format of nifti.(T1/T1C/T2/FLAIR).
# Skull stripping
1. Apply HD-BET deep learning method to generate brainmask.
2. Use my own model, with label of brainstem,cerebellum and brain(tr do).
# Registration
1. Rigid registration with NiftiReg.
2. Any registration from Antspy package(to do).
# Segmentation
Apply my deel learning model to get the label for tumor(to do).
## Plan
### Image super-resolution
Augment the image with under sampling in some axis.
### Miss modality gheneration
Generate T1,T2 according to T1C and FLAIR, since T1 and T2 are not so important for diagnosis but required by some model.
