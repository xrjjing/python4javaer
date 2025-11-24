# 10_EAFP_异常优先的编码风格

## 技巧说明

- EAFP：Easier to Ask Forgiveness than Permission；
- 与其写大量「条件判断」，不如直接尝试执行，再通过异常处理错误；
- 特别适合文件操作、字典访问、网络请求等场景。

---

## 示例 demo（见 `demo_eafp.py`）

示例对比：

- LBYL（Look Before You Leap）风格：先 `if` 判断；
- EAFP 风格：直接访问，捕获 `KeyError` / `FileNotFoundError` 等。

---

## 练习建议

1. 在文件相关逻辑里，尝试用 `try/except FileNotFoundError` 替代 `os.path.exists` + `if`；  
2. 在字典访问中，尝试用 `try/except KeyError` 或 `get` 代替多重判断；  
3. 在调用外部接口时，结合异常封装统一错误处理逻辑（例如 `JavaServiceError`）。

