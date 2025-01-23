from setuptools import setup, find_packages

# Đảm bảo tệp README.md được mở đúng cách
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vietnamese_conceptizer",  # Tên package, cần duy nhất trên PyPI
    version="0.1.2",  # Phiên bản
    author="Bui Van Tan; Luong Duc Thang",  # Tác giả
    author_email="luongducthang289@gmail.com",  # Email tác giả
    description="A tool for processing text files and normalizing data using a dictionary",
    long_description=long_description,  # Nội dung mô tả dài từ README.md
    long_description_content_type="text/markdown",  # Định dạng của README.md
    url="https://github.com/luongducthangDS/vietnamese_conceptizer",  # URL repo
    packages=find_packages(),  # Tìm và liệt kê các package
    package_data={ 
        "vietnamese_conceptizer": ["data/WORDS_WordNet_And_VCL_ALL_sorted.txt"],  # Các file dữ liệu bổ sung
    },
    include_package_data=True,  # Bao gồm file từ package_data
    classifiers=[
        "Programming Language :: Python :: 3",  # Ngôn ngữ hỗ trợ
        "License :: OSI Approved :: MIT License",  # Loại giấy phép
        "Operating System :: OS Independent",  # Hệ điều hành
    ],
    python_requires=">=3.7",  # Yêu cầu phiên bản Python
    install_requires=[ 
        "pandas",  # Các thư viện phụ thuộc
    ],
    license="MIT",  # Loại giấy phép
)
