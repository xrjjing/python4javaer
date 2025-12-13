/* 工具箱（M2）通用算法工具：Base64 / UUID / 命名转换
 *
 * 设计目标：
 * - 纯算法、无 DOM 依赖，便于在浏览器与 Node 环境复用与单元测试
 * - 输入输出统一按 UTF-8 处理
 */
(function (root, factory) {
    // UMD：浏览器挂到 window；Node 通过 module.exports 导出
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = factory();
    } else {
        root.DogToolboxM2Utils = factory();
    }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
    'use strict';

    function isNodeEnv() {
        return typeof process !== 'undefined' && process.versions && process.versions.node;
    }

    function getWebCrypto() {
        // 浏览器/Node(含 Web Crypto) 兼容
        if (typeof crypto !== 'undefined') return crypto;
        if (isNodeEnv()) {
            try {
                // eslint-disable-next-line global-require
                const nodeCrypto = require('crypto');
                return nodeCrypto.webcrypto;
            } catch (e) {
                return null;
            }
        }
        return null;
    }

    function utf8ToBytes(text) {
        if (typeof TextEncoder !== 'undefined') {
            return new TextEncoder().encode(String(text ?? ''));
        }
        if (isNodeEnv()) {
            return Uint8Array.from(Buffer.from(String(text ?? ''), 'utf8'));
        }
        // 兜底：最差情况只处理 ASCII
        const s = String(text ?? '');
        const arr = new Uint8Array(s.length);
        for (let i = 0; i < s.length; i++) arr[i] = s.charCodeAt(i) & 0xff;
        return arr;
    }

    function bytesToUtf8(bytes) {
        const u8 = bytes instanceof Uint8Array ? bytes : Uint8Array.from(bytes || []);
        if (typeof TextDecoder !== 'undefined') {
            // fatal=true：遇到非法 UTF-8 直接抛错，便于前端提示
            return new TextDecoder('utf-8', { fatal: true }).decode(u8);
        }
        if (isNodeEnv()) {
            return Buffer.from(u8).toString('utf8');
        }
        let s = '';
        for (let i = 0; i < u8.length; i++) s += String.fromCharCode(u8[i]);
        return s;
    }

    function bytesToBase64(bytes) {
        const u8 = bytes instanceof Uint8Array ? bytes : Uint8Array.from(bytes || []);
        if (typeof btoa === 'function') {
            let binary = '';
            const chunkSize = 0x8000;
            for (let i = 0; i < u8.length; i += chunkSize) {
                const chunk = u8.subarray(i, i + chunkSize);
                binary += String.fromCharCode.apply(null, Array.from(chunk));
            }
            return btoa(binary);
        }
        if (isNodeEnv()) {
            return Buffer.from(u8).toString('base64');
        }
        throw new Error('当前环境不支持 Base64 编码');
    }

    function normalizeBase64Input(input) {
        const raw = String(input ?? '');
        const stripped = raw.replace(/\s+/g, '');
        if (!stripped) return '';
        // base64 字符集校验（支持标准 base64，不包含 base64url）
        if (!/^[A-Za-z0-9+/=]+$/.test(stripped)) {
            throw new Error('非法 Base64：包含不支持的字符');
        }
        // 自动补齐 padding
        const mod = stripped.length % 4;
        if (mod === 1) {
            throw new Error('非法 Base64：长度不合法');
        }
        if (mod === 2) return stripped + '==';
        if (mod === 3) return stripped + '=';
        return stripped;
    }

    function base64ToBytes(base64Text) {
        const normalized = normalizeBase64Input(base64Text);
        if (!normalized) return new Uint8Array(0);

        if (typeof atob === 'function') {
            const binary = atob(normalized);
            const bytes = new Uint8Array(binary.length);
            for (let i = 0; i < binary.length; i++) {
                bytes[i] = binary.charCodeAt(i) & 0xff;
            }
            return bytes;
        }
        if (isNodeEnv()) {
            // Buffer 对非法输入容错较多，已在 normalizeBase64Input 做严格校验
            return Uint8Array.from(Buffer.from(normalized, 'base64'));
        }
        throw new Error('当前环境不支持 Base64 解码');
    }

    function base64EncodeTextUtf8(text) {
        return bytesToBase64(utf8ToBytes(text));
    }

    function base64DecodeToTextUtf8(base64Text) {
        return bytesToUtf8(base64ToBytes(base64Text));
    }

    function generateUuidV4() {
        const c = getWebCrypto();
        if (!c) throw new Error('当前环境不支持安全随机数（crypto）');
        if (typeof c.randomUUID === 'function') {
            return c.randomUUID();
        }
        if (typeof c.getRandomValues !== 'function') {
            throw new Error('当前环境不支持 getRandomValues');
        }
        const bytes = new Uint8Array(16);
        c.getRandomValues(bytes);
        // 版本号：0100
        bytes[6] = (bytes[6] & 0x0f) | 0x40;
        // 变体：10xx
        bytes[8] = (bytes[8] & 0x3f) | 0x80;
        const hex = Array.from(bytes, b => b.toString(16).padStart(2, '0')).join('');
        return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`;
    }

    function splitWords(input) {
        const raw = String(input ?? '').trim();
        if (!raw) return [];
        // 统一分隔符为空格，再做 camel/pascal 拆分
        const normalized = raw.replace(/[_\-]+/g, ' ').replace(/\s+/g, ' ');
        const parts = normalized.split(' ').filter(Boolean);
        const words = [];
        // 兼容：USER_ID / userID / UserIDNumber / user2Age 等
        const pattern = /[A-Z]+(?=[A-Z][a-z]|[0-9]|$)|[A-Z]?[a-z]+|[0-9]+/g;
        for (const part of parts) {
            const matches = part.match(pattern);
            if (matches) words.push(...matches);
        }
        return words;
    }

    function isAcronym(word) {
        const w = String(word ?? '');
        return w.length > 1 && w === w.toUpperCase() && w !== w.toLowerCase();
    }

    function titleize(word) {
        const w = String(word ?? '');
        if (!w) return '';
        if (isAcronym(w)) return w;
        const lower = w.toLowerCase();
        return lower.charAt(0).toUpperCase() + lower.slice(1);
    }

    function toNamingFormats(input) {
        const words = splitWords(input);
        if (!words.length) {
            return {
                space: '',
                camelSpace: '',
                kebab: '',
                snakeUpper: '',
                pascal: '',
                camel: '',
                snake: ''
            };
        }

        const lowerWords = words.map(w => String(w).toLowerCase());
        const upperWords = words.map(w => String(w).toUpperCase());

        const pascal = words.map(titleize).join('');
        const camel = lowerWords[0] + words.slice(1).map(titleize).join('');

        return {
            space: lowerWords.join(' '),
            camelSpace: words.map(titleize).join(' '),
            kebab: lowerWords.join('-'),
            snakeUpper: upperWords.join('_'),
            pascal,
            camel,
            snake: lowerWords.join('_')
        };
    }

    return {
        base64EncodeTextUtf8,
        base64DecodeToTextUtf8,
        generateUuidV4,
        toNamingFormats,
        // 仅供测试/调试
        _splitWords: splitWords
    };
});

