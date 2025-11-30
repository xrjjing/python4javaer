---
title: 09_Project 业务域与 RBAC 实战说明
---

> 本文基于 `rbac_auth_service` 项目，重点讲清：
> - 如何在已有 RBAC 体系下新增一个业务域（Project）；
> - 分层结构（Controller / Service / Repository / Model / Schema）之间如何协作；
> - 实际调用路径与可扩展思路。

## 1. 场景与目标

### 1.1 场景设定

假设我们在做一个「项目管理系统」的后端服务：

- 每个用户可以拥有自己的项目（Project）；
- 用户登录后，只能操作自己名下的项目；
- 不同用户的权限由角色与权限码控制（RBAC）：
  - 普通用户：可以查看、创建、修改自己的项目；
  - 管理员：拥有对所有项目资源的完整权限（示例中主要体现在权限分配上）。

在这个场景下，我们希望做到：

- 用 **和 Java 类似的分层结构** 实现一个完整业务域；
- 同时利用已有的 RBAC（角色/权限）体系做统一访问控制；
- 为后续扩展更多业务域（Task、Issue 等）打模板。

### 1.2 与 Java 思维的映射

| 概念           | 本项目中的对应位置                                   |
|----------------|------------------------------------------------------|
| Entity / Model | `app/models.py` 中的 `User / Role / Permission / Project` |
| DTO / VO       | `app/schemas.py` 中的 `ProjectCreate / ProjectUpdate / ProjectOut` |
| Repository/DAO | `app/repositories/project_repository.py`             |
| Service        | `app/services/project_service.py`                    |
| Controller     | `app/routers/projects.py`                            |
| Security       | `app/security.py` + `app/dependencies.py`            |

你可以把 `Project` 整条链路当成一个 **「Java 风格模块化 Web 服务」在 Python/FastAPI 下的落地版本**。

---

## 2. 模型设计：Project 与 User 的关系

文件：`app/models.py`

- `User` 模型中新增：
  - `projects: Mapped[list["Project"]]`  
    表示「一个用户拥有多个项目」的一对多关系。
- `Project` 模型字段：
  - `id`: 主键
  - `name`: 项目名称
  - `description`: 描述，可空
  - `status`: 字符串状态，默认 `"active"`（你可以约定 active/archived 等）
  - `owner_id`: 外键，指向 `users.id`
  - `created_at` / `updated_at`: 创建与更新时间
- 唯一约束：

```python
__table_args__ = (
    UniqueConstraint("owner_id", "name", name="uq_project_owner_name"),
)
```

含义：**同一个用户下面，项目名称不能重复**。  
这是非常典型的业务约束建模方式，建议你对照着在数据库中实际看看生成的表结构。

---

## 3. Schema 设计：请求与响应体

文件：`app/schemas.py`

### 3.1 基础结构

- `ProjectBase`：公共字段
  - `name`: 项目名称（带最小/最大长度校验）
  - `description`: 描述
- `ProjectCreate(ProjectBase)`：
  - 用于创建项目的请求体。
- `ProjectUpdate`：
  - 全部字段为可选：`name` / `description` / `status`
  - 适合 `PUT/PATCH` 场景的部分更新。
- `ProjectOut`：
  - 用于响应的完整数据结构：
    - `id/name/description/status/owner_id`
    - `created_at/updated_at`

在 Java 中你可能会写成 `ProjectCreateDTO / ProjectUpdateDTO / ProjectVO`，这里用 Pydantic 做了同样的拆分。

---

## 4. Repository 层：只关心持久化

文件：`app/repositories/project_repository.py`

职责非常单一：**对 Project 做数据库操作**，不关心 HTTP、不关心业务文案。

核心方法：

- `list_projects_by_owner(db, owner_id)`  
  查询某个用户的所有项目。
- `get_project_by_id_for_owner(db, project_id, owner_id)`  
  按 ID + owner_id 查询，天然保证「只能操作自己的资源」。
- `create_project_for_owner(db, owner_id, name, description)`  
  创建项目并提交事务。
- `save_project(db, project)`  
  用于更新后的持久化。
- `delete_project(db, project)`  
  删除项目。

你可以对照 `todo_repository.py` 理解：两者结构几乎相同，只是实体与字段不同。

---

## 5. Service 层：业务规则与异常语义

文件：`app/services/project_service.py`

这里是业务逻辑的核心位置，做三件事：

1. 调用 Repository 完成数据读写；
2. 处理业务规则（例如资源归属检查）；
3. 用异常表达业务语义（供上层路由转换为 HTTP 状态）。

主要方法：

- `list_projects_for_user(db, user)`  
  - 入参直接用 `User` 模型；
  - 内部调用 `list_projects_by_owner`。
- `create_project_for_user(db, user, project_in)`  
  - 强制以当前登录用户为 owner；
  - 不允许客户端指定 `owner_id`。
- `update_project_for_user(db, user, project_id, project_in)`：
  - 先用 `get_project_by_id_for_owner` 校验「是否存在且属于当前用户」；
  - 若失败 → 抛 `ValueError("Project 不存在或不属于当前用户")`；
  - 然后根据 `ProjectUpdate` 中实际传入的字段做更新；
  - 最后调用 `save_project`。
- `delete_project_for_user(db, user, project_id)`：
  - 同样先校验归属；
  - 不通过 → `ValueError`；
  - 通过 → 删除。

> 设计习惯：  
> - **Service 层不直接知道 HTTP 状态码**，而是用异常来表达“业务事件”；  
> - 上层 Router 再决定这个异常对应 400/404/403 之类。

---

## 6. Router 层：HTTP 协议与 RBAC 权限

文件：`app/routers/projects.py`

### 6.1 依赖与前缀

- `router = APIRouter(prefix="/projects", tags=["projects"])`
- 依赖注入：
  - `get_db`: 提供数据库会话；
  - `get_current_active_user`: 获取当前登录且激活的用户；
  - `require_permissions`: 基于权限码做访问控制。

### 6.2 具体接口

1. **GET `/projects/`**
   - 依赖：`Depends(require_permissions("projects:read"))`
   - 功能：列出当前用户的所有项目。
   - 返回：`APIResponse[List[ProjectOut]]`

2. **POST `/projects/`**
   - 依赖：`projects:write`
   - 请求体：`ProjectCreate`
   - 状态码：`201 CREATED`
   - 功能：为当前用户创建一个项目。

3. **PUT `/projects/{project_id}`**
   - 依赖：`projects:write`
   - 请求体：`ProjectUpdate`
   - 逻辑：
     - 调用 `update_project_for_user`；
     - 捕获 `ValueError` → 返回 `404 Not Found`；
   - 返回：`APIResponse[ProjectOut]`

4. **DELETE `/projects/{project_id}`**
   - 依赖：`projects:delete`
   - 逻辑：
     - 调用 `delete_project_for_user`；
     - 捕获 `ValueError` → 返回 `404 Not Found`；
   - 成功：`204 No Content`，无 body。

通过这种写法，**Router 层只做 3 件事**：

- 把 HTTP 请求解析成 Python 对象（query/path/body）；
- 调用 Service；
- 做异常到 HTTP 的映射（配合统一响应模型）。

---

## 7. RBAC 权限：如何挂上去的？

### 7.1 权限码设计

在 `init_rbac_data.py` 中，Project 相关权限为：

- `projects:read`   —— 查看项目列表；
- `projects:write`  —— 创建与更新项目；
- `projects:delete` —— 删除项目。

角色分配：

- `admin` 角色：拥有所有 `todos:*` + `projects:*` + `tasks:*` 权限；
- `user`  角色：拥有 `todos:read/write` + `projects:read/write` + `tasks:read/write`。

### 7.2 权限检查入口

文件：`app/dependencies.py`

- `require_permissions(*perm_codes: str)` 返回一个依赖函数：
  - 从当前用户的角色集合中收集所有权限码；
  - 若用户是超级管理员，直接放行；
  - 否则检查是否包含任意一个 `perm_codes`；
  - 不满足时抛出 `HTTPException(403)`。

因此在 Router 中写：

```python
@router.get(
    "/",
    dependencies=[Depends(require_permissions("projects:read"))],
)
```

就相当于在 Java 里写：

```java
@PreAuthorize(\"hasAuthority('projects:read')\")
public List<Project> listProjects(...) { ... }
```

---

## 8. 测试：如何验证这条链路？

文件：`test_rbac_api.py`

- `init_rbac_data`：
  - 在测试数据库中创建 `projects:*` 权限；
  - 分配给 `admin/user` 角色，与生产初始化逻辑保持一致。
- `test_user_project_rbac` 测试用例：
  1. 使用普通用户 `alice` 登录获取 Token；
  2. `POST /projects/` 创建一个项目；
  3. `GET /projects/` 确认能看到刚创建的项目；
  4. `PUT /projects/{id}` 更新描述并验证返回结果。

> 建议练习：  
> - 自己再写一个测试：没有 `projects:delete` 权限的用户尝试删除项目，应该返回 403；  
> - 或者尝试让用户访问别人的项目 ID，看看是否会返回 404。

---

## 9. Project + Task 组合建模小结

现在仓库中已经按上面步骤真实实现了一条 Project + Task 组合链路：

- ORM 模型：`Project` 一对多 `Task`，通过 `project_id` 关联；
- 路由结构：`/projects` 管理项目，`/projects/{project_id}/tasks` 管理子资源；
- 权限设计：
  - `projects:*` 控制项目级操作；
  - `tasks:*` 控制任务级操作（示例中普通用户拥有 read/write，delete 仅给管理员）；
- 测试：`test_rbac_api.py` 中的 `test_user_project_rbac` + `test_user_task_rbac` 一起覆盖了 Project + Task 的典型访问路径。

这条链路可以作为「真实业务建模」的练习样板：你可以把 Project 想成“项目/订单/工单”，把 Task 想成“子任务/明细项”，再尝试根据自己的业务做字段和关系的调整。

---

## 10. 作为模板如何复用？

当你需要为这个 RBAC 服务再增加一个业务域（例如 Task）时，可以直接按如下步骤套用模板：

1. 在 `models.py` 中新增 `Task` 模型，并与 `User` 建立关系；
2. 在 `schemas.py` 中新增 `TaskCreate / TaskUpdate / TaskOut`；
3. 新建 `app/repositories/task_repository.py`，仿照 Project 写 CRUD；
4. 新建 `app/services/task_service.py`，处理归属与业务规则；
5. 新建 `app/routers/tasks.py`，绑定路由与权限码；
6. 在 `init_rbac_data.py` 中增加 `tasks:*` 权限，并分配到角色；
7. 写一个 `test_task_rbac` 集成测试。

**只要这条链路你能自己独立敲出来，就说明你已经完成了从「会写 FastAPI Demo」到「能搭出结构化 Web 服务」的跨越。**
