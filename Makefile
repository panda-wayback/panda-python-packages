.PHONY: help install install-dev test test-cov clean build lint format check all release

# 默认目标：显示帮助信息
help:
	@echo "📦 Panda Python Packages - 可用命令:"
	@echo ""
	@echo "  make install       - 安装包（开发模式）"
	@echo "  make install-dev   - 安装开发依赖（包括测试工具）"
	@echo "  make test          - 运行所有测试"
	@echo "  make test-cov      - 运行测试并生成覆盖率报告"
	@echo "  make test-html     - 运行测试并生成 HTML 覆盖率报告"
	@echo "  make build         - 构建分发包（wheel）"
	@echo "  make clean         - 清理临时文件和构建产物"
	@echo "  make lint          - 代码检查（如果配置了）"
	@echo "  make format        - 代码格式化（如果配置了）"
	@echo "  make check         - 运行所有检查（测试 + lint）"
	@echo "  make all           - 运行完整检查流程（测试 + 构建）"
	@echo "  make release       - 打 tag 并发布正式版本到 PyPI"
	@echo ""

# 安装包（开发模式）
install:
	@echo "📥 安装包（开发模式）..."
	pip install -e .

# 安装开发依赖（包括测试工具）
install-dev:
	@echo "📥 安装开发依赖..."
	pip install -e ".[test]"
	@echo "✅ 开发环境设置完成！"

# 运行所有测试
test:
	@echo "🧪 运行测试..."
	pytest

# 运行测试并显示覆盖率
test-cov:
	@echo "🧪 运行测试并生成覆盖率报告..."
	pytest --cov=src/panda_python_packages --cov-report=term-missing

# 运行测试并生成 HTML 覆盖率报告
test-html:
	@echo "🧪 运行测试并生成 HTML 覆盖率报告..."
	pytest --cov=src/panda_python_packages --cov-report=html
	@echo "✅ 覆盖率报告已生成: htmlcov/index.html"

# 构建分发包
build:
	@echo "🔨 构建分发包..."
	rm -rf dist/ build/ *.egg-info
	hatch build
	@echo "✅ 构建完成！文件在 dist/ 目录"

# 清理临时文件和构建产物
clean:
	@echo "🧹 清理临时文件..."
	find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	rm -rf dist/ build/ .pytest_cache/ .coverage htmlcov/ .mypy_cache/ .ruff_cache/
	@echo "✅ 清理完成！"

# 代码检查（如果安装了 ruff 或 flake8）
lint:
	@echo "🔍 代码检查..."
	@if command -v ruff > /dev/null; then \
		echo "使用 ruff 检查代码..."; \
		ruff check src/ tests/; \
	elif command -v flake8 > /dev/null; then \
		echo "使用 flake8 检查代码..."; \
		flake8 src/ tests/; \
	else \
		echo "⚠️  未安装代码检查工具（ruff 或 flake8）"; \
		echo "   安装 ruff: pip install ruff"; \
		echo "   或安装 flake8: pip install flake8"; \
	fi

# 代码格式化（如果安装了 ruff 或 black）
format:
	@echo "✨ 格式化代码..."
	@if command -v ruff > /dev/null; then \
		echo "使用 ruff 格式化代码..."; \
		ruff format src/ tests/; \
	elif command -v black > /dev/null; then \
		echo "使用 black 格式化代码..."; \
		black src/ tests/; \
	else \
		echo "⚠️  未安装代码格式化工具（ruff 或 black）"; \
		echo "   安装 ruff: pip install ruff"; \
		echo "   或安装 black: pip install black"; \
	fi

# 运行所有检查（测试 + lint）
check: test lint
	@echo "✅ 所有检查完成！"

# 完整流程：测试 + 构建
all: clean test build
	@echo "✅ 完整流程执行完成！"

# 打 tag 并发布正式版本
# 使用方法: make release 或 make release TAG=v1.0.0
release:
	@if [ -z "$(TAG)" ]; then \
		VERSION=$$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/'); \
		TAG="v$$VERSION"; \
	else \
		TAG="$(TAG)"; \
	fi; \
	echo "🚀 准备发布正式版本..."; \
	echo "📌 将创建 tag: $$TAG"; \
	echo ""; \
	echo "🏷️  创建 tag: $$TAG"; \
	git tag -a "$$TAG" -m "Release $$TAG" || exit 1; \
	echo "📤 推送 tag 到远程仓库..."; \
	git push origin "$$TAG" || (echo "❌ 推送失败，请检查远程仓库配置" && exit 1); \
	echo ""; \
	echo "✅ Tag $$TAG 已创建并推送"; \
	echo "🔄 GitHub Actions 将自动触发，发布到正式 PyPI"
