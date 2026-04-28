# 博客编辑器迁移方案：Quasar Editor → md-editor-v3

## 背景

将项目现有的文章编辑器从 Quasar 自带的 `<q-editor>`（输出 HTML）迁移到第三方 Markdown 编辑器 `md-editor-v3`（输出 Markdown）。现有测试数据可直接删除，无需考虑数据迁移兼容性问题。

---

## 1. 依赖安装

在 `frontend/` 目录下安装 `md-editor-v3`：

```bash
cd frontend && npm install md-editor-v3
```

---

## 2. 全局样式注册

**文件：`frontend/src/main.ts`**

在入口文件引入编辑器全局样式：

```ts
import 'md-editor-v3/lib/style.css'
```

> 可选：如有需要，可在此处调用 `config()` 做全局配置（如自定义代码高亮 CDN、语言包覆盖等）。

---

## 3. 编辑器替换（核心）

**文件：`frontend/src/components/ArticleEditor.vue`**

当前使用的是 Quasar 的 `<q-editor>`，输出 **HTML**。

### 修改内容

- **导入组件**：
  ```ts
  import { MdEditor } from 'md-editor-v3'
  ```

- **替换组件**：将 `<q-editor v-model="conentRef" min-height="5rem" />` 替换为：
  ```vue
  <MdEditor
    v-model="conentRef"
    language="zh-CN"
    :toolbarsExclude="['mermaid', 'katex', 'github']"
    placeholder="开始写作..."
    style="height: 500px"
  />
  ```

- **调整默认值**：`conentRef` 的默认值从 `'文章正文'` 改为 Markdown 友好的初始文本，例如：
  ```ts
  const conentRef = ref<string>(
    props.articleToEdit?.content ?? '# 文章标题\n\n在这里开始写作...'
  )
  ```

- **图片上传处理**：当前后端没有图片上传接口。建议先设置 `noUploadImg` 属性禁用编辑器内置上传入口，用户仍可通过粘贴外链地址插入图片。后续如需本地上传，可再接入 `onUploadImg` 事件。

---

## 4. 文章详情页渲染改造

**文件：`frontend/src/components/ArticleCard.vue`**

当前直接用 `v-html` 渲染 HTML：

```vue
<div class="text-body1 text-grey-7" v-html="article.content!.replace(/\n/g, '<br>')" />
```

### 修改内容

- **导入组件**：
  ```ts
  import { MdPreview } from 'md-editor-v3'
  ```

- **替换渲染方式**：
  ```vue
  <MdPreview :modelValue="article.content || ''" language="zh-CN" />
  ```

- **移除原样式类**：`text-body1 text-grey-7` 可以保留或去掉，`MdPreview` 自带样式。如有暗黑模式需求，可同步绑定 `theme` 属性。

---

## 5. 文章列表页渲染改造

**文件：`frontend/src/components/ArticleList.vue`**

列表中同样使用了 `v-html` 渲染内容摘要（第 214 行附近）。

### 修改内容

- 替换为 `MdPreview`，但保留 `line-clamp-5` 的限制，避免列表中渲染过长：
  ```vue
  <MdPreview
    :modelValue="article.content || ''"
    language="zh-CN"
    class="line-clamp-5"
  />
  ```

- **性能考量**：列表每页约 10 篇文章，每篇实例化一个 `MdPreview`（包含代码高亮、Markdown 编译）在可接受范围内。若后期列表页卡顿，可改为**纯文本截取方案**（前端去除 Markdown 语法符号后截断显示）。

---

## 6. GPT 写作助手 Prompt 调整

**文件：`backend/blogapp/modules/gpt_writer/chatgpt_settings.yml`**

当前 Prompt 明确要求 GPT 使用 **HTML 标签**（`<b>`、`<i>`）格式化输出：

```yaml
prompt: "…文章内容必须使用以下 HTML 标签格式化：<b>、<i>…"
```

### 修改内容

将 Prompt 改为要求输出 **Markdown 格式**：

```yaml
prompt: "…文章内容请使用 Markdown 格式排版（如 **加粗**、*斜体*）。回复中只写文章内容，不要标题，也不要单独提及标签"
```

这样 GPT 生成的文章直接就是 Markdown，进入编辑器无需转换。

---

## 7. 后端模型与数据库

**无需改动。**

- `ArticleDocument` 和 `ArticleCreateOrUpdate` 中的 `content` 字段本来就是 `str | None`，数据库层面只是纯文本存储，HTML 和 Markdown 对它来说没有区别。
- 无需迁移或修改后端路由。

---

## 8. 现有数据清理

现有数据均为测试数据且可以删除。建议：

- 直接清空 MongoDB 的 `articles` 集合，避免旧的 HTML 内容在新编辑器里显示为一堆标签源码，影响体验。

---

## 修改文件清单

| 文件 | 修改类型 |
|---|---|
| `frontend/package.json` | 新增依赖 `md-editor-v3` |
| `frontend/src/main.ts` | 引入全局样式 |
| `frontend/src/components/ArticleEditor.vue` | 核心：替换 `<q-editor>` 为 `<MdEditor>` |
| `frontend/src/components/ArticleCard.vue` | 替换 `v-html` 为 `<MdPreview>` |
| `frontend/src/components/ArticleList.vue` | 替换 `v-html` 为 `<MdPreview>` |
| `backend/blogapp/modules/gpt_writer/chatgpt_settings.yml` | 修改 Prompt，要求 Markdown 输出 |

---

## 潜在注意点

1. **图片上传**：当前没有后端图片上传接口，建议先用 `noUploadImg` 禁用，后续按需扩展。
2. **工具栏精简**：通过 `toolbarsExclude` 去掉不常用的 `mermaid`、`katex`、`github`，保持界面简洁。
3. **主题同步**：如果 Quasar 项目支持暗黑模式，`MdEditor` / `MdPreview` 的 `theme` 属性需要和你的主题状态同步绑定。
4. **列表性能**：`ArticleList` 中大量使用 `MdPreview` 若出现性能问题，可改为纯文本摘要方案。

---

## 参考文档

- [md-editor-v3 API 文档](https://imzbf.github.io/md-editor-v3/zh-CN/api/)
