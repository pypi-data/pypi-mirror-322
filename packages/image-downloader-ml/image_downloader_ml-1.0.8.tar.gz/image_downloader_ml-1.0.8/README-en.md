# Image Downloader

---
> Download related images through search engines using keywords, suitable for dataset collection in deep learning, machine learning, and similar scenarios.


[中文介绍](https://github.com/2635064692/image-downloader/blob/main/README.md)

[English Introduction](https://github.com/2635064692/image-downloader/blob/main/README-en.md)
## Introduction
- This tool supports image search on multiple search engines, including Google, Bing, Baidu, etc. (see the support roadmap for details).
- Supports downloading high-quality images directly from Google’s original site, which can be applied to dataset collection for fields like machine learning and deep learning.
- Retrieves original website links for the searched images and downloads images from the original sites.
- Similar to the functionality of `google-images-download`, but more practical and enhanced.
- Supports [java version](https://github.com/2635064692/Image-Downloader-java) 
- Supports [python version](https://github.com/2635064692/image-downloader)
## Usage
- Install dependencies
   ```shell
    pip install image-downloader-ml
   ```
- Usage example
   ```shell
    image-downloader-ml -l 20 -o "./output"  -k "Broken traffic guardrail"  -plt 5  -kf "./sample_config.json"
   ```

## Support Plan

- [ √ ] Google Image Search
- [ √ ] Bing Image Search
- [ √ ] Baidu Image Search


## Disclaimer

This program allows you to download a large number of images from search engines. Please do not download or use any images that violate copyright laws. Google Images is a search engine that indexes images and allows you to locate them. It does not create its own images and therefore does not own any copyrights. The original creators of the images hold the copyright.

In regions and countries where images are published, the images are automatically protected by copyright laws, even if there is no explicit copyright notice. Unless under "fair use" exceptions, you may not copy copyrighted images without the owner's permission, or you may face legal consequences such as warnings, cease-and-desist letters, or copyright lawsuits. Please use with caution! This script/code is intended for educational purposes only.