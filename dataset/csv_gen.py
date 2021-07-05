import csv
import os

def create_csv(path):
    count = 0
    with open(os.path.join(os.getcwd(), 'dataset.csv'), 'w') as f:
        writer = csv.writer(f)
        writer.writerow(('label', 'image'))
        for root, _, filenames in os.walk(path):
            label = root.split('\\')[-1]
            for filename in filenames:
                img_path = os.path.join(root, filename)
                writer.writerow((label, img_path))
                count+= 1
                print(f'progress: {count} element')

if __name__ == '__main__':
    create_csv(os.path.abspath('result'))
