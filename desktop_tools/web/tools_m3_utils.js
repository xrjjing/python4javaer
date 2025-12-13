/* 工具箱（M3）通用算法工具：JWT 解码 / 时间戳转换（UTC / UTC+8）
 *
 * 设计目标：
 * - 纯算法、无 DOM 依赖，便于浏览器与 Node 环境复用与单元测试
 * - 避免依赖本机时区：格式化统一使用 UTC getter + 手动偏移
 */
(function (root, factory) {
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = factory();
    } else {
        root.DogToolboxM3Utils = factory();
    }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
    'use strict';

    function isNodeEnv() {
        return typeof process !== 'undefined' && process.versions && process.versions.node;
    }

    function bytesToUtf8(bytes) {
        const u8 = bytes instanceof Uint8Array ? bytes : Uint8Array.from(bytes || []);
        if (typeof TextDecoder !== 'undefined') {
            return new TextDecoder('utf-8', { fatal: true }).decode(u8);
        }
        if (isNodeEnv()) {
            return Buffer.from(u8).toString('utf8');
        }
        let s = '';
        for (let i = 0; i < u8.length; i++) s += String.fromCharCode(u8[i]);
        return s;
    }

    function base64UrlToBytes(input) {
        const raw = String(input ?? '').trim();
        if (!raw) return new Uint8Array(0);

        // base64url -> base64
        let b64 = raw.replace(/-/g, '+').replace(/_/g, '/');
        // 去掉空白
        b64 = b64.replace(/\s+/g, '');
        // padding
        const mod = b64.length % 4;
        if (mod === 1) {
            throw new Error('非法 base64url：长度不合法');
        }
        if (mod === 2) b64 += '==';
        else if (mod === 3) b64 += '=';

        // 字符集校验（标准 base64）
        if (!/^[A-Za-z0-9+/=]+$/.test(b64)) {
            throw new Error('非法 base64url：包含不支持的字符');
        }

        if (typeof atob === 'function') {
            const binary = atob(b64);
            const bytes = new Uint8Array(binary.length);
            for (let i = 0; i < binary.length; i++) {
                bytes[i] = binary.charCodeAt(i) & 0xff;
            }
            return bytes;
        }
        if (isNodeEnv()) {
            return Uint8Array.from(Buffer.from(b64, 'base64'));
        }
        throw new Error('当前环境不支持 base64url 解码');
    }

    function base64UrlDecodeToJsonText(segment) {
        const text = bytesToUtf8(base64UrlToBytes(segment));
        // 只要不是合法 JSON 就报错，保持“输出 JSON”的约束
        const obj = JSON.parse(text);
        return JSON.stringify(obj, null, 2);
    }

    function normalizeJwtInput(input) {
        let raw = String(input ?? '').trim();
        if (!raw) return '';
        // 支持 Bearer token
        raw = raw.replace(/^Bearer\s+/i, '').trim();
        return raw;
    }

    function decodeJwt(input, inputType = 'auto') {
        const raw = normalizeJwtInput(input);
        if (!raw) {
            return { headerJson: '', payloadJson: '', warning: '', errors: [] };
        }

        const errors = [];
        let headerSeg = '';
        let payloadSeg = '';
        let warning = '未校验签名（仅做解码）';

        const parts = raw.split('.').filter(p => p.length > 0);

        const type = String(inputType || 'auto');
        if (type === 'jwt') {
            if (parts.length < 2) {
                errors.push('JWT 格式不完整：至少需要 header.payload');
            } else {
                headerSeg = parts[0];
                payloadSeg = parts[1];
                if (parts.length < 3) warning = '未包含签名段（仅做解码）';
            }
        } else if (type === 'header_payload') {
            if (parts.length !== 2) {
                errors.push('格式应为 header.payload 两段');
            } else {
                headerSeg = parts[0];
                payloadSeg = parts[1];
                warning = '未包含签名段（仅做解码）';
            }
        } else if (type === 'header') {
            headerSeg = raw;
            payloadSeg = '';
            warning = '仅解码 Header（未校验签名）';
        } else if (type === 'payload') {
            headerSeg = '';
            payloadSeg = raw;
            warning = '仅解码 Payload（未校验签名）';
        } else {
            // auto
            if (parts.length >= 2) {
                headerSeg = parts[0];
                payloadSeg = parts[1];
                if (parts.length < 3) warning = '未包含签名段（仅做解码）';
            } else {
                // 仅一段：按 payload 处理
                payloadSeg = raw;
                warning = '自动识别为仅 Payload（未校验签名）';
            }
        }

        let headerJson = '';
        let payloadJson = '';

        if (headerSeg) {
            try {
                headerJson = base64UrlDecodeToJsonText(headerSeg);
            } catch (e) {
                errors.push(`Header 解码失败：${e?.message || String(e)}`);
            }
        }
        if (payloadSeg) {
            try {
                payloadJson = base64UrlDecodeToJsonText(payloadSeg);
            } catch (e) {
                errors.push(`Payload 解码失败：${e?.message || String(e)}`);
            }
        }

        return { headerJson, payloadJson, warning, errors };
    }

    function pad2(n) {
        return String(n).padStart(2, '0');
    }

    function pad3(n) {
        return String(n).padStart(3, '0');
    }

    function pad9BigInt(n) {
        const s = n.toString();
        return s.padStart(9, '0');
    }

    function divMod(a, b) {
        // b > 0
        let q = a / b;
        let r = a % b;
        if (r < 0n) {
            r += b;
            q -= 1n;
        }
        return { q, r };
    }

    function formatUnixMillis(unixMillisBig, tzOffsetMs, withMillis) {
        const offset = BigInt(tzOffsetMs || 0);
        const adjusted = unixMillisBig + offset;
        const msNum = Number(adjusted);
        if (!Number.isFinite(msNum)) throw new Error('时间超出可处理范围');
        const d = new Date(msNum);
        const y = d.getUTCFullYear();
        const m = d.getUTCMonth() + 1;
        const day = d.getUTCDate();
        const hh = d.getUTCHours();
        const mm = d.getUTCMinutes();
        const ss = d.getUTCSeconds();
        const ms = d.getUTCMilliseconds();
        const base = `${y}-${pad2(m)}-${pad2(day)} ${pad2(hh)}:${pad2(mm)}:${pad2(ss)}`;
        return withMillis ? `${base}.${pad3(ms)}` : base;
    }

    function formatUnixNanos(unixMillisBig, nanosWithinSecond, tzOffsetMs) {
        const base = formatUnixMillis(unixMillisBig, tzOffsetMs, true);
        // base 末尾是 .SSS，替换为 9 位纳秒
        const suffix = pad9BigInt(nanosWithinSecond);
        return base.replace(/\.\d{3}$/, `.${suffix}`);
    }

    function detectTimeInputType(text) {
        const t = String(text ?? '').trim();
        if (!t) return { type: 'auto', label: '空' };
        if (/^-?\d+$/.test(t)) {
            const len = t.replace(/^-/, '').length;
            if (len <= 10) return { type: 'unix_s', label: 'Unix时间戳(秒)' };
            if (len <= 13) return { type: 'unix_ms', label: 'Unix时间戳(毫秒)' };
            if (len <= 16) return { type: 'unix_ms', label: 'Unix时间戳(毫秒)' };
            return { type: 'unix_ns', label: 'Unix时间戳(纳秒)' };
        }
        return { type: 'datetime', label: '标准时间' };
    }

    function parseDateTime(text) {
        const t = String(text ?? '').trim();
        const m = t.match(/^(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2}):(\d{2})(?:\.(\d{1,3}))?$/);
        if (!m) throw new Error('标准时间格式应为 YYYY-MM-DD HH:mm:ss 或带毫秒 .SSS');
        const year = parseInt(m[1], 10);
        const month = parseInt(m[2], 10);
        const day = parseInt(m[3], 10);
        const hh = parseInt(m[4], 10);
        const mm = parseInt(m[5], 10);
        const ss = parseInt(m[6], 10);
        const ms = m[7] ? parseInt(m[7].padEnd(3, '0'), 10) : 0;
        return { year, month, day, hh, mm, ss, ms };
    }

    function parseTimeInput(text, inputType, tzOffsetMs) {
        const raw = String(text ?? '').trim();
        if (!raw) return { unixMillis: null, nanosWithinSecond: null, detectedLabel: '空', errors: [] };

        const errors = [];
        let type = String(inputType || 'auto');
        let detectedLabel = '';
        if (type === 'auto') {
            const detected = detectTimeInputType(raw);
            type = detected.type;
            detectedLabel = `自动识别：${detected.label}`;
        } else {
            detectedLabel = '手动选择';
        }

        try {
            if (type === 'unix_s') {
                const big = BigInt(raw);
                const unixMillis = big * 1000n;
                return { unixMillis, nanosWithinSecond: 0n, detectedLabel, errors };
            }
            if (type === 'unix_ms') {
                const big = BigInt(raw);
                const unixMillis = big;
                const mod = divMod(big, 1000n);
                const nanosWithinSecond = mod.r * 1000000n;
                return { unixMillis, nanosWithinSecond, detectedLabel, errors };
            }
            if (type === 'unix_ns') {
                const big = BigInt(raw);
                const secMod = divMod(big, 1000000000n);
                const sec = secMod.q;
                const nanosWithinSecond = secMod.r;
                const unixMillis = sec * 1000n + nanosWithinSecond / 1000000n;
                return { unixMillis, nanosWithinSecond, detectedLabel, errors };
            }
            if (type === 'datetime') {
                const dt = parseDateTime(raw);
                const baseUtcMs = BigInt(Date.UTC(dt.year, dt.month - 1, dt.day, dt.hh, dt.mm, dt.ss, dt.ms));
                const unixMillis = baseUtcMs - BigInt(tzOffsetMs || 0);
                const mod = divMod(unixMillis, 1000n);
                const nanosWithinSecond = mod.r * 1000000n;
                return { unixMillis, nanosWithinSecond, detectedLabel, errors };
            }
            errors.push('不支持的输入类型');
            return { unixMillis: null, nanosWithinSecond: null, detectedLabel, errors };
        } catch (e) {
            errors.push(e?.message || String(e));
            return { unixMillis: null, nanosWithinSecond: null, detectedLabel, errors };
        }
    }

    function getNowValues(tzOffsetMs, nowMillis = Date.now()) {
        const nowMsBig = BigInt(Math.trunc(nowMillis));
        const unixSec = nowMsBig / 1000n;
        return {
            stdSec: formatUnixMillis(nowMsBig, tzOffsetMs, false),
            unixSec: unixSec.toString(),
            stdMs: formatUnixMillis(nowMsBig, tzOffsetMs, true),
            unixMs: nowMsBig.toString()
        };
    }

    return {
        decodeJwt,
        parseTimeInput,
        formatUnixMillis,
        formatUnixNanos,
        getNowValues,
        detectTimeInputType,
        // 仅测试/调试
        _base64UrlToBytes: base64UrlToBytes
    };
});

