import nibabel as nib
import numpy as np
import os
from architectures.arch_creator import generate_model
import csv

def read_meanstd(gen_conf, test_conf, case_name) :
    mean_filename = generate_output_filename(
            gen_conf['model_path'],
            test_conf['dataset'],
            case_name,
            test_conf['approach'],
            test_conf['dimension'],
            str(test_conf['patch_shape']),
            str(test_conf['extraction_step'])+'_mean',
            'npz')
#     with open(mean_filename, mode='r') as infile:
#         reader = csv.reader(infile)
#         mean = {rows[0]:np.array(rows[1]) for rows in reader}
    mean = {}
    mean_f = np.load(mean_filename)
    mean['input'] = mean_f['mean_input']
    mean['output'] = mean_f['mean_output']
        
    std_filename = generate_output_filename(
            gen_conf['model_path'],
            test_conf['dataset'],
            case_name,
            test_conf['approach'],
            test_conf['dimension'],
            str(test_conf['patch_shape']),
            str(test_conf['extraction_step'])+'_std',
            'npz')
#     with open(std_filename, mode='r') as infile:
#         reader = csv.reader(infile)
#         std = {rows[0]:np.array(rows[1]) for rows in reader}
    std = {}
    std_f = np.load(std_filename)
    std['input'] = std_f['std_input']
    std['output'] = std_f['std_output']
    return mean, std

def read_model(gen_conf, train_conf, case_name) :
    model = generate_model(gen_conf, train_conf)

    model_filename = generate_output_filename(
        gen_conf['model_path'],
        train_conf['dataset'],
        case_name,
        train_conf['approach'],
        train_conf['dimension'],
        str(train_conf['patch_shape']),
        str(train_conf['extraction_step']),
        'h5')

    model.load_weights(model_filename)

    return model

def read_dataset(gen_conf, train_conf, trainTestFlag = 'train') :
    dataset = train_conf['dataset']
    dataset_path = gen_conf['dataset_path']
    dataset_info = gen_conf['dataset_info'][dataset]
    if dataset == 'IBADAN-k8':
        return read_IBADAN_data(dataset_path, dataset_info, trainTestFlag)
    if dataset == 'HBN':
        return read_HBN_dataset(dataset_path, dataset_info, trainTestFlag)
    if dataset == 'HCP-Wu-Minn-Contrast' :
        return read_HCPWuMinnContrast_dataset(dataset_path, dataset_info, trainTestFlag)
    if dataset == 'iSeg2017' :
        return read_iSeg2017_dataset(dataset_path, dataset_info)
    if dataset == 'IBSR18' :
        return read_IBSR18_dataset(dataset_path, dataset_info)
    if dataset == 'MICCAI2012' :
        return read_MICCAI2012_dataset(dataset_path, dataset_info)
    if dataset == 'IBSR' :
        return read_IBSR_dataset(dataset_path, dataset_info)
    
def read_IBSR_dataset(dataset_path,
                      dataset_info,
                      trainTestFlag = 'train'):
    dimensions = dataset_info['dimensions']
    sparse_scale = dataset_info['sparse_scale']
    input_dimension = tuple(np.array(dimensions)/sparse_scale)
    modalities = dataset_info['modalities']
    path = dataset_info['path']
    pattern = dataset_info['general_pattern']
    modality_categories = dataset_info['modality_categories']
    in_postfix = dataset_info['postfix'][0]
    out_postfix = dataset_info['postfix'][1]
    if trainTestFlag == 'train' :
        subject_lib = dataset_info['training_subjects']
        num_volumes = dataset_info['num_volumes'][0]
    elif trainTestFlag == 'test' :
        subject_lib = dataset_info['test_subjects']
        num_volumes = dataset_info['num_volumes'][1]
    else :
        raise ValueError("trainTestFlag should be declared as 'train'/'test'/'evaluation'")

    in_data = np.zeros((num_volumes, modalities) + input_dimension)
    out_data = np.zeros((num_volumes, modalities) + dimensions)

    for img_idx in range(num_volumes):
        for mod_idx in range(modalities):
            in_filename = os.path.join(dataset_path,
                                       path,
                                       pattern).format(subject_lib[img_idx],
                                                       subject_lib[img_idx],
                                                       in_postfix)
            in_data[img_idx, mod_idx] = read_volume(in_filename)
            out_filename = os.path.join(dataset_path,
                                        path,
                                        pattern).format(subject_lib[img_idx],
                                                        subject_lib[img_idx],
                                                        out_postfix)
            out_data[img_idx, mod_idx] = read_volume(out_filename)

    return in_data, out_data

def read_IBADAN_data(dataset_path,
                     dataset_info,
                     trainTestFlag = 'test'):
    dimensions = dataset_info['dimensions']
    sparse_scale = dataset_info['sparse_scale']
    input_dimension = tuple(np.array(dimensions)/sparse_scale)
    modalities = dataset_info['modalities']
    path = dataset_info['path']
    pattern = dataset_info['general_pattern']
    modality_categories = dataset_info['modality_categories']
    in_postfix = dataset_info['postfix'][0]
    out_postfix = dataset_info['postfix'][1]
    if trainTestFlag == 'train' :
        subject_lib = dataset_info['training_subjects']
        num_volumes = dataset_info['num_volumes'][0]
    elif trainTestFlag == 'test' :
        subject_lib = dataset_info['test_subjects']
        num_volumes = dataset_info['num_volumes'][1]
    else :
        raise ValueError("trainTestFlag should be declared as 'train'/'test'/'evaluation'")

    in_data = np.zeros((num_volumes, modalities) + input_dimension)
    out_data = np.zeros((num_volumes, modalities) + dimensions)

    for img_idx in range(num_volumes):
        for mod_idx in range(modalities):
            in_filename = os.path.join(dataset_path,
                                        path,
                                        pattern).format(subject_lib[img_idx],
                                                        modality_categories[mod_idx],
                                                        in_postfix)
            in_data[img_idx, mod_idx] = read_volume(in_filename)
            if trainTestFlag != 'test' :
                out_filename = os.path.join(dataset_path,
                                            path,
                                            pattern).format(subject_lib[img_idx],
                                                            modality_categories[mod_idx],
                                                            out_postfix)
                out_data[img_idx, mod_idx] = read_volume(out_filename)

    return in_data, out_data

def read_HBN_dataset(dataset_path,
                     dataset_info,
                     trainTestFlag = 'train'):
    dimensions = dataset_info['dimensions']
    sparse_scale = dataset_info['sparse_scale']
    input_dimension = tuple(np.array(dimensions)//sparse_scale)
    modalities = dataset_info['modalities']
    path = dataset_info['path']
    pattern = dataset_info['general_pattern']
    modality_categories = dataset_info['modality_categories']
    in_postfix = dataset_info['postfix'][0]
    out_postfix = dataset_info['postfix'][1]
    if trainTestFlag == 'train' :
        subject_lib = dataset_info['training_subjects']
        num_volumes = dataset_info['num_volumes'][0]
    elif trainTestFlag == 'test' :
        subject_lib = dataset_info['test_subjects']
        num_volumes = dataset_info['num_volumes'][1]
    else :
        raise ValueError("trainTestFlag should be declared as 'train'/'test'/'evaluation'")

    in_data = np.zeros((num_volumes, modalities) + input_dimension)
    out_data = np.zeros((num_volumes, modalities) + dimensions)

    for img_idx in range(num_volumes):
        for mod_idx in range(modalities):
            in_filename = os.path.join(dataset_path,
                                        path,
                                        pattern).format(subject_lib[img_idx], subject_lib[img_idx],
                                                        modality_categories[mod_idx],
                                                        in_postfix)
            in_data[img_idx, mod_idx] = read_volume(in_filename)
            out_filename = os.path.join(dataset_path,
                                        path,
                                        pattern).format(subject_lib[img_idx], subject_lib[img_idx],
                                                        modality_categories[mod_idx],
                                                        out_postfix)
            out_data[img_idx, mod_idx] = read_volume(out_filename)

    return in_data, out_data

def read_HCPWuMinnContrast_dataset(dataset_path,
                                   dataset_info,
                                   trainTestFlag = 'train'):
    dimensions = dataset_info['dimensions']
    sparse_scale = dataset_info['sparse_scale']
    input_dimension = tuple(np.array(dimensions)//sparse_scale)
    modalities = dataset_info['modalities']
    path = dataset_info['path']
    pattern = dataset_info['general_pattern']
    modality_categories = dataset_info['modality_categories']
    in_postfix = dataset_info['postfix'][0]
    out_postfix = dataset_info['postfix'][1]
    if trainTestFlag == 'train' :
        subject_lib = dataset_info['training_subjects']
        num_volumes = dataset_info['num_volumes'][0]
    elif trainTestFlag == 'test' :
        subject_lib = dataset_info['test_subjects']
        num_volumes = dataset_info['num_volumes'][1]
    else :
        raise ValueError("trainTestFlag should be declared as 'train'/'test'/'evaluation'")
    print(num_volumes, modalities, input_dimension)
    in_data = np.zeros((num_volumes, modalities) + input_dimension)
    out_data = np.zeros((num_volumes, modalities) + dimensions)

    for img_idx in range(num_volumes):
        for mod_idx in range(modalities):
            in_filename = os.path.join(dataset_path,
                                        path,
                                        pattern).format(subject_lib[img_idx],
                                                        modality_categories[mod_idx],
                                                        in_postfix)
            in_data[img_idx, mod_idx] = read_volume(in_filename)
            out_filename = os.path.join(dataset_path,
                                            path,
                                            pattern).format(subject_lib[img_idx],
                                                            modality_categories[mod_idx],
                                                            out_postfix)
            out_data[img_idx, mod_idx] = read_volume(out_filename)

    return in_data, out_data

def read_iSeg2017_dataset(dataset_path, dataset_info) :
    num_volumes = dataset_info['num_volumes']
    dimensions = dataset_info['dimensions']
    modalities = dataset_info['modalities']
    path = dataset_info['path']
    pattern = dataset_info['general_pattern']
    inputs = dataset_info['inputs']

    image_data = np.zeros((num_volumes, modalities) + dimensions)
    labels = np.zeros((num_volumes, 1) + dimensions)

    for img_idx in range(num_volumes) :
        filename = dataset_path + path + pattern.format(str(img_idx + 1), inputs[0])
        image_data[img_idx, 0] = read_volume(filename)#[:, :, :, 0]
        
        filename = dataset_path + path + pattern.format(str(img_idx + 1), inputs[1])
        image_data[img_idx, 1] = read_volume(filename)#[:, :, :, 0]

        filename = dataset_path + path + pattern.format(img_idx + 1, inputs[1])
        labels[img_idx, 0] = read_volume(filename)[:, :, :, 0]

        image_data[img_idx, 1] = labels[img_idx, 0] != 0

    label_mapper = {0 : 0, 10 : 0, 150 : 1, 250 : 2}
    for key in label_mapper.keys() :
        labels[labels == key] = label_mapper[key]

    return image_data, labels

def read_IBSR18_dataset(dataset_path, dataset_info) :
    num_volumes = dataset_info['num_volumes']
    dimensions = dataset_info['dimensions']
    modalities = dataset_info['modalities']
    path = dataset_info['path']
    pattern = dataset_info['general_pattern']
    inputs = dataset_info['inputs']

    image_data = np.zeros((num_volumes, modalities) + dimensions)
    labels = np.zeros((num_volumes, 1) + dimensions)

    for img_idx in range(num_volumes) :
        filename = dataset_path + path + pattern.format(img_idx + 1, inputs[0])
        image_data[img_idx, 0] = read_volume(filename)[:, :, :, 0]

        filename = dataset_path + path + pattern.format(img_idx + 1, inputs[1])
        labels[img_idx, 0] = read_volume(filename)[:, :, :, 0]

    return image_data, labels

def read_MICCAI2012_dataset(dataset_path, dataset_info) :
    num_volumes = dataset_info['num_volumes']
    dimensions = dataset_info['dimensions']
    modalities = dataset_info['modalities']
    path = dataset_info['path']
    pattern = dataset_info['general_pattern']
    folder_names = dataset_info['folder_names']

    image_data = np.zeros((np.sum(num_volumes), modalities) + dimensions)
    labels = np.zeros((np.sum(num_volumes), 1) + dimensions)

    training_set = [1000, 1006, 1009, 1012, 1015, 1001, 1007,
        1010, 1013, 1017, 1002, 1008, 1011, 1014, 1036]

    testing_set = [1003, 1019, 1038, 1107, 1119, 1004, 1023, 1039, 1110, 1122, 1005,
        1024, 1101, 1113, 1125, 1018, 1025, 1104, 1116, 1128]

    for img_idx, image_name in enumerate(training_set) :
        filename = dataset_path + path + pattern[0].format(folder_names[0], image_name)
        image_data[img_idx, 0] = read_volume(filename)

        filename = dataset_path + path + pattern[1].format(folder_names[1], image_name)
        labels[img_idx, 0] = read_volume(filename)

        image_data[img_idx, 0] = np.multiply(image_data[img_idx, 0], labels[img_idx, 0] != 0)
        image_data[img_idx, 1] = labels[img_idx, 0] != 0

    for img_idx, image_name in enumerate(testing_set) :
        idx = img_idx + num_volumes[0]
        filename = dataset_path + path + pattern[0].format(folder_names[2], image_name)
        image_data[idx, 0] = read_volume(filename)

        filename = dataset_path + path + pattern[1].format(folder_names[3], image_name)
        labels[idx, 0] = read_volume(filename)

        image_data[idx, 0] = np.multiply(image_data[idx, 0], labels[idx, 0] != 0)
        image_data[idx, 1] = labels[idx, 0] != 0

    labels[labels > 4] = 0

    return image_data, labels

'''
    Read reconstructed results at evaluation step
'''
def read_result_volume(gen_conf, test_conf) :
    dataset = test_conf['dataset']
    if dataset == 'HCP-Wu-Minn-Contrast' :
        return read_result_volume_HCPWuMinnContrast(gen_conf, test_conf)
    ##  todo: template for the other datasets
    # elif dataset == 'MICCAI2012' :
    #     return save_volume_MICCAI2012(gen_conf, test_conf, volume, case_idx)
    # else:
    #     return save_volume_else(gen_conf, test_conf, volume, case_idx)

def read_result_volume_HCPWuMinnContrast(gen_conf, test_conf) :
    dataset = test_conf['dataset']
    dataset_info = gen_conf['dataset_info'][dataset]
    dimensions = dataset_info['dimensions']
    modalities = dataset_info['modalities']
    modality_categories = dataset_info['modality_categories']
    subject_lib = dataset_info['test_subjects']
    num_volumes = dataset_info['num_volumes'][1]

    out_data = np.zeros((num_volumes, modalities) + dimensions)

    for img_idx in range(num_volumes):
        for mod_idx in range(modalities):
            out_filename = generate_output_filename(
                gen_conf['results_path'],
                test_conf['dataset'],
                subject_lib[img_idx] + '_' + modality_categories[mod_idx],
                test_conf['approach'],
                test_conf['dimension'],
                str(test_conf['patch_shape']),
                str(test_conf['extraction_step']),
                dataset_info['format'])
            out_data[img_idx, mod_idx] = read_volume(out_filename)

    return out_data

def save_volume(gen_conf, test_conf, volume, case_idx) :
    dataset = test_conf['dataset']
    if dataset == 'IBADAN-k8' :
        return save_volume_IBADAN(gen_conf, test_conf, volume, case_idx)
    elif dataset == 'HBN' :
        return save_volume_HBN(gen_conf, test_conf, volume, case_idx)
    elif dataset == 'HCP-Wu-Minn-Contrast' :
        return save_volume_HCPWuMinnContrast(gen_conf, test_conf, volume, case_idx)
    elif dataset == 'MICCAI2012' :
        return save_volume_MICCAI2012(gen_conf, test_conf, volume, case_idx)
    else:
        return save_volume_else(gen_conf, test_conf, volume, case_idx)

def save_volume_IBADAN(gen_conf, test_conf, volume, case_idx) :
    # todo: check conf and modalities
    dataset = test_conf['dataset']
    dataset_info = gen_conf['dataset_info'][dataset]
    dataset_path = gen_conf['dataset_path']
    path = dataset_info['path']
    pattern = dataset_info['general_pattern']
    modality_categories = dataset_info['modality_categories']
    in_postfix = dataset_info['postfix'][0]
    subject_lib = dataset_info['test_subjects']
    num_volumes = dataset_info['num_volumes'][1]
    sparse_scale = dataset_info['sparse_scale']

    data_filename = os.path.join(dataset_path,
                                 path,
                                 pattern).format(subject_lib[case_idx[0]],
                                                 modality_categories[case_idx[1]],
                                                 in_postfix)
    image_data = read_volume_data(data_filename)

    ## change affine in the nii header
    if sparse_scale is not None:
        assert len(sparse_scale) == 3, "The length of sparse_scale is not equal to 3."
        # print image_data.affine
        nifty_affine = np.dot(image_data.affine, np.diag(tuple(1.0/np.array(sparse_scale))+(1.0, )))
        # print nifty_affine

    ## check and make folder
    out_filename = generate_output_filename(
        gen_conf['results_path'],
        test_conf['dataset'],
        subject_lib[case_idx[0]]+'_'+modality_categories[case_idx[1]],
        test_conf['approach'],
        test_conf['dimension'],
        str(test_conf['patch_shape']),
        str(test_conf['extraction_step']),
        dataset_info['format'])
    out_foldername = os.path.dirname(out_filename)
    if not os.path.isdir(out_foldername) :
        os.makedirs(out_foldername)
    print("Save file at {}".format(out_filename))
    __save_volume(volume, nifty_affine, out_filename, dataset_info['format'])

def save_volume_HBN(gen_conf, test_conf, volume, case_idx) :
    # todo: check conf and modalities
    dataset = test_conf['dataset']
    dataset_info = gen_conf['dataset_info'][dataset]
    dataset_path = gen_conf['dataset_path']
    path = dataset_info['path']
    pattern = dataset_info['general_pattern']
    modality_categories = dataset_info['modality_categories']
    in_postfix = dataset_info['postfix'][0]
    subject_lib = dataset_info['test_subjects']
    num_volumes = dataset_info['num_volumes'][1]
    sparse_scale = dataset_info['sparse_scale']

    data_filename = os.path.join(dataset_path,
                                 path,
                                 pattern).format(subject_lib[case_idx[0]], subject_lib[case_idx[0]],
                                                 modality_categories[case_idx[1]],
                                                 in_postfix)
    image_data = read_volume_data(data_filename)

    ## change affine in the nii header
    if sparse_scale is not None:
        assert len(sparse_scale) == 3, "The length of sparse_scale is not equal to 3."
        # print image_data.affine
        nifty_affine = np.dot(image_data.affine, np.diag(tuple(1.0/np.array(sparse_scale))+(1.0, )))
        # print nifty_affine

    ## check and make folder
    out_filename = generate_output_filename(
        gen_conf['results_path'],
        test_conf['dataset'],
        subject_lib[case_idx[0]]+'_'+modality_categories[case_idx[1]],
        test_conf['approach'],
        test_conf['dimension'],
        str(test_conf['patch_shape']),
        str(test_conf['extraction_step']),
        dataset_info['format'])
    out_foldername = os.path.dirname(out_filename)
    if not os.path.isdir(out_foldername) :
        os.makedirs(out_foldername)
    print("Save file at {}".format(out_filename))
    __save_volume(volume, nifty_affine, out_filename, dataset_info['format'])

def save_volume_HCPWuMinnContrast(gen_conf, test_conf, volume, case_idx) :
    # todo: check conf and modalities
    dataset = test_conf['dataset']
    dataset_info = gen_conf['dataset_info'][dataset]
    dataset_path = gen_conf['dataset_path']
    path = dataset_info['path']
    pattern = dataset_info['general_pattern']
    modality_categories = dataset_info['modality_categories']
    in_postfix = dataset_info['postfix'][0]
    subject_lib = dataset_info['test_subjects']
    num_volumes = dataset_info['num_volumes'][1]
    sparse_scale = dataset_info['sparse_scale']

    data_filename = os.path.join(dataset_path,
                                 path,
                                 pattern).format(subject_lib[case_idx[0]],
                                                 modality_categories[case_idx[1]],
                                                 in_postfix)
    image_data = read_volume_data(data_filename)

    ## change affine in the nii header
    if sparse_scale is not None:
        assert len(sparse_scale) == 3, "The length of sparse_scale is not equal to 3."
        # print image_data.affine
        nifty_affine = np.dot(image_data.affine, np.diag(tuple(1.0/np.array(sparse_scale))+(1.0, )))
        # print nifty_affine

    ## check and make folder
    out_filename = generate_output_filename(
        gen_conf['results_path'],
        test_conf['dataset'],
        subject_lib[case_idx[0]]+'_'+modality_categories[case_idx[1]],
        test_conf['approach'],
        test_conf['dimension'],
        str(test_conf['patch_shape']),
        str(test_conf['extraction_step']),
        dataset_info['format'])
    out_foldername = os.path.dirname(out_filename)
    if not os.path.isdir(out_foldername) :
        os.makedirs(out_foldername)
    print("Save file at {}".format(out_filename))
    __save_volume(volume, nifty_affine, out_filename, dataset_info['format'])

def save_volume_MICCAI2012(gen_conf, train_conf, volume, case_idx) :
    dataset = train_conf['dataset']
    approach = train_conf['approach']
    extraction_step = train_conf['extraction_step_test']
    dataset_info = gen_conf['dataset_info'][dataset]
    dataset_path = gen_conf['dataset_path']
    results_path = gen_conf['results_path']
    path = dataset_info['path']
    pattern = dataset_info['general_pattern']
    folder_names = dataset_info['folder_names']

    data_filename = dataset_path + path + pattern[1].format(folder_names[3], case_idx)
    image_data = read_volume_data(data_filename)

    volume = np.multiply(volume, image_data.get_data() != 0)

    out_filename = results_path + path + pattern[2].format(folder_names[3], str(case_idx), approach + ' - ' + str(extraction_step))

    __save_volume(volume, image_data.affine, out_filename, dataset_info['format'])

def save_volume_else(gen_conf, train_conf, volume, case_idx) :
    dataset = train_conf['dataset']
    approach = train_conf['approach']
    extraction_step = train_conf['extraction_step_test']
    dataset_info = gen_conf['dataset_info'][dataset]
    dataset_path = gen_conf['dataset_path']
    results_path = gen_conf['results_path']
    path = dataset_info['path']
    pattern = dataset_info['general_pattern']
    inputs = dataset_info['inputs']

    if dataset == 'iSeg2017' or dataset == 'IBSR18':
        volume_tmp = np.zeros(volume.shape + (1, ))
        volume_tmp[:, :, :, 0] = volume
        volume = volume_tmp

    data_filename = dataset_path + path + pattern.format(case_idx, inputs[-1])
    image_data = read_volume_data(data_filename)

    volume = np.multiply(volume, image_data.get_data() != 0)

    if dataset == 'iSeg2017' :
        volume[image_data.get_data() != 0] = volume[image_data.get_data() != 0] + 1

        label_mapper = {0 : 0, 1 : 10, 2 : 150, 3 : 250}
        for key in label_mapper.keys() :
            volume[volume == key] = label_mapper[key]

    out_filename = results_path + path + pattern.format(case_idx, approach + ' - ' + str(extraction_step))

    ## mkdir
    if not os.path.isdir(os.path.dirname(out_filename)):
        os.makedirs(os.path.dirname(out_filename))

    __save_volume(volume, image_data.affine, out_filename, dataset_info['format'])

def __save_volume(volume, nifty_affine, filename, format) :
    img = None
    if format == 'nii' :
        img = nib.Nifti1Image(volume.astype('float32'), nifty_affine) # uint8
    if format == 'analyze' :
        img = nib.analyze.AnalyzeImage(volume.astype('float32'), nifty_affine) # uint8
    nib.save(img, filename)

def read_volume(filename) :
    return read_volume_data(filename).get_data()

def read_volume_data(filename) :
    return nib.load(filename)

def generate_output_filename(
    path, dataset, case_name, approach, dimension, patch_shape, extraction_step, extension) :
#     file_pattern = '{}/{}/{:02}-{}-{}-{}-{}.{}'
    file_pattern = '{}/{}/{}-{}-{}-{}-{}.{}'
    print(file_pattern.format(path, dataset, case_name, approach, dimension, patch_shape, extraction_step, extension))
    return file_pattern.format(path, dataset, case_name, approach, dimension, patch_shape, extraction_step, extension)
