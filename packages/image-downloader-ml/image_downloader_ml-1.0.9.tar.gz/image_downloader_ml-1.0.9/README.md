# Image Downloader

---
> 使用搜索引擎通过关键字下载相关图片，适用于深度学习、机器学习等数据集收集场景。

[中文介绍](https://github.com/2635064692/image-downloader/blob/main/README.md)

[English Introduction](https://github.com/2635064692/image-downloader/blob/main/README-en.md)

## 功能介绍
- 本工具支持多种搜索引擎的图片搜索，包括 Google、Bing、Baidu 等（详见支持计划）。
- 支持google搜索原始站点的清晰图片下载，能够用于机器学习、深度学习等领域数据集搜集的应用。
- 通过检索出的图片获取原站点链接，对原站点内的图片进行下载。
- 本工具类似google-images-download功能，但更为实用
- 支持 [java](https://github.com/2635064692/Image-Downloader-java) 版本
- 支持 [python](https://github.com/2635064692/image-downloader) 版本
## 使用方式
- 安装依赖
   ```shell
    pip install image-downloader-ml
   ```
- 使用方式
   ```shell
    image-downloader-ml -l 20 -o "./output"  -k "Broken traffic guardrail"  -plt 5  -kf "./sample_config.json"
   ```

## 支持计划

- [ √ ] Google 图片搜索
- [ √ ] Bing 图片搜索
- [ √ ] Baidu 图片搜索


## 免责声明

该程序可让你从搜索引擎上下载大量图片。请不要下载或使用任何违反版权条款的图片。谷歌图片是一个搜索引擎，它只是为图片编制索引，并允许你查找图片。它并不制作自己的图片，因此也不拥有任何图片的版权。图片的原创者拥有版权。

在相关地区、国家出版的图片，即使没有明确的版权警告，也自动受到其所有者的版权保护。除非在 "合理使用 "的情况下，否则未经所有者许可，您不得复制受版权保护的图片，否则您可能面临律师警告、停止侵权信和版权诉讼的风险。请谨慎使用！本脚本/代码仅用于教育目的。
