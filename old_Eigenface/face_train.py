import os
import numpy as np
from PIL import Image

def vector2img(v):
    v_ = np.reshape(v, (20, 20))
    img = Image.fromarray(v_)
    return img

def get_train_data(m):
    train_data = []
    for root, dir, file_list in os.walk("./project1-data-Recognition"):
        print(root)
        for file in file_list:
            if os.path.splitext(file)[-1] == '.pgm':
                im = Image.open("./project1-data-Recognition/" + file)
                img = np.array(im.resize((20, 20), Image.BILINEAR)).reshape(400, 1)
                train_data.append(img)
                print(img.shape)
                print(file)
    return train_data

if __name__ == "__main__":
    m = 5
    train_data= get_train_data(m)
    print('训练数据量：', np.shape(train_data))
    print('类别数量：', 40)
    x_mean = np.mean(train_data, axis=0)
    # print('x_mean',np.shape(x_mean))
    np.savetxt('face_mean.txt', x_mean)
    # calculate the cov mat
    mat = np.zeros((400, 400))
    n = len(train_data)
    for i in range(n):
        x = train_data[i][:] - x_mean
        mat += np.dot(x, x.T)
        # print(i)
    mat /= n
    # calculate the eigen values and eigen vectors
    eig_values, eig_vectors = np.linalg.eig(mat)
    # eig_values = np.real(eig_values)
    # eig_vectors = np.real(eig_vectors)
    # np.savetxt('eigVector.txt', eig_vectors)
    # np.savetxt('eigValue.txt', eig_values)

    # save the first k eigen vectors
    d = input('输入能量百分比(1-100整数)：')
    k = int(int(d) * 5)
    eigValues_real = np.real(eig_values[:k])
    eigVectors_real = np.real(eig_vectors[:, :k])
    np.savetxt('./model/eigValues_real.txt', eigValues_real)
    np.savetxt('./model/eigVectors_real.txt', eigVectors_real)

    # save data of each class
    model_data = np.zeros((40, k))
    for i in range(40):
        for j in range(m):
            model_data[i][:] += np.dot(train_data[i * m + j][:].T, eigVectors_real).reshape((k))
        model_data[i][:] /= m
    np.savetxt('./model/model_data.txt', model_data)