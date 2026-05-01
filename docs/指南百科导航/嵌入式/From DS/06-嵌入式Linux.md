# 06 - 嵌入式 Linux

> 预计时间：3-4 个月  
> 目标：能够在一款 Linux 开发板上运行系统，编写应用层多进程/多线程程序，并初步了解驱动开发

## 1. Linux 基础

### 必需技能

- 文件系统与目录结构（/etc, /dev, /proc）
- 常用命令（ls, cd, cp, mv, grep, find, chmod, ps, top, netstat）
- 文本编辑器（vim/nano）
- Shell 脚本（变量、循环、条件判断）

### 📘 推荐书籍

- 《鸟哥的 Linux 私房菜》（基础篇）

## 2. Linux 应用编程

### 文件 I/O

- 标准 C 库函数（fopen, fread）与系统调用（open, read）
- 文件描述符、重定向

### 进程与线程

- fork, exec, wait, exit
- 线程创建（pthread_create）、同步（互斥锁、条件变量）

### 进程间通信（IPC）

- 管道（pipe, FIFO）
- 信号（signal）
- 共享内存 + 信号量
- 消息队列（System V）
- 套接字（socket）—— 见网络编程

### 网络编程

- TCP/UDP 客户端/服务器模型
- 阻塞与非阻塞、select/poll/epoll

### 🛠️ 实践项目

- 多线程文件拷贝器
- 简易 Web 服务器（返回静态页面）
- TCP 聊天室（多客户端 + 广播）

## 3. 嵌入式 Linux 系统构建

### 交叉编译工具链

- 在 PC 上为 ARM 平台编译程序（arm-linux-gnueabihf-gcc）
- 通过 NFS 或 scp 将程序传到开发板运行

### 系统构建工具

- **Buildroot**：快速生成根文件系统
- **Yocto**：功能强大但学习曲线陡峭，适合大规模项目

### 引导与内核

- U-Boot 编译与烧写
- 配置 Linux 内核（make menuconfig）
- 设备树（Device Tree）基础语法

### 推荐开发板

- 树莓派 3B/4B（资料极多，但非工业级）
- 野火/正点原子 i.MX6ULL 板（¥300-500，专为教学设计）
- LubanCat-Zero（RK3566，性价比高）

## 4. Linux 驱动开发入门

### 字符设备驱动

- 注册设备号、file_operations 结构体
- 实现 open, read, write, ioctl
- 测试驱动（insmod, rmmod, mknod）

### 设备树

- 在设备树中添加一个 GPIO LED 节点
- 驱动中获取设备树属性

### 常见驱动框架

- GPIO 驱动（gpiolib）
- 中断处理（request_irq，中断上下半部）
- 平台驱动（platform_driver）

### 📘 推荐书籍

- 《Linux 设备驱动开发》（第 2 版，John Madieu）
- 《ARM64 体系结构编程与实践》（安辉）

### 🎥 视频课程

- 百问网（韦东山）嵌入式 Linux 视频

> 完成本阶段，你已经具备全职嵌入式 Linux 工程师的基础能力。如果想深入某个方向，请阅读下一章。