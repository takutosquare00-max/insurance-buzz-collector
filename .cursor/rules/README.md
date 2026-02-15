# Cursor ルール

このフォルダにはプロジェクト用の Cursor AI ルール（`.mdc` ファイル）を配置します。

## 使い方

- **常時適用**: `alwaysApply: true` を frontmatter に設定
- **ファイルパターン**: `globs: ["**/*.py"]` で特定ファイルに適用
- **手動参照**: `@rule-name` でチャット時に参照

## 例

```yaml
---
description: タイ保険プロジェクトのコーディング規約
globs: ["**/*.py"]
---
# Python コーディング規約
- 日本語でコメントを記述
- type hint を使用する
```
