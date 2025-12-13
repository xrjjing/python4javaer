/* 工具箱（M6）通用算法工具：文本对比（行级 Myers Diff）+ JSON 格式化
 *
 * 设计目标：
 * - 纯算法、无 DOM 依赖，便于浏览器与 Node 环境复用与单元测试
 * - 默认按“行”对比，适合 Text/JSON 等常见场景
 */
(function (root, factory) {
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = factory();
    } else {
        root.DogToolboxM6Utils = factory();
    }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
    'use strict';

    function splitLines(text) {
        return String(text ?? '').split(/\r?\n/);
    }

    // Myers Diff（基于行数组），输出 op 列表：equal/insert/delete
    function myersDiff(a, b) {
        const A = Array.isArray(a) ? a : [];
        const B = Array.isArray(b) ? b : [];
        const N = A.length;
        const M = B.length;
        const max = N + M;
        const offset = max;

        let v = new Array(2 * max + 1).fill(0);
        const trace = [];

        for (let d = 0; d <= max; d++) {
            const v2 = v.slice();
            for (let k = -d; k <= d; k += 2) {
                let x;
                const idxK = offset + k;
                if (k === -d || (k !== d && v[offset + k - 1] < v[offset + k + 1])) {
                    x = v[offset + k + 1];
                } else {
                    x = v[offset + k - 1] + 1;
                }
                let y = x - k;
                while (x < N && y < M && A[x] === B[y]) {
                    x++;
                    y++;
                }
                v2[idxK] = x;
                if (x >= N && y >= M) {
                    trace.push(v2);
                    return backtrack(trace, A, B, offset);
                }
            }
            trace.push(v2);
            v = v2;
        }
        return backtrack(trace, A, B, offset);
    }

    function backtrack(trace, A, B, offset) {
        let x = A.length;
        let y = B.length;
        const ops = [];

        for (let d = trace.length - 1; d > 0; d--) {
            const vPrev = trace[d - 1];
            const k = x - y;
            let prevK;
            if (k === -d || (k !== d && vPrev[offset + k - 1] < vPrev[offset + k + 1])) {
                prevK = k + 1;
            } else {
                prevK = k - 1;
            }
            const prevX = vPrev[offset + prevK];
            const prevY = prevX - prevK;

            while (x > prevX && y > prevY) {
                ops.push({ type: 'equal', value: A[x - 1] });
                x--;
                y--;
            }

            if (x === prevX) {
                ops.push({ type: 'insert', value: B[y - 1] });
                y--;
            } else {
                ops.push({ type: 'delete', value: A[x - 1] });
                x--;
            }
        }

        while (x > 0 && y > 0) {
            ops.push({ type: 'equal', value: A[x - 1] });
            x--;
            y--;
        }
        while (x > 0) {
            ops.push({ type: 'delete', value: A[x - 1] });
            x--;
        }
        while (y > 0) {
            ops.push({ type: 'insert', value: B[y - 1] });
            y--;
        }

        return ops.reverse();
    }

    // 将 op 列表转换为“左右对齐”的行列表：null 表示该侧无该行
    function opsToSideBySideRows(ops) {
        const rows = [];
        let dels = [];
        let ins = [];

        function flush() {
            const max = Math.max(dels.length, ins.length);
            for (let i = 0; i < max; i++) {
                const left = i < dels.length ? dels[i] : null;
                const right = i < ins.length ? ins[i] : null;
                let type = 'equal';
                if (left !== null && right !== null) type = 'change';
                else if (left !== null) type = 'delete';
                else if (right !== null) type = 'insert';
                rows.push({ left, right, type });
            }
            dels = [];
            ins = [];
        }

        for (const op of ops || []) {
            if (op.type === 'equal') {
                flush();
                rows.push({ left: op.value, right: op.value, type: 'equal' });
            } else if (op.type === 'delete') {
                dels.push(op.value);
            } else if (op.type === 'insert') {
                ins.push(op.value);
            }
        }
        flush();
        return rows;
    }

    function buildSideBySideDiff(leftText, rightText) {
        const leftLines = splitLines(leftText);
        const rightLines = splitLines(rightText);
        const ops = myersDiff(leftLines, rightLines);
        const rows = opsToSideBySideRows(ops);

        let leftNo = 0;
        let rightNo = 0;
        const numbered = rows.map(r => {
            const ln = r.left !== null ? (++leftNo) : null;
            const rn = r.right !== null ? (++rightNo) : null;
            return { ...r, leftNo: ln, rightNo: rn };
        });
        return { rows: numbered };
    }

    function formatJson(text) {
        const raw = String(text ?? '').trim();
        if (!raw) return '';
        const obj = JSON.parse(raw);
        return JSON.stringify(obj, null, 2);
    }

    return {
        splitLines,
        myersDiff,
        buildSideBySideDiff,
        formatJson
    };
});

