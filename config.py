general_configuration = {
    'num_classes' : 3, # label classes
    # 'dataset_path' : '/Users/hongxianglin/document/ucl_coding/P5_mri_image/', # PC
    'dataset_path' : '/home/harrylin/', # cluster
    # 'base_path' : '/Users/hongxianglin/document/ucl_coding/P3_IQT_Unet/tutorial_result/', # PC
    'base_path' : '/home/harrylin/iqt_tutorial_results', # cluster
    'job_name' : 'default',
    'log_path' : 'log',
    'model_path' : 'models',
    'results_path' : 'result',
    'evaluation_path': 'evaluation',
    'dataset_info' : {
        'iSeg2017' : {
            'format' : 'analyze',
            'dimensions' : (144, 192, 256),
            'num_volumes' : 10,
            'modalities' : 2,
            'general_pattern' : 'subject-{}-{}.hdr',
            'path' : 'iSeg2017/iSeg-2017-Training/',
            'inputs' : ['T1', 'T2', 'label']
        },
        'IBSR18' : {
            'format' : 'nii',
            'dimensions' : (256, 128, 256),
            'num_volumes' : 10, # at least 3
            'modalities' : 1,
            'general_pattern' : 'IBSR_{0:02}/IBSR_{0:02}_{1}.nii.gz',
            'path' : 'IBSR18/',
            'inputs' : ['ana_strip', 'segTRI_ana']
        },
        'MICCAI2012' : {
            'format' : 'nii',
            'dimensions' : (256, 287, 256),
            'num_volumes' : [15, 20],
            'modalities' : 1,
            'general_pattern' : ['{}/{}_tmp.nii.gz', '{}/{}_3C_tmp.nii.gz', '{}/{}_{}.nii.gz'],
            'path' : 'MICCAI2012/',
            'folder_names' : ['training-images', 'training-labels', 'testing-images', 'testing-labels']
        },
        'HCP-Wu-Minn-Contrast': {
            'format' : 'nii',
            'dimensions': (260, 311, 256), # output shape
            'num_volumes': [3, 1], # train and test
            'modalities': 1,
            'general_pattern': '{}/T1w/{}_acpc_dc_restore_brain{}.nii',
            'path': 'HCP',
            'postfix_category': {'cnn_input': 0, 'cnn_gt': 1, 'preproc_out': 2, 'preproc_in': 3},
            'postfix': ['_procin', '_sim036T_ds6_gap2_groundtruth', '_procin', '_sim036T_ds6_gap2_groundtruth'],
            'modality_categories': ['T1w', 'T2w', 'FLAIR', 'T2starw'],
            'downsample_scale' : 8,
            'sparse_scale' : [1, 1, 8],
            'shrink_dim' : 3,
            'is_preproc': False, # input pre-processing
            'upsample_scale': [1, 1, 8],
            'interp_order' : 3 # try 0-5
        },
        'HBN': {
            'format': 'nii',
            'dimensions': (176, 256, 256),  # output shape
            'num_volumes': [15, 5],  # train and test
            'modalities': 1,
            'general_pattern': '{}/{}_{}{}.nii',
            'path': 'HBN-data',
            # 'postfix': ['.nii_sim036T_ds5_gap1_GM53_WM61', '_SS'],
            'postfix': ['_sim036T_2d_GM50_WM63_pre', '', '_sim036T_2d_GM50_WM63'],
            # 'postfix': ['_sim036T_2d_GM12_WM14_k8', '', '_sim036T_2d_GM12_WM14_k8', '.nii_sim036T_GM12_WM14'],
            'modality_categories': ['T1w', 'T2w', 'FLAIR', 'T2starw'],
            'downsample_scale': 6,
            'sparse_scale': [1, 1, 6],
            'shrink_dim': 3,
            'is_preproc': False,  # input pre-processing
            'upsample_scale': [1, 1, 6],
        }
    }
}

training_configuration = {
    'retrain' : True,
    'activation' : 'null',
    'approach' : 'SRUnet',
    'dataset' : 'HCP-Wu-Minn-Contrast',
    'dimension' : 3,
    'extraction_step' : (16, 16, 16),
    'extraction_step_test' :(16, 16, 16),
    'loss' : 'mean_squared_error',
    'metrics' : ['mse'],
    'batch_size' : 32,
    'num_epochs' : 200,
    'optimizer' : 'Adam',
    'output_shape' : (32, 32, 32),
    'output_shape_test' : (16, 16, 16),
    'patch_shape' : (32, 32, 4),
    'bg_discard_percentage' : 0.2,
    'patience' : 5,
    'validation_split' : 0.20,
    'verbose' : 1, # 0: save message flow in log, 1: process bar record, 2: epoch output record
    'shuffle' : True,
    'decay' : 0.000001,
    'learning_rate' : 0.001,
    'downsize_factor' : 1,
    'num_kernels' : 3,
    'num_filters' : 128,
    'mapping_times' : 2
}
