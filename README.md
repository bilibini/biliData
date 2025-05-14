
# 基于数据挖掘的 B 站博主数据预测平台

> 旨在构建一个基于数据挖掘的 B 站UP主数据预测平台。项目由四个主要模块组成：API 后端服务（PHP）、数据爬取模块（Python）、播放量预测模型（Python）和前端展示页面（Vue）。该项目可用于分析 B 站UP主及视频数据，并对未来播放量进行预测。

## 📁 项目结构概览

```
├── LICENSE
├── README.md
├── api.txt
├── biliApiPHP/            # API后端服务 (PHP)
├── biliPredict/           # 播放量预测模型 (Python)
├── biliSpiders/           # 数据爬虫模块 (Python)
└── biliWeb/               # 前端展示界面 (Vue)
```

---

## 🛠 技术栈

| 模块         | 技术/语言        |
|--------------|------------------|
| 后端 API     | PHP + MySQL      |
| 数据爬虫     | Python + Requests |
| 预测模型     | Python + Scikit-learn / TensorFlow |
| 前端展示     | Vue.js + Vite    |

---

## 🧩 功能模块说明

### 1. `biliApiPHP` - API 接口服务（PHP）

- 提供用户登录注册接口
- 支持获取用户信息、UP 主信息、视频数据等
- 包含数据库连接配置、任务管理、代理 IP 管理等功能
- 支持通过 Nginx/Apache 部署

### 2. `biliSpiders` - 数据爬虫模块（Python）

- 实现对 B 站用户、UP 主、视频等数据的采集
- 支持分类 ID 映射表
- 使用代理 IP 池防止封禁
- 提供上传器模块将数据存入数据库

### 3. `biliPredict` - 视频播放量预测（Python）

- 利用历史数据训练预测模型
- 可预测未来一段时间内的视频播放量
- 支持多种机器学习算法（如线性回归、随机森林等）
- 提供配置文件和依赖管理

### 4. `biliWeb` - 前端展示页面（Vue）

- 基于 Vue 3 + Vite 构建
- 包括登录、注册、首页、UP 主列表、视频详情页等
- 使用 Vue Router 和 Vuex 进行状态管理
- 提供 Admin 管理后台页面

---

## 🎬 功能展示

以下是一个功能演示的 GIF 动图：

![功能演示](./biliData_dome.gif)


---

## 💭 碎言碎语

本项目是我在2023年的本科毕业设计，原本打算在毕业后开源毕设，但完成毕设后一直在工作与毕业的事务中繁忙，在其途中电脑也坏掉了  
但最近我的导师找我要曾经的毕业论文（因：母校在收集近几年的优秀作品）  
于是我又翻出了我坏了快2年的电脑(是的，还没扔，打算找时间修好的，结果一直没时间...)拆出其硬盘用转接器链接到现在的电脑中  
因此该毕设得以重见天日，故现在将其开源  
其实当时写的也不是很好，现在回头看很多地方写的不够成熟，不过毕竟那么多日夜赶出来的，感兴趣的同学可以看看：）  

注：代码完成于2023年初，肯定有些API已经用不了了，需要更改一些API与设置。

---

## 🙏 感谢

特别感谢 [SocialSisterYi/bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect) 项目，它为B站API提供了详尽的收集和整理，这对本项目的开发提供了极大的帮助和支持。如果你对B站API有兴趣或需要进一步了解，强烈推荐参考这个优秀的开源项目。

---

## 🚀 快速部署指南

### 1. 克隆项目

```bash
git clone https://github.com/bilibini/biliData.git
cd biliData
```

### 2. 安装依赖

#### 前端（biliWeb）

```bash
cd biliWeb
npm install
```

#### 后端 API（biliApiPHP）

- 需要部署到支持 PHP 的服务器上（如 Apache/Nginx）
- 修改 `mydb/config.php` 中的数据库连接信息

#### 爬虫（biliSpiders）

```bash
cd biliSpiders
pip install -r requirements.txt
```

#### 预测模型（biliPredict）

```bash
cd biliPredict
pip install -r requirements.txt
```

### 3. 数据库准备

- 创建 MySQL 数据库并导入相关表结构
- 修改 `mydb.py` 或 `config.php` 中的数据库配置

### 4. 运行项目

#### 启动前端

```bash
cd biliWeb
npm run dev
```

#### 启动后端 API

- 部署在 PHP 服务器中即可访问接口

#### 启动爬虫

```bash
cd biliSpiders
python main.py
```

#### 启动预测模型

```bash
cd biliPredict
python main.py
```

---



## 📌 使用建议

- 若你希望部署完整平台，请确保服务器环境已安装 PHP、MySQL、Python 和 Node.js。
- 爬虫部分需要遵守 B 站的 Robots 协议，合理控制请求频率。
- 预测模型可根据实际需求更换为深度学习模型以提升准确率。

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=bilibini/biliData&type=Date)](https://www.star-history.com/#bilibini/biliData&Date)

---

## 🤝 贡献与反馈

欢迎提交 PR、Issue 或 Star 本项目！

- 如果你发现了 Bug，请提交 Issue 描述问题。
- 如果你想改进代码或添加新功能，请 Fork 项目并提交 Pull Request。
- 项目持续优化中，欢迎提出宝贵意见。

---

## 📄 License

本项目采用 [Apache-2.0 license](LICENSE)，你可以自由使用、修改和分发。

---

> 作者：bilibini  
> GitHub 项目地址：[https://github.com/bilibini/biliData](https://github.com/bilibini/biliData)

