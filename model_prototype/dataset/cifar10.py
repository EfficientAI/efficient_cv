
import torch
from torchvision import datasets
import torchvision.transforms as transforms
from torch.utils.data import Dataset

is_cuda = torch.cuda.is_available()
device = torch.device("cuda" if is_cuda else "cpu")


class dataset(Dataset):
    def __init__(self, data_path, split='train'):
        transform = transforms.Compose(
            [transforms.ToTensor(),
             transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
        )
        train = True if split == 'train' else False
        self.dataset = datasets.CIFAR10(root=data_path,
                                        train=train, download=True,
                                        transform=transform)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        img, label = self.dataset[idx]
        img = img.to(device)
        return img, label

    def __len__(self):
        return len(self.dataset)

################################## Test ########################################


def test():
    d = dataset()
    print(len(d))
    img1, label1 = d[0]
    print(img1.size(), label1)
    img2, label2 = d[1]
    print(img2.size(), label2)


if __name__ == "__main__":
    test()
