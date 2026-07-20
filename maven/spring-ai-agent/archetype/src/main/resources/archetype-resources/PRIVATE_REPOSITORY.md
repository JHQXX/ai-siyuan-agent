# 🏠 私有 Maven 仓库（jhqxx）使用指南

本项目已**预配置**了 JHQXX 私有 Nexus 仓库，仓库 ID 为 `jhqxx`。
地址：`https://nexus.azhi-home.top/repository/my-private-maven/`

⚠️ **重要**：Nexus 已禁用匿名访问（Disable anonymous access），
所有操作（拉包、上传）都需要账号密码认证。

---

## 📋 一次性配置：Maven 认证

编辑 `~/.m2/settings.xml`，添加：

```xml
<servers>
    <server>
        <id>jhqxx</id>
        <username>admin</username>
        <password>你的Nexus密码</password>
    </server>
</servers>
```

⚠️ `<id>jhqxx</id>` 必须跟 pom.xml 里的 `<repository><id>` 一致！

---

## 📥 场景 1：拉取私有包（作为依赖）

**取消注释** pom.xml 里 `<repositories>` 中的内容：

```xml
<repositories>
    <repository>
        <id>jhqxx</id>
        <name>JHQXX Private Nexus</name>
        <url>https://nexus.azhi-home.top/repository/my-private-maven/</url>
        <releases>
            <enabled>true</enabled>
        </releases>
        <snapshots>
            <enabled>false</enabled>
        </snapshots>
    </repository>
</repositories>
```

然后像使用普通依赖一样：

```xml
<dependencies>
    <dependency>
        <groupId>com.lizhi</groupId>
        <artifactId>my-private-lib</artifactId>
        <version>1.0.0</version>
    </dependency>
</dependencies>
```

Maven 会自动用 `admin/你的密码` 去 `jhqxx` 仓库拉包。

---

## 📤 场景 2：发布包到 Nexus

**取消注释** pom.xml 里 `<distributionManagement>` 中的内容：

```xml
<distributionManagement>
    <repository>
        <id>jhqxx</id>
        <name>JHQXX Private Nexus</name>
        <url>https://nexus.azhi-home.top/repository/my-private-maven/</url>
    </repository>
</distributionManagement>
```

然后执行：

```bash
mvn clean deploy
```

会自动推送到你的 Nexus。

---

## 🔧 IDEA 中配置

**Windows / macOS / Linux 都一样**：

1. **File** → **Settings** → **Build, Execution, Deployment** → **Maven**
2. 点 **"Override"** 旁边的 User settings file
3. 选择你的 `~/.m2/settings.xml`
4. 保存

之后 IDEA 会用 settings.xml 里的认证信息。

---

## 🧪 测试认证是否生效

### 测试 1：拉一个包
```bash
mvn dependency:get \
  -Dartifact=com.lizhi:my-private-lib:1.0.0 \
  -DremoteRepositories=jhqxx::default::https://nexus.azhi-home.top/repository/my-private-maven/
```

成功 = 看到 `BUILD SUCCESS`
失败 = 看到 401 Unauthorized → 检查密码

### 测试 2：发布包
```bash
mvn deploy
```

应该上传到 `https://nexus.azhi-home.top/repository/my-private-maven/`

---

## ❓ 故障排查

### Q: 报 401 Unauthorized

```
[ERROR] Failed to read artifact descriptor... 401 Unauthorized
```

**解决**：
1. 检查 `~/.m2/settings.xml` 里 `<server><id>` 跟 pom.xml 里 `<repository><id>` 是否一致
2. 检查密码是否正确
3. 试试直接在浏览器访问 URL，看能不能打开

### Q: 报 Could not resolve dependencies

```
[ERROR] Could not resolve dependencies for project... Could not find artifact...
```

**可能原因**：
1. 仓库 URL 写错了
2. 仓库名字不对（你 Nexus 里叫 `my-private-maven` 还是其他？）

**解决**：
1. 打开 Nexus：`https://nexus.azhi-home.top`
2. 齿轮 → **Repositories** 看真实仓库名
3. 同步更新 pom.xml 里的 URL

### Q: 如何完全禁用 Nexus 配置？

不需要 Nexus 时，把 pom.xml 里 `<repositories>` 和 `<distributionManagement>` 的注释加上即可。

---

## 🆚 跟 Maven Central 的关系

| 仓库 | 用途 | 用法 |
|------|------|------|
| Maven Central | 公共包（Spring、Apache 等） | 默认就支持，无需配置 |
| **jhqxx** (Nexus) | 你的私有包 | 需要手动取消注释启用 |

两者**互不影响**：
- 默认只走 Maven Central
- 启用 jhqxx 后，私有包从 Nexus 拉，公共包还是从 Maven Central 拉

---

## 📚 部署你自己的 Nexus？

参考父仓库的 [nexus/](https://github.com/JHQXX/all-package/tree/main/nexus) 目录，里面有完整的 `docker-compose.yml`，一键启动。